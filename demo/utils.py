"""Helper utilities phục vụ hiển thị Streamlit GUI."""

from typing import List, Tuple, Optional
import os
import cv2
import numpy as np


def get_default_base_dir() -> str:
    """Trả về thư mục dữ liệu cơ sở (data/full)."""
    return "data/full"


def get_default_data_dir() -> str:
    """Trả về thư mục ảnh (data/full/images)."""
    return "data/full/images"



def list_sample_cases(data_dir: Optional[str] = None) -> List[str]:
    """Lấy danh sách các file ảnh có sẵn trong thư mục ảnh (mặc định ưu tiên data/full)."""
    if data_dir is None:
        data_dir = get_default_data_dir()
    if not os.path.exists(data_dir):
        return []
    return sorted([f for f in os.listdir(data_dir) if f.endswith(".png")])


def _read_grayscale(path: str) -> Optional[np.ndarray]:
    """Đọc ảnh xám từ đường dẫn, kể cả khi đường dẫn chứa ký tự Unicode trên Windows."""
    if not os.path.exists(path):
        return None
    try:
        encoded = np.fromfile(path, dtype=np.uint8)
    except OSError:
        return None
    if encoded.size == 0:
        return None
    return cv2.imdecode(encoded, cv2.IMREAD_GRAYSCALE)


def load_image_and_mask(sample_id: str, base_dir: Optional[str] = None) -> Tuple[Optional[np.ndarray], Optional[np.ndarray]]:
    """Nạp ảnh MRI gốc và mặt nạ Ground Truth tương ứng (mặc định ưu tiên data/full)."""
    if base_dir is None:
        base_dir = get_default_base_dir()
    img_path = os.path.join(base_dir, "images", f"{sample_id}.png")
    mask_path = os.path.join(base_dir, "masks", f"{sample_id}_mask.png")

    img = _read_grayscale(img_path)
    mask = _read_grayscale(mask_path)
    return img, mask

