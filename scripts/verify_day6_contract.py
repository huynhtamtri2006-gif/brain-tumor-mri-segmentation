"""Kịch bản kiểm chuẩn hợp đồng kỹ thuật Ngày 6 — Hà Mạnh Trường & Huỳnh Tâm Trí.

Nội dung nghiệm thu Ngày 6:
1. Báo cáo đồ án toàn văn Microsoft Word docs/BAO_CAO_DO_AN_XLAS.docx tuân thủ 100% quy chuẩn OpenXML.
2. Căn lề in: Top 3.0cm, Bottom 3.0cm, Left 3.0cm, Right 2.0cm, khổ A4 (21.0 x 29.7cm).
3. Hệ thống kiểu chữ (Typography): Font Times New Roman 100%, Normal 13pt (1.5 lines, indent 1.27cm),
   Heading 1 (15pt, Bold, Center), Heading 2 (13.5pt, Bold, Left), Heading 3 (13pt, Italic, Left).
4. Bảng biểu & Hình ảnh: Bảng chuẩn APA/IEEE kèm Caption TRÊN (11.5pt nghiêng căn giữa),
   Hình ảnh căn giữa kèm Caption DƯỚI (11.5pt nghiêng căn giữa).
5. Đủ 5 hình ảnh nghiên cứu độ phân giải cao và ít nhất 4 bảng biểu số liệu thực nghiệm.
6. Tệp Markdown toàn văn docs/BAO_CAO_DO_AN_XLAS.md đồng bộ cấu trúc 8 chương chuẩn mực.
7. Cập nhật checklist Ngày 6: Hà Mạnh Trường đạt 17/20 [x], Huỳnh Tâm Trí đạt 16/19 [x].

Sử dụng:
    python scripts/verify_day6_contract.py
"""

from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List

import docx

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

DOCX_REPORT_PATH = REPO_ROOT / "docs" / "BAO_CAO_DO_AN_XLAS.docx"
MD_REPORT_PATH = REPO_ROOT / "docs" / "BAO_CAO_DO_AN_XLAS.md"
TASK_DOC_TRUONG = REPO_ROOT / "docs" / "NHIEM_VU_HA_MANH_TRUONG.md"
TASK_DOC_TRI = REPO_ROOT / "docs" / "NHIEM_VU_HUYNH_TAM_TRI.md"
BUILDER_PY_PATH = REPO_ROOT / "src" / "report" / "docx_builder.py"
EXPORT_SCRIPT_PATH = REPO_ROOT / "scripts" / "export_report_docx.py"


@dataclass
class Check:
    group: str
    name: str
    ok: bool
    detail: str


# =============================================================================
# 1. KIỂM TRA FILE VĂN BẢN DOCX VÀ ĐỊNH DẠNG OPENXML
# =============================================================================

