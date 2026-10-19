#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Xuất hình minh họa 6 bước Tách sọ não cho Báo cáo Chương 4.

Sử dụng chuỗi 6 bước trong `src/preprocessing/skull_strip.py`
(Gaussian -> Otsu -> Opening -> LCC -> Closing & Hole Filling -> Bitwise-AND)
và lưu lưới 2x3 độ phân giải cao vào `reports/figures/skull_stripping_steps.png`.

Chạy từ thư mục gốc repo:

    python scripts/export_skull_stripping_figure.py
"""

from pathlib import Path
import sys

import cv2
import matplotlib

matplotlib.use("Agg")  # Backend không cần màn hình (CI/terminal)
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # pragma: no cover - môi trường không hỗ trợ reconfigure
        pass

from src.preprocessing.skull_strip import strip_skull  # noqa: E402

OUTPUT_PATH = ROOT / "reports" / "figures" / "skull_stripping_steps.png"
PREFERRED_FULL_IMAGE = ROOT / "data" / "full" / "images" / "TCGA_CS_4941_19960909_13.png"
FALLBACK_SAMPLE_IMAGE = ROOT / "data" / "sample" / "images" / "mri_brain_tumor_01.png"


def resolve_sample_image() -> Path:
    """Chọn ảnh mẫu: ưu tiên tập full TCGA-LGG thực tế, fallback sang sample."""
    if PREFERRED_FULL_IMAGE.is_file():
        return PREFERRED_FULL_IMAGE
    if FALLBACK_SAMPLE_IMAGE.is_file():
        return FALLBACK_SAMPLE_IMAGE
    for directory in (ROOT / "data" / "full" / "images", ROOT / "data" / "sample" / "images"):
        if directory.is_dir():
            for candidate in sorted(directory.glob("*.png")):
                return candidate
    raise FileNotFoundError("Không tìm thấy ảnh MRI mẫu trong data/full/images hoặc data/sample/images")


def main() -> int:
    image_path = resolve_sample_image()
    image = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise RuntimeError(f"cv2.imread thất bại: {image_path}")

    _, _, steps = strip_skull(image, return_intermediates=True)

    panels = [
        ("1. Ảnh MRI gốc", steps["original"], "gray"),
        ("2. Phân ngưỡng Otsu", steps["otsu"], "gray"),
        ("3. Phép mở hình thái học (Opening)", steps["opened"], "gray"),
        ("4. Thành phần liên thông lớn nhất (LCC)", steps["lcc"], "gray"),
        ("5. Mặt nạ não hoàn chỉnh (Closing + Hole Filling)", steps["closed_and_filled"], "gray"),
        ("6. Não sạch sọ (Bitwise-AND)", steps["stripped"], "gray"),
    ]

    plt.rcParams["font.family"] = "DejaVu Sans"
    fig, axes = plt.subplots(2, 3, figsize=(15, 9), dpi=300)
    for axis, (title, panel, cmap) in zip(axes.ravel(), panels):
        axis.imshow(panel, cmap=cmap, vmin=0, vmax=255)
        axis.set_title(title, fontsize=12, fontweight="bold")
        axis.axis("off")

    fig.suptitle(
        "Quy trình 6 bước tách sọ não (Skull Stripping) trên ảnh MRI",
        fontsize=16, fontweight="bold", y=0.98,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.96))

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_PATH, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    size_kb = OUTPUT_PATH.stat().st_size / 1024
    print(f"Đã xuất: {OUTPUT_PATH.relative_to(ROOT)} ({size_kb:.1f} KB)")
    print(f"Ảnh nguồn: {image_path.relative_to(ROOT)} • shape={image.shape}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
