# KỊCH BẢN & DÀN Ý SLIDE THUYẾT TRÌNH BẢO VỆ ĐỒ ÁN
## Đề tài: Phân đoạn và phát hiện khối u não trên ảnh cộng hưởng từ MRI
**Học phần:** Xử lý ảnh số (2026–2027) — Khoa CNTT — HUIT  
**Nhóm thuyết trình:** Hà Mạnh Trường (Nhóm trưởng) & Huỳnh Tâm Trí (Thành viên)  
**Thời lượng dự kiến:** 10 – 12 phút thuyết trình + 5 phút phản biện hỏi đáp (Q&A)

---

## 🎯 PHÂN CHIA THỜI LƯỢNG & PHẦN NÓI CỦA 2 SINH VIÊN

| Slide | Tiêu Đề Slide | Nội Dung Trọng Tâm | Người Trình Bày | Thời Lượng |
| :---: | :--- | :--- | :---: | :---: |
| **1** | **Bìa Đồ Án** | Tên đề tài, Giảng viên hướng dẫn, Thông tin 2 sinh viên | **Trường** | 30s |
| **2** | **Đặt Vấn Đề** | Tính nguy hiểm của u não & Tầm quan trọng của ảnh MRI | **Trường** | 45s |
| **3** | **Mục Tiêu & Đóng Góp** | Xây dựng pipeline DIP tự động, đo kích thước & Bounding Box | **Trường** | 45s |
| **4** | **Kiến Trúc Pipeline** | Sơ đồ luồng 4 tầng: Tiền xử lý $\rightarrow$ Tách sọ $\rightarrow$ Phân đoạn $\rightarrow$ Đánh giá | **Trường** | 60s |
| **5** | **Tách Sọ Não (Skull Stripping)** | Trực quan hóa 6 bước: Otsu $\rightarrow$ Opening $\rightarrow$ LCC $\rightarrow$ Hole Fill | **Trường** | 60s |
| **6** | **Phương Án A: Watershed** | Nguyên lý biến đổi khoảng cách Euclidean & Điểm hạt giống | **Trường** | 60s |
| **7** | **Phương Án B: Region Growing** | Nguyên lý tìm cực đại cường độ & Lan truyền 8 láng giềng BFS | **Trường** | 60s |
| **8** | **Dữ Liệu Thực Nghiệm (TCGA-LGG)** | 20 mẫu chuẩn hóa $256 \times 256$, Ground truth bác sĩ, 3 nhóm u | **Trí** *(Chuyển lời)* | 45s |
| **9** | **Rút Trích Đặc Trưng Hình Học** | Đo diện tích u ($S_{\text{tumor}}$), Tỷ lệ % u/não, Độ tròn Circularity | **Trí** | 60s |
| **10** | **Bộ Đo Định Lượng Y Khoa** | Công thức & ý nghĩa y khoa của Dice, IoU, Sensitivity, Specificity | **Trí** | 60s |
| **11** | **Bảng So Sánh Định Lượng** | Bảng Mean $\pm$ Std của 2 phương án & Thời gian chạy (< 20ms) | **Trí** | 60s |
| **12** | **Biểu Đồ So Sánh Từng Ca** | Biểu đồ cột Bar chart đối sánh Dice trên 20 ca bệnh | **Trí** | 45s |
| **13** | **Phân Tích Ca Thất Bại (Failure)** | Phân tích ca u nhỏ (< 1.5%) và u bờ mờ bị under-segmentation | **Trường** | 60s |
| **14** | **Giới Thiệu Web Demo (Streamlit)** | Ảnh chụp màn hình ứng dụng tương tác, các chức năng chính | **Trí** | 45s |
| **15** | **Demo Trực Tiếp (Live / Video)** | Thao tác chạy thử trực tiếp trên ứng dụng `demo/app.py` | **Trí** | 90s |
| **16** | **Kết Luận & Hướng Phát Triển** | Tổng kết thành tựu đạt được & Hướng mở rộng 3D thể tích u | **Trường** | 45s |
| **17** | **Lời Cảm Ơn & Q&A** | Lời cảm ơn hội đồng và sẵn sàng trả lời phản biện | **Cả hai** | - |

---

## 💡 CÁC CÂU HỎI THƯỜNG GẶP CỦA HỘI ĐỒNG (Stress-test Q&A)

1. **Hỏi:** *Tại sao không dùng U-Net hay Deep Learning mà lại dùng Watershed và Region Growing?*
   * **Đáp:** Đồ án tuân thủ đúng Quy tắc vàng của môn Xử lý ảnh số (chiếm 50% điểm vào thuật toán DIP truyền thống). Watershed và Region Growing cho phép giải trình minh bạch từng tham số toán học, chạy siêu nhanh dưới 20ms mà không cần GPU đắt tiền hay tập dữ liệu huấn luyện hàng chục ngàn ảnh.
2. **Hỏi:** *Tại sao bước Tách sọ não (Skull Stripping) lại cực kỳ quan trọng?*
   * **Đáp:** Xương sọ và da đầu trên ảnh MRI có tín hiệu tăng sáng rất mạnh (hyperintense). Nếu không tách sọ trước, các thuật toán phân ngưỡng hoặc phân thủy sẽ nhận nhầm xương sọ thành khối u, dẫn đến kết quả sai lệch nghiêm trọng.
3. **Hỏi:** *Độ tròn Circularity có ý nghĩa y khoa gì?*
   * **Đáp:** Giúp hỗ trợ phân loại sơ bộ tính chất u: Khối u có $C \approx 1$ thường là u tròn đều, có bao xơ rõ ràng (thường là u màng não Meningioma lành tính); trong khi khối u có $C \ll 1$ bờ gồ ghề, xâm lấn vào các rãnh cuộn não (thường là u thần kinh đệm ác tính Glioma).
