"""Thuật toán phân đoạn khối u não bằng Marker-controlled Watershed.

Phụ trách: Hà Mạnh Trường (MSSV: 2045240326).
Tài liệu tham khảo: Gonzalez & Woods (4th Ed), Chapter 10 (Image Segmentation - Watersheds).
"""

from typing import Optional
import numpy as np
import cv2
from .base import BaseSegmenter


class WatershedSegmenter(BaseSegmenter):
    """Bộ phân đoạn u não sử dụng biến đổi khoảng cách Euclidean và giải thuật phân thủy Watershed."""

    def __init__(self, dist_thresh_ratio: float = 0.4, bg_dilate_kernel: int = 3):
        self.dist_thresh_ratio = dist_thresh_ratio
        self.bg_dilate_kernel = bg_dilate_kernel

    def segment(self, brain_image: np.ndarray) -> np.ndarray:
        return segment_watershed(
            brain_image,
            dist_thresh_ratio=self.dist_thresh_ratio,
            bg_dilate_kernel=self.bg_dilate_kernel
        )


def segment_watershed(
    brain_image: np.ndarray,
    dist_thresh_ratio: float = 0.4,
    bg_dilate_kernel: int = 3
) -> np.ndarray:
    """Phân đoạn khối u não trên ảnh đã tách sọ bằng Marker-controlled Watershed.
    
    Quy trình 6 bước DIP:
    1. Lọc nhị phân sơ bộ vùng tăng sáng trong nhu mô não (Otsu thresholding trên mô não).
    2. Biến đổi khoảng cách Euclidean (cv2.distanceTransform) tìm tâm khối u.
    3. Xác định vùng chắc chắn là u (Sure Foreground) từ ngưỡng bản đồ khoảng cách.
    4. Xác định vùng chắc chắn là não lành (Sure Background) bằng phép giãn nở (Dilation).
    5. Đánh dấu các điểm hạt giống (Markers) bằng cv2.connectedComponents.
    6. Thực thi cv2.watershed và trích xuất mặt nạ u nhị phân.
    
    Args:
        brain_image: Ảnh xám não đã tách sọ (H, W), dtype uint8.
        dist_thresh_ratio: Tỷ lệ ngưỡng khoảng cách cực đại để lấy tâm u (mặc định 0.4).
        bg_dilate_kernel: Kích thước kernel giãn nở để tạo vùng nền.
        
    Returns:
        np.ndarray: Mặt nạ nhị phân khối u (H, W), dtype uint8 với {0, 255}.
    """
    if len(brain_image.shape) == 3:
        gray = cv2.cvtColor(brain_image, cv2.COLOR_BGR2GRAY)
    else:
        gray = brain_image.copy()

    # Chỉ xét trong vùng não có tín hiệu (> 0)
    non_zero_pixels = gray[gray > 0]
    if len(non_zero_pixels) == 0:
        return np.zeros_like(gray, dtype=np.uint8)

    # 1. Ngưỡng hóa sơ bộ tìm vùng u tăng sáng
    # Khối u não trên ảnh T1-CE/FLAIR thường có cường độ nằm ở phân vị cao
    high_thresh = np.percentile(non_zero_pixels, 85)
    _, binary_tumor = cv2.threshold(gray, int(high_thresh), 255, cv2.THRESH_BINARY)

    # 2. Phép mở nhẹ làm sạch nhiễu hạt
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opening = cv2.morphologyEx(binary_tumor, cv2.MORPH_OPEN, kernel, iterations=1)

    # 3. Biến đổi khoảng cách Euclidean
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    max_dist = dist_transform.max()
    if max_dist == 0:
        return np.zeros_like(gray, dtype=np.uint8)

    # 4. Xác định Sure Foreground & Sure Background
    _, sure_fg = cv2.threshold(dist_transform, dist_thresh_ratio * max_dist, 255, 0)
    sure_fg = np.uint8(sure_fg)

    dilate_k = cv2.getStructuringElement(cv2.MORPH_RECT, (bg_dilate_kernel, bg_dilate_kernel))
    sure_bg = cv2.dilate(opening, dilate_k, iterations=2)
    unknown = cv2.subtract(sure_bg, sure_fg)

    # 5. Đánh dấu Markers
    _, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0

    # 6. Chạy Watershed trên ảnh 3 kênh
    img_3ch = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    markers = cv2.watershed(img_3ch, markers)

    # Vùng u là các marker có giá trị > 1 (khác nền = 1 và biên = -1)
    tumor_mask = np.zeros_like(gray, dtype=np.uint8)
    tumor_mask[markers > 1] = 255

    return tumor_mask
