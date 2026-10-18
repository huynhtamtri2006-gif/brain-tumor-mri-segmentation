# BẢN PHÂN CÔNG NHIỆM VỤ ĐỘC LẬP — TUẦN 1
## Thành viên phụ trách: HÀ MẠNH TRƯỜNG (MSSV: 2045240326)
* **Vai trò trong đồ án:** Nhóm trưởng — Kiến trúc sư Pipeline & Phụ trách Thuật toán Xử lý ảnh số (DIP Core)
* **Học phần:** Xử lý ảnh số (2026–2027) — Khoa CNTT — Trường ĐH Công Thương TP.HCM (HUIT)
* **Đề tài:** Phân đoạn và phát hiện khối u não trên ảnh cộng hưởng từ MRI

---

## 🎯 1. Mục Tiêu Trọng Tâm Trong Tuần 1 Của Trường
Tập trung 100% vào **quản trị học vụ, thiết kế kiến trúc hệ thống và đặc tả thuật toán xử lý ảnh số**. Hoàn toàn **không phụ thuộc** vào phần việc của Huỳnh Tâm Trí và **chưa cần viết code logic** trong tuần này.

---

## 📋 2. Chi Tiết Các Hạng Mục Công Việc Độc Lập

### Hạng mục 1: Quản trị học vụ & Thiết lập chuẩn Repository
* **Nội dung:**
  * Điền và nộp phiếu đăng ký đề tài chính thức trên Google Classroom theo mẫu của Giảng viên hướng dẫn.
  * Thiết lập quy ước nhánh Git (`main`, `feat/truong-...`) để bảo vệ lịch sử commit minh chứng cho cá nhân.
* **Sản phẩm bàn giao:** Đề tài được GV duyệt trên Classroom + Repository đã cấu hình xong quyền truy cập.

### Hạng mục 2: Soạn thảo Bản đặc tả kỹ thuật Pipeline (`docs/SPEC_PIPELINE_MRI.md`)
* **Nội dung:** Viết tài liệu thiết kế kỹ thuật chi tiết cho pipeline xử lý ảnh số gồm 2 khối thuật toán nòng cốt:
  1. **Khối Tách sọ não (Skull Stripping):**
     * Nguyên lý phân ngưỡng Otsu tách vùng đầu khỏi nền tối.
     * Biến đổi hình thái học (Morphological Opening/Closing) bằng phần tử cấu trúc dạng đĩa (disk/ellipse structuring element) để cắt đứt cuống nối giữa màng não và xương sọ.
     * Thuật toán trích xuất thành phần liên thông lớn nhất (Largest Connected Component - LCC) để giữ lại nhu mô não nguyên vẹn.
     * Thuật toán lấp lỗ hổng (Hole Filling) và nhân bitwise-AND để tạo ảnh não sạch sọ.
  2. **Khối Phân đoạn khối u lõi (Core Tumor Segmentation):**
     * **Phương án A (Baseline chính):** Marker-controlled Watershed (Biến đổi khoảng cách Euclidean Distance Transform $\rightarrow$ Xác định điểm hạt giống Foreground/Background $\rightarrow$ Phân thủy Watershed).
     * **Phương án B (Phương án đối chứng):** Seeded Region Growing (Phát triển vùng từ hạt giống cực đại cường độ trong mô não) HOẶC Phân cụm K-Means.
* **Sản phẩm bàn giao:** File tài liệu `docs/SPEC_PIPELINE_MRI.md` có đầy đủ công thức, giải thích tham số và sơ đồ luồng.

### Hạng mục 3: Đọc và tổng hợp tài liệu chuyên ngành DIP
* **Nội dung:** Đọc kỹ các chương liên quan trực tiếp trong giáo trình:
  * Sách Gonzalez & Woods (4th Edition): **Chương 9** (Morphological Image Processing) & **Chương 10** (Image Segmentation).
  * Giáo trình Xử lý ảnh số HUIT: Phần phân ngưỡng tự động và phép lọc phi tuyến (Bilateral filter).
* **Sản phẩm bàn giao:** Danh mục tài liệu trích dẫn chuẩn bị sẵn cho Mục IV (Cơ sở lý thuyết) của Báo cáo đồ án.

---

## 📅 3. Lịch Trình Thực Hiện 7 Ngày (Dành Riêng Cho Trường)

| Ngày | Công việc cụ thể | Trạng thái |
| :--- | :--- | :---: |
| **Thứ 2** | Nộp đơn đăng ký đề tài trên Classroom; phân quyền repo cho Trí. | [ ] |
| **Thứ 3** | Đọc Gonzalez & Woods Chương 9 (Erosion, Dilation, Opening, Closing, Connected Components). | [ ] |
| **Thứ 4** | Đọc Gonzalez & Woods Chương 10 (Watershed, Distance Transform, Region Growing). | [ ] |
| **Thứ 5** | Viết bản nháp phần 1: Thuật toán Tách sọ não trong `docs/SPEC_PIPELINE_MRI.md`. | [ ] |
| **Thứ 6** | Viết bản nháp phần 2: Thuật toán Phân đoạn u (Watershed & Region Growing) trong Spec. | [ ] |
| **Thứ 7** | Hoàn thiện toàn bộ file `docs/SPEC_PIPELINE_MRI.md`, kiểm tra lại công thức và sơ đồ. | [ ] |
| **Chủ nhật** | Họp giao ban 15 phút với Trí, tổng kết tuần 1 và chốt kế hoạch tuần 2. | [ ] |

---

## ✅ 4. Tiêu Chí Nghiệm Thu (Definition of Done) Của Trường
Trường được coi là hoàn thành xuất sắc Tuần 1 khi đạt đủ 3 tiêu chí sau:
1. Đề tài được giảng viên ghi nhận trên hệ thống lớp học.
2. File `docs/SPEC_PIPELINE_MRI.md` được viết hoàn chỉnh, rõ ràng, giảng viên đọc hiểu được ngay cơ chế tách sọ và phân đoạn u.
3. Không bị vướng bất kỳ dòng code logic nào chạy lỗi vì tuần này chưa cần cài đặt mã nguồn.
