"""Script thực thi toàn diện 1 chạm (One-click Experiment Runner).

Tự động chạy toàn bộ pipeline xử lý ảnh số (Watershed & Region Growing)
trên toàn bộ 3,929 lát cắt chuẩn TCGA-LGG (data/full).
Tối ưu hóa đa tiến trình (Multiprocessing) để tính toán siêu tốc.

Sử dụng:
    python scripts/run_all_experiments.py
"""

import os
import sys
import time
import argparse
import glob
from concurrent.futures import ProcessPoolExecutor
import pandas as pd
import numpy as np
import cv2

# Thêm đường dẫn gốc
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.preprocessing.skull_strip import strip_skull
from src.segmentation.watershed import segment_watershed
from src.segmentation.region_growing import segment_region_growing
from src.evaluation.metrics import calculate_all_metrics

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


def evaluate_single_sample(args):
    """Hàm worker xử lý 1 mẫu ảnh độc lập phục vụ multiprocessing."""
    img_path, mask_path, method = args
    sample_id = os.path.basename(img_path).replace(".png", "")
    
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    gt_mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
    
    if img is None or gt_mask is None:
        return None
        
    start_t = time.perf_counter()
    stripped, _ = strip_skull(img)
    if method == "watershed":
        pred_mask = segment_watershed(stripped, dist_thresh_ratio=0.4)
        method_name = "Watershed (Baseline)"
    else:
        pred_mask = segment_region_growing(stripped, tolerance=15)
        method_name = "Region Growing (Đối chứng)"
        
    elapsed_ms = (time.perf_counter() - start_t) * 1000.0
    
    m = calculate_all_metrics(pred_mask, gt_mask)
    has_tumor_gt = int(np.sum(gt_mask > 0)) > 0
    
    return {
        "sample_id": sample_id,
        "method": method_name,
        "has_tumor_gt": has_tumor_gt,
        "tumor_pixels_gt": int(np.sum(gt_mask > 0)),
        "tumor_pixels_pred": int(np.sum(pred_mask > 0)),
        "dice": m["dice"],
        "iou": m["iou"],
        "sensitivity": m["sensitivity"],
        "specificity": m["specificity"],
        "latency_ms": round(elapsed_ms, 2)
    }


def run_benchmark_parallel(images_dir, masks_dir, method="watershed", max_workers=None):
    image_files = sorted(glob.glob(os.path.join(images_dir, "*.png")))
    tasks = []
    for img_p in image_files:
        fname = os.path.basename(img_p)
        mask_p = os.path.join(masks_dir, fname.replace(".png", "_mask.png"))
        if os.path.exists(mask_p):
            tasks.append((img_p, mask_p, method))
            
    results = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        for r in executor.map(evaluate_single_sample, tasks, chunksize=32):
            if r is not None:
                results.append(r)
                
    return pd.DataFrame(results)


