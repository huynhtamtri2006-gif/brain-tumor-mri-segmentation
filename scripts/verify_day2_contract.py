#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kiểm chuẩn tự động Hợp đồng Kỹ thuật Ngày 2 — Hà Mạnh Trường (2045240326).

Xác minh tối thiểu 20 mục:
  1. Cấu hình YAML đủ khoá preprocessing (bilateral_filter, clahe, skull_stripping).
  2. 4 chữ ký hàm tiền xử lý/tách sọ khớp đặc tả §4.
  3. Tương thích ngược khi `return_intermediates=False`.
  4. Hợp đồng `return_intermediates=True` (đủ 8 khoá trung gian, đúng shape/dtype).
  5. Bất biến DIP `stripped[mask == 0] == 0` và tính nhất quán chuỗi 6 bước.
  6. An toàn với ảnh rỗng (không crash, không chia cho 0).
  7. Hình minh họa `reports/figures/skull_stripping_steps.png` tồn tại, > 50 KB.
  8. Notebook Ngày 2 (`02_preprocessing_and_skull_stripping.ipynb`) tồn tại và có output cells (bao gồm ảnh).
  9. Checklist tài liệu: đúng 3 ô Ngày 2 là `[x]`, 14 ô Ngày 3–7 giữ `[ ]`.

Chạy từ thư mục gốc repo:

    python scripts/verify_day2_contract.py

