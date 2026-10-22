"""Class điều phối toàn diện BrainTumorPipeline kết nối 4 tầng xử lý ảnh số.

Quy trình khép kín:
Ảnh gốc MRI -> Lọc nhiễu Bilateral & CLAHE -> Tách sọ (Skull Stripping) 
           -> Phân đoạn u (Watershed / Region Growing) 
           -> Trích xuất đặc trưng & Bounding Box 
           -> Đánh giá định lượng so với Ground Truth (nếu có).
"""

from typing import Tuple, Optional, Dict, Any
import numpy as np

from src.preprocessing.filters import apply_bilateral_filter, apply_clahe
from src.preprocessing.skull_strip import strip_skull
from src.segmentation.watershed import segment_watershed
from src.segmentation.region_growing import segment_region_growing
from src.measurement.features import extract_tumor_features, DiagnosticResult
from src.measurement.visualization import draw_tumor_overlay, create_comparison_quad
from src.evaluation.metrics import calculate_dice, calculate_iou


class BrainTumorPipeline:
    """Hệ thống điều phối xử lý ảnh số chẩn đoán khối u não MRI."""

    def __init__(self, method: str = "watershed", params: Optional[Dict[str, Any]] = None) -> None:
        """Khởi tạo pipeline với phương pháp phân đoạn mong muốn.
        
        Args:
            method: 'watershed' (Baseline chính) hoặc 'region_growing' (Đối chứng).
            params: Dictionary chứa các siêu tham số tùy chỉnh.
        """
        self.method = method.lower()
        self.params = params or {}

    def process(
        self,
        image: np.ndarray,
        gt_mask: Optional[np.ndarray] = None
    ) -> Tuple[DiagnosticResult, Dict[str, np.ndarray]]:
        """Thực thi toàn bộ pipeline xử lý từ ảnh đầu vào đến kết quả đo lường và hình ảnh trực quan.
        
        Args:
            image: Ảnh MRI gốc (H, W), uint8.
            gt_mask: Mặt nạ Ground Truth (nếu có để tính Dice/IoU).
            
        Returns:
            Tuple[DiagnosticResult, Dict[str, np.ndarray]]:
                - DiagnosticResult: Chứa diện tích, tỷ lệ, độ tròn, bbox, Dice, IoU.
                - Dict: Các ảnh trung gian {'original', 'filtered', 'stripped', 'tumor_mask', 'overlay', 'quad'}.
        """
        # 1. Tiền xử lý lọc nhiễu
        filtered = apply_bilateral_filter(image)

        # 2. Tách sọ não (Skull Stripping)
        stripped_brain, brain_mask = strip_skull(filtered)

        # 3. Phân đoạn khối u theo phương pháp đã chọn (Strategy Pattern)
        if self.method == "region_growing":
            tol = self.params.get("intensity_tolerance", 15)
            tumor_mask = segment_region_growing(stripped_brain, tolerance=tol)
        else:
            ratio = self.params.get("dist_thresh_ratio", 0.4)
            tumor_mask = segment_watershed(stripped_brain, dist_thresh_ratio=ratio)

        # 4. Đo lường đặc trưng hình thái học
        diag_res = extract_tumor_features(tumor_mask, brain_mask)

        # 5. Nếu có Ground Truth, tính chỉ số đánh giá y khoa
        if gt_mask is not None:
            diag_res.dice_score = calculate_dice(tumor_mask, gt_mask)
            diag_res.iou_score = calculate_iou(tumor_mask, gt_mask)

        # 6. Trực quan hóa
        overlay = draw_tumor_overlay(image, tumor_mask, diag_res)
        quad = create_comparison_quad(image, stripped_brain, tumor_mask, overlay)

        intermediates = {
            "original": image,
            "filtered": filtered,
            "stripped": stripped_brain,
            "brain_mask": brain_mask,
            "tumor_mask": tumor_mask,
            "overlay": overlay,
            "quad": quad
        }

        return diag_res, intermediates
