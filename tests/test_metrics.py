"""Unit test kiểm thử module tính toán bộ đo y khoa Dice, IoU, Sensitivity, Specificity."""

import numpy as np
from src.evaluation.metrics import (
    calculate_dice,
    calculate_iou,
    calculate_sensitivity,
    calculate_specificity,
    calculate_all_metrics
)


def test_perfect_match():
    mask = np.zeros((10, 10), dtype=np.uint8)
    mask[2:6, 2:6] = 255

    dice = calculate_dice(mask, mask)
    iou = calculate_iou(mask, mask)
    sens = calculate_sensitivity(mask, mask)
    spec = calculate_specificity(mask, mask)

    assert abs(dice - 1.0) < 1e-4
    assert abs(iou - 1.0) < 1e-4
    assert abs(sens - 1.0) < 1e-4
    assert abs(spec - 1.0) < 1e-4


def test_zero_overlap():
    mask1 = np.zeros((10, 10), dtype=np.uint8)
    mask2 = np.zeros((10, 10), dtype=np.uint8)
    mask1[0:3, 0:3] = 255
    mask2[7:10, 7:10] = 255

    dice = calculate_dice(mask1, mask2)
    iou = calculate_iou(mask1, mask2)
    sens = calculate_sensitivity(mask1, mask2)

    assert dice < 1e-3
    assert iou < 1e-3
    assert sens < 1e-3


def test_empty_masks():
    empty1 = np.zeros((10, 10), dtype=np.uint8)
    empty2 = np.zeros((10, 10), dtype=np.uint8)

    assert calculate_dice(empty1, empty2) == 1.0
    assert calculate_iou(empty1, empty2) == 1.0


def test_calculate_all_metrics(sample_tumor_mask):
    # Dịch chuyển nhẹ mặt nạ để test
    shifted = np.roll(sample_tumor_mask, shift=3, axis=0)
    metrics = calculate_all_metrics(shifted, sample_tumor_mask)

    assert "dice" in metrics
    assert "iou" in metrics
    assert "sensitivity" in metrics
    assert "specificity" in metrics
    assert 0.0 <= metrics["dice"] <= 1.0
