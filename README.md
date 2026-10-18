# Phân Đoạn & Phát Hiện Khối U Não Trên Ảnh Cộng Hưởng Từ (MRI)
### Brain Tumor Segmentation and Detection in Magnetic Resonance Imaging (MRI)

> **Đồ án kết thúc học phần:** Xử lý ảnh số (Digital Image Processing)  
> **Đơn vị:** Bộ môn Khoa học Dữ liệu — Khoa Công nghệ Thông tin — Trường Đại học Công Thương TP. Hồ Chí Minh (HUIT)  
> **Năm học:** 2026–2027  
> **Repository:** [brain-tumor-mri-segmentation](https://github.com/mtzwyu/brain-tumor-mri-segmentation)

---

## 👥 Nhóm sinh viên thực hiện

| STT | Họ và Tên | Mã số sinh viên (MSSV) | Vai trò / Phân công chính |
| :---: | :--- | :---: | :--- |
| 1 | **Hà Mạnh Trường** | **2045240326** | **Trưởng nhóm**, Pipeline tiền xử lý & Tách sọ não (Skull Stripping), Thuật toán phân đoạn u não lõi (Watershed/Region Growing), Báo cáo khoa học |
| 2 | **Huỳnh Tâm Trí** | **2045240315** | **Thành viên**, Thu thập & chuẩn hóa dữ liệu MRI Ground Truth, Rút trích đặc trưng hình học khối u, Đánh giá định lượng (Dice/IoU), Demo GUI |

---

## 🎯 1. Mục tiêu và Ý nghĩa Đề tài

* **Bối cảnh y tế:** Khối u não (Brain Tumor: u tế bào đệm - Glioma, u màng não - Meningioma, u tuyến yên - Pituitary) là một trong những bệnh lý thần kinh nguy hiểm nhất. Ảnh cộng hưởng từ (MRI) là tiêu chuẩn vàng trong chẩn đoán, nhưng việc khoanh vùng thủ công tốn nhiều thời gian và phụ thuộc chủ quan vào kinh nghiệm bác sĩ.
* **Mục tiêu đầu vào:** Ảnh chụp MRI sọ não 2D lát cắt (Axial/Coronal/Sagittal) ở chuỗi xung T1-CE hoặc FLAIR (định dạng JPG, PNG).
* **Mục tiêu đầu ra:**
  1. Mặt nạ phân đoạn khối u não (Binary Segmentation Mask).
  2. Hộp giới hạn (Bounding Box) và đường bao (Contour) định vị ổ u não.
  3. Báo cáo định lượng y tế: Diện tích khối u ($S_{\text{tumor}}$), tọa độ tâm u (Centroid), độ gồ ghề bờ u (Circularity), và tỷ lệ % u/nhu mô não.
  4. Đánh giá so sánh với Ground Truth chuyên gia qua: **Dice Score, IoU, Sensitivity, Specificity**.
* **Nguyên tắc kỹ thuật cốt lõi:** Lấy kỹ thuật **Xử lý ảnh số cổ điển (Digital Image Processing - DIP)** làm trọng tâm thực nghiệm, xây dựng bước tách hộp sọ (**Skull Stripping**) bằng hình thái học và so sánh tối thiểu 2 phương án phân đoạn theo đúng đề cương Bộ môn.

---

## 🔬 2. Sơ đồ Pipeline Xử lý 7 Bước

```
[Ảnh MRI Sọ Não Gốc (T1-CE / FLAIR)]
                │
                ▼
1. 【Tiền xử lý & Cải thiện chất lượng ảnh】
   ├── Chuẩn hóa kích thước (512x512) & dải pixel [0, 255]
   ├── Khử nhiễu Rician: Lọc trung vị (Median Filter) & Lọc Bilateral bảo toàn biên u
   └── Tăng cường tương phản mô mềm não: CLAHE (kênh xám)
                │
                ▼
2. 【Tách sọ não (Skull Stripping - Kỹ thuật DIP kinh điển)】
   ├── Phân ngưỡng nhị phân loại bỏ nền ngoài sọ
   ├── Phép toán hình thái học (Morphological Opening/Closing) cắt cầu nối mô
   ├── Tìm thành phần liên thông lớn nhất (Largest Connected Component)
   └── Sinh mặt nạ nhu mô não (Brain Mask) loại bỏ hoàn toàn xương sọ và da đầu
                │
                ▼
3. 【Phân đoạn khối u lõi (Core Tumor Segmentation) — So sánh 2 phương án】
   ├── Phương án A (Baseline DIP cổ điển):
   │     Distance Transform ➔ Điểm hạt giống (Markers) ➔ Phân thủy Watershed
   │     HOẶC Phát triển vùng (Region Growing) từ điểm cực đại cường độ
   └── Phương án B (Cải tiến / Đối chứng):
         Phân cụm K-Means pixel trên không gian cường độ/kết cấu GLCM HOẶC Mạng U-Net
                │
                ▼
4. 【Định vị & Đo lường đặc trưng khối u】
   ├── Trích xuất Contour và Bounding Box màu đỏ cảnh báo quanh khối u
   ├── Tính toán diện tích khối u (S_tumor) và tỷ lệ % u / diện tích não
   └── Tính độ tròn (Circularity = 4π * Area / Perimeter^2) đánh giá độ gồ ghề bờ u
                │
                ▼
5. 【Đánh giá định lượng & Trực quan hóa】
   ├── So sánh mặt nạ dự đoán với Ground Truth: Dice (F1), IoU, Sensitivity, Specificity
   ├── Phân tích các ca u nhỏ, u bờ mờ (Failure Cases)
   └── Đo thời gian xử lý trung bình mỗi ca chụp (ms)
                │
                ▼
6. 【Chương trình ứng dụng Demo (GUI)】
   └── Giao diện web Streamlit cho phép bác sĩ nạp ảnh MRI, chọn phương pháp, xem ảnh tách sọ, mặt nạ u và tải báo cáo kết quả
```

---

## 📂 3. Cấu trúc Thư mục Dự án

```
brain-tumor-mri-segmentation/
├── .agents/                        # Bộ kỹ năng AI Agent hỗ trợ phát triển (Matt Pocock Skills)
├── docs/                           # Tài liệu đề cương, báo cáo đồ án và kết quả thực nghiệm
│   ├── BAO_CAO_DO_AN_XLAS.md       # Báo cáo toàn văn đồ án định dạng Markdown
│   ├── BAO_CAO_DO_AN_XLAS.docx     # Báo cáo chuẩn thể thức Bộ Giáo dục (Times New Roman 13pt, lề 3-3-3-2 cm)
│   ├── BENCHMARK_RESULTS.csv       # Tổng hợp định lượng 3,929 lát cắt theo lát bệnh lý & não lành
│   ├── BENCHMARK_RESULTS_FULL.csv  # Chi tiết 7,858 kết quả thực nghiệm từng lát cắt
│   ├── DATA_EXPLORATION_REPORT.md  # Báo cáo thống kê dữ liệu 110 bệnh nhân TCGA-LGG
│   └── KHUNG_NOI_DUNG_TONG_QUAT... # Khung nội dung chuẩn hóa của Bộ môn
├── data/                           # Dữ liệu ảnh MRI sọ não
│   ├── README.md                   # Mô tả cấu trúc hai tầng và quy cách mặt nạ u
│   ├── sample/                     # [Tầng 1 - In Git] 20 ca mẫu kiểm thử nhanh
│   │   ├── images/                 # Ảnh MRI sọ não gốc (.png, 256x256)
│   │   ├── masks/                  # Mặt nạ Ground Truth u não (.png, 256x256)
│   │   └── metadata.csv            # Metadata diện tích u của 20 mẫu
│   └── full/                       # [Tầng 2 - Gitignored] Toàn bộ 3,929 lát cắt chuẩn TCGA-LGG
│       ├── images/                 # 3,929 ảnh MRI (.png, 256x256)
│       ├── masks/                  # 3,929 mặt nạ Ground Truth (.png, 256x256)
│       └── metadata.csv            # Metadata chi tiết 110 bệnh nhân (3,929 lát)
├── src/                            # Mã nguồn module xử lý ảnh số lõi
│   ├── preprocessing/              # Lọc nhiễu Rician, CLAHE, Tách sọ (Skull Stripping)
│   ├── segmentation/               # Watershed & Marker Distance Transform, Region Growing
│   ├── measurement/                # Đo diện tích u, độ tròn Circularity, Bounding Box
│   └── evaluation/                 # Tính Dice, IoU, Sensitivity, Specificity
├── demo/                           # Ứng dụng giao diện minh họa (Streamlit GUI tương tác)
│   ├── app.py                      # Giao diện chính hỗ trợ chuyển đổi data/full và data/sample
│   └── utils.py                    # Tiện ích hiển thị và xuất báo cáo PDF/Excel
├── notebooks/                      # 4 Jupyter Notebooks thực nghiệm trực quan
│   ├── 01_data_exploration.ipynb   # Khám phá và phân tích phân bố dữ liệu
│   ├── 02_preprocessing_and_skull_stripping.ipynb # Khử nhiễu & tách sọ não
│   ├── 03_segmentation_comparison.ipynb # So sánh thuật toán phân đoạn
│   └── 04_quantitative_evaluation.ipynb # Đánh giá định lượng trên toàn bộ tập dữ liệu
├── scripts/                        # Scripts tự động hóa
│   ├── download_full_dataset.py    # Tải toàn bộ 3,929 lát cắt từ Hugging Face
│   ├── run_all_experiments.py      # Benchmark đa tiến trình xử lý 3,929 lát cắt (~25s)
│   ├── export_report_docx.py       # Xuất báo cáo Word đúng chuẩn lề 3-3-3-2 cm
│   └── create_notebooks.py         # Khởi tạo tự động các notebook thực nghiệm
├── tests/                          # Bộ kiểm thử đơn vị tự động (Pytest)
├── AGENTS.md                       # Thông tin nhóm & Quy chuẩn kỹ thuật toàn cục
├── requirements.txt                # Thư viện phụ thuộc (OpenCV, NumPy, Streamlit, python-docx...)
└── README.md                       # Tài liệu tổng quan dự án
```

---

## 📊 4. Kết Quả Thực Nghiệm Benchmark Quy Mô Toàn Bộ Dữ Liệu (3,929 Lát Cắt)

Toàn bộ 3,929 lát cắt từ 110 bệnh nhân TCGA-LGG được phân tích và đánh giá định lượng độc lập giữa hai giải thuật DIP cổ điển:

| Nhóm dữ liệu kiểm thử | Phương pháp | Dice Score ($F_1$) | IoU (Jaccard) | Sensitivity | Specificity | Độ trễ (ms/ảnh) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Lát cắt có u (1,373 lát)** | **Marker-controlled Watershed** | **0.4446 ± 0.3014** | **0.3368 ± 0.2677** | **0.4436 ± 0.3170** | **0.9915 ± 0.0107** | **6.13 ± 3.32 ms** |
| | Region Growing | 0.1990 ± 0.2682 | 0.1416 ± 0.2119 | 0.2226 ± 0.3221 | 0.9851 ± 0.0432 | 12.13 ± 22.83 ms |
| **Lát não lành (2,556 lát)** | **Marker-controlled Watershed** | N/A (Không u) | N/A | N/A | **0.9904 ± 0.0100** | **6.15 ± 3.40 ms** |
| | Region Growing | N/A (Không u) | N/A | N/A | 0.9760 ± 0.0480 | 12.05 ± 21.50 ms |

> 📌 **Nhận xét chuyên môn:**
> 1. **Watershed vượt trội toàn diện:** Nhờ cơ chế gieo mầm hạt giống dựa trên biến đổi khoảng cách Euclid (Euclidean Distance Transform) trên mặt nạ tách sọ, Watershed đạt Dice 0.4446 (gấp 2.23 lần Region Growing) và thời gian thực thi ổn định chỉ ~6.13 ms/lát cắt.
> 2. **Kiểm soát dương tính giả tuyệt hảo:** Độ đặc hiệu (Specificity) trên lát não lành đạt **99.04%** (Watershed) và **97.60%** (Region Growing), khẳng định bước tách sọ não (Skull Stripping) loại bỏ triệt để tín hiệu nhiễu từ hộp sọ và màng não.

---

## 🚀 5. Hướng Dẫn Cài Đặt & Chạy Hệ Thống (Quickstart)

### Bước 1: Cài đặt môi trường
```bash
git clone https://github.com/mtzwyu/brain-tumor-mri-segmentation.git
cd brain-tumor-mri-segmentation
pip install -r requirements.txt
```

### Bước 2: Tải dữ liệu toàn bộ (3,929 lát cắt)
```bash
# Tải và giải nén tự động 3,929 lát cắt từ Hugging Face (~1-2 phút tùy mạng)
python scripts/download_full_dataset.py
```

### Bước 3: Chạy Benchmark đa tiến trình toàn bộ 3,929 lát cắt
```bash
# Chạy đánh giá đa luồng tốc độ cao (~25 giây hoàn thành toàn bộ 3,929 ảnh)
python scripts/run_all_experiments.py
```

### Bước 4: Khởi chạy Giao diện Tương tác Web (Streamlit Demo)
```bash
streamlit run demo/app.py
```

### Bước 5: Chạy Kiểm thử Đơn vị Tự động (Unit Tests)
```bash
pytest -v
```

---

## 📋 6. Kế hoạch Nộp Sản phẩm theo chuẩn Khoa CNTT

* **Báo cáo đồ án:** Soạn thảo theo chuẩn 10 mục của Khoa CNTT (Word và PDF).
* **Mã nguồn:** Toàn bộ pipeline xử lý ảnh số sạch, có chú thích chi tiết, kèm demo tương tác.
* **Tập dữ liệu:** Bộ dữ liệu kiểm thử kèm ground truth mask khối u não.
* **Slide thuyết trình:** Tóm tắt bối cảnh, phương pháp, kết quả định lượng và kết luận.

