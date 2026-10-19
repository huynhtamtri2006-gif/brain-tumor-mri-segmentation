"""Rút trích đặc trưng hình học và tính toán thông số chẩn đoán khối u não.

Phụ trách: Huỳnh Tâm Trí (MSSV: 2045240315).
Tài liệu tham khảo: Gonzalez & Woods (4th Ed), Chapter 11 (Feature Extraction - Shape Descriptors).
"""

from dataclasses import dataclass
from typing import Tuple, Optional, Dict, Any
import math
import numpy as np
import cv2


@dataclass
class DiagnosticResult:
    """Cấu trúc dữ liệu chứa kết quả chẩn đoán và đặc trưng hình học khối u não."""
    tumor_detected: bool
    tumor_area_px: int
    brain_area_px: int
    tumor_ratio_percent: float
    perimeter_px: float
    circularity: float
    bbox: Optional[Tuple[int, int, int, int]]  # (x, y, w, h)
    dice_score: Optional[float] = None
    iou_score: Optional[float] = None

    @property
    def tumor_area_pixels(self) -> int:
        """Alias tương thích cho tumor_area_px."""
        return self.tumor_area_px

    def to_dict(self) -> Dict[str, Any]:
        """Chuyển đổi kết quả sang dictionary để hiển thị hoặc lưu JSON/CSV."""
        return {
            "tumor_detected": self.tumor_detected,
            "tumor_area_px": self.tumor_area_px,
            "brain_area_px": self.brain_area_px,
            "tumor_ratio_percent": round(self.tumor_ratio_percent, 2),
            "perimeter_px": round(self.perimeter_px, 2),
            "circularity": round(self.circularity, 3),
            "bbox": self.bbox,
            "dice_score": round(self.dice_score, 4) if self.dice_score is not None else None,
            "iou_score": round(self.iou_score, 4) if self.iou_score is not None else None
        }


def calculate_circularity(area: float, perimeter: float) -> float:
    """Tính độ tròn (Circularity / Compactness) của khối u.
    
    Công thức: C = (4 * π * Area) / (Perimeter^2)
    - C xấp xỉ 1.0: Khối u tròn đều (thường gặp ở u màng não Meningioma lành tính).
    - C << 1.0: Bờ u gồ ghề, khuyết lõm hoặc phân nhánh xâm lấn (u ác tính Glioma).
    
    Args:
        area: Diện tích (số pixel hoặc đơn vị mm2).
        perimeter: Chu vi đường bao u.
        
    Returns:
        float: Giá trị độ tròn trong khoảng [0, 1].
    """
    if perimeter <= 0:
        return 0.0
    circ = (4.0 * math.pi * area) / (perimeter * perimeter)
    return min(1.0, max(0.0, float(circ)))


def extract_tumor_features(
    tumor_mask: np.ndarray,
    brain_mask: Optional[np.ndarray] = None,
    min_area_thresh: int = 30
) -> DiagnosticResult:
    """Trích xuất toàn bộ đặc trưng hình học của khối u từ mặt nạ phân đoạn.
    
    Args:
        tumor_mask: Mặt nạ nhị phân u não (H, W), dtype uint8 với {0, 255}.
        brain_mask: Mặt nạ nhị phân toàn bộ não để tính tỷ lệ chiếm chỗ (tùy chọn).
        min_area_thresh: Diện tích tối thiểu để công nhận là có u (tránh nhiễu).
        
    Returns:
        DiagnosticResult: Đối tượng chứa toàn bộ thông số định lượng chẩn đoán.
    """
    tumor_pixels = int(np.sum(tumor_mask > 0))
    brain_pixels = int(np.sum(brain_mask > 0)) if brain_mask is not None else (256 * 256)

    if tumor_pixels < min_area_thresh:
        return DiagnosticResult(
            tumor_detected=False,
            tumor_area_px=0,
            brain_area_px=brain_pixels,
            tumor_ratio_percent=0.0,
            perimeter_px=0.0,
            circularity=0.0,
            bbox=None
        )

    # Tìm contour lớn nhất của khối u
    contours, _ = cv2.findContours(tumor_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return DiagnosticResult(
            tumor_detected=False,
            tumor_area_px=tumor_pixels,
            brain_area_px=brain_pixels,
            tumor_ratio_percent=(tumor_pixels / brain_pixels) * 100.0,
            perimeter_px=0.0,
            circularity=0.0,
            bbox=None
        )

    largest_contour = max(contours, key=cv2.contourArea)
    perimeter = cv2.arcLength(largest_contour, True)
    circularity = calculate_circularity(tumor_pixels, perimeter)
    x, y, w, h = cv2.boundingRect(largest_contour)

    ratio = (tumor_pixels / brain_pixels) * 100.0 if brain_pixels > 0 else 0.0

    return DiagnosticResult(
        tumor_detected=True,
        tumor_area_px=tumor_pixels,
        brain_area_px=brain_pixels,
        tumor_ratio_percent=ratio,
        perimeter_px=perimeter,
        circularity=circularity,
        bbox=(x, y, w, h)
    )
