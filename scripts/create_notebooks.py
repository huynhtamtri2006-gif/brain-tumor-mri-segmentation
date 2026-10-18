"""Script tạo 4 file Jupyter Notebook chuẩn hóa phục vụ báo cáo và thực nghiệm đồ án.

Học phần: Xử lý ảnh số (2026-2027) - HUIT.
"""

import os
import json

os.makedirs("notebooks", exist_ok=True)

def make_notebook(cells):
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.12"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }

def md_cell(text):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in text.strip().split("\n")]
    }

def code_cell(code):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in code.strip().split("\n")]
    }

# ==========================================
# NOTEBOOK 1: KHÁM PHÁ DỮ LIỆU
# ==========================================
nb1_cells = [
    md_cell("""# Notebook 1: Khảo Sát & Khám Phá Dữ Liệu MRI U Não (TCGA-LGG)
**Đồ án Xử lý ảnh số (2026–2027) — Khoa CNTT — HUIT**  
**Nhóm sinh viên:** Hà Mạnh Trường (2045240326) & Huỳnh Tâm Trí (2045240315)  
**Phụ trách chính:** Huỳnh Tâm Trí

---
### Mục tiêu:
1. Nạp và kiểm tra bảng thống kê 20 ca bệnh mẫu từ `data/sample/metadata.csv`.
2. Khảo sát phân bố diện tích u, tỷ lệ % u/não.
3. Trực quan hóa hình thái khối u trên ảnh MRI và mặt nạ Ground Truth."""),

    code_cell("""import os
import sys
import pandas as pd
import numpy as np
import cv2
import matplotlib.pyplot as plt

# Thêm thư mục gốc vào đường dẫn hệ thống
sys.path.append(os.path.abspath(".."))
plt.rcParams['figure.figsize'] = (12, 6)
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')"""),

    md_cell("""### 1. Đọc và Thống Kê Metadata 20 Ca Bệnh"""),
    code_cell("""meta_path = "../data/sample/metadata.csv"
df = pd.read_csv(meta_path)
print(f"Tổng số mẫu: {len(df)}")
df.head(10)"""),

    md_cell("""### 2. Phân Tích Thống Kê Diện Tích & Tỷ Lệ Khối U"""),
    code_cell("""fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Biểu đồ phân bố diện tích
axes[0].hist(df['tumor_area_pixels'], bins=8, color='#3B82F6', edgecolor='black', alpha=0.7)
axes[0].set_title("Phân Bố Diện Tích Khối U (Pixels)", fontsize=13, fontweight='bold')
axes[0].set_xlabel("Diện tích (pixels)")
axes[0].set_ylabel("Số lượng ca")

# Biểu đồ tỷ lệ % u trên thiết diện não
axes[1].hist(df['tumor_ratio_percent'], bins=8, color='#10B981', edgecolor='black', alpha=0.7)
axes[1].set_title("Phân Bố Tỷ Lệ % U / Thiết Diện Ảnh", fontsize=13, fontweight='bold')
axes[1].set_xlabel("Tỷ lệ %")
axes[1].set_ylabel("Số lượng ca")

plt.tight_layout()
plt.show()

print("Thống kê mô tả tỷ lệ u (%):")
print(df['tumor_ratio_percent'].describe())"""),

    md_cell("""### 3. Trực Quan Hóa 6 Mẫu Đại Diện (U Nhỏ, U Trung Bình, U Lớn)"""),
    code_cell("""sample_indices = [0, 4, 6, 8, 10, 18] # Đại diện các kích thước u khác nhau

fig, axes = plt.subplots(2, 6, figsize=(18, 6))

for col_idx, idx in enumerate(sample_indices):
    row = df.iloc[idx]
    img_p = os.path.join("../data/sample/images", row['image_file'])
    mask_p = os.path.join("../data/sample/masks", row['mask_file'])
    
    img = cv2.imread(img_p, cv2.IMREAD_GRAYSCALE)
    mask = cv2.imread(mask_p, cv2.IMREAD_GRAYSCALE)
    
    # Hàng 1: Ảnh gốc
    axes[0, col_idx].imshow(img, cmap='gray')
    axes[0, col_idx].set_title(f"{row['sample_id']}\\n{row['tumor_ratio_percent']}%", fontsize=10)
    axes[0, col_idx].axis('off')
    
    # Hàng 2: Mặt nạ Ground Truth
    axes[1, col_idx].imshow(mask, cmap='hot')
    axes[1, col_idx].set_title(f"Area: {row['tumor_area_pixels']}px", fontsize=10)
    axes[1, col_idx].axis('off')

plt.suptitle("Một Số Mẫu Ảnh MRI Não & Mặt Nạ Ground Truth Benchmark (TCGA-LGG)", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()""")
]

