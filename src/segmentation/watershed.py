"""Thuật toán phân đoạn khối u não bằng Marker-controlled Watershed.

Phụ trách: Hà Mạnh Trường (MSSV: 2045240326).
Tài liệu tham khảo: Gonzalez & Woods (4th Ed), Chapter 10 (Image Segmentation - Watersheds).
"""

from typing import Dict, Tuple, Union
import numpy as np
import cv2
from .base import BaseSegmenter


INTERMEDIATE_KEYS = (
    "original", "binary_high", "opened", "dist_transform",
    "sure_fg", "sure_bg", "unknown", "markers", "tumor_mask",
)


def _empty_intermediates(shape: Tuple[int, int]) -> Dict[str, np.ndarray]:
    """Tạo dict 9 ảnh trung gian toàn 0 cho nhánh fail-safe."""
    return {key: np.zeros(shape, dtype=np.uint8) for key in INTERMEDIATE_KEYS}


def _to_display_uint8(image: np.ndarray) -> np.ndarray:
    """Chuẩn hoá ảnh số thực (EDT) về uint8 [0, 255] để lưu trung gian."""
    if image.dtype == np.uint8:
        return image
    if float(image.max()) == 0.0:
        return np.zeros(image.shape, dtype=np.uint8)
    return cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)


def _filter_small_components(tumor_mask: np.ndarray, min_tumor_area: int) -> np.ndarray:
    """Loại bỏ các đảo u có diện tích nhỏ hơn min_tumor_area."""
    if min_tumor_area <= 0:
        return tumor_mask
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(
        (tumor_mask > 0).astype(np.uint8), connectivity=8
    )
    if num_labels <= 1:
        return tumor_mask
    keep = np.zeros(num_labels, dtype=bool)
    keep[1:] = stats[1:, cv2.CC_STAT_AREA] >= min_tumor_area
    return np.where(keep[labels], 255, 0).astype(np.uint8)


class WatershedSegmenter(BaseSegmenter):
    """Bộ phân đoạn u não sử dụng biến đổi khoảng cách Euclidean và giải thuật phân thủy Watershed."""

    def __init__(
        self,
        dist_thresh_ratio: float = 0.4,
        bg_dilate_kernel: int = 3,
        min_tumor_area: int = 50
    ) -> None:
        self.dist_thresh_ratio = dist_thresh_ratio
        self.bg_dilate_kernel = bg_dilate_kernel
        self.min_tumor_area = min_tumor_area

    def segment(
        self,
        brain_image: np.ndarray,
        return_intermediates: bool = False
    ) -> Union[np.ndarray, Tuple[np.ndarray, Dict[str, np.ndarray]]]:
        return segment_watershed(
            brain_image,
            dist_thresh_ratio=self.dist_thresh_ratio,
            bg_dilate_kernel=self.bg_dilate_kernel,
            min_tumor_area=self.min_tumor_area,
            return_intermediates=return_intermediates
        )