def main():
    parser = argparse.ArgumentParser(description="Chạy thực nghiệm đánh giá mô hình phân đoạn u não MRI.")
    parser.add_argument("--data-dir", type=str, default=None, help="Thư mục dữ liệu (mặc định data/full)")

    parser.add_argument("--workers", type=int, default=None, help="Số tiến trình CPU song song")
    args = parser.parse_args()

    # Tự động chọn thư mục dữ liệu
    if args.data_dir:
        data_dir = args.data_dir
    else:
        data_dir = "data/full"


    img_dir = os.path.join(data_dir, "images")
    mask_dir = os.path.join(data_dir, "masks")

    if not os.path.exists(img_dir) or not os.path.exists(mask_dir):
        print(f"Lỗi: Không tìm thấy thư mục dữ liệu {data_dir}!")
        return

    num_samples = len([f for f in os.listdir(img_dir) if f.endswith('.png')])
    print("=" * 75)
    print("  CHIẾN DỊCH THỰC NGHIỆM ĐÁNH GIÁ ĐỊNH LƯỢNG — ĐỒ ÁN XỬ LÝ ẢNH SỐ (HUIT)")
    print(f"  Tập dữ liệu: {data_dir} ({num_samples} lát cắt MRI)")
    print("  Phương pháp so sánh: Marker-controlled Watershed vs Seeded Region Growing")
    print("=" * 75)

    # 1. Chạy Benchmark Watershed
    print(f"\n[1/2] Đang chạy thực nghiệm Watershed (Baseline) trên {num_samples} mẫu (Multiprocessing)...")
    t0_ws = time.perf_counter()
    df_ws = run_benchmark_parallel(img_dir, mask_dir, method="watershed", max_workers=args.workers)
    t_ws = time.perf_counter() - t0_ws
    print(f"--> Hoàn tất Watershed ({len(df_ws)} mẫu) trong {t_ws:.2f}s (~{len(df_ws)/max(t_ws, 0.001):.1f} fps)!")

    # 2. Chạy Benchmark Region Growing
    print(f"\n[2/2] Đang chạy thực nghiệm Region Growing (Đối chứng) trên {num_samples} mẫu (Multiprocessing)...")
    t0_rg = time.perf_counter()
    df_rg = run_benchmark_parallel(img_dir, mask_dir, method="region_growing", max_workers=args.workers)
    t_rg = time.perf_counter() - t0_rg
    print(f"--> Hoàn tất Region Growing ({len(df_rg)} mẫu) trong {t_rg:.2f}s (~{len(df_rg)/max(t_rg, 0.001):.1f} fps)!")

    # 3. Phân tách tập dương tính (có u) và âm tính (không u) nếu là tập full
    pos_ws = df_ws[df_ws["has_tumor_gt"]] if "has_tumor_gt" in df_ws else df_ws
    pos_rg = df_rg[df_rg["has_tumor_gt"]] if "has_tumor_gt" in df_rg else df_rg
    neg_ws = df_ws[~df_ws["has_tumor_gt"]] if "has_tumor_gt" in df_ws else df_ws
    neg_rg = df_rg[~df_rg["has_tumor_gt"]] if "has_tumor_gt" in df_rg else df_rg

    # 4. Tạo bảng tổng hợp so sánh (Tập lát cắt có u)
    summary_pos_df = pd.DataFrame({
        "Chỉ Số Đánh Giá Y Khoa": [
            "Quy mô lát cắt có u đánh giá",
            "Dice Score (DSC / F1)",
            "IoU (Jaccard Index)",
            "Sensitivity (Độ nhạy)",
            "Specificity (Độ đặc hiệu)",
            "Độ trễ trung bình (ms/ảnh)"
        ],
        "Watershed (Baseline)": [
            f"{len(pos_ws)} lát cắt",
            f"{pos_ws['dice'].mean():.4f} +/- {pos_ws['dice'].std():.4f}",
            f"{pos_ws['iou'].mean():.4f} +/- {pos_ws['iou'].std():.4f}",
            f"{pos_ws['sensitivity'].mean():.4f} +/- {pos_ws['sensitivity'].std():.4f}",
            f"{pos_ws['specificity'].mean():.4f} +/- {pos_ws['specificity'].std():.4f}",
            f"{df_ws['latency_ms'].mean():.2f} +/- {df_ws['latency_ms'].std():.2f} ms"
        ],
        "Region Growing (Đối chứng)": [
            f"{len(pos_rg)} lát cắt",
            f"{pos_rg['dice'].mean():.4f} +/- {pos_rg['dice'].std():.4f}",
            f"{pos_rg['iou'].mean():.4f} +/- {pos_rg['iou'].std():.4f}",
            f"{pos_rg['sensitivity'].mean():.4f} +/- {pos_rg['sensitivity'].std():.4f}",
            f"{pos_rg['specificity'].mean():.4f} +/- {pos_rg['specificity'].std():.4f}",
            f"{df_rg['latency_ms'].mean():.2f} +/- {df_rg['latency_ms'].std():.2f} ms"
        ]
    })

    print("\n" + "=" * 75)
    print("  BẢNG TỔNG HỢP KẾT QUẢ ĐỊNH LƯỢNG TRÊN LÁT CẮT CÓ U (MEAN +/- STD)")
    print("=" * 75)
    print(summary_pos_df.to_string(index=False))
    print("=" * 75)

    if len(neg_ws) > 0:
        print("\n" + "-" * 75)
        print(f"  ĐÁNH GIÁ TRÊN TẬP LÁT CẮT NÃO LÀNH KHÔNG U ({len(neg_ws)} LÁT CẮT):")
        print(f"  * Watershed Specificity:      {neg_ws['specificity'].mean():.4f} +/- {neg_ws['specificity'].std():.4f}")
        print(f"  * Region Growing Specificity: {neg_rg['specificity'].mean():.4f} +/- {neg_rg['specificity'].std():.4f}")
        print("-" * 75)

    # 5. Lưu kết quả ra file
    out_csv = "docs/BENCHMARK_RESULTS.csv"
    summary_pos_df.to_csv(out_csv, index=False, encoding='utf-8')
    print(f"\n✅ Đã cập nhật bảng kết quả tóm tắt vào: {out_csv}")

    # Nếu là tập lớn, lưu chi tiết từng lát cắt
    if num_samples > 100:
        full_detail = pd.concat([df_ws, df_rg]).reset_index(drop=True)
        out_detail_csv = "docs/BENCHMARK_RESULTS_FULL.csv"
        full_detail.to_csv(out_detail_csv, index=False, encoding='utf-8')
        print(f"✅ Đã lưu kết quả chi tiết {len(full_detail)} dòng vào: {out_detail_csv}")


if __name__ == "__main__":
    main()
