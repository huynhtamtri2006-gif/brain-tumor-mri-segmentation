"""Thuật toán phân đoạn khối u não bằng Seeded Region Growing (Phát triển vùng từ điểm hạt giống).

Phụ trách: Hà Mạnh Trường (MSSV: 2045240326).
Tài liệu tham khảo: Gonzalez & Woods (4th Ed), Chapter 10 (Image Segmentation - Region-Based Segmentation).
"""

from typing import Optional, Tuple, List
from collections import deque
import numpy as np
import cv2
from .base import BaseSegmenter


class RegionGrowingSegmenter(BaseSegmenter):
    """Bộ phân đoạn u não sử dụng giải thuật phát triển vùng từ hạt giống cực đại cường độ."""

    def __init__(self, tolerance: int = 15, min_area: int = 50, max_area: int = 25000) -> None:
        self.tolerance = tolerance
        self.min_area = min_area
        self.max_area = max_area

    def segment(self, brain_image: np.ndarray) -> np.ndarray:
        return segment_region_growing(
            brain_image,
            tolerance=self.tolerance,
            min_area=self.min_area,
            max_area=self.max_area
        )


def find_seed_point(brain_image: np.ndarray) -> Optional[Tuple[int, int]]:
    """Tự động tìm tọa độ điểm hạt giống (Seed Point) có cường độ sáng cao nhất trong nhu mô não.
    
    Args:
        brain_image: Ảnh xám não đã tách sọ (H, W), dtype uint8.
        
    Returns:
        Optional[Tuple[int, int]]: Tọa độ (hàng, cột) của điểm hạt giống, hoặc None nếu ảnh rỗng.
    """
    if len(brain_image.shape) == 3:
        gray = cv2.cvtColor(brain_image, cv2.COLOR_BGR2GRAY)
    else:
        gray = brain_image

    # Làm mịn nhẹ để tránh điểm nhiễu đơn lẻ
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # Chỉ tìm điểm cực đại trong vùng não (> 0)
    if blurred.max() == 0:
        return None

    # Tìm vị trí giá trị cực đại
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(blurred)
    # max_loc trả về (cột x, hàng y) của OpenCV -> chuyển về (hàng y, cột x)
    return (max_loc[1], max_loc[0])


def segment_region_growing(
    brain_image: np.ndarray,
    tolerance: int = 15,
    seed_point: Optional[Tuple[int, int]] = None,
    min_area: int = 50,
    max_area: int = 25000
) -> np.ndarray:
    """Phân đoạn khối u não bằng thuật toán phát triển vùng (Region Growing).
    
    Quy trình:
    1. Xác định điểm hạt giống (Seed Point) tự động qua cường độ cực đại trong não.
    2. Lan truyền vùng theo láng giềng 8 điểm kết nối sử dụng hàng đợi BFS.
    3. Tiêu chí thu nạp: |I(p) - I(seed)| <= tolerance.
    4. Hậu xử lý hình thái học (Morphological Closing) để lấp lỗ trống và làm mịn bờ u.
    
    Args:
        brain_image: Ảnh não đã tách sọ (H, W), dtype uint8.
        tolerance: Ngưỡng dung sai độ sáng so với hạt giống.
        seed_point: Tọa độ (y, x) hạt giống. Nếu None, tự động tìm điểm cực đại.
        min_area: Diện tích vùng u tối thiểu (pixel) để loại bỏ nhiễu.
        max_area: Diện tích vùng u tối đa cho phép.
        
    Returns:
        np.ndarray: Mặt nạ nhị phân khối u (H, W), dtype uint8 với {0, 255}.
    """
    if len(brain_image.shape) == 3:
        gray = cv2.cvtColor(brain_image, cv2.COLOR_BGR2GRAY)
    else:
        gray = brain_image.copy()

    h, w = gray.shape
    segmented_mask = np.zeros((h, w), dtype=np.uint8)

    if seed_point is None:
        seed_point = find_seed_point(gray)
        if seed_point is None:
            return segmented_mask

    seed_y, seed_x = seed_point
    seed_val = float(gray[seed_y, seed_x])

    visited = np.zeros((h, w), dtype=bool)
    queue = deque([(seed_y, seed_x)])
    visited[seed_y, seed_x] = True

    # 8 hướng láng giềng
    neighbors = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    pixel_count = 0

    while queue:
        cy, cx = queue.popleft()
        segmented_mask[cy, cx] = 255
        pixel_count += 1

        if pixel_count > max_area:
            break

        for dy, dx in neighbors:
            ny, nx = cy + dy, cx + dx
            if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx]:
                visited[ny, nx] = True
                # Chỉ phát triển trong vùng não (> 0) và thỏa mãn dung sai
                pixel_val = float(gray[ny, nx])
                if pixel_val > 0 and abs(pixel_val - seed_val) <= tolerance:
                    queue.append((ny, nx))

    # Hậu xử lý nếu diện tích hợp lệ
    if min_area <= pixel_count <= max_area:
        k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        segmented_mask = cv2.morphologyEx(segmented_mask, cv2.MORPH_CLOSE, k, iterations=1)
    else:
        # Nếu diện tích quá nhỏ (nhiễu) hoặc quá lớn (tràn não), coi như không tìm thấy u
        segmented_mask.fill(0)

    return segmented_mask