def segment_watershed(
    brain_image: np.ndarray,
    dist_thresh_ratio: float = 0.4,
    bg_dilate_kernel: int = 3,
    min_tumor_area: int = 50,
    return_intermediates: bool = False,
) -> Union[np.ndarray, Tuple[np.ndarray, Dict[str, np.ndarray]]]:
    """Phân đoạn khối u não trên ảnh đã tách sọ bằng Marker-controlled Watershed.

    Quy trình 6 bước DIP (Gonzalez & Woods Ch.10):
    1. Lọc nhị phân sơ bộ vùng tăng sáng trong nhu mô não (phân vị 85).
    2. Phép mở hình thái học 3x3 khử nhiễu đốm hạt.
    3. Biến đổi khoảng cách Euclidean (cv2.distanceTransform) tìm tâm khối u.
    4. Xác định vùng chắc chắn là u (Sure Foreground) từ ngưỡng bản đồ khoảng cách.
    5. Xác định vùng chắc chắn là não lành (Sure Background) bằng phép giãn nở.
    6. Đánh dấu markers, chạy cv2.watershed và lọc đảo nhỏ bằng min_tumor_area.

    Args:
        brain_image: Ảnh xám não đã tách sọ (H, W), dtype uint8.
        dist_thresh_ratio: Tỷ lệ ngưỡng khoảng cách cực đại để lấy tâm u (mặc định 0.4).
        bg_dilate_kernel: Kích thước kernel giãn nở để tạo vùng nền.
        min_tumor_area: Diện tích tối thiểu (pixel) để giữ lại một đảo u.
        return_intermediates: Nếu True, trả thêm từ điển 9 ảnh trung gian.

    Returns:
        - return_intermediates=False: mặt nạ nhị phân u (H, W) uint8 {0, 255}.
        - return_intermediates=True: Tuple (tumor_mask, intermediates) với các khoá
          'original', 'binary_high', 'opened', 'dist_transform', 'sure_fg',
          'sure_bg', 'unknown', 'markers', 'tumor_mask' (cùng shape, uint8).
    """
    if len(brain_image.shape) == 3:
        gray = cv2.cvtColor(brain_image, cv2.COLOR_BGR2GRAY)
    else:
        gray = brain_image.copy()

    h, w = gray.shape
    zeros = np.zeros((h, w), dtype=np.uint8)
    steps = _empty_intermediates((h, w))
    steps["original"] = gray.copy()

    # Chỉ xét trong vùng não có tín hiệu (> 0)
    non_zero_pixels = gray[gray > 0]
    if len(non_zero_pixels) == 0:
        return (zeros, steps) if return_intermediates else zeros

    # 1. Ngưỡng hóa sơ bộ tìm vùng u tăng sáng
    # Khối u não trên ảnh T1-CE/FLAIR thường có cường độ nằm ở phân vị cao
    high_thresh = np.percentile(non_zero_pixels, 85)
    _, binary_high = cv2.threshold(gray, int(high_thresh), 255, cv2.THRESH_BINARY)
    steps["binary_high"] = binary_high

    # 2. Phép mở nhẹ làm sạch nhiễu hạt
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opened = cv2.morphologyEx(binary_high, cv2.MORPH_OPEN, kernel, iterations=1)
    steps["opened"] = opened

    # 3. Biến đổi khoảng cách Euclidean
    dist_transform = cv2.distanceTransform(opened, cv2.DIST_L2, 5)
    steps["dist_transform"] = _to_display_uint8(dist_transform)
    max_dist = dist_transform.max()
    if max_dist == 0:
        return (zeros, steps) if return_intermediates else zeros

    # 4. Xác định Sure Foreground & Sure Background
    _, sure_fg = cv2.threshold(dist_transform, dist_thresh_ratio * max_dist, 255, 0)
    sure_fg = np.uint8(sure_fg)
    steps["sure_fg"] = sure_fg

    dilate_k = cv2.getStructuringElement(cv2.MORPH_RECT, (bg_dilate_kernel, bg_dilate_kernel))
    sure_bg = cv2.dilate(opened, dilate_k, iterations=2)
    steps["sure_bg"] = sure_bg

    unknown = cv2.subtract(sure_bg, sure_fg)
    steps["unknown"] = unknown

    # 5. Đánh dấu Markers
    _, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0
    # Lưu markers đầu vào (trước khi watershed sửa tại chỗ) dưới dạng uint8
    steps["markers"] = np.clip(markers, 0, 255).astype(np.uint8)

    # 6. Chạy Watershed trên ảnh 3 kênh
    img_3ch = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    markers = cv2.watershed(img_3ch, markers)

    # Vùng u là các marker có giá trị > 1 (khác nền = 1 và biên = -1)
    tumor_mask = np.zeros_like(gray, dtype=np.uint8)
    tumor_mask[markers > 1] = 255

    # 7. Hậu xử lý: lọc bỏ các đảo nhiễu nhỏ hơn min_tumor_area
    tumor_mask = _filter_small_components(tumor_mask, min_tumor_area)
    steps["tumor_mask"] = tumor_mask

    return (tumor_mask, steps) if return_intermediates else tumor_mask
