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
├── docs/                           # Tài liệu đề cương, danh mục đề tài và hướng dẫn học phần
│   ├── 7. DANH_SACH_DE_TAI...pdf   # Danh mục đề tài gợi ý của Bộ môn
│   ├── 9. Ke_hoach_thuc_ĐA...pdf   # Kế hoạch thực hiện 15 tuần của Bộ môn
│   ├── KHUNG_NOI_DUNG_TONG_QUAT... # Khung nội dung chuẩn hóa cho mọi đề tài (PDF + MD)
│   └── agents/                     # Cấu hình issue tracker, triage labels, domain docs
├── data/                           # Dữ liệu ảnh MRI sọ não
│   ├── README.md                   # Mô tả cấu trúc, quy cách và các link tải nguồn
│   ├── sample/                     # Tập ảnh mẫu phục vụ thử nghiệm nhanh (20 ca chuẩn)
│   │   ├── images/                 # Ảnh MRI sọ não gốc (.png, 256x256)
│   │   ├── masks/                  # Mặt nạ nhị phân khối u Ground Truth (.png, 256x256)
│   │   └── metadata.csv            # Bảng thông tin ca bệnh và diện tích u
│   ├── raw/                        # (Đã gitignore) Nơi lưu toàn bộ dữ liệu tải về
│   └── processed/                  # (Đã gitignore) Nơi lưu ảnh sau khi tách sọ/tiền xử lý
│
│   * 🔗 Nguồn chính (Hugging Face Datasets): https://huggingface.co/datasets/Ehsan-rmz/lgg-mri-segmentation-research
│   * 🔗 Nguồn dự phòng (Kaggle Benchmark): https://www.kaggle.com/datasets/mateuszbuda/lgg-mri-segmentation
│   * 🔗 Kho gốc y sinh (TCIA NIH/NCI): https://wiki.cancerimagingarchive.net/display/Public/TCGA-LGG
├── src/                            # Mã nguồn hệ thống (sẽ xây dựng theo các tuần)
│   ├── preprocessing/              # Lọc nhiễu, CLAHE, Tách sọ (Skull Stripping)
│   ├── segmentation/               # Watershed, Region Growing, K-Means
│   ├── measurement/                # Đo diện tích u, độ tròn, Bounding Box
│   └── evaluation/                 # Tính Dice, IoU, Sensitivity, Specificity
├── demo/                           # Ứng dụng giao diện minh họa (Streamlit GUI)
├── scripts/                        # Scripts tải dữ liệu và biên dịch tài liệu PDF
├── AGENTS.md                       # Thông tin nhóm & Quy chuẩn kỹ thuật toàn cục
├── requirements.txt                # Thư viện phụ thuộc (OpenCV, NumPy, Streamlit, Typst...)
└── README.md                       # Tài liệu tổng quan dự án
```

---

## 📋 4. Kế hoạch Nộp Sản phẩm theo chuẩn Khoa CNTT

* **Báo cáo đồ án:** Soạn thảo theo chuẩn 10 mục của Khoa CNTT (Word và PDF).
* **Mã nguồn:** Toàn bộ pipeline xử lý ảnh số sạch, có chú thích chi tiết, kèm demo tương tác.
* **Tập dữ liệu:** Bộ dữ liệu kiểm thử kèm ground truth mask khối u não.
* **Slide thuyết trình:** Tóm tắt bối cảnh, phương pháp, kết quả định lượng và kết luận.
