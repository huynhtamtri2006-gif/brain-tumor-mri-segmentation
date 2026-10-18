"""Helper utilities phục vụ hiển thị Streamlit GUI."""

from typing import List
import os
import cv2
import numpy as np


def list_sample_cases(sample_dir: str = "data/sample/images") -> List[str]:
    """Lấy danh sách các file mẫu có sẵn trong data/sample/images."""
    if not os.path.exists(sample_dir):
        return []
    return sorted([f for f in os.listdir(sample_dir) if f.endswith(".png")])


def load_image_and_mask(sample_id: str, base_dir: str = "data/sample") -> Tuple_Loaded:
    """Nạp ảnh MRI gốc và mặt nạ Ground Truth tương ứng."""
    img_path = os.path.join(base_dir, "images", f"{sample_id}.png")
    mask_path = os.path.join(base_dir, "masks", f"{sample_id}_mask.png")

    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE) if os.path.exists(img_path) else None
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE) if os.path.exists(mask_path) else None
    return img, mask


Tuple_Loaded = tuple
