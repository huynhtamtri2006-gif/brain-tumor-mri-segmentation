"""Thuật toán Tách sọ não (Skull Stripping) 6 bước trên ảnh MRI.

Phụ trách: Hà Mạnh Trường (MSSV: 2045240326).
Tài liệu tham khảo: Gonzalez & Woods (4th Ed), Chapter 9 (Morphological Image Processing).

Quy trình 6 bước DIP:
1. Khử nhiễu sơ bộ bằng Gaussian blur (5x5, sigma=1.0).
2. Phân ngưỡng nhị phân Otsu tự động tách đầu khỏi nền đen.
3. Phép mở hình thái học (Morphological Opening) cắt đứt cầu nối mô giữa màng não và xương sọ.
4. Trích xuất thành phần liên thông lớn nhất (Largest Connected Component - LCC).
5. Phép đóng hình thái học (Closing) khép rãnh nhỏ và lấp đầy lỗ hổng não thất (Hole Filling).
6. Phép nhân Bitwise-AND với ảnh gốc để thu được ảnh não sạch sọ.
"""

from typing import Dict, Optional, Tuple, Union
import numpy as np
import cv2


def _build_brain_mask_steps(
    gray: np.ndarray,
    kernel_size: int
) -> Tuple[np.ndarray, Dict[str, np.ndarray]]:
    """Thực thi chuỗi 6 bước và trả về mặt nạ não kèm toàn bộ ảnh trung gian.

    Args:
        gray: Ảnh MRI xám đầu vào (H, W), dtype uint8.
        kernel_size: Kích thước phần tử cấu trúc elip cho phép Opening.

    Returns:
        Tuple[np.ndarray, Dict[str, np.ndarray]]: (brain_mask, intermediates) với
        các khoá 'original', 'denoised', 'otsu', 'opened', 'lcc',
        'closed_and_filled', 'brain_mask', 'stripped'.
    """
    steps: Dict[str, np.ndarray] = {}

    # 1. Khử nhiễu sơ bộ bằng Gaussian blur
    steps["original"] = gray.copy()
    denoised = cv2.GaussianBlur(gray, (5, 5), sigmaX=1.0)
    steps["denoised"] = denoised

    # 2. Ngưỡng hóa tự động Otsu
    _, otsu = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    steps["otsu"] = otsu

    # 3. Phép mở hình thái học với phần tử cấu trúc elip
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
    opened = cv2.morphologyEx(otsu, cv2.MORPH_OPEN, kernel, iterations=2)
    steps["opened"] = opened

    # 4. Tìm thành phần liên thông lớn nhất (Nhu mô não)
    lcc = np.zeros_like(gray, dtype=np.uint8)
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(opened, connectivity=8)
    if num_labels > 1:
        # Bỏ qua label 0 (nền đen), tìm nhãn có diện tích lớn nhất
        largest_label = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
        lcc[labels == largest_label] = 255
    steps["lcc"] = lcc

    # 5. Phép đóng hình thái học + lấp đầy lỗ hổng bên trong nhu mô não
    close_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    closed = cv2.morphologyEx(lcc, cv2.MORPH_CLOSE, close_kernel, iterations=1)

    mask_floodfill = closed.copy()
    h, w = closed.shape
    fill_mask = np.zeros((h + 2, w + 2), np.uint8)
    cv2.floodFill(mask_floodfill, fill_mask, (0, 0), 255)
    mask_holes = cv2.bitwise_not(mask_floodfill)
    brain_mask = cv2.bitwise_or(closed, mask_holes)
    steps["closed_and_filled"] = brain_mask.copy()

    # 6. Bitwise-AND giữ lại nhu mô não trên ảnh gốc
    steps["brain_mask"] = brain_mask
    steps["stripped"] = cv2.bitwise_and(gray, gray, mask=brain_mask)

    return brain_mask, steps


def extract_brain_mask(
    image: np.ndarray,
    kernel_size: int = 5,
    return_intermediates: bool = False
) -> Union[np.ndarray, Tuple[np.ndarray, Dict[str, np.ndarray]]]:
    """Tạo mặt nạ nhị phân nhu mô não (Brain Mask), loại bỏ xương sọ và da đầu.

    Args:
        image: Ảnh MRI xám đầu vào (H, W), dtype uint8 [0, 255].
        kernel_size: Kích thước phần tử cấu trúc dạng đĩa (disk/ellipse).
        return_intermediates: Nếu True, trả thêm từ điển ảnh trung gian 6 bước.

    Returns:
        - return_intermediates=False: np.ndarray mặt nạ nhị phân (H, W),
          dtype uint8, giá trị {0, 255}.
        - return_intermediates=True: Tuple[np.ndarray, Dict[str, np.ndarray]] gồm
          (brain_mask, intermediates).
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    brain_mask, steps = _build_brain_mask_steps(gray, kernel_size)
    if return_intermediates:
        return brain_mask, steps
    return brain_mask


def strip_skull(
    image: np.ndarray,
    brain_mask: Optional[np.ndarray] = None,
    return_intermediates: bool = False
) -> Union[Tuple[np.ndarray, np.ndarray],
           Tuple[np.ndarray, np.ndarray, Dict[str, np.ndarray]]]:
    """Tách sọ não khỏi ảnh MRI gốc.

    Args:
        image: Ảnh MRI xám đầu vào (H, W), dtype uint8.
        brain_mask: Mặt nạ não đã tính trước (nếu có). Nếu None, hàm sẽ tự gọi
            extract_brain_mask.
        return_intermediates: Nếu True, trả thêm từ điển ảnh trung gian 6 bước.

    Returns:
        - return_intermediates=False: Tuple (ảnh_sau_tách_sọ, mặt_nạ_nhu_mô_não).
        - return_intermediates=True: Tuple (ảnh_sau_tách_sọ, mặt_nạ_nhu_mô_não,
          intermediates).
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    steps: Optional[Dict[str, np.ndarray]] = None
    if brain_mask is None:
        if return_intermediates:
            brain_mask, steps = extract_brain_mask(gray, return_intermediates=True)
        else:
            brain_mask = extract_brain_mask(gray)

    # Nhân bitwise-AND để giữ lại vùng não sạch sọ
    stripped_brain = cv2.bitwise_and(gray, gray, mask=brain_mask)

    if not return_intermediates:
        return stripped_brain, brain_mask

    if steps is None:
        # Mặt nạ được truyền từ ngoài: vẫn dựng chuỗi trung gian chuẩn để báo cáo.
        _, steps = extract_brain_mask(gray, return_intermediates=True)
        steps["brain_mask"] = brain_mask
    steps["stripped"] = stripped_brain
    return stripped_brain, brain_mask, steps
