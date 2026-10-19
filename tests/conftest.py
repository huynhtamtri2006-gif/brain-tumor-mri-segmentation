"""Fixtures nạp dữ liệu mẫu phục vụ kiểm thử tự động."""

import os
import pytest
import cv2
import numpy as np


@pytest.fixture
def sample_mri_image() -> np.ndarray:
    """Fixture nạp ảnh MRI mẫu (ưu tiên data/full, fallback data/sample)."""
    full_path = "data/full/images/TCGA_CS_4941_19960909_13.png"
    if os.path.exists(full_path):
        img = cv2.imread(full_path, cv2.IMREAD_GRAYSCALE)
        if img is not None:
            return img
    img_path = "data/sample/images/mri_brain_tumor_01.png"
    if os.path.exists(img_path):
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        return img
    # Fallback tạo ảnh nhân tạo nếu chưa có data
    synthetic = np.zeros((256, 256), dtype=np.uint8)
    cv2.circle(synthetic, (128, 128), 80, 150, -1)  # Giả lập não
    cv2.circle(synthetic, (140, 140), 20, 240, -1)  # Giả lập u
    return synthetic


@pytest.fixture
def sample_tumor_mask() -> np.ndarray:
    """Fixture nạp mặt nạ Ground Truth mẫu (ưu tiên data/full, fallback data/sample)."""
    full_path = "data/full/masks/TCGA_CS_4941_19960909_13_mask.png"
    if os.path.exists(full_path):
        mask = cv2.imread(full_path, cv2.IMREAD_GRAYSCALE)
        if mask is not None:
            return mask
    mask_path = "data/sample/masks/mri_brain_tumor_01_mask.png"
    if os.path.exists(mask_path):
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
        return mask
    synthetic = np.zeros((256, 256), dtype=np.uint8)
    cv2.circle(synthetic, (140, 140), 20, 255, -1)
    return synthetic
