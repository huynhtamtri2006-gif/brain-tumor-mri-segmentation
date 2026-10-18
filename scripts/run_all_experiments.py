"""Script thực thi toàn diện 1 chạm (One-click Experiment Runner).

Tự động chạy toàn bộ pipeline xử lý ảnh số trên 20 mẫu bệnh nhân TCGA-LGG,
tính toán bảng chỉ số Mean ± Std, đo thời gian xử lý và in báo cáo chuẩn.

Sử dụng:
    python scripts/run_all_experiments.py
"""

import os
import sys
import time
import pandas as pd
import numpy as np

# Thêm đường dẫn gốc
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.preprocessing.skull_strip import strip_skull
from src.segmentation.watershed import segment_watershed
from src.segmentation.region_growing import segment_region_growing
from src.evaluation.benchmark import run_benchmark

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("=" * 70)
    print("  CHIEN DICH THUC NGHIEM TOAN DIEN — DO AN XU LY ANH SO (HUIT)")
    print("  De tai: Phan doan & Phat hien khoi u nao tren anh MRI (TCGA-LGG)")
    print("  Nhom sinh vien: Ha Manh Truong (Lead) & Huynh Tam Tri (Member)")
    print("=" * 70)

    img_dir = "data/sample/images"
    mask_dir = "data/sample/masks"

    if not os.path.exists(img_dir) or not os.path.exists(mask_dir):
        print("Loi: Khong tim thay thu muc data/sample!")
        return

    # 1. Chạy Benchmark Phương án A: Watershed
    print("\n[1/2] Dang chay thuc nghiem Phuong an A: Marker-controlled Watershed (Baseline)...")
    def predict_ws(img):
        stripped, _ = strip_skull(img)
        return segment_watershed(stripped, dist_thresh_ratio=0.4)

    start_ws = time.perf_counter()
    df_ws = run_benchmark(img_dir, mask_dir, predict_ws, method_name="Watershed (Baseline)")
    time_ws = time.perf_counter() - start_ws
    print(f"--> Hoan tat 20 mau Watershed trong {time_ws:.2f}s!")

    # 2. Chạy Benchmark Phương án B: Region Growing
    print("\n[2/2] Dang chay thuc nghiem Phuong an B: Seeded Region Growing (Doi chung)...")
    def predict_rg(img):
        stripped, _ = strip_skull(img)
        return segment_region_growing(stripped, tolerance=15)

    start_rg = time.perf_counter()
    df_rg = run_benchmark(img_dir, mask_dir, predict_rg, method_name="Region Growing (Doi chung)")
    time_rg = time.perf_counter() - start_rg
    print(f"--> Hoan tat 20 mau Region Growing trong {time_rg:.2f}s!")

    # 3. Tạo bảng tổng hợp so sánh chuẩn học thuật (Mean ± Std)
    summary_df = pd.DataFrame({
        "Chi So Danh Gia Y Khoa": [
            "Dice Score (DSC / F1)",
            "IoU (Jaccard Index)",
            "Sensitivity (Do nhay)",
            "Specificity (Dac hieu)",
            "Do tre trung binh (ms)"
        ],
        "Watershed (Baseline)": [
            f"{df_ws['dice'].mean():.4f} +/- {df_ws['dice'].std():.4f}",
            f"{df_ws['iou'].mean():.4f} +/- {df_ws['iou'].std():.4f}",
            f"{df_ws['sensitivity'].mean():.4f} +/- {df_ws['sensitivity'].std():.4f}",
            f"{df_ws['specificity'].mean():.4f} +/- {df_ws['specificity'].std():.4f}",
            f"{df_ws['latency_ms'].mean():.2f} +/- {df_ws['latency_ms'].std():.2f} ms"
        ],
        "Region Growing (Doi chung)": [
            f"{df_rg['dice'].mean():.4f} +/- {df_rg['dice'].std():.4f}",
            f"{df_rg['iou'].mean():.4f} +/- {df_rg['iou'].std():.4f}",
            f"{df_rg['sensitivity'].mean():.4f} +/- {df_rg['sensitivity'].std():.4f}",
            f"{df_rg['specificity'].mean():.4f} +/- {df_rg['specificity'].std():.4f}",
            f"{df_rg['latency_ms'].mean():.2f} +/- {df_rg['latency_ms'].std():.2f} ms"
        ]
    })

    print("\n" + "=" * 70)
    print("  BANG TONG HOP KET QUA DINH LUONG SO SANH 2 PHUONG PHAP (MEAN +/- STD)")
    print("=" * 70)
    print(summary_df.to_string(index=False))
    print("=" * 70)

    # Lưu kết quả ra CSV
    out_csv = "docs/BENCHMARK_RESULTS.csv"
    summary_df.to_csv(out_csv, index=False)
    print(f"\nDa luu bang ket qua so sanh dinh luong vao {out_csv}")

if __name__ == "__main__":
    main()
