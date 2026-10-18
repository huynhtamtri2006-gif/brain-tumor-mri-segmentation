"""Bộ lọc khử nhiễu Rician và tăng cường độ tương phản ảnh MRI.

Phụ trách: Hà Mạnh Trường (MSSV: 2045240326).
Tài liệu tham khảo: Gonzalez & Woods (4th Ed), Chapter 3 (Intensity Transformations) & Chapter 5 (Restoration).
"""

from typing import Tuple
import numpy as np
import cv2

def apply_bilateral_filter(
    image: np.ndarray,
    d: int = 9,
    sigma_color: float = 75.0,
    sigma_space: float = 75.0
) -> np.ndarray:
    """Khử nhiễu Rician trên ảnh MRI nhưng bảo toàn độ sắc nét đường bờ khối u.
    
    Args:
        image: Ảnh MRI xám đầu vào (H, W), dtype uint8 [0, 255].
        d: Đường kính vùng lân cận điểm ảnh.
        sigma_color: Độ lệch chuẩn của hàm Gauss trong không gian mức xám.
        sigma_space: Độ lệch chuẩn của hàm Gauss trong không gian tọa độ.
        
    Returns:
        np.ndarray: Ảnh sau khi khử nhiễu, cùng kích thước và dtype với ảnh đầu vào.
    """
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.bilateralFilter(image, d=d, sigmaColor=sigma_color, sigmaSpace=sigma_space)


def apply_clahe(
    image: np.ndarray,
    clip_limit: float = 2.0,
    tile_grid_size: Tuple[int, int] = (8, 8)
) -> np.ndarray:
    """Tăng cường độ tương phản thích ứng giới hạn độ tương phản (CLAHE).
    
    Args:
        image: Ảnh MRI xám đầu vào (H, W), dtype uint8 [0, 255].
        clip_limit: Ngưỡng cắt lược đồ xám để tránh khuếch đại nhiễu nền.
        tile_grid_size: Kích thước lưới chia nhỏ ảnh để cân bằng cục bộ.
        
    Returns:
        np.ndarray: Ảnh sau khi tăng tương phản mô não.
    """
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    return clahe.apply(image)