# ==========================================
# NOTEBOOK 2: TÁCH SỌ NÃO (SKULL STRIPPING)
# ==========================================
nb2_cells = [
    md_cell("""# Notebook 2: Nghiên Cứu & Cài Đặt Thuật Toán Tách Sọ Não (Skull Stripping)
**Đồ án Xử lý ảnh số (2026–2027) — Khoa CNTT — HUIT**  
**Nhóm sinh viên:** Hà Mạnh Trường (2045240326) & Huỳnh Tâm Trí (2045240315)  
**Phụ trách chính:** Hà Mạnh Trường

---
### Cơ sở lý thuyết DIP:
1. **Khử nhiễu Rician:** Lọc Bilateral (`cv2.bilateralFilter`) bảo toàn biên đối tượng.
2. **Nhị phân hóa:** Ngưỡng tự động Otsu (`cv2.THRESH_OTSU`).
3. **Hình thái học:** Phép mở (`MORPH_OPEN`) với phần tử cấu trúc elip cắt đứt cầu nối mô.
4. **Trích xuất nhu mô:** Tìm thành phần liên thông lớn nhất (Largest Connected Component - LCC).
5. **Lấp đầy lỗ hổng:** Kỹ thuật FloodFill lấp đầy não thất."""),

    code_cell("""import os
import sys
import numpy as np
import cv2
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(".."))
from src.preprocessing.filters import apply_bilateral_filter
from src.preprocessing.skull_strip import extract_brain_mask, strip_skull"""),

    md_cell("""### 1. Phân Tích Chi Tiết Từng Bước Tách Sọ Trên 1 Ca Bệnh"""),
    code_cell("""# Nạp ảnh ca bệnh 01
img_path = "../data/sample/images/mri_brain_tumor_01.png"
img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

# Bước 1: Khử nhiễu Bilateral
denoised = apply_bilateral_filter(img, d=9, sigma_color=75.0, sigma_space=75.0)

# Bước 2: Ngưỡng hóa Otsu
_, otsu_thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Bước 3: Phép mở hình thái học (Morphological Opening)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
opened = cv2.morphologyEx(otsu_thresh, cv2.MORPH_OPEN, kernel, iterations=2)

# Bước 4: Trích xuất thành phần liên thông lớn nhất (LCC)
num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(opened, connectivity=8)
largest_label = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
lcc_mask = np.zeros_like(img)
lcc_mask[labels == largest_label] = 255

# Bước 5: Lấp đầy lỗ hổng (Hole Filling)
filled_mask = extract_brain_mask(denoised, kernel_size=5)

# Bước 6: Ảnh não sạch sọ
stripped, _ = strip_skull(denoised, filled_mask)

# Vẽ biểu đồ 6 bước
steps = [
    ("1. Ảnh MRI Gốc", img, 'gray'),
    ("2. Ngưỡng Hóa Otsu", otsu_thresh, 'gray'),
    ("3. Morphological Opening", opened, 'gray'),
    ("4. LCC Nhu Mô Não", lcc_mask, 'gray'),
    ("5. Brain Mask (Filled)", filled_mask, 'gray'),
    ("6. Não Sau Tách Sọ", stripped, 'gray')
]

fig, axes = plt.subplots(2, 3, figsize=(15, 9))
for i, (title, step_img, cmap) in enumerate(steps):
    r, c = i // 3, i % 3
    axes[r, c].imshow(step_img, cmap=cmap)
    axes[r, c].set_title(title, fontsize=12, fontweight='bold')
    axes[r, c].axis('off')

plt.suptitle("Quy Trình 6 Bước Tách Sọ Não Bằng Kỹ Thuật Xử Lý Ảnh Số", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()"""),

    md_cell("""### 2. Kiểm Thử Tính Bền Vững Trên 4 Ca Khác Nhau"""),
    code_cell("""test_cases = ["mri_brain_tumor_02", "mri_brain_tumor_07", "mri_brain_tumor_11", "mri_brain_tumor_17"]

fig, axes = plt.subplots(4, 3, figsize=(12, 14))

for idx, case_name in enumerate(test_cases):
    p = f"../data/sample/images/{case_name}.png"
    im = cv2.imread(p, cv2.IMREAD_GRAYSCALE)
    mask = extract_brain_mask(im)
    res, _ = strip_skull(im, mask)
    
    axes[idx, 0].imshow(im, cmap='gray')
    axes[idx, 0].set_title(f"Gốc: {case_name}")
    axes[idx, 0].axis('off')
    
    axes[idx, 1].imshow(mask, cmap='hot')
    axes[idx, 1].set_title("Brain Mask")
    axes[idx, 1].axis('off')
    
    axes[idx, 2].imshow(res, cmap='gray')
    axes[idx, 2].set_title("Não Sạch Sọ")
    axes[idx, 2].axis('off')

plt.tight_layout()
plt.show()""")
]

