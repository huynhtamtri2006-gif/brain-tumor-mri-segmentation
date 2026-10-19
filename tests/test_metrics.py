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


def test_manual_4x4_calculation():
    """Kiểm tra độ chính xác số học đối chiếu tính tay trên ma trận 4x4 (16 pixels)."""
    gt = np.zeros((4, 4), dtype=np.uint8)
    pred = np.zeros((4, 4), dtype=np.uint8)

    # GT có 4 pixel dương tính: (0,0), (0,1), (1,0), (1,1)
    gt[0:2, 0:2] = 255
    # Pred trùng 2 pixel: (0,1), (1,1) và dự đoán nhầm 2 pixel ngoài: (0,2), (1,2)
    pred[0:2, 1:3] = 255

    # TP = 2, FP = 2, FN = 2, TN = 10
    dice = calculate_dice(pred, gt)
    iou = calculate_iou(pred, gt)
    sens = calculate_sensitivity(pred, gt)
    spec = calculate_specificity(pred, gt)

    # Dice = 2*2 / (2*2 + 2 + 2) = 0.5
    assert abs(dice - 0.5) < 1e-3
    # IoU = 2 / (2 + 2 + 2) = 1/3
    assert abs(iou - (1.0 / 3.0)) < 1e-3
    # Sens = 2 / 4 = 0.5
    assert abs(sens - 0.5) < 1e-3
    # Spec = 10 / 12 = 5/6
    assert abs(spec - (5.0 / 6.0)) < 1e-3


def test_pred_empty_gt_positive():
    """Trường hợp bỏ sót hoàn toàn khối u (Missed detection): GT có u nhưng Pred rỗng."""
    gt = np.zeros((8, 8), dtype=np.uint8)
    gt[2:4, 2:4] = 255
    pred = np.zeros((8, 8), dtype=np.uint8)

    assert calculate_dice(pred, gt) < 1e-4
    assert calculate_iou(pred, gt) < 1e-4
    assert calculate_sensitivity(pred, gt) == 0.0
    assert calculate_specificity(pred, gt) == 1.0


def test_gt_empty_pred_positive():
    """Trường hợp báo động giả (False alarm): Lát não lành nhưng Pred nhận nhầm có u."""
    gt = np.zeros((8, 8), dtype=np.uint8)
    pred = np.zeros((8, 8), dtype=np.uint8)
    pred[2:4, 2:4] = 255

    assert calculate_dice(pred, gt) < 1e-4
    assert calculate_iou(pred, gt) < 1e-4
    assert calculate_sensitivity(pred, gt) == 0.0
    assert calculate_specificity(pred, gt) < 1.0