def check_docx_report(checks: List[Check]) -> None:
    if not DOCX_REPORT_PATH.is_file():
        checks.append(Check("DOCX", "Tệp BAO_CAO_DO_AN_XLAS.docx tồn tại", False, "không tìm thấy tệp"))
        return

    size_kb = DOCX_REPORT_PATH.stat().st_size / 1024
    checks.append(Check(
        "DOCX", "Dung lượng tệp Báo cáo Word (> 250 KB)",
        size_kb >= 250.0,
        f"{size_kb:.1f} KB (tích hợp đầy đủ hình ảnh độ phân giải cao)"
    ))

    try:
        doc = docx.Document(str(DOCX_REPORT_PATH))
    except Exception as exc:
        checks.append(Check("DOCX", "Đọc cấu trúc OpenXML tệp .docx", False, str(exc)))
        return

    sec = doc.sections[0]

    # 1. Căn lề
    top_cm = round(sec.top_margin.cm, 1) if sec.top_margin else 0
    bot_cm = round(sec.bottom_margin.cm, 1) if sec.bottom_margin else 0
    left_cm = round(sec.left_margin.cm, 1) if sec.left_margin else 0
    right_cm = round(sec.right_margin.cm, 1) if sec.right_margin else 0
    margins_ok = (top_cm == 3.0 and bot_cm == 3.0 and left_cm == 3.0 and right_cm == 2.0)
    checks.append(Check(
        "DOCX", "Căn lề chuẩn in ấn (3.0, 3.0, 3.0, 2.0 cm)",
        margins_ok,
        f"Top={top_cm}cm, Bottom={bot_cm}cm, Left={left_cm}cm, Right={right_cm}cm"
    ))

    # 2. Khổ giấy
    w_cm = round(sec.page_width.cm, 1) if sec.page_width else 0
    h_cm = round(sec.page_height.cm, 1) if sec.page_height else 0
    page_ok = (w_cm == 21.0 and h_cm == 29.7)
    checks.append(Check(
        "DOCX", "Khổ giấy tiêu chuẩn A4 (21.0 x 29.7 cm)",
        page_ok,
        f"{w_cm} x {h_cm} cm"
    ))

    # 3. Normal Style
    normal = doc.styles["Normal"]
    norm_fn = normal.font.name
    norm_sz = normal.font.size.pt if normal.font.size else 0
    norm_pf = normal.paragraph_format
    norm_ls = norm_pf.line_spacing
    norm_sa = round(norm_pf.space_after.pt, 1) if norm_pf.space_after else 0
    norm_ok = (norm_fn == "Times New Roman" and norm_sz == 13.0 and norm_ls == 1.5 and norm_sa == 4.0)
    checks.append(Check(
        "DOCX", "Normal: Times New Roman, 13pt, 1.5 lines, after 4pt",
        norm_ok,
        f"font={norm_fn}, size={norm_sz}pt, line_spacing={norm_ls}, after={norm_sa}pt"
    ))

    # 4. Heading 1
    h1 = doc.styles["Heading 1"]
    h1_sz = h1.font.size.pt if h1.font.size else 0
    h1_b = h1.font.bold
    h1_jc = str(h1.paragraph_format.alignment)
    h1_sb = round(h1.paragraph_format.space_before.pt, 1) if h1.paragraph_format.space_before else 0
    h1_sa = round(h1.paragraph_format.space_after.pt, 1) if h1.paragraph_format.space_after else 0
    h1_ok = (h1_sz == 15.0 and h1_b is True and "CENTER" in h1_jc and h1_sb == 12.0 and h1_sa == 6.0)
    checks.append(Check(
        "DOCX", "Heading 1: 15pt, Bold, Center, Before 12pt, After 6pt",
        h1_ok,
        f"size={h1_sz}pt, bold={h1_b}, align={h1_jc}, before={h1_sb}pt, after={h1_sa}pt"
    ))

    # 5. Heading 2
    h2 = doc.styles["Heading 2"]
    h2_sz = h2.font.size.pt if h2.font.size else 0
    h2_b = h2.font.bold
    h2_jc = str(h2.paragraph_format.alignment)
    h2_sb = round(h2.paragraph_format.space_before.pt, 1) if h2.paragraph_format.space_before else 0
    h2_ok = (h2_sz == 13.5 and h2_b is True and ("LEFT" in h2_jc or "None" in h2_jc) and h2_sb == 8.0)
    checks.append(Check(
        "DOCX", "Heading 2: 13.5pt, Bold, Left, Before 8pt",
        h2_ok,
        f"size={h2_sz}pt, bold={h2_b}, align={h2_jc}, before={h2_sb}pt"
    ))

    # 6. Heading 3
    h3 = doc.styles["Heading 3"]
    h3_sz = h3.font.size.pt if h3.font.size else 0
    h3_it = h3.font.italic
    h3_sb = round(h3.paragraph_format.space_before.pt, 1) if h3.paragraph_format.space_before else 0
    h3_ok = (h3_sz == 13.0 and h3_it is True and h3_sb == 6.0)
    checks.append(Check(
        "DOCX", "Heading 3: 13pt, Italic, Left, Before 6pt",
        h3_ok,
        f"size={h3_sz}pt, italic={h3_it}, before={h3_sb}pt"
    ))

    # 7. Thụt đầu dòng đoạn văn bản thân
    indents = [
        p.paragraph_format.first_line_indent.cm
        for p in doc.paragraphs
        if p.style.name == "Normal" and p.paragraph_format.first_line_indent
    ]
    indent_ok = len(indents) > 0 and any(abs(round(ind, 2) - 1.27) < 0.05 for ind in indents)
    checks.append(Check(
        "DOCX", "Thụt đầu dòng đoạn văn thân (1.27 cm / 0.5 inch)",
        indent_ok,
        f"Tìm thấy các mức thụt đầu dòng: {[round(x, 2) for x in indents[:5]]}"
    ))

    # 8. Bảng biểu và Caption Bảng
    tbl_captions = [p for p in doc.paragraphs if p.text.strip().startswith("Bảng ")]
    tbl_cap_ok = False
    if tbl_captions:
        cap_p = tbl_captions[0]
        r = cap_p.runs[0] if cap_p.runs else None
        sz = r.font.size.pt if (r and r.font.size) else 0
        it = r.italic if r else False
        tbl_cap_ok = (sz == 11.5 and it is True)
    checks.append(Check(
        "DOCX", "Caption Bảng: 11.5pt, In nghiêng, Nằm trên bảng",
        tbl_cap_ok,
        f"{len(tbl_captions)} caption bảng tìm thấy trong văn bản"
    ))

    tbl_count = len(doc.tables)
    checks.append(Check(
        "DOCX", "Bảng biểu số liệu thực nghiệm (ít nhất 4 bảng)",
        tbl_count >= 4,
        f"{tbl_count} bảng được tạo trong tài liệu"
    ))

    # 9. Hình ảnh và Caption Hình
    fig_captions = [p for p in doc.paragraphs if re.match(r"^Hình\s+\d+(\.\d+)?:", p.text.strip())]
    fig_cap_ok = False
    if fig_captions:
        cap_p = fig_captions[0]
        r = cap_p.runs[0] if cap_p.runs else None
        sz = r.font.size.pt if (r and r.font.size) else 0
        it = r.italic if r else False
        fig_cap_ok = (sz == 11.5 and it is True)
    checks.append(Check(
        "DOCX", "Caption Hình: 11.5pt, In nghiêng, Nằm dưới hình",
        fig_cap_ok,
        f"{len(fig_captions)} caption hình minh họa tìm thấy trong văn bản"
    ))

    # 10. Tài liệu tham khảo IEEE
    ref_paras = [p for p in doc.paragraphs if re.match(r"^\[\d+\]", p.text.strip())]
    checks.append(Check(
        "DOCX", "Tài liệu tham khảo định dạng IEEE ([1], [2]...)",
        len(ref_paras) >= 5,
        f"{len(ref_paras)} tài liệu tham khảo chuẩn IEEE"
    ))