# ==========================================
# NOTEBOOK 3: SO SÁNH 2 PHƯƠNG PHÁP PHÂN ĐOẠN
# ==========================================
nb3_cells = [
    md_cell("""# Notebook 3: Thử Nghiệm So Sánh 2 Phương Pháp Phân Đoạn U Não
**Đồ án Xử lý ảnh số (2026–2027) — Khoa CNTT — HUIT**  
**Nhóm sinh viên:** Hà Mạnh Trường (2045240326) & Huỳnh Tâm Trí (2045240315)  
**Phụ trách chính:** Cả hai thành viên

---
### Tiêu chí Bộ môn (Chiếm 15% + 50% điểm đồ án):
Bắt buộc so sánh tối thiểu **02 phương án hoặc cấu hình xử lý**:
* **Phương án A (Baseline chính):** **Marker-controlled Watershed** (Biến đổi khoảng cách Euclidean $\rightarrow$ Hạt giống $\rightarrow$ Phân thủy).
* **Phương án B (Đối chứng):** **Seeded Region Growing** (Tự tìm hạt giống cực đại cường độ $\rightarrow$ Lan truyền 8 láng giềng)."""),

    code_cell("""import os
import sys
import numpy as np
import cv2
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(".."))
from src.preprocessing.skull_strip import strip_skull
from src.segmentation.watershed import segment_watershed
from src.segmentation.region_growing import segment_region_growing
from src.measurement.features import extract_tumor_features
from src.measurement.visualization import draw_tumor_overlay
from src.evaluation.metrics import calculate_dice, calculate_iou"""),

    md_cell("""### 1. So Sánh Trực Quan Trên 3 Ca Điển Hình (U Nhỏ, U Trung Bình, U Lớn)"""),
    code_cell("""cases = [
    ("mri_brain_tumor_11", "Ca U Nhỏ (1.12%)"),
    ("mri_brain_tumor_02", "Ca U Trung Bình (4.04%)"),
    ("mri_brain_tumor_07", "Ca U Lớn (9.44%)")
]

fig, axes = plt.subplots(3, 5, figsize=(18, 11))

for row_idx, (case_id, desc) in enumerate(cases):
    img_p = f"../data/sample/images/{case_id}.png"
    mask_p = f"../data/sample/masks/{case_id}_mask.png"
    
    orig = cv2.imread(img_p, cv2.IMREAD_GRAYSCALE)
    gt = cv2.imread(mask_p, cv2.IMREAD_GRAYSCALE)
    stripped, b_mask = strip_skull(orig)
    
    # 1. Chạy Watershed
    mask_ws = segment_watershed(stripped, dist_thresh_ratio=0.4)
    dice_ws = calculate_dice(mask_ws, gt)
    
    # 2. Chạy Region Growing
    mask_rg = segment_region_growing(stripped, tolerance=15)
    dice_rg = calculate_dice(mask_rg, gt)
    
    # 3. Vẽ Bounding Box cảnh báo
    res_ws = extract_tumor_features(mask_ws, b_mask)
    annotated = draw_tumor_overlay(orig, mask_ws, res_ws)
    
    # Cột 1: Ảnh gốc
    axes[row_idx, 0].imshow(orig, cmap='gray')
    axes[row_idx, 0].set_title(f"{desc}\\nẢnh Gốc", fontsize=10)
    axes[row_idx, 0].axis('off')
    
    # Cột 2: Ground Truth
    axes[row_idx, 1].imshow(gt, cmap='gray')
    axes[row_idx, 1].set_title("Ground Truth Bác Sĩ", fontsize=10)
    axes[row_idx, 1].axis('off')
    
    # Cột 3: Watershed
    axes[row_idx, 2].imshow(mask_ws, cmap='Blues')
    axes[row_idx, 2].set_title(f"Watershed\\nDice = {dice_ws:.4f}", fontsize=10, color='blue', fontweight='bold')
    axes[row_idx, 2].axis('off')
    
    # Cột 4: Region Growing
    axes[row_idx, 3].imshow(mask_rg, cmap='Greens')
    axes[row_idx, 3].set_title(f"Region Growing\\nDice = {dice_rg:.4f}", fontsize=10, color='green', fontweight='bold')
    axes[row_idx, 3].axis('off')
    
    # Cột 5: Bounding Box
    axes[row_idx, 4].imshow(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB))
    axes[row_idx, 4].set_title(f"Khoanh Vùng Đỏ\\nArea: {res_ws.tumor_area_px}px", fontsize=10)
    axes[row_idx, 4].axis('off')

plt.suptitle("So Sánh Hiệu Quả Phân Đoạn: Watershed (Baseline) vs. Region Growing (Đối Chứng)", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()""")
]

