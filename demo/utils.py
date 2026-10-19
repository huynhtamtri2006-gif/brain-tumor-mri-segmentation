"""Helper utilities phục vụ hiển thị Streamlit GUI."""

from typing import List, Tuple, Optional
import os
import cv2
import numpy as np


def get_default_base_dir() -> str:
    """Trả về thư mục dữ liệu cơ sở mặc định (ưu tiên data/full, fallback data/sample)."""
    full_dir = "data/full"
    if os.path.exists(os.path.join(full_dir, "images")) and len(os.listdir(os.path.join(full_dir, "images"))) > 50:
        return full_dir
    return "data/sample"


def get_default_data_dir() -> str:
    """Trả về thư mục ảnh mặc định (ưu tiên data/full/images, fallback data/sample/images)."""
    return os.path.join(get_default_base_dir(), "images")


def list_sample_cases(data_dir: Optional[str] = None) -> List[str]:
    """Lấy danh sách các file ảnh có sẵn trong thư mục ảnh (mặc định ưu tiên data/full)."""
    if data_dir is None:
        data_dir = get_default_data_dir()
    if not os.path.exists(data_dir):
        return []
    return sorted([f for f in os.listdir(data_dir) if f.endswith(".png")])


def load_image_and_mask(sample_id: str, base_dir: Optional[str] = None) -> Tuple[Optional[np.ndarray], Optional[np.ndarray]]:
    """Nạp ảnh MRI gốc và mặt nạ Ground Truth tương ứng (mặc định ưu tiên data/full)."""
    if base_dir is None:
        base_dir = get_default_base_dir()
    img_path = os.path.join(base_dir, "images", f"{sample_id}.png")
    mask_path = os.path.join(base_dir, "masks", f"{sample_id}_mask.png")

    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE) if os.path.exists(img_path) else None
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE) if os.path.exists(mask_path) else None
    return img, mask

