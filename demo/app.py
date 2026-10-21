"""Web demo Streamlit cho pipeline phân đoạn u não trên ảnh MRI."""

from __future__ import annotations

import csv
import io
import os
import sys

import cv2
import numpy as np
import streamlit as st

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from demo.utils import list_sample_cases, load_image_and_mask
from src.pipeline import BrainTumorPipeline


st.set_page_config(
    page_title="Phân đoạn u não MRI | HUIT",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
      :root { --ink: #172b4d; --muted: #62748a; --line: #dbe3ec; --blue: #1769aa; }
      .block-container { max-width: 1440px; padding-top: 3.5rem; padding-bottom: 3rem; }
      [data-testid="stSidebar"] { background: #f5f8fc; border-right: 1px solid var(--line); }
      [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
      [data-testid="stSidebar"] h3 { color: var(--ink); }
      .app-eyebrow { color: var(--blue); font-size: .78rem; font-weight: 700;
        letter-spacing: .12em; text-transform: uppercase; margin-bottom: .5rem; }
      .app-title { color: var(--ink); font-size: 2rem; font-weight: 750;
        line-height: 1.2; margin: 0; }
      .app-subtitle { color: var(--muted); font-size: 1rem; margin-top: .65rem; }
      .section-label { color: var(--ink); font-size: 1.15rem; font-weight: 700;
        padding-top: .3rem; }
      div[data-testid="stMetric"] { background: #fff; border: 1px solid var(--line);
        border-radius: 12px; padding: 1rem 1.1rem; }
      div[data-testid="stMetricLabel"] p { color: var(--muted); }
      div[data-testid="stAlert"] { border-radius: 10px; }
      a[data-testid="stHeaderActionElements"] { display: none !important; }
      hr { border-color: var(--line); }
    </style>
    """,
    unsafe_allow_html=True,
)


def decode_upload(uploaded_file: object) -> np.ndarray | None:
    """Đọc ảnh tải lên thành ảnh xám OpenCV."""
    if uploaded_file is None:
        return None
    raw = np.frombuffer(uploaded_file.getvalue(), dtype=np.uint8)
    return cv2.imdecode(raw, cv2.IMREAD_GRAYSCALE)


def result_signature(
    source_key: str,
    method_key: str,
    params: dict[str, float | int],
) -> tuple[object, ...]:
    return (source_key, method_key, *sorted(params.items()))


st.markdown('<div class="app-eyebrow">Đồ án xử lý ảnh số · HUIT</div>', unsafe_allow_html=True)
st.markdown('<h1 class="app-title">Phân đoạn khối u não trên ảnh MRI</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="app-subtitle">Thử nghiệm hai phương pháp phân đoạn và đối chiếu kết quả với mặt nạ tham chiếu.</p>',
    unsafe_allow_html=True,
)
st.divider()


with st.sidebar:
    st.title("Thiết lập phân tích")
    st.caption("Chọn nguồn ảnh và cấu hình phương pháp xử lý.")

    source_mode = st.radio(
        "Nguồn ảnh",
        ("Kho TCGA-LGG trên máy", "Tải ảnh từ thiết bị"),
        index=0,
    )

    input_img: np.ndarray | None = None
    input_gt_mask: np.ndarray | None = None
    source_key = ""
    sample_id: str | None = None

    if source_mode == "Kho TCGA-LGG trên máy":
        image_dir = os.path.join(PROJECT_ROOT, "data", "full", "images")
        full_files = list_sample_cases(image_dir)
        if full_files:
            patient_query = st.text_input(
                "Lọc mã bệnh nhân",
                placeholder="Ví dụ: TCGA_CS_4941",
            ).strip().upper()
            filtered_files = (
                [name for name in full_files if patient_query in name.upper()]
                if patient_query
                else full_files[:100]
            )
            if filtered_files:
                selected_file = st.selectbox(
                    "Lát cắt MRI",
                    filtered_files,
                    help=f"Hiển thị {len(filtered_files)} trên tổng số {len(full_files)} ảnh.",
                )
                sample_id = os.path.splitext(selected_file)[0]
                input_img, input_gt_mask = load_image_and_mask(
                    sample_id,
                    base_dir=os.path.join(PROJECT_ROOT, "data", "full"),
                )
                source_key = f"dataset:{sample_id}"
            else:
                st.warning("Không tìm thấy ảnh nào khớp với mã bệnh nhân này.")
        else:
            st.info(
                "Kho ảnh đầy đủ chưa có trên máy chủ này. Hãy tải ảnh lên hoặc chạy ứng dụng trên máy có data/full."
            )

    else:
        uploaded_image = st.file_uploader(
            "Ảnh MRI",
            type=("png", "jpg", "jpeg", "tif", "tiff"),
            help="Ảnh sẽ được đọc ở thang xám để xử lý.",
        )
        input_img = decode_upload(uploaded_image)
        if uploaded_image is not None:
            source_key = f"upload:{uploaded_image.name}:{uploaded_image.size}"
        uploaded_mask = st.file_uploader(
            "Mặt nạ tham chiếu (không bắt buộc)",
            type=("png", "jpg", "jpeg", "tif", "tiff"),
            key="ground_truth_upload",
        )
        input_gt_mask = decode_upload(uploaded_mask)

    st.divider()
    method_label = st.selectbox(
        "Phương pháp phân đoạn",
        ("Watershed", "Region Growing"),
    )
    method_key = "watershed" if method_label == "Watershed" else "region_growing"

    if method_key == "watershed":
        dist_ratio = st.slider("Ngưỡng khoảng cách", 0.1, 0.9, 0.4, 0.05)
        pipeline_params: dict[str, float | int] = {"dist_thresh_ratio": dist_ratio}
    else:
        tolerance = st.slider("Dung sai cường độ", 5, 40, 15, 1)
        pipeline_params = {"intensity_tolerance": tolerance}

    run_button = st.button(
        "Chạy phân đoạn",
        type="primary",
        width="stretch",
        disabled=input_img is None,
    )


if input_img is None:
    st.info("Chọn một lát cắt trong thanh bên hoặc tải ảnh MRI lên để bắt đầu.")
else:
    current_signature = result_signature(source_key, method_key, pipeline_params)

    if run_button:
        with st.spinner("Đang tiền xử lý và phân đoạn ảnh..."):
            pipeline = BrainTumorPipeline(method=method_key, params=pipeline_params)
            diagnostic, intermediates = pipeline.process(input_img, gt_mask=input_gt_mask)
            st.session_state["segmentation_result"] = {
                "signature": current_signature,
                "diagnostic": diagnostic,
                "intermediates": intermediates,
            }

    saved_result = st.session_state.get("segmentation_result")
    if not saved_result or saved_result["signature"] != current_signature:
        st.info("Ảnh đã sẵn sàng. Nhấn “Chạy phân đoạn” để xem kết quả.")
    else:
        diagnostic = saved_result["diagnostic"]
        intermediates = saved_result["intermediates"]

        st.markdown('<div class="section-label">Kết quả định lượng</div>', unsafe_allow_html=True)
        metric_cols = st.columns(5)
        metric_cols[0].metric(
            "Trạng thái",
            "Có vùng" if diagnostic.tumor_detected else "Không có",
        )
        metric_cols[1].metric("Diện tích dự đoán", f"{diagnostic.tumor_area_px:,} px")
        metric_cols[2].metric("Tỷ lệ trên vùng não", f"{diagnostic.tumor_ratio_percent:.2f}%")
        metric_cols[3].metric("Độ tròn", f"{diagnostic.circularity:.3f}")
        metric_cols[4].metric(
            "Dice so với tham chiếu",
            f"{diagnostic.dice_score:.4f}" if diagnostic.dice_score is not None else "Chưa có",
        )

        if sample_id:
            st.caption(f"Mã lát cắt: {sample_id} · Phương pháp: {method_label}")
        elif input_gt_mask is None:
            st.caption("Chưa tải mặt nạ tham chiếu; Dice không được tính.")

        st.divider()
        st.markdown('<div class="section-label">Các bước xử lý ảnh</div>', unsafe_allow_html=True)
        image_cols = st.columns(4)
        image_items = (
            ("Ảnh MRI gốc", intermediates["original"], None),
            ("Ảnh sau tách sọ", intermediates["stripped"], None),
            ("Mặt nạ dự đoán", intermediates["tumor_mask"], None),
            ("Vùng phân đoạn trên ảnh", intermediates["overlay"], "BGR"),
        )
        for column, (label, image, channels) in zip(image_cols, image_items):
            with column:
                st.caption(label)
                if channels:
                    st.image(image, width="stretch", channels=channels)
                else:
                    st.image(image, width="stretch")

        if input_gt_mask is not None:
            st.divider()
            st.markdown('<div class="section-label">Đối chiếu mặt nạ</div>', unsafe_allow_html=True)
            gt_col, pred_col = st.columns(2)
            with gt_col:
                st.caption("Ground Truth")
                st.image(input_gt_mask, width="stretch")
            with pred_col:
                st.caption("Mặt nạ dự đoán")
                st.image(intermediates["tumor_mask"], width="stretch")

        report = io.StringIO()
        writer = csv.writer(report)
        writer.writerow(("sample_id", "method", "tumor_detected", "tumor_area_px", "tumor_ratio_percent", "circularity", "dice", "iou"))
        writer.writerow((
            sample_id or "uploaded_image",
            method_label,
            diagnostic.tumor_detected,
            diagnostic.tumor_area_px,
            round(diagnostic.tumor_ratio_percent, 4),
            round(diagnostic.circularity, 4),
            diagnostic.dice_score,
            diagnostic.iou_score,
        ))
        st.download_button(
            "Tải báo cáo kết quả CSV",
            data=report.getvalue().encode("utf-8-sig"),
            file_name=f"segmentation_{sample_id or 'upload'}.csv",
            mime="text/csv",
        )

st.divider()
st.caption("Đồ án học phần Xử lý ảnh số · HUIT · Kết quả chỉ phục vụ mục đích học tập và nghiên cứu.")