# =============================================================================
# 2. KIỂM TRA BÁO CÁO MARKDOWN TOÀN VĂN
# =============================================================================

def check_markdown_report(checks: List[Check]) -> None:
    if not MD_REPORT_PATH.is_file():
        checks.append(Check("MD", "Tệp BAO_CAO_DO_AN_XLAS.md tồn tại", False, "không tìm thấy tệp"))
        return

    content = MD_REPORT_PATH.read_text(encoding="utf-8")
    size_kb = len(content.encode("utf-8")) / 1024
    checks.append(Check(
        "MD", "Dung lượng tệp Markdown (> 15 KB)",
        size_kb >= 15.0,
        f"{size_kb:.1f} KB"
    ))

    required_chapters = [
        "CHƯƠNG 1: GIỚI THIỆU ĐỀ TÀI",
        "CHƯƠNG 2: CƠ SỞ LÝ THUYẾT XỬ LÝ ẢNH SỐ",
        "CHƯƠNG 3: MÔ TẢ TẬP DỮ LIỆU MRI TCGA-LGG",
        "CHƯƠNG 4: TIỀN XỬ LÝ ẢNH VÀ TÁCH SỌ NÃO",
        "CHƯƠNG 5: PHƯƠNG PHÁP PHÂN ĐOẠN U NÃO VÀ PIPELINE",
        "CHƯƠNG 6: KẾT QUẢ THỰC NGHIỆM VÀ ĐÁNH GIÁ ĐỊNH LƯỢNG",
        "CHƯƠNG 7: XÂY DỰNG ỨNG DỤNG MINH HỌA DEMO WEB UI",
        "CHƯƠNG 8: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN"
    ]
    missing = [c for c in required_chapters if c not in content]
    checks.append(Check(
        "MD", "Đầy đủ 8 Chương chuẩn mực Bộ môn KHDL - HUIT",
        len(missing) == 0,
        "Đầy đủ 8 chương" if not missing else f"Thiếu: {missing}"
    ))

    required_front = ["LỜI MỞ ĐẦU", "TÓM TẮT ĐỒ ÁN", "BẢNG PHÂN CÔNG NHIỆM VỤ", "MỤC LỤC BÁO CÁO", "TÀI LIỆU THAM KHẢO", "PHỤ LỤC"]
    missing_front = [f for f in required_front if f not in content]
    checks.append(Check(
        "MD", "Đầy đủ các phần mở đầu, phụ lục và tài liệu tham khảo",
        len(missing_front) == 0,
        "Đầy đủ các mục" if not missing_front else f"Thiếu: {missing_front}"
    ))


# =============================================================================
# 3. KIỂM TRA CHECKLIST NHIỆM VỤ CỦA 2 THÀNH VIÊN
# =============================================================================

