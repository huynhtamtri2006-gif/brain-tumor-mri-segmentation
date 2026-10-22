#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kiểm chuẩn tự động Hợp đồng Kỹ thuật Ngày 3 — Hà Mạnh Trường (2045240326).

Xác minh tối thiểu 19 mục:
  CFG: cấu hình `segmentation.watershed` trong YAML.
  SIG: chữ ký `segment_watershed`, `WatershedSegmenter.__init__`, `.segment`.
  BC : tương thích ngược khi `return_intermediates=False`.
  API: hợp đồng `return_intermediates=True` — 2-tuple, đủ 9 ảnh trung gian uint8.
  INV: mặt nạ u nằm trong nội não, ảnh rỗng fail-safe, quét ratio 0.2–0.6.
  FLT: bộ lọc `min_tumor_area` loại bỏ đảo nhỏ.
  FIG: đồ thị khảo sát độ nhạy tồn tại và > 30 KB.
  DOC: checklist Ngày 3 = 3 `[x]`, Ngày 4–7 = 11 `[ ]`, tổng 9 `[x]` / 11 `[ ]`.

Chạy từ thư mục gốc repo:

    python scripts/verify_day3_contract.py

Mã thoát: 0 nếu toàn bộ kiểm tra đạt, 1 nếu có bất kỳ mục nào thất bại.
"""

from __future__ import annotations

import inspect
import re
import sys
import typing
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple

import cv2
import numpy as np
import yaml

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # pragma: no cover - môi trường không hỗ trợ reconfigure
        pass

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.preprocessing.skull_strip import strip_skull  # noqa: E402
from src.segmentation.watershed import (  # noqa: E402
    INTERMEDIATE_KEYS,
    WatershedSegmenter,
    segment_watershed,
)

SAMPLE_IMAGE = ROOT / "data" / "full" / "images" / "TCGA_CS_4941_19960909_13.png"
FIGURE_PATH = ROOT / "reports" / "figures" / "watershed_param_sensitivity.png"
TASK_DOC = ROOT / "docs" / "NHIEM_VU_HA_MANH_TRUONG.md"
RATIOS = (0.2, 0.3, 0.4, 0.5, 0.6)

_REQUIRED = object()


@dataclass
class Check:
    """Một dòng kết quả kiểm tra."""

    group: str
    name: str
    ok: bool
    detail: str


# =============================================================================
# 1. CẤU HÌNH YAML
# =============================================================================

def check_config(checks: List[Check]) -> None:
    path = ROOT / "configs" / "default_params.yaml"
    if not path.is_file():
        checks.append(Check("CFG", "Nạp YAML", False, "không tìm thấy configs/default_params.yaml"))
        return

    try:
        with path.open("r", encoding="utf-8") as fh:
            config = yaml.safe_load(fh)
    except Exception as exc:  # noqa: BLE001
        checks.append(Check("CFG", "Nạp YAML (encoding=utf-8)", False,
                            f"{type(exc).__name__}: {exc}"))
        return

    checks.append(Check("CFG", "Nạp YAML (encoding=utf-8)", isinstance(config, dict),
                        "configs/default_params.yaml"))

    node = (config.get("segmentation") or {}).get("watershed")
    missing = [p for p in ("dist_thresh_ratio", "bg_dilate_kernel")
               if not isinstance(node, dict) or p not in node]
    if missing:
        checks.append(Check("CFG", "segmentation.watershed", False,
                            "thiếu khoá: " + ", ".join(missing)))
    else:
        checks.append(Check("CFG", "segmentation.watershed", True,
                            ", ".join(f"{p}={node[p]!r}"
                                      for p in ("dist_thresh_ratio", "bg_dilate_kernel"))))


# =============================================================================
# 2. CHỮ KÝ HÀM
# =============================================================================

def _canonical(annotation: Any) -> str:
    if annotation is inspect.Parameter.empty or annotation is inspect.Signature.empty:
        return ""
    if annotation is None or annotation is type(None):
        return "None"
    if isinstance(annotation, str):
        return annotation
    origin = typing.get_origin(annotation)
    args = typing.get_args(annotation)
    if origin is typing.Union:
        if len(args) == 2 and type(None) in args:
            inner = args[0] if args[1] is type(None) else args[1]
            return f"Optional[{_canonical(inner)}]"
        return "Union[" + ", ".join(_canonical(a) for a in args) + "]"
    if origin is not None:
        prefix = {tuple: "Tuple", dict: "Dict", list: "List", set: "Set"}.get(
            origin, getattr(origin, "__name__", str(origin))
        )
        return f"{prefix}[" + ", ".join(_canonical(a) for a in args) + "]"
    if annotation is np.ndarray:
        return "np.ndarray"
    if annotation is typing.Any:
        return "Any"
    return getattr(annotation, "__name__", str(annotation))


def _render_signature(signature: inspect.Signature) -> str:
    parts: List[str] = []
    for param in signature.parameters.values():
        text = param.name
        annotation = _canonical(param.annotation)
        if annotation:
            text += f": {annotation}"
        if param.default is not inspect.Parameter.empty:
            text += f" = {param.default!r}"
        parts.append(text)
    rendered = "(" + ", ".join(parts) + ")"
    returns = _canonical(signature.return_annotation)
    return f"{rendered} -> {returns}" if returns else rendered


SIGNATURE_CONTRACT = [
    (
        "segment_watershed",
        segment_watershed,
        [
            ("brain_image", _REQUIRED),
            ("dist_thresh_ratio", 0.4),
            ("bg_dilate_kernel", 3),
            ("min_tumor_area", 50),
            ("return_intermediates", False),
        ],
        "Union[np.ndarray, Tuple[np.ndarray, Dict[str, np.ndarray]]]",
    ),
    (
        "WatershedSegmenter.__init__",
        WatershedSegmenter.__init__,
        [
            ("self", _REQUIRED),
            ("dist_thresh_ratio", 0.4),
            ("bg_dilate_kernel", 3),
            ("min_tumor_area", 50),
        ],
        "None",
    ),
    (
        "WatershedSegmenter.segment",
        WatershedSegmenter.segment,
        [
            ("self", _REQUIRED),
            ("brain_image", _REQUIRED),
            ("return_intermediates", False),
        ],
        "Union[np.ndarray, Tuple[np.ndarray, Dict[str, np.ndarray]]]",
    ),
]


def check_signatures(checks: List[Check]) -> None:
    for label, function, expected_params, expected_return in SIGNATURE_CONTRACT:
        signature = inspect.signature(function)
        params = list(signature.parameters.values())
        problems: List[str] = []

        if len(params) != len(expected_params):
            problems.append(f"{len(params)} tham số (đặc tả {len(expected_params)})")
        for actual, (name, default) in zip(params, expected_params):
            if actual.name != name:
                problems.append(f"tham số '{actual.name}' thay vì '{name}'")
                continue
            if actual.kind is not inspect.Parameter.POSITIONAL_OR_KEYWORD:
                problems.append(f"'{name}' không phải positional-or-keyword")
            if default is _REQUIRED:
                if actual.default is not inspect.Parameter.empty:
                    problems.append(f"'{name}' không được có giá trị mặc định")
            elif actual.default != default:
                problems.append(f"'{name}' mặc định {actual.default!r} thay vì {default!r}")

        actual_return = _canonical(signature.return_annotation)
        if actual_return != expected_return:
            problems.append(f"trả về {actual_return or '<empty>'} thay vì {expected_return}")

        checks.append(Check(
            "SIG", label, not problems,
            "; ".join(problems) if problems else f"{label}{_render_signature(signature)}",
        ))


# =============================================================================
# 3. HỢP ĐỒNG return_intermediates & BẤT BIẾN
# =============================================================================

def _load_stripped() -> Tuple[np.ndarray, np.ndarray]:
    image = cv2.imread(str(SAMPLE_IMAGE), cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Không đọc được ảnh mẫu: {SAMPLE_IMAGE}")
    stripped, _ = strip_skull(image)
    return image, stripped


def check_backward_compatibility(checks: List[Check], stripped: np.ndarray) -> None:
    mask = segment_watershed(stripped)
    ok = (
        isinstance(mask, np.ndarray) and mask.shape == stripped.shape
        and mask.dtype == np.uint8
        and set(np.unique(mask).tolist()).issubset({0, 255})
    )
    checks.append(Check("BC", "segment_watershed() trả mask 2D", ok,
                        f"type={type(mask).__name__} • shape={getattr(mask, 'shape', None)} • "
                        f"dtype={getattr(mask, 'dtype', None)}"))

    class_mask = WatershedSegmenter().segment(stripped)
    class_ok = (
        isinstance(class_mask, np.ndarray) and class_mask.shape == stripped.shape
        and class_mask.dtype == np.uint8
        and set(np.unique(class_mask).tolist()).issubset({0, 255})
    )
    checks.append(Check("BC", "WatershedSegmenter.segment() trả mask 2D", class_ok,
                        f"type={type(class_mask).__name__} • "
                        f"{'khớp hàm tự do' if class_ok and np.array_equal(mask, class_mask) else 'lệch hàm tự do'}"))


def check_intermediates(checks: List[Check], stripped: np.ndarray) -> None:
    result = segment_watershed(stripped, return_intermediates=True)
    tuple_ok = isinstance(result, tuple) and len(result) == 2
    checks.append(Check("API", "Trả 2-tuple (mask, intermediates)", tuple_ok,
                        f"{len(result) if isinstance(result, tuple) else '?'} phần tử"))
    if not tuple_ok:
        return

    mask, steps = result
    keys_ok = set(steps) == set(INTERMEDIATE_KEYS)
    checks.append(Check(
        "API", "Đủ 9 khoá trung gian", keys_ok,
        f"{len(steps)} khoá" if keys_ok
        else "lệch: " + ", ".join(sorted(set(INTERMEDIATE_KEYS) ^ set(steps))),
    ))

    shape_problems: List[str] = []
    for key in INTERMEDIATE_KEYS:
        value = steps.get(key)
        if not isinstance(value, np.ndarray):
            shape_problems.append(f"{key}: thiếu")
        elif value.shape != stripped.shape:
            shape_problems.append(f"{key}.shape={value.shape}")
        elif value.dtype != np.uint8:
            shape_problems.append(f"{key}.dtype={value.dtype}")
    checks.append(Check("API", "9 ảnh trung gian (H,W) uint8", not shape_problems,
                        "; ".join(shape_problems) if shape_problems
                        else f"{len(INTERMEDIATE_KEYS)} ảnh • shape={stripped.shape}"))

    checks.append(Check("API", "mask khớp intermediates['tumor_mask']",
                        np.array_equal(mask, steps["tumor_mask"]),
                        "tumor_mask đồng nhất"))


def check_invariants(checks: List[Check], stripped: np.ndarray) -> None:
    mask = segment_watershed(stripped)
    outside = int(np.count_nonzero(mask[stripped == 0]))
    checks.append(Check("INV", "Mặt nạ u nằm trong nội não", outside == 0,
                        f"{outside} pixel u ngoài nhu mô"))

    empty = np.zeros((256, 256), dtype=np.uint8)
    try:
        mask_plain = segment_watershed(empty)
        mask_rich, steps = segment_watershed(empty, return_intermediates=True)
        empty_ok = (
            mask_plain.shape == empty.shape and int(np.count_nonzero(mask_plain)) == 0
            and int(np.count_nonzero(mask_rich)) == 0
            and set(steps) == set(INTERMEDIATE_KEYS)
            and all(v.shape == empty.shape and v.dtype == np.uint8
                    and int(np.count_nonzero(v)) == 0 for v in steps.values())
        )
        detail = "ảnh đen → mask 0 (cả 2 chế độ), 9 ảnh trung gian toàn 0"
    except ZeroDivisionError as exc:
        empty_ok = False
        detail = f"ZeroDivisionError: {exc}"
    except Exception as exc:  # noqa: BLE001 - mọi ngoại lệ đều vi phạm fail-safe
        empty_ok = False
        detail = f"{type(exc).__name__}: {exc}"
    checks.append(Check("INV", "Ảnh rỗng fail-safe", empty_ok, detail))

    ratio_problems: List[str] = []
    for ratio in RATIOS:
        varied = segment_watershed(stripped, dist_thresh_ratio=ratio)
        if (varied.shape != stripped.shape or varied.dtype != np.uint8
                or not set(np.unique(varied).tolist()).issubset({0, 255})
                or int(np.count_nonzero(varied[stripped == 0])) != 0):
            ratio_problems.append(f"ratio={ratio}")
    checks.append(Check("INV", "Ổn định khi ratio ∈ [0.2, 0.6]", not ratio_problems,
                        "; ".join(ratio_problems) if ratio_problems
                        else "5 mức ratio giữ shape/dtype/nhị phân/nội não"))


# =============================================================================
# 4. BỘ LỌC min_tumor_area
# =============================================================================

def _component_areas(mask: np.ndarray) -> List[int]:
    num_labels, _, stats, _ = cv2.connectedComponentsWithStats(
        (mask > 0).astype(np.uint8), connectivity=8
    )
    return sorted(stats[1:, cv2.CC_STAT_AREA].tolist(), reverse=True)


def check_area_filter(checks: List[Check]) -> None:
    image = np.zeros((256, 256), dtype=np.uint8)
    cv2.circle(image, (128, 128), 100, 100, -1)            # Nhu mô não
    cv2.circle(image, (90, 128), 15, 255, -1)              # Đảo lớn ~700 px
    cv2.rectangle(image, (178, 128), (180, 131), 255, -1)  # Đảo nhỏ 3x4 = 12 px

    unfiltered = _component_areas(
        segment_watershed(image, dist_thresh_ratio=0.1, min_tumor_area=0)
    )
    small_detected = any(area < 50 for area in unfiltered) and any(area >= 500 for area in unfiltered)
    checks.append(Check("FLT", "min_tumor_area=0 giữ đảo nhỏ 12 px", small_detected,
                        f"diện tích các đảo: {unfiltered}"))

    filtered = _component_areas(
        segment_watershed(image, dist_thresh_ratio=0.1, min_tumor_area=50)
    )
    filtered_ok = bool(filtered) and all(area >= 50 for area in filtered) and max(filtered) >= 500
    checks.append(Check("FLT", "min_tumor_area=50 loại sạch đảo nhỏ", filtered_ok,
                        f"diện tích còn lại: {filtered}"))


# =============================================================================
# 5. HÌNH MINH HỌA & CHECKLIST
# =============================================================================

def check_figure(checks: List[Check]) -> None:
    if not FIGURE_PATH.is_file():
        checks.append(Check("FIG", "Đồ thị độ nhạy > 30 KB", False,
                            "không tìm thấy reports/figures/watershed_param_sensitivity.png"))
        return
    size_kb = FIGURE_PATH.stat().st_size / 1024
    rendered = cv2.imread(str(FIGURE_PATH), cv2.IMREAD_GRAYSCALE)
    ok = size_kb > 30 and rendered is not None and rendered.shape[0] > 500
    checks.append(Check("FIG", "Đồ thị độ nhạy > 30 KB", ok,
                        f"{size_kb:.1f} KB • "
                        f"{rendered.shape if rendered is not None else 'imread lỗi'}"))


def check_docs(checks: List[Check]) -> None:
    if not TASK_DOC.is_file():
        checks.append(Check("DOC", "Checklist Ngày 3", False, "không tìm thấy tài liệu nhiệm vụ"))
        return

    text = TASK_DOC.read_text(encoding="utf-8")
    matches = list(re.finditer(r"^###\s.*?NGÀY\s+(\d+)", text, re.MULTILINE))
    sections: Dict[int, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[int(match.group(1))] = text[match.start():end]

    day3 = sections.get(3)
    if day3 is None:
        checks.append(Check("DOC", "Ngày 3: 3 ô [x]", False, "không tìm thấy mục Ngày 3"))
    else:
        checked = day3.count("- [x]")
        unchecked = day3.count("- [ ]")
        checks.append(Check("DOC", "Ngày 3: 3 [x] • 0 [ ]",
                            checked == 3 and unchecked == 0,
                            f"{checked} [x] • {unchecked} [ ]"))

    # Ngày 1–3 không bị hồi quy và tổng số ô checklist luôn đủ 20.
    earlier = [sections[d] for d in (1, 2, 3) if d in sections]
    earlier_checked = sum(s.count("- [x]") for s in earlier)
    earlier_unchecked = sum(s.count("- [ ]") for s in earlier)
    checks.append(Check("DOC", "Ngày 1–3: 9 [x] không hồi quy",
                        earlier_checked == 9 and earlier_unchecked == 0,
                        f"{earlier_checked} [x] • {earlier_unchecked} [ ]"))

    total_checked = text.count("- [x]")
    total_unchecked = text.count("- [ ]")
    checks.append(Check("DOC", "Tổng 20 ô checklist (>= 9 [x])",
                        total_checked + total_unchecked == 20 and total_checked >= 9,
                        f"{total_checked} [x] • {total_unchecked} [ ]"))


# =============================================================================
# 6. BÁO CÁO
# =============================================================================

def render_report(checks: List[Check]) -> None:
    headers = ("Nhóm", "Nội dung kiểm tra", "Kết quả", "Chi tiết")
    rows = [(c.group, c.name, "PASS" if c.ok else "FAIL", c.detail) for c in checks]
    widths = [
        max(len(headers[i]), *(len(row[i]) for row in rows)) if rows else len(headers[i])
        for i in range(len(headers))
    ]
    line = "+" + "+".join("-" * (w + 2) for w in widths) + "+"

    def fmt(cells: Tuple[str, str, str, str]) -> str:
        return "| " + " | ".join(cell.ljust(widths[i]) for i, cell in enumerate(cells)) + " |"

    print(line)
    print(fmt(headers))
    print(line)
    previous_group = None
    for check in checks:
        if previous_group is not None and check.group != previous_group:
            print(line)
        previous_group = check.group
        print(fmt((check.group, check.name, "PASS" if check.ok else "FAIL", check.detail)))
    print(line)

    labels = {
        "CFG": "Cấu hình YAML",
        "SIG": "Chữ ký hàm",
        "BC": "Tương thích ngược",
        "API": "Hợp đồng intermediates",
        "INV": "Bất biến & fail-safe",
        "FLT": "Bộ lọc min_tumor_area",
        "FIG": "Đồ thị độ nhạy",
        "DOC": "Checklist tài liệu",
    }
    print()
    for group, label in labels.items():
        subset = [c for c in checks if c.group == group]
        if subset:
            print(f"  • {label:<28} {sum(1 for c in subset if c.ok)}/{len(subset)} đạt")
    passed = sum(1 for c in checks if c.ok)
    print(f"  TỔNG CỘNG: {passed}/{len(checks)} kiểm tra đạt")


def main() -> int:
    checks: List[Check] = []

    print("=" * 78)
    print("KIỂM CHUẨN HỢP ĐỒNG KỸ THUẬT NGÀY 3 — HÀ MẠNH TRƯỜNG (2045240326)")
    print("Marker-controlled Watershed • min_tumor_area • Khảo sát siêu tham số")
    print("=" * 78)
    print()

    check_config(checks)
    check_signatures(checks)

    try:
        _, stripped = _load_stripped()
        checks.append(Check("INV", "Nạp ảnh mẫu & tách sọ", stripped.shape == (256, 256),
                            f"{SAMPLE_IMAGE.name} • shape={stripped.shape}"))
        check_backward_compatibility(checks, stripped)
        check_intermediates(checks, stripped)
        check_invariants(checks, stripped)
    except Exception as exc:  # noqa: BLE001
        checks.append(Check("INV", "Nạp ảnh mẫu & tách sọ", False,
                            f"{type(exc).__name__}: {exc}"))

    check_area_filter(checks)
    check_figure(checks)
    check_docs(checks)

    render_report(checks)

    failed = [c for c in checks if not c.ok]
    print()
    if failed:
        print(f"KẾT LUẬN: THẤT BẠI — {len(failed)} mục không đạt:")
        for check in failed:
            print(f"  - [{check.group}] {check.name}: {check.detail}")
        return 1

    print("KẾT LUẬN: ĐẠT — toàn bộ hợp đồng kỹ thuật Ngày 3 được xác minh.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
