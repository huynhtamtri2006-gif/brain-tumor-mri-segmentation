"""Bộ đo định lượng y khoa đánh giá phân đoạn khối u não.

Phụ trách: Huỳnh Tâm Trí (MSSV: 2045240315).
Tài liệu tham khảo: Buda et al. (2019) TCGA-LGG Benchmark, Taha & Hanbury (2015) Metrics for evaluating 3D medical image segmentation.
"""

from typing import Dict
import numpy as np


def calculate_dice(pred_mask: np.ndarray, gt_mask: np.ndarray, smooth: float = 1e-6) -> float:
    """Tính chỉ số tương đồng Dice Similarity Coefficient (DSC / F1-Score).
    
    Công thức: Dice = (2 * |P ∩ G|) / (|P| + |G|) = (2 * TP) / (2 * TP + FP + FN)
    
    Args:
        pred_mask: Mặt nạ nhị phân dự đoán bởi thuật toán (H, W).
        gt_mask: Mặt nạ Ground Truth do chuyên gia y tế gán nhãn (H, W).
        smooth: Hằng số làm trơn tránh chia cho 0 khi cả 2 mặt nạ đều rỗng.
        
    Returns:
        float: Điểm Dice trong khoảng [0.0, 1.0].
    """
    p = (pred_mask > 0).astype(np.float32)
    g = (gt_mask > 0).astype(np.float32)

    intersection = np.sum(p * g)
    total_area = np.sum(p) + np.sum(g)

    if total_area == 0:
        return 1.0  # Cả 2 đều rỗng (không có u và dự đoán đúng không có u)

    if intersection == 0:
        return 0.0

    return float((2.0 * intersection + smooth) / (total_area + smooth))


def calculate_iou(pred_mask: np.ndarray, gt_mask: np.ndarray, smooth: float = 1e-6) -> float:
    """Tính chỉ số Jaccard Index (Intersection over Union - IoU).
    
    Công thức: IoU = |P ∩ G| / |P ∪ G| = TP / (TP + FP + FN) = Dice / (2 - Dice)
    
    Args:
        pred_mask: Mặt nạ dự đoán (H, W).
        gt_mask: Mặt nạ Ground Truth (H, W).
        
    Returns:
        float: Điểm IoU trong khoảng [0.0, 1.0].
    """
    p = (pred_mask > 0).astype(np.float32)
    g = (gt_mask > 0).astype(np.float32)

    intersection = np.sum(p * g)
    union = np.sum(p) + np.sum(g) - intersection

    if union == 0:
        return 1.0

    if intersection == 0:
        return 0.0

    return float((intersection + smooth) / (union + smooth))


def calculate_sensitivity(pred_mask: np.ndarray, gt_mask: np.ndarray, smooth: float = 1e-6) -> float:
    """Tính độ nhạy (Sensitivity / Recall / True Positive Rate).
    
    Đo tỷ lệ pixel u thực tế được thuật toán phát hiện thành công:
    Sensitivity = TP / (TP + FN)
    
    Args:
        pred_mask: Mặt nạ dự đoán (H, W).
        gt_mask: Mặt nạ Ground Truth (H, W).
        
    Returns:
        float: Giá trị độ nhạy trong khoảng [0.0, 1.0].
    """
    p = (pred_mask > 0).astype(np.float32)
    g = (gt_mask > 0).astype(np.float32)

    tp = np.sum(p * g)
    actual_positives = np.sum(g)

    if actual_positives == 0:
        return 1.0 if np.sum(p) == 0 else 0.0

    if tp == 0:
        return 0.0

    return float((tp + smooth) / (actual_positives + smooth))


def calculate_specificity(pred_mask: np.ndarray, gt_mask: np.ndarray, smooth: float = 1e-6) -> float:
    """Tính độ đặc hiệu (Specificity / True Negative Rate).
    
    Đo khả năng không nhận nhầm mô não lành thành u não:
    Specificity = TN / (TN + FP)
    
    Args:
        pred_mask: Mặt nạ dự đoán (H, W).
        gt_mask: Mặt nạ Ground Truth (H, W).
        
    Returns:
        float: Giá trị độ đặc hiệu trong khoảng [0.0, 1.0].
    """
    p = (pred_mask > 0).astype(np.bool_)
    g = (gt_mask > 0).astype(np.bool_)

    tn = np.sum((~p) & (~g))
    fp = np.sum(p & (~g))
    actual_negatives = tn + fp

    if actual_negatives == 0:
        return 1.0

    if tn == 0:
        return 0.0

    return float((tn + smooth) / (actual_negatives + smooth))



def calculate_all_metrics(pred_mask: np.ndarray, gt_mask: np.ndarray) -> Dict[str, float]:
    """Tính toán đồng thời cả 4 chỉ số y khoa phục vụ báo cáo thực nghiệm.
    
    Args:
        pred_mask: Mặt nạ dự đoán (H, W).
        gt_mask: Mặt nạ Ground Truth (H, W).
        
    Returns:
        Dict[str, float]: Từ điển chứa {'dice', 'iou', 'sensitivity', 'specificity'}.
    """
    return {
        "dice": round(calculate_dice(pred_mask, gt_mask), 4),
        "iou": round(calculate_iou(pred_mask, gt_mask), 4),
        "sensitivity": round(calculate_sensitivity(pred_mask, gt_mask), 4),
        "specificity": round(calculate_specificity(pred_mask, gt_mask), 4)
    }