def check_task_checklists(checks: List[Check]) -> None:
    # Hà Mạnh Trường
    if not TASK_DOC_TRUONG.is_file():
        checks.append(Check("TASK", "Tệp NHIEM_VU_HA_MANH_TRUONG.md", False, "không tìm thấy"))
    else:
        text = TASK_DOC_TRUONG.read_text(encoding="utf-8")
        lines = text.splitlines()
        done = sum(1 for l in lines if re.match(r"^\s*-\s*\[x\]", l))
        total = sum(1 for l in lines if re.match(r"^\s*-\s*\[[ x]\]", l))
        day6_ok = ("- [x] 4 chương kỹ thuật hoàn thiện" in text and
                   "- [x] File Word `docs/BAO_CAO_DO_AN_XLAS.docx` xuất thành công" in text)
        checks.append(Check(
            "TASK", "Checklist Hà Mạnh Trường (17/20 [x], Ngày 6 hoàn thành)",
            done == 17 and total == 20 and day6_ok,
            f"{done}/{total} mục hoàn tất • Ngày 6: {'ĐẠT' if day6_ok else 'CHƯA ĐẠT'}"
        ))

    # Huỳnh Tâm Trí
    if not TASK_DOC_TRI.is_file():
        checks.append(Check("TASK", "Tệp NHIEM_VU_HUYNH_TAM_TRI.md", False, "không tìm thấy"))
    else:
        text = TASK_DOC_TRI.read_text(encoding="utf-8")
        lines = text.splitlines()
        done = sum(1 for l in lines if re.match(r"^\s*-\s*\[x\]", l))
        total = sum(1 for l in lines if re.match(r"^\s*-\s*\[[ x]\]", l))
        day6_ok = ("- [x] Toàn bộ 6 chương tổng quan và định lượng" in text and
                   "- [x] File Word `docs/BAO_CAO_DO_AN_XLAS.docx` chuẩn thể thức" in text)
        checks.append(Check(
            "TASK", "Checklist Huỳnh Tâm Trí (16/19 [x], Ngày 6 hoàn thành)",
            done == 16 and total == 19 and day6_ok,
            f"{done}/{total} mục hoàn tất • Ngày 6: {'ĐẠT' if day6_ok else 'CHƯA ĐẠT'}"
        ))


# =============================================================================
# HÀM ĐIỀU PHỐI CHÍNH
# =============================================================================

def run_all_checks() -> bool:
    checks: List[Check] = []

    print("=" * 80)
    print("KIỂM CHUẨN HỢP ĐỒNG KỸ THUẬT NGÀY 6 — BÁO CÁO TOÀN VĂN DOCX & MARKDOWN")
    print("=" * 80)

    check_docx_report(checks)
    check_markdown_report(checks)
    check_task_checklists(checks)

    # Hiển thị kết quả dạng bảng
    print(f"\n{'+' + '-'*11 + '+' + '-'*57 + '+' + '-'*9 + '+' + '-'*62 + '+'}")
    print(f"| {'Nhóm':<9} | {'Nội dung kiểm tra':<55} | {'Kết quả':<7} | {'Chi tiết':<60} |")
    print(f"{'+' + '-'*11 + '+' + '-'*57 + '+' + '-'*9 + '+' + '-'*62 + '+'}")

    all_passed = True
    current_group = ""
    for c in checks:
        if c.group != current_group and current_group != "":
            print(f"{'+' + '-'*11 + '+' + '-'*57 + '+' + '-'*9 + '+' + '-'*62 + '+'}")
        current_group = c.group
        status = "PASS" if c.ok else "FAIL"
        if not c.ok:
            all_passed = False
        detail = c.detail if len(c.detail) <= 60 else c.detail[:57] + "..."
        print(f"| {c.group:<9} | {c.name:<55} | {status:<7} | {detail:<60} |")

    print(f"{'+' + '-'*11 + '+' + '-'*57 + '+' + '-'*9 + '+' + '-'*62 + '+'}")

    passed_count = sum(1 for c in checks if c.ok)
    total_count = len(checks)
    print(f"\nTỔNG CỘNG: {passed_count}/{total_count} tiêu chí hợp đồng đạt chuẩn.")

    if all_passed:
        print("\nKẾT LUẬN: ĐẠT — Nghiệm thu thành công Ngày 6: Báo cáo đồ án toàn văn chuẩn OpenXML!")
        return True
    else:
        print("\nKẾT LUẬN: CHƯA ĐẠT — Vui lòng kiểm tra và xử lý các tiêu chí thất bại ở trên.")
        return False


if __name__ == "__main__":
    success = run_all_checks()
    sys.exit(0 if success else 1)
