"""Module trực quan hóa kết quả phân đoạn, vẽ Bounding Box và tạo lưới ảnh so sánh.

Phụ trách: Huỳnh Tâm Trí (MSSV: 2045240315).
"""

from typing import Tuple, Optional
import numpy as np
import cv2
from .features import DiagnosticResult


def draw_tumor_overlay(
    original_image: np.ndarray,
    tumor_mask: np.ndarray,
    result: DiagnosticResult,
    color_bgr: Tuple[int, int, int] = (0, 0, 255),
    thickness: int = 2
) -> np.ndarray:
    """Vẽ đường bao u và Bounding Box màu cảnh báo đỏ lên ảnh gốc.
    
    Args:
        original_image: Ảnh MRI gốc (H, W) hoặc (H, W, 3).
        tumor_mask: Mặt nạ u nhị phân (H, W).
        result: Đối tượng DiagnosticResult chứa tọa độ bbox.
        color_bgr: Màu vẽ OpenCV (mặc định Đỏ = (0, 0, 255)).
        thickness: Độ dày nét vẽ.
        
    Returns:
        np.ndarray: Ảnh màu BGR (H, W, 3) có vẽ Bounding Box và chú thích.
    """
    if len(original_image.shape) == 2:
        canvas = cv2.cvtColor(original_image, cv2.COLOR_GRAY2BGR)
    else:
        canvas = original_image.copy()

    if not result.tumor_detected or result.bbox is None:
        cv2.putText(
            canvas, "No Tumor Detected", (10, 25),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2
        )
        return canvas

    x, y, w, h = result.bbox
    # Vẽ Bounding Box
    cv2.rectangle(canvas, (x, y), (x + w, y + h), color_bgr, thickness)

    # Vẽ đường bao mịn của u
    contours, _ = cv2.findContours(tumor_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(canvas, contours, -1, (0, 255, 255), 1)  # Màu vàng viền u

    # Thêm nhãn thông số
    label = f"Tumor: {result.tumor_area_px}px ({result.tumor_ratio_percent:.1f}%)"
    cv2.putText(
        canvas, label, (max(5, x), max(15, y - 5)),
        cv2.FONT_HERSHEY_SIMPLEX, 0.45, color_bgr, 1, cv2.LINE_AA
    )
    return canvas


def create_comparison_quad(
    original: np.ndarray,
    stripped: np.ndarray,
    pred_mask: np.ndarray,
    annotated: np.ndarray
) -> np.ndarray:
    """Tạo lưới 4 ảnh $2 \times 2$ so sánh các bước: [Gốc | Tách sọ | Mặt nạ | Khoanh u].
    
    Args:
        original: Ảnh MRI xám gốc.
        stripped: Ảnh sau tách sọ não.
        pred_mask: Mặt nạ phân đoạn u.
        annotated: Ảnh đã vẽ Bounding Box.
        
    Returns:
        np.ndarray: Ảnh ghép $2 \times 2$ có tiêu đề từng ô (2H, 2W, 3).
    """
    def to_bgr(img):
        if len(img.shape) == 2:
            return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        return img.copy()

    im1 = to_bgr(original)
    im2 = to_bgr(stripped)
    im3 = to_bgr(pred_mask)
    im4 = to_bgr(annotated)

    # Đóng dấu tiêu đề lên góc từng ảnh
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(im1, "1. Original MRI", (8, 20), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(im2, "2. Skull Stripped", (8, 20), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(im3, "3. Tumor Mask", (8, 20), font, 0.5, (0, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(im4, "4. Detection (BBox)", (8, 20), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)

    top_row = np.hstack([im1, im2])
    bottom_row = np.hstack([im3, im4])
    return np.vstack([top_row, bottom_row])