Mã thoát: 0 nếu toàn bộ kiểm tra đạt, 1 nếu có bất kỳ mục nào thất bại.
"""

from __future__ import annotations

import inspect
import json
import re
import sys
import typing
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

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

from src.preprocessing.filters import apply_bilateral_filter, apply_clahe  # noqa: E402
from src.preprocessing.skull_strip import extract_brain_mask, strip_skull  # noqa: E402

SAMPLE_IMAGE = (
    ROOT / "data" / "full" / "images" / "TCGA_CS_4941_19960909_13.png"
    if (ROOT / "data" / "full" / "images" / "TCGA_CS_4941_19960909_13.png").is_file()
    else ROOT / "data" / "sample" / "images" / "mri_brain_tumor_01.png"
)
FIGURE_PATH = ROOT / "reports" / "figures" / "skull_stripping_steps.png"
NOTEBOOKS = (
    ROOT / "notebooks" / "02_preprocessing_and_skull_stripping.ipynb",
)
TASK_DOC = ROOT / "docs" / "NHIEM_VU_HA_MANH_TRUONG.md"
TARGET_SHAPE = (256, 256)
INTERMEDIATE_KEYS = {
    "original", "denoised", "otsu", "opened",
    "lcc", "closed_and_filled", "brain_mask", "stripped",
}

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
        checks.append(Check("CFG", "Nạp YAML (encoding=utf-8)", isinstance(config, dict),
                            "configs/default_params.yaml"))
    except Exception as exc:  # noqa: BLE001
        checks.append(Check("CFG", "Nạp YAML (encoding=utf-8)", False,
                            f"{type(exc).__name__}: {exc}"))
        return

    preprocessing = config.get("preprocessing", {})
    expectations = [
        ("preprocessing.bilateral_filter", "bilateral_filter",
         ["d", "sigma_color", "sigma_space"]),
        ("preprocessing.clahe", "clahe", ["clip_limit", "tile_grid_size"]),
    ]
    for label, key, params in expectations:
        node = preprocessing.get(key)
        missing = [p for p in params if not isinstance(node, dict) or p not in node]
        if missing:
            checks.append(Check("CFG", label, False, "thiếu khoá: " + ", ".join(missing)))
        else:
            checks.append(Check("CFG", label, True,
                                ", ".join(f"{p}={node[p]!r}" for p in params)))

    # Chấp nhận cả hai cách đặt tên: skull_stripping (thực tế) và skull_strip (nhiệm vụ).
    skull_key = next((k for k in ("skull_stripping", "skull_strip") if k in preprocessing), None)
    if skull_key is None:
        checks.append(Check("CFG", "preprocessing.skull_stripping", False, "thiếu nhánh cấu hình"))
    else:
        node = preprocessing[skull_key]
        missing = [p for p in ("kernel_size", "morph_iterations")
                   if not isinstance(node, dict) or p not in node]
        if missing:
            checks.append(Check("CFG", "preprocessing.skull_stripping", False,
                                "thiếu khoá: " + ", ".join(missing)))
        else:
            checks.append(Check("CFG", "preprocessing.skull_stripping", True,
                                ", ".join(f"{p}={node[p]!r}" for p in
                                          ("kernel_size", "morph_iterations"))
                                + f" (khoá thực tế: {skull_key})"))


# =============================================================================
# 2. CHỮ KÝ HÀM
# =============================================================================

SIGNATURE_CONTRACT = [
    (
        "apply_bilateral_filter",
        [("image", _REQUIRED), ("d", 9), ("sigma_color", 75.0), ("sigma_space", 75.0)],
        "np.ndarray",
    ),
    (
        "apply_clahe",
        [("image", _REQUIRED), ("clip_limit", 2.0), ("tile_grid_size", (8, 8))],
        "np.ndarray",
    ),
    (
        "extract_brain_mask",
        [("image", _REQUIRED), ("kernel_size", 5), ("return_intermediates", False)],
        "Union[np.ndarray, Tuple[np.ndarray, Dict[str, np.ndarray]]]",
    ),
    (
        "strip_skull",
        [("image", _REQUIRED), ("brain_mask", None), ("return_intermediates", False)],
        "Union[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray, Dict[str, np.ndarray]]]",
    ),
]


def _canonical(annotation: Any) -> str:
    if annotation is inspect.Parameter.empty or annotation is inspect.Signature.empty:
        return ""
    if annotation is type(None):
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


def check_signatures(checks: List[Check]) -> None:
    functions = {"apply_bilateral_filter": apply_bilateral_filter, "apply_clahe": apply_clahe,
                 "extract_brain_mask": extract_brain_mask, "strip_skull": strip_skull}

    for label, expected_params, expected_return in SIGNATURE_CONTRACT:
        signature = inspect.signature(functions[label])
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
# 3. HỢP ĐỒNG return_intermediates
# =============================================================================

def _load_image() -> Optional[np.ndarray]:
    if not SAMPLE_IMAGE.is_file():
        return None
    return cv2.imread(str(SAMPLE_IMAGE), cv2.IMREAD_GRAYSCALE)


def check_backward_compatibility(checks: List[Check], image: np.ndarray) -> None:
    """Gọi kiểu cũ (mặc định False) phải giữ nguyên hành vi trả về."""
    mask_plain = extract_brain_mask(image)
    plain_ok = (
        isinstance(mask_plain, np.ndarray) and mask_plain.shape == image.shape
        and mask_plain.dtype == np.uint8
        and set(np.unique(mask_plain).tolist()).issubset({0, 255})
    )
    checks.append(Check("BC", "extract_brain_mask() trả mask 2D", plain_ok,
                        f"type={type(mask_plain).__name__} • shape={getattr(mask_plain, 'shape', None)}"))

    result = strip_skull(image)
    two_tuple_ok = isinstance(result, tuple) and len(result) == 2
    checks.append(Check("BC", "strip_skull(image) trả 2-tuple", two_tuple_ok,
                        f"{len(result) if isinstance(result, tuple) else '?'} phần tử"))

    stripped, mask = result if two_tuple_ok else (None, None)
    passed_mask = strip_skull(image, mask_plain)
    with_mask_ok = (
        isinstance(passed_mask, tuple) and len(passed_mask) == 2
        and np.array_equal(passed_mask[1], mask_plain)
    )
    checks.append(Check("BC", "strip_skull(image, mask) trả 2-tuple", with_mask_ok,
                        "mặt nạ truyền vào được giữ nguyên"))

    if two_tuple_ok and mask is not None:
        invariant_ok = bool(np.all(stripped[mask == 0] == 0))
    else:
        invariant_ok = False
    checks.append(Check("INV", "stripped[mask == 0] == 0", invariant_ok,
                        "bất biến DIP I4"))


def check_intermediates(checks: List[Check], image: np.ndarray) -> None:
    mask_rich = extract_brain_mask(image, return_intermediates=True)
    extract_shape_ok = isinstance(mask_rich, tuple) and len(mask_rich) == 2
    checks.append(Check("API", "extract_brain_mask(True) trả 2-tuple", extract_shape_ok,
                        f"{len(mask_rich) if isinstance(mask_rich, tuple) else '?'} phần tử"))

    if not extract_shape_ok:
        return
    mask, steps = mask_rich
    keys_ok = set(steps) == INTERMEDIATE_KEYS
    checks.append(Check("API", "extract: đủ 8 khoá trung gian", keys_ok,
                        f"{len(steps)} khoá" if keys_ok
                        else "thiếu: " + ", ".join(sorted(INTERMEDIATE_KEYS - set(steps)))))

    rounded = strip_skull(image, return_intermediates=True)
    strip_shape_ok = isinstance(rounded, tuple) and len(rounded) == 3
    checks.append(Check("API", "strip_skull(True) trả 3-tuple", strip_shape_ok,
                        f"{len(rounded) if isinstance(rounded, tuple) else '?'} phần tử"))
    if not strip_shape_ok:
        return
    stripped, mask_out, steps_out = rounded

    checks.append(Check(
        "API", "mask & stripped khớp intermediates",
        np.array_equal(mask, steps["brain_mask"]) and np.array_equal(mask_out, mask)
        and np.array_equal(stripped, steps_out["stripped"]),
        "brain_mask & stripped đồng nhất giữa 2 hàm",
    ))

    shape_problems: List[str] = []
    for key in sorted(INTERMEDIATE_KEYS):
        value = steps_out.get(key)
        if not isinstance(value, np.ndarray):
            shape_problems.append(f"{key}: thiếu")
        elif value.shape != image.shape:
            shape_problems.append(f"{key}.shape={value.shape}")
        elif value.dtype != np.uint8:
            shape_problems.append(f"{key}.dtype={value.dtype}")
    checks.append(Check("API", "8 ảnh trung gian (H,W) uint8", not shape_problems,
                        "; ".join(shape_problems) if shape_problems
                        else f"{len(INTERMEDIATE_KEYS)} ảnh • shape={image.shape}"))

    # Thứ tự hình thái học: opened ⊆ otsu; lcc ⊆ opened; mask ⊇ lcc;
    # stripped = ảnh gốc AND mask.
    opened_outside = cv2.bitwise_and(steps_out["opened"], cv2.bitwise_not(steps_out["otsu"]))
    lcc_outside = cv2.bitwise_and(steps_out["lcc"], cv2.bitwise_not(steps_out["opened"]))
    mask_missing_lcc = cv2.bitwise_and(steps_out["lcc"], cv2.bitwise_not(steps_out["brain_mask"]))
    chain_ok = (
        int(np.count_nonzero(opened_outside)) == 0
        and int(np.count_nonzero(lcc_outside)) == 0
        and int(np.count_nonzero(mask_missing_lcc)) == 0
        and np.array_equal(stripped, cv2.bitwise_and(image, image, mask=mask))
    )
    checks.append(Check("API", "Chuỗi 6 bước nhất quán (⊆ / AND)", chain_ok,
                        "Otsu ⊇ Opening ⊇ LCC ⊆ Mask • stripped = ảnh gốc AND mask"))


def check_empty_image(checks: List[Check]) -> None:
    empty = np.zeros(TARGET_SHAPE, dtype=np.uint8)
    try:
        mask = extract_brain_mask(empty)
        stripped, mask2, steps = strip_skull(empty, return_intermediates=True)
        empty_ok = (
            mask.shape == empty.shape and int(np.count_nonzero(mask)) == 0
            and int(np.count_nonzero(stripped)) == 0
            and set(steps) == INTERMEDIATE_KEYS
            and np.array_equal(mask, mask2)
        )
        detail = "ảnh đen → mask 0, stripped 0, đủ 8 khoá, không ngoại lệ"
    except ZeroDivisionError as exc:
        empty_ok = False
        detail = f"ZeroDivisionError: {exc}"
    except Exception as exc:  # noqa: BLE001 - mọi ngoại lệ đều vi phạm fail-safe
        empty_ok = False
        detail = f"{type(exc).__name__}: {exc}"
    checks.append(Check("INV", "Ảnh rỗng an toàn (fail-safe)", empty_ok, detail))


# =============================================================================
# 4. HÌNH MINH HỌA, NOTEBOOK, TÀI LIỆU
# =============================================================================

def check_figure(checks: List[Check]) -> None:
    if not FIGURE_PATH.is_file():
        checks.append(Check("FIG", "Tồn tại hình 6 bước", False,
                            "không tìm thấy reports/figures/skull_stripping_steps.png"))
        return
    size_kb = FIGURE_PATH.stat().st_size / 1024
    rendered = cv2.imread(str(FIGURE_PATH), cv2.IMREAD_GRAYSCALE)
    ok = size_kb > 50 and rendered is not None and rendered.shape[0] > 1000
    checks.append(Check(
        "FIG", "Hình 6 bước > 50 KB & đọc được", ok,
        f"{size_kb:.1f} KB • {rendered.shape if rendered is not None else 'imread lỗi'}",
    ))


def check_notebooks(checks: List[Check]) -> None:
    for path in NOTEBOOKS:
        relative = path.relative_to(ROOT)
        if not path.is_file():
            checks.append(Check("NB", str(relative), False, "không tìm thấy tệp"))
            continue
        try:
            notebook = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            checks.append(Check("NB", str(relative), False, f"JSON lỗi: {exc}"))
            continue

        code_cells = [c for c in notebook.get("cells", []) if c.get("cell_type") == "code"]
        executed = [c for c in code_cells if c.get("execution_count") is not None]
        with_output = [c for c in code_cells if c.get("outputs")]
        png_outputs = sum(
            1 for c in code_cells for o in c.get("outputs", [])
            if "image/png" in o.get("data", {})
        )
        ok = (
            len(code_cells) > 0 and len(executed) == len(code_cells)
            and len(with_output) >= 3 and png_outputs >= 1
        )
        checks.append(Check(
            "NB", str(relative), ok,
            f"{len(executed)}/{len(code_cells)} cell đã chạy • "
            f"{len(with_output)} cell có output • {png_outputs} ảnh PNG",
        ))


def check_docs(checks: List[Check]) -> None:
    if not TASK_DOC.is_file():
        checks.append(Check("DOC", "Checklist Ngày 2", False, "không tìm thấy tài liệu nhiệm vụ"))
        return

    text = TASK_DOC.read_text(encoding="utf-8")
    matches = list(re.finditer(r"^###\s.*?NGÀY\s+(\d+)", text, re.MULTILINE))
    sections: Dict[int, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[int(match.group(1))] = text[match.start():end]

    day2 = sections.get(2)
    if day2 is None:
        checks.append(Check("DOC", "Ngày 2: 3 ô [x]", False, "không tìm thấy mục Ngày 2"))
    else:
        checked = day2.count("- [x]")
        unchecked = day2.count("- [ ]")
        checks.append(Check("DOC", "Ngày 2: 3 ô [x], 0 ô [ ]", checked == 3 and unchecked == 0,
                            f"{checked} [x] • {unchecked} [ ]"))

    later = [sections[d] for d in range(3, 8) if d in sections]
    later_checked = sum(s.count("- [x]") for s in later)
    later_unchecked = sum(s.count("- [ ]") for s in later)
    checks.append(Check("DOC", "Ngày 3–7: 14 ô [ ] nguyên vẹn",
                        later_checked == 0 and later_unchecked == 14,
                        f"{later_checked} [x] • {later_unchecked} [ ]"))

    total_checked = text.count("- [x]")
    total_unchecked = text.count("- [ ]")
    checks.append(Check("DOC", "Toàn tài liệu: 6 [x] / 14 [ ]",
                        total_checked == 6 and total_unchecked == 14,
                        f"{total_checked} [x] • {total_unchecked} [ ]"))


# =============================================================================
# 5. BÁO CÁO
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
        "INV": "Bất biến & an toàn",
        "FIG": "Hình minh họa",
        "NB": "Notebook Ngày 2",
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
    print("KIỂM CHUẨN HỢP ĐỒNG KỸ THUẬT NGÀY 2 — HÀ MẠNH TRƯỜNG (2045240326)")
    print("Tiền xử lý • Tách sọ 6 bước • Notebook 02 • Hình báo cáo Chương 4")
    print("=" * 78)
    print()

    check_config(checks)
    check_signatures(checks)

    image = _load_image()
    if image is None:
        checks.append(Check("INV", "Nạp ảnh mẫu", False,
                            f"không tìm thấy {SAMPLE_IMAGE}"))
    else:
        rel_path = SAMPLE_IMAGE.relative_to(ROOT) if SAMPLE_IMAGE.is_relative_to(ROOT) else SAMPLE_IMAGE.name
        checks.append(Check("INV", "Nạp ảnh mẫu", image.shape == TARGET_SHAPE,
                            f"{rel_path} • shape={image.shape} • dtype={image.dtype}"))
        check_backward_compatibility(checks, image)
        check_intermediates(checks, image)

    check_empty_image(checks)
    check_figure(checks)
    check_notebooks(checks)
    check_docs(checks)

    render_report(checks)

    failed = [c for c in checks if not c.ok]
    print()
    if failed:
        print(f"KẾT LUẬN: THẤT BẠI — {len(failed)} mục không đạt:")
        for check in failed:
            print(f"  - [{check.group}] {check.name}: {check.detail}")
        return 1

    print("KẾT LUẬN: ĐẠT — toàn bộ hợp đồng kỹ thuật Ngày 2 được xác minh.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
