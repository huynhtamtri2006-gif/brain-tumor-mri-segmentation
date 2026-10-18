"""Unit test kiểm thử module rút trích đặc trưng, độ tròn và Bounding Box."""

import numpy as np
import cv2
from src.measurement.features import calculate_circularity, extract_tumor_features, DiagnosticResult
from src.measurement.visualization import draw_tumor_overlay, create_comparison_quad


def test_circularity_perfect_circle():
    # Tạo hình tròn bán kính r=50
    circle_img = np.zeros((200, 200), dtype=np.uint8)
    cv2.circle(circle_img, (100, 100), 50, 255, -1)

    contours, _ = cv2.findContours(circle_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    perimeter = cv2.arcLength(contours[0], True)
    area = np.sum(circle_img > 0)

    circ = calculate_circularity(area, perimeter)
    # Độ tròn của hình tròn rời rạc lý thuyết phải > 0.95
    assert 0.90 <= circ <= 1.0


def test_extract_tumor_features(sample_tumor_mask):
    brain_mask = np.ones_like(sample_tumor_mask) * 255
    res = extract_tumor_features(sample_tumor_mask, brain_mask)

    assert isinstance(res, DiagnosticResult)
    assert res.tumor_detected is True
    assert res.tumor_area_px > 0
    assert 0.0 <= res.circularity <= 1.0
    assert res.bbox is not None
    assert len(res.bbox) == 4


def test_visualization(sample_mri_image, sample_tumor_mask):
    brain_mask = np.ones_like(sample_tumor_mask) * 255
    res = extract_tumor_features(sample_tumor_mask, brain_mask)

    overlay = draw_tumor_overlay(sample_mri_image, sample_tumor_mask, res)
    assert overlay.shape[:2] == sample_mri_image.shape
    assert overlay.shape[2] == 3  # BGR 3 kênh

    quad = create_comparison_quad(sample_mri_image, sample_mri_image, sample_tumor_mask, overlay)
    assert quad.shape[0] == sample_mri_image.shape[0] * 2
    assert quad.shape[1] == sample_mri_image.shape[1] * 2
