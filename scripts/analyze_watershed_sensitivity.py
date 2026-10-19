#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Khảo sát độ nhạy siêu tham số `dist_thresh_ratio` của Marker-controlled Watershed.

Lấy mẫu lát cắt CÓ U từ `data/full/metadata.csv`, chạy chuỗi
Tách sọ -> Watershed cho 5 mức `dist_thresh_ratio` và tính Dice, IoU,
Sensitivity, Specificity trung bình so với Ground Truth.

Kết quả: bảng số liệu trên terminal + đồ thị 2 biểu đồ
`reports/figures/watershed_param_sensitivity.png` (dpi=300).

Chạy từ thư mục gốc repo:

    python scripts/analyze_watershed_sensitivity.py
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path
from typing import Dict, List

import cv2
import matplotlib

matplotlib.use("Agg")  # Backend không cần màn hình (CI/terminal)
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # pragma: no cover - môi trường không hỗ trợ reconfigure
        pass

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.evaluation.metrics import calculate_all_metrics  # noqa: E402
from src.preprocessing.skull_strip import strip_skull  # noqa: E402
from src.segmentation.watershed import segment_watershed  # noqa: E402

DATA_ROOT = ROOT / "data" / "full"
METADATA_PATH = DATA_ROOT / "metadata.csv"
OUTPUT_PATH = ROOT / "reports" / "figures" / "watershed_param_sensitivity.png"
RATIOS = (0.2, 0.3, 0.4, 0.5, 0.6)
SAMPLE_LIMIT = 30
METRIC_KEYS = ("dice", "iou", "sensitivity", "specificity")


def select_positive_slices(limit: int = SAMPLE_LIMIT) -> List[Dict[str, str]]:
    """Chọn các lát cắt có u, rải đều trên toàn bộ danh sách metadata."""
    with METADATA_PATH.open("r", encoding="utf-8", newline="") as fh:
        rows = [row for row in csv.DictReader(fh)
                if row.get("has_tumor", "").strip().lower() == "true"]

    if not rows:
        raise RuntimeError("metadata.csv không có lát cắt nào has_tumor=True")
    if len(rows) <= limit:
        return rows

    # Lấy mẫu hệ thống (deterministic), khử trùng lặp chỉ số.
    indices = sorted({int(round(i)) for i in np.linspace(0, len(rows) - 1, limit)})
    return [rows[i] for i in indices]


def evaluate_ratios(rows: List[Dict[str, str]]) -> Dict[float, Dict[str, float]]:
    """Chạy watershed cho từng mức ratio và trả về chỉ số trung bình."""
    accum: Dict[float, Dict[str, List[float]]] = {
        ratio: {key: [] for key in METRIC_KEYS} for ratio in RATIOS
    }
    used = 0

    for row in rows:
        image_path = DATA_ROOT / "images" / row["image_file"]
        mask_path = DATA_ROOT / "masks" / row["mask_file"]
        image = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
        gt_mask = cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE)
        if image is None or gt_mask is None:
            continue

        stripped, _ = strip_skull(image)
        for ratio in RATIOS:
            pred_mask = segment_watershed(stripped, dist_thresh_ratio=ratio)
            metrics = calculate_all_metrics(pred_mask, gt_mask)
            for key in METRIC_KEYS:
                accum[ratio][key].append(float(metrics[key]))
        used += 1

    if used == 0:
        raise RuntimeError("Không đọc được cặp ảnh/mặt nạ nào từ data/full")

    print(f"Đã đánh giá {used} lát cắt có u (trên {len(rows)} lát cắt được chọn).")
    return {
        ratio: {key: float(np.mean(values)) for key, values in metrics.items()}
        for ratio, metrics in accum.items()
    }


def plot_sensitivity(summary: Dict[float, Dict[str, float]]) -> None:
    """Vẽ 2 biểu đồ: (Dice, IoU) và (Sensitivity, Specificity) theo ratio."""
    ratios = list(RATIOS)
    dice = [summary[r]["dice"] for r in ratios]
    iou = [summary[r]["iou"] for r in ratios]
    sensitivity = [summary[r]["sensitivity"] for r in ratios]
    specificity = [summary[r]["specificity"] for r in ratios]

    plt.rcParams["font.family"] = "DejaVu Sans"
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)

    axes[0].plot(ratios, dice, marker="o", linewidth=2.2, color="#d62728", label="Dice")
    axes[0].plot(ratios, iou, marker="s", linewidth=2.2, color="#1f77b4", label="IoU")
    axes[0].set_title("Chỉ số tương đồng Dice & IoU", fontsize=13, fontweight="bold")
    axes[0].set_xlabel("dist_thresh_ratio")
    axes[0].set_ylabel("Giá trị trung bình")
    axes[0].set_xticks(ratios)
    axes[0].set_ylim(0.0, 1.02)
    axes[0].grid(True, linestyle="--", alpha=0.5)
    axes[0].legend()

    axes[1].plot(ratios, sensitivity, marker="^", linewidth=2.2, color="#2ca02c",
                 label="Sensitivity")
    axes[1].plot(ratios, specificity, marker="v", linewidth=2.2, color="#9467bd",
                 label="Specificity")
    axes[1].set_title("Độ nhạy & Độ đặc hiệu", fontsize=13, fontweight="bold")
    axes[1].set_xlabel("dist_thresh_ratio")
    axes[1].set_ylabel("Giá trị trung bình")
    axes[1].set_xticks(ratios)
    axes[1].set_ylim(0.0, 1.02)
    axes[1].grid(True, linestyle="--", alpha=0.5)
    axes[1].legend()

    fig.suptitle(
        "Khảo sát độ nhạy siêu tham số dist_thresh_ratio — Marker-controlled Watershed",
        fontsize=15, fontweight="bold",
    )
    fig.tight_layout(rect=(0, 0, 1, 0.94))

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_PATH, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main() -> int:
    rows = select_positive_slices()
    summary = evaluate_ratios(rows)

    header = f"{'ratio':>6} | {'Dice':>7} | {'IoU':>7} | {'Sens':>7} | {'Spec':>7}"
    print()
    print(header)
    print("-" * len(header))
    for ratio in RATIOS:
        m = summary[ratio]
        print(f"{ratio:>6.1f} | {m['dice']:>7.4f} | {m['iou']:>7.4f} | "
              f"{m['sensitivity']:>7.4f} | {m['specificity']:>7.4f}")

    best_ratio = max(RATIOS, key=lambda r: summary[r]["dice"])
    print(f"\nMức tối ưu theo Dice trung bình: dist_thresh_ratio = {best_ratio:.1f}")

    plot_sensitivity(summary)
    size_kb = OUTPUT_PATH.stat().st_size / 1024
    print(f"Đã xuất: {OUTPUT_PATH.relative_to(ROOT)} ({size_kb:.1f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
