# Hệ Thống Tổng Quát Phân Đoạn & Phát Hiện Tổn Thương Trên Ảnh Y Tế
### Generalized Multi-Modal Medical Image Lesion Segmentation and Detection System

> **Đồ án kết thúc học phần:** Xử lý ảnh số (Digital Image Processing)  
> **Đơn vị:** Bộ môn Khoa học Dữ liệu — Khoa Công nghệ Thông tin — Trường Đại học Công Thương TP. Hồ Chí Minh (HUIT)  
> **Năm học:** 2026–2027  
> **Repository:** [medical-image-lesion-segmentation](https://github.com/mtzwyu/medical-image-lesion-segmentation)

---

## 👥 Nhóm sinh viên thực hiện

| STT | Họ và Tên | Mã số sinh viên (MSSV) | Vai trò / Phân công chính |
| :---: | :--- | :---: | :--- |
| 1 | **Hà Mạnh Trường** | **2045240326** | **Trưởng nhóm**, Kiến trúc pipeline tổng quát DIP, Thuật toán phân đoạn lõi đa phương thức (Otsu/Watershed/Region Growing), Báo cáo khoa học |
| 2 | **Huỳnh Tâm Trí** | **2045240315** | **Thành viên**, Tổ chức dữ liệu đa phương thức & Ground Truth, Rút trích đặc trưng hình học/kết cấu, Đánh giá định lượng (Dice/IoU), Xây dựng ứng dụng Demo GUI |

---

## 🎯 1. Tầm nhìn & Phạm vi Tổng quát của Đồ án

Đồ án xây dựng một **Khung hệ thống xử lý ảnh số tổng quát (Generalized Medical DIP Framework)** có khả năng thích ứng linh hoạt để phân đoạn, phát hiện và đo lường kích thước các ổ tổn thương trên **nhiều phương thức ảnh y tế phổ biến (Multi-Modal Medical Imaging)**:

```
                                  ┌─────────────────────────────┐
                                  │      ẢNH Y TẾ ĐẦU VÀO       │
                                  └──────────────┬──────────────┘
                                                 │
                  ┌──────────────────────────────┼──────────────────────────────┐
                  ▼                              ▼                              ▼
          【Ảnh Soi Da】                 【Ảnh X-Quang Phổi】             【Ảnh Não MRI】
         (Dermoscopy - ISIC)             (Chest X-ray - CXR)            (Brain Tumor MRI)
                  │                              │                              │
                  └──────────────────────────────┼──────────────────────────────┘
                                                 │
                                                 ▼
                  ┌─────────────────────────────────────────────────────────────┐
                  │          BỘ TIỀN XỬ LÝ THÍCH ỨNG (ADAPTIVE DIP)             │
                  │   - Cân bằng tương phản thích nghi giới hạn (CLAHE)         │
                  │   - Lọc nhiễu bảo toàn ranh giới (Bilateral / Median)        │
                  │   - Chuẩn hóa không gian màu & mức xám (Lab / Grayscale)    │
                  └──────────────────────────────┬──────────────────────────────┘
                                                 │
                                                 ▼
                  ┌─────────────────────────────────────────────────────────────┐
                  │           ĐỘNG CƠ PHÂN ĐOẠN LÕI (CORE SEGMENTATION)         │
                  │   - Multi-Otsu & Adaptive Thresholding                      │
                  │   - Xử lý hình thái học (Opening / Closing / Gradient)      │
                  │   - Distance Transform + Phân thủy Watershed                │
                  │   - Phân vùng phát triển vùng (Region Growing)              │
                  └──────────────────────────────┬──────────────────────────────┘
                                                 │
                                                 ▼
                  ┌─────────────────────────────────────────────────────────────┐
                  │           PHÁT HIỆN, ĐO LƯỜNG & ĐỊNH LƯỢNG Y TẾ             │
                  │   - Trích xuất Contour, Bounding Box & Convex Hull           │
                  │   - Tính diện tích tổn thương (S) & tỷ lệ % vùng bệnh       │
                  │   - Đánh giá định lượng: Dice Score, IoU, Sensitivity       │
                  └──────────────────────────────┬──────────────────────────────┘
                                                 │
                                                 ▼
                  ┌─────────────────────────────────────────────────────────────┐
                  │             ỨNG DỤNG MINH HỌA ĐA PHƯƠNG THỨC                │
                  │   Cho phép chuyển đổi linh hoạt: Da liễu ↔ X-quang ↔ MRI    │
                  └─────────────────────────────────────────────────────────────┘
```

---

## 🔬 2. Ba Phương thức Ảnh Y tế Trọng tâm Được Hỗ trợ

| Phương thức ảnh y tế | Dạng tổn thương đích | Thách thức xử lý ảnh số | Giải pháp kỹ thuật DIP tương ứng |
| :--- | :--- | :--- | :--- |
| **1. Ảnh Da liễu (Dermoscopy)** *(Dataset ISIC / PH2)* | Tổn thương u hắc tố (Melanoma), nốt ruồi bất thường, ung thư biểu mô | Lông da, bọt khí, viền tối quang học, độ tương phản vùng biên yếu | Phép biến đổi Black-hat + Inpainting tẩy lông; CLAHE kênh $L^*$ trong không gian Lab; Multi-Otsu; Watershed |
| **2. Ảnh X-quang Phổi (Chest X-ray)** *(Dataset Montgomery / COVID-QU-Ex)* | Vùng thâm nhiễm, đông đặc phổi, đốm mờ viêm phổi, tổn thương do virus | Tổn thương nằm chồng đè lên xương sườn/xương đòn; dải tương phản hẹp | CLAHE tăng cường chi tiết mô mềm; Lọc Bilateral khử nhiễu lượng tử; Phân vùng lồng ngực bằng Adaptive threshold + Morphology |
| **3. Ảnh Não MRI (Brain MRI)** *(Dataset Figshare / BraTS)* | Khối u não (Brain Tumor: Glioma, Meningioma, Pituitary) | Độ sáng mô não không đồng nhất; ranh giới mô mềm u não phức tạp | Chuẩn hóa mức xám; Cắt tách hộp sọ (Skull stripping) bằng Threshold + Convex Hull; Phân cụm K-Means pixel / Region Growing |

---

## 📐 3. Quy trình Thực nghiệm Chuẩn mực (Khớp Đề cương HUIT)

Hệ thống được thiết kế theo đúng quy định của Bộ môn Khoa học Dữ liệu (HUIT):
* **Baseline cổ điển (Thuần DIP):** Tiền xử lý (CLAHE + Bilateral) $\rightarrow$ Phân ngưỡng (Otsu / Adaptive) $\rightarrow$ Xử lý hình thái học (Opening / Closing) $\rightarrow$ Watershed tách vùng dính.
* **Phương án cải tiến / So sánh đối chứng:** Phân cụm K-Means trên không gian màu kết hợp đặc trưng kết cấu GLCM Haralick / LBP hoặc mô hình mạng nơ-ron phân đoạn nhẹ (U-Net).
* **Đánh giá so sánh định lượng:**
  * Chỉ số tương đồng Dice: $\text{Dice} = \frac{2 |P \cap G|}{|P| + |G|}$
  * Chỉ số Jaccard (IoU): $\text{IoU} = \frac{|P \cap G|}{|P \cup G|}$
  * Độ nhạy (Sensitivity): $\text{Sensitivity} = \frac{\text{TP}}{\text{TP} + \text{FN}}$
  * Độ đặc hiệu (Specificity): $\text{Specificity} = \frac{\text{TN}}{\text{TN} + \text{FP}}$
  * Đo thời gian xử lý trung bình trên từng khung hình/ảnh (Latency ms).

---

## 📂 4. Cấu trúc Thư mục Dự án

```
medical-image-lesion-segmentation/
├── .agents/                        # Cấu hình kỹ năng AI Agent hỗ trợ đồ án
├── docs/                           # Đề cương môn học, kế hoạch 15 tuần & khung nội dung chuẩn
│   ├── 7. DANH_SACH_DE_TAI...pdf   # Danh mục đề tài gợi ý
│   ├── 9. Ke_hoach_thuc_ĐA...pdf   # Kế hoạch thực hiện đồ án 15 tuần
│   ├── KHUNG_NOI_DUNG_TONG_QUAT... # Khung nội dung chuẩn hóa mọi đề tài (PDF + MD)
│   └── agents/                     # Cấu hình issue tracker, triage labels, domain docs
├── data/                           # Quản lý dữ liệu đa phương thức
│   ├── README.md                   # Mô tả cấu trúc và quy cách dữ liệu
│   ├── sample/                     # Tập ảnh mẫu đa phương thức phục vụ thử nghiệm nhanh
│   │   ├── skin/                   # Mẫu ảnh tổn thương da liễu (ISIC)
│   │   │   ├── images/
│   │   │   ├── masks/
│   │   │   └── metadata.csv
│   │   ├── xray/                   # Mẫu ảnh tổn thương X-quang phổi (Montgomery / CXR)
│   │   │   ├── images/
│   │   │   └── masks/
│   │   └── mri/                    # Mẫu ảnh khối u não MRI (Figshare)
│   │       ├── images/
│   │       └── masks/
│   ├── raw/                        # (Đã gitignore) Nơi lưu dữ liệu lớn khi mở rộng
│   └── processed/                  # (Đã gitignore) Nơi lưu ảnh sau tiền xử lý
├── src/                            # Mã nguồn kiến trúc hệ thống (sẽ xây dựng theo các tuần)
│   ├── preprocessing/              # Các kỹ thuật tiền xử lý thích ứng (CLAHE, Bilateral, Hair removal)
│   ├── segmentation/               # Các thuật toán phân đoạn (Otsu, Watershed, Region Growing)
│   ├── measurement/                # Đo diện tích, chu vi, tỷ lệ % và vẽ Bounding Box
│   └── evaluation/                 # Tính Dice, IoU, Sensitivity, Specificity
├── demo/                           # Giao diện tương tác đa phương thức (Streamlit GUI)
├── scripts/                        # Scripts tải dữ liệu và biên dịch tài liệu PDF
├── AGENTS.md                       # Thông tin nhóm & Quy chuẩn kỹ thuật toàn cục
├── requirements.txt                # Thư viện phụ thuộc (OpenCV, NumPy, Streamlit, Typst...)
└── README.md                       # Tài liệu tổng quan dự án
```

---

## 📋 5. Kế hoạch Nộp Sản phẩm

* **Báo cáo đồ án:** Soạn thảo theo chuẩn 10 mục của Khoa CNTT (Word và PDF).
* **Mã nguồn:** Toàn bộ pipeline xử lý ảnh số sạch, có chú thích chi tiết, kèm demo tương tác.
* **Tập dữ liệu:** Bộ dữ liệu kiểm thử kèm ground truth mask cho từng phương thức.
* **Slide thuyết trình:** Tóm tắt bối cảnh, phương pháp, kết quả định lượng và kết luận.
