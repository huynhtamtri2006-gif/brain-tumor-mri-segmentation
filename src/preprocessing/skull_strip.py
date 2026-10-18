"""Thuật toán Tách sọ não (Skull Stripping) trên ảnh MRI.

Phụ trách: Hà Mạnh Trường (MSSV: 2045240326).
Tài liệu tham khảo: Gonzalez & Woods (4th Ed), Chapter 9 (Morphological Image Processing).
Kỹ thuật DIP áp dụng:
1. Phân ngưỡng nhị phân Otsu tự động tách đầu khỏi nền đen.
2. Phép mở hình thái học (Morphological Opening) cắt đứt cầu nối mô giữa màng não và xương sọ.
3. Trích xuất thành phần liên thông lớn nhất (Largest Connected Component - LCC).
4. Phép lấp đầy lỗ hổng (Hole Filling) khôi phục nhu mô não thất.
5. Phép nhân Bitwise-AND với ảnh gốc để thu được ảnh não sạch sọ.
"""

from typing import Tuple, Optional
import numpy as np
import cv2


def extract_brain_mask(image: np.ndarray, kernel_size: int = 5) -> np.ndarray:
    """Tạo mặt nạ nhị phân nhu mô não (Brain Mask), loại bỏ xương sọ và da đầu.
    
    Args:
        image: Ảnh MRI xám đầu vào (H, W), dtype uint8 [0, 255].
        kernel_size: Kích thước phần tử cấu trúc dạng đĩa (disk/ellipse).
        
    Returns:
        np.ndarray: Mặt nạ nhị phân nhu mô não (H, W), dtype uint8, giá trị {0, 255}.
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    # 1. Ngưỡng hóa tự động Otsu
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 2. Phép mở hình thái học với phần tử cấu trúc elip
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
    opened = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

    # 3. Tìm thành phần liên thông lớn nhất (Nhu mô não)
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(opened, connectivity=8)
    if num_labels <= 1:
        return np.zeros_like(gray, dtype=np.uint8)

    # Bỏ qua label 0 (nền đen), tìm nhãn có diện tích lớn nhất
    largest_label = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
    brain_mask = np.zeros_like(gray, dtype=np.uint8)
    brain_mask[labels == largest_label] = 255

    # 4. Lấp đầy lỗ hổng bên trong nhu mô não (Hole filling)
    mask_floodfill = brain_mask.copy()
    h, w = brain_mask.shape
    fill_mask = np.zeros((h + 2, w + 2), np.uint8)
    cv2.floodFill(mask_floodfill, fill_mask, (0, 0), 255)
    mask_holes = cv2.bitwise_not(mask_floodfill)
    filled_brain_mask = cv2.bitwise_or(brain_mask, mask_holes)

    return filled_brain_mask


def strip_skull(
    image: np.ndarray,
    brain_mask: Optional[np.ndarray] = None
) -> Tuple[np.ndarray, np.ndarray]:
    """Tách sọ não khỏi ảnh MRI gốc.
    
    Args:
        image: Ảnh MRI xám đầu vào (H, W), dtype uint8.
        brain_mask: Mặt nạ não đã tính trước (nếu có). Nếu None, hàm sẽ tự gọi extract_brain_mask.
        
    Returns:
        Tuple[np.ndarray, np.ndarray]: (ảnh_sau_tách_sọ, mặt_nạ_nhu_mô_não).
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    if brain_mask is None:
        brain_mask = extract_brain_mask(gray)

    # Nhân bitwise-AND để giữ lại vùng não sạch sọ
    stripped_brain = cv2.bitwise_and(gray, gray, mask=brain_mask)
    return stripped_brain, brain_mask