# ==========================================
# NOTEBOOK 4: ĐÁNH GIÁ ĐỊNH LƯỢNG Y KHOA
# ==========================================
nb4_cells = [
    md_cell("""# Notebook 4: Đánh Giá Định Lượng Toàn Diện 20 Ca Bệnh (Benchmark Evaluation)
**Đồ án Xử lý ảnh số (2026–2027) — Khoa CNTT — HUIT**  
**Nhóm sinh viên:** Hà Mạnh Trường (2045240326) & Huỳnh Tâm Trí (2045240315)  
**Phụ trách chính:** Huỳnh Tâm Trí

---
### Tiêu chí định lượng y khoa:
1. **Dice Similarity Coefficient (DSC / F1):** Độ trùng lặp diện tích u.
2. **Jaccard Index (IoU):** Tỷ lệ giao trên hợp.
3. **Sensitivity (Độ nhạy):** Khả năng không bỏ sót pixel u não.
4. **Specificity (Độ đặc hiệu):** Khả năng không nhận nhầm mô lành thành u.
5. **Độ trễ trung bình (Latency ms/ảnh).**"""),

    code_cell("""import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(".."))
from src.preprocessing.skull_strip import strip_skull
from src.segmentation.watershed import segment_watershed
from src.segmentation.region_growing import segment_region_growing
from src.evaluation.benchmark import run_benchmark"""),

    md_cell("""### 1. Thực Thi Benchmark Trên Toàn Bộ 20 Mẫu Ảnh"""),
    code_cell("""img_dir = "../data/sample/images"
mask_dir = "../data/sample/masks"

# Hàm wrapper cho Watershed
def predict_watershed(img):
    stripped, _ = strip_skull(img)
    return segment_watershed(stripped)

# Hàm wrapper cho Region Growing
def predict_region_growing(img):
    stripped, _ = strip_skull(img)
    return segment_region_growing(stripped)

print("Đang chạy benchmark Watershed...")
df_ws = run_benchmark(img_dir, mask_dir, predict_watershed, method_name="Watershed")

print("Đang chạy benchmark Region Growing...")
df_rg = run_benchmark(img_dir, mask_dir, predict_region_growing, method_name="Region Growing")"""),

    md_cell("""### 2. Bảng Tổng Hợp So Sánh Thống Kê (Mean ± Std)"""),
    code_cell("""summary = pd.DataFrame({
    "Chỉ Số Đánh Giá": ["Dice Score (DSC)", "IoU (Jaccard)", "Sensitivity (Độ nhạy)", "Specificity (Đặc hiệu)", "Thời gian xử lý (ms)"],
    "Watershed (Baseline)": [
        f"{df_ws['dice'].mean():.4f} ± {df_ws['dice'].std():.4f}",
        f"{df_ws['iou'].mean():.4f} ± {df_ws['iou'].std():.4f}",
        f"{df_ws['sensitivity'].mean():.4f} ± {df_ws['sensitivity'].std():.4f}",
        f"{df_ws['specificity'].mean():.4f} ± {df_ws['specificity'].std():.4f}",
        f"{df_ws['latency_ms'].mean():.2f} ± {df_ws['latency_ms'].std():.2f} ms"
    ],
    "Region Growing (Đối chứng)": [
        f"{df_rg['dice'].mean():.4f} ± {df_rg['dice'].std():.4f}",
        f"{df_rg['iou'].mean():.4f} ± {df_rg['iou'].std():.4f}",
        f"{df_rg['sensitivity'].mean():.4f} ± {df_rg['sensitivity'].std():.4f}",
        f"{df_rg['specificity'].mean():.4f} ± {df_rg['specificity'].std():.4f}",
        f"{df_rg['latency_ms'].mean():.2f} ± {df_rg['latency_ms'].std():.2f} ms"
    ]
})

summary"""),

    md_cell("""### 3. Biểu Đồ Cột So Sánh Điểm Dice Trên Từng Ca Bệnh"""),
    code_cell("""x = np.arange(len(df_ws))
width = 0.38

fig, ax = plt.subplots(figsize=(16, 6))
rects1 = ax.bar(x - width/2, df_ws['dice'], width, label='Watershed (Baseline)', color='#3B82F6', alpha=0.85)
rects2 = ax.bar(x + width/2, df_rg['dice'], width, label='Region Growing (Đối chứng)', color='#10B981', alpha=0.85)

ax.set_ylabel('Điểm Dice Similarity Coefficient', fontsize=12)
ax.set_title('So Sánh Điểm Dice Score Giữa 2 Phương Pháp Trên 20 Ca Bệnh TCGA-LGG', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels([f"Ca {i+1:02d}" for i in range(len(df_ws))], rotation=45)
ax.legend(fontsize=12)
ax.set_ylim(0, 1.05)
ax.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()""")
]

# Ghi ra 4 files
with open("notebooks/01_data_exploration.ipynb", "w", encoding="utf-8") as f:
    json.dump(make_notebook(nb1_cells), f, indent=1, ensure_ascii=False)
print("Da tao notebooks/01_data_exploration.ipynb")

with open("notebooks/02_skull_stripping.ipynb", "w", encoding="utf-8") as f:
    json.dump(make_notebook(nb2_cells), f, indent=1, ensure_ascii=False)
print("Da tao notebooks/02_skull_stripping.ipynb")

with open("notebooks/03_tumor_segmentation_comparison.ipynb", "w", encoding="utf-8") as f:
    json.dump(make_notebook(nb3_cells), f, indent=1, ensure_ascii=False)
print("Da tao notebooks/03_tumor_segmentation_comparison.ipynb")

with open("notebooks/04_quantitative_evaluation.ipynb", "w", encoding="utf-8") as f:
    json.dump(make_notebook(nb4_cells), f, indent=1, ensure_ascii=False)
print("Da tao notebooks/04_quantitative_evaluation.ipynb")

print("\nHOAN TAT TAO 4 JUPYTER NOTEBOOKS!")
