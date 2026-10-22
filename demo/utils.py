"""Helper utilities phục vụ hiển thị Streamlit GUI chuẩn PACS y tế."""

from __future__ import annotations

import os
from typing import Dict, List, Optional, Tuple, Any
import cv2
import numpy as np


def get_default_base_dir() -> str:
    """Trả về thư mục dữ liệu cơ sở (data/full)."""
    return "data/full"


def get_default_data_dir() -> str:
    """Trả về thư mục ảnh (data/full/images)."""
    return "data/full/images"


def list_sample_cases(data_dir: Optional[str] = None) -> List[str]:
    """Lấy danh sách các file ảnh có sẵn trong thư mục ảnh (mặc định ưu tiên data/full)."""
    if data_dir is None:
        data_dir = get_default_data_dir()
    if not os.path.exists(data_dir):
        return []
    return sorted([f for f in os.listdir(data_dir) if f.endswith(".png")])


def _read_grayscale(path: str) -> Optional[np.ndarray]:
    """Đọc ảnh xám từ đường dẫn, hỗ trợ Unicode trên Windows."""
    if not os.path.exists(path):
        return None
    try:
        encoded = np.fromfile(path, dtype=np.uint8)
    except OSError:
        return None
    if encoded.size == 0:
        return None
    return cv2.imdecode(encoded, cv2.IMREAD_GRAYSCALE)


def load_image_and_mask(sample_id: str, base_dir: Optional[str] = None) -> Tuple[Optional[np.ndarray], Optional[np.ndarray]]:
    """Nạp ảnh MRI gốc và mặt nạ Ground Truth tương ứng (mặc định ưu tiên data/full)."""
    if base_dir is None:
        base_dir = get_default_base_dir()
    img_path = os.path.join(base_dir, "images", f"{sample_id}.png")
    mask_path = os.path.join(base_dir, "masks", f"{sample_id}_mask.png")

    img = _read_grayscale(img_path)
    mask = _read_grayscale(mask_path)
    return img, mask


def generate_error_map(orig_gray: np.ndarray, pred_mask: np.ndarray, gt_mask: np.ndarray) -> np.ndarray:
    """Tạo ảnh màu RGB trực quan hóa sai số phân đoạn y sinh:
    - Xanh lá cây (True Positive - TP): Vùng thuật toán phát hiện đúng u theo Ground Truth.
    - Đỏ tươi (False Positive - FP): Vùng thuật toán báo nhầm mô lành thành u.
    - Vàng cam (False Negative - FN): Vùng khối u thực tế bị thuật toán bỏ sót.
    - Nền: Ảnh MRI gốc giảm độ sáng (dimmed) để làm nổi bật các vùng màu.
    """
    base = cv2.cvtColor(orig_gray, cv2.COLOR_GRAY2RGB)
    base = (base.astype(np.float32) * 0.40).astype(np.uint8)

    p_bin = (pred_mask > 0)
    g_bin = (gt_mask > 0)

    tp = p_bin & g_bin
    fp = p_bin & (~g_bin)
    fn = (~p_bin) & g_bin

    # Màu RGB chuẩn y tế
    base[tp] = [34, 197, 94]    # Xanh lá cây (True Positive)
    base[fp] = [239, 68, 68]    # Đỏ tươi (False Positive)
    base[fn] = [245, 158, 11]   # Vàng cam (False Negative)

    return base


# Danh mục các ca lâm sàng tiêu biểu (Curated Presets)
PRESET_CASES: List[Dict[str, Any]] = [
    {
        "id": "TCGA_CS_6290_20000917_10",
        "title": "Ca 1: U Điển Hình Bờ Rõ",
        "badge": "Dice 0.971",
        "badge_color": "#10b981",
        "desc": "Khối u kích thước trung bình (1,247 px), độ tương phản cao, bờ rõ ràng.",
        "type": "positive"
    },
    {
        "id": "TCGA_CS_6186_20000601_16",
        "title": "Ca 2: U Kích Thước Lớn",
        "badge": "Area 2,079 px",
        "badge_color": "#3b82f6",
        "desc": "Khối u phát triển rộng (2,079 px), chiếm tỷ lệ lớn khoang sọ não.",
        "type": "positive"
    },
    {
        "id": "TCGA_CS_4942_19970222_12",
        "title": "Ca 3: U Bờ Phức Tạp",
        "badge": "Dice 0.943",
        "badge_color": "#f59e0b",
        "desc": "Khối u có ranh giới thâm nhiễm (1,383 px), viền nhiều rãnh gồ ghề.",
        "type": "positive"
    },
    {
        "id": "TCGA_DU_5851_19950428_2",
        "title": "Ca 4: Não Lành Không U",
        "badge": "Spec 99.9%",
        "badge_color": "#8b5cf6",
        "desc": "Lát cắt âm tính hoàn toàn không có bệnh lý (Healthy Control Case).",
        "type": "negative"
    }
]
