import os
import sys
import shutil
import urllib.request
import json
import numpy as np
import cv2
import pandas as pd

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("=== TAI 20 MAU ANH MRI U NAO BENCHMARK (TCGA-LGG) ===")
    
    # 1. Duong dan luu tru
    sample_dir = "data/sample"
    img_dir = os.path.join(sample_dir, "images")
    mask_dir = os.path.join(sample_dir, "masks")
    
    # Don dep thu muc cu neu co
    for old_dir in ["data/sample/skin", "data/sample/xray", "data/sample/mri"]:
        if os.path.exists(old_dir):
            shutil.rmtree(old_dir, ignore_errors=True)
            print(f"Da don dep thu muc cu: {old_dir}")
            
    os.makedirs(img_dir, exist_ok=True)
    os.makedirs(mask_dir, exist_ok=True)
    
    # 2. Lay danh sach files tu Hugging Face
    api_url = "https://huggingface.co/api/datasets/Ehsan-rmz/lgg-mri-segmentation-research"
    req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
    
    mask_files = [s.get('rfilename') for s in data.get('siblings', []) if s.get('rfilename', '').endswith('_mask.tif')]
    print(f"Tong so lat cat MRI co san: {len(mask_files)}")
    
    base_url = "https://huggingface.co/datasets/Ehsan-rmz/lgg-mri-segmentation-research/resolve/main/"
    
    curated_samples = []
    # Chon lat cat tu nhieu benh nhan khac nhau de dam bao tinh da dang
    patient_count = {}
    
    for rpath in mask_files:
        if len(curated_samples) >= 20:
            break
            
        parts = rpath.split('/')
        if len(parts) < 2:
            continue
        patient_folder = parts[1]
        mask_fname = parts[-1]
        img_fname = mask_fname.replace('_mask.tif', '.tif')
        img_rpath = f"data/{patient_folder}/{img_fname}"
        
        # Gioi han toi da 2 lat cat moi benh nhan de da dang hoa
        if patient_count.get(patient_folder, 0) >= 2:
            continue
            
        mask_dl_url = base_url + rpath
        try:
            req_m = urllib.request.Request(mask_dl_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req_m) as resp_m:
                mask_bytes = resp_m.read()
            mask_arr = cv2.imdecode(np.frombuffer(mask_bytes, np.uint8), cv2.IMREAD_UNCHANGED)
            if mask_arr is None:
                continue
                
            tumor_pixels = int(np.sum(mask_arr > 0))
            # Chon cac ca co u ro rang (tu 500 den 8000 pixels)
            if 500 <= tumor_pixels <= 8000:
                # Tai anh tuong ung
                img_dl_url = base_url + img_rpath
                req_i = urllib.request.Request(img_dl_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req_i) as resp_i:
                    img_bytes = resp_i.read()
                img_arr = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_UNCHANGED)
                if img_arr is None:
                    continue
                
                idx = len(curated_samples) + 1
                sample_id = f"mri_brain_tumor_{idx:02d}"
                out_img_name = f"{sample_id}.png"
                out_mask_name = f"{sample_id}_mask.png"
                
                cv2.imwrite(os.path.join(img_dir, out_img_name), img_arr)
                cv2.imwrite(os.path.join(mask_dir, out_mask_name), mask_arr)
                
                total_pixels = mask_arr.shape[0] * mask_arr.shape[1]
                tumor_ratio = round((tumor_pixels / total_pixels) * 100, 2)
                
                curated_samples.append({
                    "sample_id": sample_id,
                    "patient_id": patient_folder,
                    "source_file": img_fname,
                    "image_file": out_img_name,
                    "mask_file": out_mask_name,
                    "width": img_arr.shape[1],
                    "height": img_arr.shape[0],
                    "tumor_area_pixels": tumor_pixels,
                    "tumor_ratio_percent": tumor_ratio
                })
                
                patient_count[patient_folder] = patient_count.get(patient_folder, 0) + 1
                print(f"[{idx:02d}/20] Tai thanh cong {sample_id} ({patient_folder}) - Dien tich u: {tumor_pixels} px ({tumor_ratio}%)")
        except Exception as e:
            continue

    meta_df = pd.DataFrame(curated_samples)
    meta_path = os.path.join(sample_dir, "metadata.csv")
    meta_df.to_csv(meta_path, index=False)
    print(f"\nHoan tat! Da luu 20 mau anh va mat na vao {img_dir} va metadata tai {meta_path}")

if __name__ == "__main__":
    main()
