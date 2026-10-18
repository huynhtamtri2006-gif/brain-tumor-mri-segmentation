"""
download_full_dataset.py - Script tải tự động 100% toàn bộ 3,929 lát cắt MRI từ TCGA-LGG (Hugging Face)
Lưu vào data/full/ (images/, masks/, metadata.csv) với chuẩn hóa PNG 256x256 uint8.
"""

import os
import sys
import glob
import time
import shutil
import cv2
import numpy as np
import pandas as pd
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from huggingface_hub import snapshot_download

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def process_single_patient(patient_dir, output_img_dir, output_mask_dir):
    """Xử lý và chuyển đổi tất cả lát cắt của một bệnh nhân sang PNG chuẩn."""
    records = []
    patient_id = os.path.basename(patient_dir)
    mask_files = glob.glob(os.path.join(patient_dir, "*_mask.tif"))
    
    for mask_path in mask_files:
        mask_fname = os.path.basename(mask_path)
        img_fname = mask_fname.replace("_mask.tif", ".tif")
        img_path = os.path.join(patient_dir, img_fname)
        
        if not os.path.exists(img_path):
            continue
            
        # Đọc ảnh gốc và mặt nạ
        img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
        
        if img is None or mask is None:
            continue
            
        # Chuẩn hóa nếu là 3 kênh hoặc khác kích thước
        if len(img.shape) == 3:
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            img_gray = img
            
        # Đảm bảo nhị phân 0 hoặc 255 cho mask
        _, mask_bin = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
        
        slice_id = mask_fname.replace("_mask.tif", "")
        out_img_name = f"{slice_id}.png"
        out_mask_name = f"{slice_id}_mask.png"
        
        out_img_path = os.path.join(output_img_dir, out_img_name)
        out_mask_path = os.path.join(output_mask_dir, out_mask_name)
        
        cv2.imwrite(out_img_path, img_gray)
        cv2.imwrite(out_mask_path, mask_bin)
        
        h, w = mask_bin.shape[:2]
        tumor_pixels = int(np.sum(mask_bin > 0))
        tumor_ratio = round((tumor_pixels / (h * w)) * 100, 4)
        has_tumor = tumor_pixels > 0
        
        records.append({
            "sample_id": slice_id,
            "patient_id": patient_id,
            "source_file": img_fname,
            "image_file": out_img_name,
            "mask_file": out_mask_name,
            "width": w,
            "height": h,
            "tumor_area_pixels": tumor_pixels,
            "tumor_ratio_percent": tumor_ratio,
            "has_tumor": has_tumor
        })
        
    return records

def main():
    print("=================================================================")
    print("🚀 BẮT ĐẦU TẢI & CHUẨN HÓA TOÀN BỘ 3,929 LÁT CẮT TCGA-LGG BENCHMARK")
    print("=================================================================")
    
    start_total = time.time()
    
    # 1. Đường dẫn thư mục
    raw_hf_dir = "data/raw_hf"
    full_dir = "data/full"
    full_img_dir = os.path.join(full_dir, "images")
    full_mask_dir = os.path.join(full_dir, "masks")
    
    os.makedirs(full_img_dir, exist_ok=True)
    os.makedirs(full_mask_dir, exist_ok=True)
    
    # 2. Tải toàn bộ repository từ Hugging Face
    print("\n[Bước 1/3] Đang tải toàn bộ dataset từ Hugging Face qua snapshot_download (16 workers)...")
    t0 = time.time()
    downloaded_path = snapshot_download(
        repo_id="Ehsan-rmz/lgg-mri-segmentation-research",
        repo_type="dataset",
        local_dir=raw_hf_dir,
        allow_patterns=["data/**", "data.csv", "README.md"],
        max_workers=16
    )
    print(f"✅ Tải xong toàn bộ tệp trong {round(time.time() - t0, 2)} giây về: {downloaded_path}")
    
    # 3. Quét các thư mục bệnh nhân
    data_content_dir = os.path.join(raw_hf_dir, "data")
    if not os.path.exists(data_content_dir):
        data_content_dir = raw_hf_dir
        
    patient_dirs = [os.path.join(data_content_dir, d) for d in os.listdir(data_content_dir) 
                    if os.path.isdir(os.path.join(data_content_dir, d)) and not d.startswith(".")]
    
    print(f"\n[Bước 2/3] Tìm thấy {len(patient_dirs)} thư mục bệnh nhân. Đang xử lý và chuyển đổi sang PNG...")
    
    all_records = []
    t1 = time.time()
    
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [
            executor.submit(process_single_patient, pdir, full_img_dir, full_mask_dir)
            for pdir in patient_dirs
        ]
        for f in futures:
            all_records.extend(f.result())
            
    print(f"✅ Đã xử lý và chuẩn hóa {len(all_records)} lát cắt trong {round(time.time() - t1, 2)} giây.")
    
    # 4. Xuất metadata.csv
    print("\n[Bước 3/3] Đang lập bảng metadata.csv thống kê toàn diện...")
    df = pd.DataFrame(all_records)
    # Sắp xếp theo patient_id và sample_id
    df = df.sort_values(by=["patient_id", "sample_id"]).reset_index(drop=True)
    metadata_path = os.path.join(full_dir, "metadata.csv")
    df.to_csv(metadata_path, index=False, encoding='utf-8')
    
    # Thống kê nhanh
    num_total = len(df)
    num_positive = int(df["has_tumor"].sum())
    num_negative = num_total - num_positive
    
    print("\n" + "=" * 65)
    print("🎉 HOÀN TẤT THIẾT LẬP DỮ LIỆU FULL 100% TCGA-LGG BENCHMARK")
    print("=" * 65)
    print(f"📁 Thư mục ảnh full:         {full_img_dir} ({len(os.listdir(full_img_dir))} files)")
    print(f"📁 Thư mục mặt nạ full:      {full_mask_dir} ({len(os.listdir(full_mask_dir))} files)")
    print(f"📄 Bảng metadata full:       {metadata_path}")
    print(f"👥 Tổng số bệnh nhân:        {df['patient_id'].nunique()} bệnh nhân")
    print(f"🖼️ Tổng số lát cắt:          {num_total} lát cắt")
    print(f"   ├─ Lát cắt có u não:      {num_positive} lát ({round(num_positive/num_total*100, 2)}%)")
    print(f"   └─ Lát cắt não lành:      {num_negative} lát ({round(num_negative/num_total*100, 2)}%)")
    if num_positive > 0:
        pos_df = df[df["has_tumor"]]
        print(f"🔬 Diện tích u (px):         Min={pos_df['tumor_area_pixels'].min()}, Max={pos_df['tumor_area_pixels'].max()}, Median={pos_df['tumor_area_pixels'].median():.1f}")
        print(f"📊 Tỷ lệ u/não (%):          Min={pos_df['tumor_ratio_percent'].min()}%, Max={pos_df['tumor_ratio_percent'].max()}%, Mean={pos_df['tumor_ratio_percent'].mean():.2f}%")
    print(f"⏱️ Tổng thời gian thực thi:   {round(time.time() - start_total, 2)} giây")
    print("=" * 65)

if __name__ == "__main__":
    main()
