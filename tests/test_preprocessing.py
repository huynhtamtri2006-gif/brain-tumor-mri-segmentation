"""Unit test kiểm thử module Tiền xử lý & Tách sọ não."""

import numpy as np
from src.preprocessing.filters import apply_bilateral_filter, apply_clahe
from src.preprocessing.skull_strip import extract_brain_mask, strip_skull


def test_bilateral_filter(sample_mri_image):
    filtered = apply_bilateral_filter(sample_mri_image)
    assert filtered.shape == sample_mri_image.shape
    assert filtered.dtype == np.uint8


def test_clahe(sample_mri_image):
    clahe_img = apply_clahe(sample_mri_image)
    assert clahe_img.shape == sample_mri_image.shape
    assert clahe_img.dtype == np.uint8


def test_skull_stripping(sample_mri_image):
    brain_mask = extract_brain_mask(sample_mri_image)
    assert brain_mask.shape == sample_mri_image.shape
    # Mask chỉ chứa 0 và 255
    unique_vals = set(np.unique(brain_mask))
    assert unique_vals.issubset({0, 255})

    stripped, mask = strip_skull(sample_mri_image, brain_mask)
    assert stripped.shape == sample_mri_image.shape
    # Vùng ngoài não phải là 0
    assert np.all(stripped[mask == 0] == 0)


def test_skull_stripping_with_intermediates(sample_mri_image):
    result = strip_skull(sample_mri_image, return_intermediates=True)
    assert len(result) == 3
    stripped, mask, intermediates = result

    expected_keys = {
        "original", "denoised", "otsu", "opened",
        "lcc", "closed_and_filled", "brain_mask", "stripped",
    }
    assert expected_keys.issubset(intermediates.keys())

    for key in expected_keys:
        step_image = intermediates[key]
        assert step_image.shape == sample_mri_image.shape
        assert step_image.dtype == np.uint8

    assert np.array_equal(mask, intermediates["brain_mask"])
    assert np.array_equal(stripped, intermediates["stripped"])
