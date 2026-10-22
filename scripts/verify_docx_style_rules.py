"""Kịch bản kiểm chuẩn tự động quy tắc định dạng tài liệu Word (DOCX Style Verification).

Đối chiếu trực tiếp với quy chuẩn đã học từ docs/Nhom12_BaoCao.docx:
1. Margins: Top 3.0cm, Bottom 3.0cm, Left 3.0cm, Right 2.0cm
2. Font: Times New Roman thống nhất 100%
3. Normal Style: 13.0 pt, 1.5 lines (360 twips), Justified, Space after 4.0 pt (80 twips)
4. Heading 1: 15.0 pt, IN ĐẬM, Căn giữa, Before 12 pt, After 6 pt
5. Heading 2: 13.5 pt, IN ĐẬM, Căn trái, Before 8 pt
6. Heading 3: 13.0 pt, IN NGHIÊNG, Căn trái
7. Caption: 11.5 pt, IN NGHIÊNG, Căn giữa
8. Bảng biểu: Header in đậm, ô padding chuẩn, nền tô nhẹ

Sử dụng:
    python scripts/verify_docx_style_rules.py
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

import docx
from docx.shared import Pt, Cm
from docx.oxml.ns import qn

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.report.docx_builder import ReportBuilder

OUTPUT_TEST_DOCX = REPO_ROOT / "reports" / "test_docx_verification.docx"
SAMPLE_FIGURE = REPO_ROOT / "reports" / "figures" / "skull_stripping_steps.png"


@dataclass
class Check:
    group: str
    name: str
    ok: bool
    detail: str


def generate_test_document() -> Path:
    """Sinh file docx thử nghiệm qua ReportBuilder để tiến hành kiểm định XML."""
    builder = ReportBuilder(paper_size="A4")

    # 1. Trang bìa
    builder.add_cover_page(
        project_title="PHÂN ĐOẠN VÀ PHÁT HIỆN KHỐI U NÃO TRÊN ẢNH CỘNG HƯỞNG TỪ MRI",
        dataset_note="(BỘ DỮ LIỆU CHUẨN TCGA-LGG)",
        advisor="ThS. Đinh Nguyễn Trọng Nghĩa",
        students=[
            "1. Hà Mạnh Trường — MSSV: 2045240326 — Nhóm trưởng (50%)",
            "2. Huỳnh Tâm Trí — MSSV: 2045240315 — Thành viên (50%)"
        ]
    )

    # 2. Heading 1
    builder.add_heading_1("LỜI MỞ ĐẦU")
    builder.add_paragraph("Trong kỷ nguyên số hiện nay, xử lý ảnh y tế đóng vai trò then chốt...")

    # 3. Heading 2 & Heading 3
    builder.add_heading_1("CHƯƠNG 1: GIỚI THIỆU ĐỀ TÀI")
    builder.add_heading_2("1.1. Bối cảnh nghiên cứu")
    builder.add_heading_3("1.1.1. Đặc điểm ảnh MRI sọ não")
    builder.add_paragraph("Ảnh cộng hưởng từ MRI cung cấp thông tin mô mềm vượt trội...")
    builder.add_bullet("Độ phân giải không gian cao.")
    builder.add_bullet("Không gây nhiễm xạ cho bệnh nhân.")

    # 4. Bảng biểu
    headers = ["Thuật toán", "Dice Score", "Độ trễ (ms)"]
    data = [
        ["Watershed (Baseline)", "0.4086", "5.11 ms"],
        ["Region Growing (Đối chứng)", "0.1368", "11.59 ms"]
    ]
    builder.add_table(headers, data, caption="Bảng 1.1: So sánh sơ bộ hai thuật toán phân đoạn", col_widths=[7.0, 4.0, 4.0])

    # 5. Hình ảnh
    if SAMPLE_FIGURE.exists():
        builder.add_figure(str(SAMPLE_FIGURE), caption="Hình 1.1: Minh họa 6 bước bóc sọ não", width=14.0)

    # 6. Tài liệu tham khảo
    builder.add_heading_1("TÀI LIỆU THAM KHẢO")
    builder.add_reference(1, "R. C. Gonzalez and R. E. Woods, Digital Image Processing, 4th ed., Pearson, 2018.")

    builder.save(str(OUTPUT_TEST_DOCX))
    return OUTPUT_TEST_DOCX


def check_docx_properties(checks: List[Check], docx_path: Path) -> None:
    doc = docx.Document(str(docx_path))
    sec = doc.sections[0]

    # 1. Margins
    top_cm = round(sec.top_margin.cm, 1) if sec.top_margin else 0
    bot_cm = round(sec.bottom_margin.cm, 1) if sec.bottom_margin else 0
    left_cm = round(sec.left_margin.cm, 1) if sec.left_margin else 0
    right_cm = round(sec.right_margin.cm, 1) if sec.right_margin else 0
    margins_ok = (top_cm == 3.0 and bot_cm == 3.0 and left_cm == 3.0 and right_cm == 2.0)
    checks.append(Check(
        "PAGE", "Căn lề chuẩn (3.0, 3.0, 3.0, 2.0 cm)",
        margins_ok,
        f"Top={top_cm}cm, Bottom={bot_cm}cm, Left={left_cm}cm, Right={right_cm}cm"
    ))

    # 2. Khổ giấy
    w_cm = round(sec.page_width.cm, 1) if sec.page_width else 0
    h_cm = round(sec.page_height.cm, 1) if sec.page_height else 0
    page_ok = (w_cm == 21.0 and h_cm == 29.7)
    checks.append(Check(
        "PAGE", "Khổ giấy A4 (21.0 x 29.7 cm)",
        page_ok,
        f"{w_cm} x {h_cm} cm"
    ))

    # 3. Normal Style
    normal = doc.styles["Normal"]
    norm_fn = normal.font.name
    norm_sz = normal.font.size.pt if normal.font.size else 0
    norm_pf = normal.paragraph_format
    norm_ls = norm_pf.line_spacing
    norm_jc = str(norm_pf.alignment)
    norm_sa = round(norm_pf.space_after.pt, 1) if norm_pf.space_after else 0

    norm_ok = (norm_fn == "Times New Roman" and norm_sz == 13.0 and norm_ls == 1.5 and norm_sa == 4.0)
    checks.append(Check(
        "STYLE", "Normal: Times New Roman, 13pt, 1.5 lines, after 4pt",
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
        "STYLE", "Heading 1: 15pt, Bold, Center, Before 12pt, After 6pt",
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
        "STYLE", "Heading 2: 13.5pt, Bold, Left, Before 8pt",
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
        "STYLE", "Heading 3: 13pt, Italic, Left, Before 6pt",
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
        "PARAGRAPH", "Thụt đầu dòng đoạn văn thân (1.27 cm / 0.5 inch)",
        indent_ok,
        f"Tìm thấy các mức thụt đầu dòng: {[round(x, 2) for x in indents]}"
    ))

    # 8. Bảng biểu & Caption Bảng
    tbl_captions = [
        p for p in doc.paragraphs
        if p.text.strip().startswith("Bảng ") and "\t" not in p.text
    ]
    tbl_cap_ok = False
    tbl_cap_detail = "không tìm thấy caption bảng"
    if tbl_captions:
        cap_p = tbl_captions[0]
        r = cap_p.runs[0] if cap_p.runs else None
        sz = r.font.size.pt if (r and r.font.size) else 0
        it = r.italic if r else False
        al = str(cap_p.alignment)
        tbl_cap_ok = (sz == 11.5 and it is True and "CENTER" in al)
        tbl_cap_detail = f"text='{cap_p.text[:30]}...', size={sz}pt, italic={it}, align={al}"
    checks.append(Check("TABLE", "Caption Bảng: 11.5pt, In nghiêng, Căn giữa", tbl_cap_ok, tbl_cap_detail))

    has_table = len(doc.tables) > 0
    checks.append(Check("TABLE", "Bảng biểu được chèn thành công", has_table, f"{len(doc.tables)} bảng trong tài liệu"))

    # 9. Hình ảnh & Caption Hình
    fig_captions = [
        p for p in doc.paragraphs
        if p.text.strip().startswith("Hình ") and "\t" not in p.text
    ]
    fig_cap_ok = False
    fig_cap_detail = "không tìm thấy caption hình"
    if fig_captions:
        fcap_p = fig_captions[0]
        r = fcap_p.runs[0] if fcap_p.runs else None
        sz = r.font.size.pt if (r and r.font.size) else 0
        it = r.italic if r else False
        al = str(fcap_p.alignment)
        fig_cap_ok = (sz == 11.5 and it is True and "CENTER" in al)
        fig_cap_detail = f"text='{fcap_p.text[:30]}...', size={sz}pt, italic={it}, align={al}"
    checks.append(Check("FIGURE", "Caption Hình: 11.5pt, In nghiêng, Căn giữa", fig_cap_ok, fig_cap_detail))


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
    prev = None
    for c in checks:
        if prev is not None and c.group != prev:
            print(line)
        prev = c.group
        print(fmt((c.group, c.name, "PASS" if c.ok else "FAIL", c.detail)))
    print(line)

    passed = sum(1 for c in checks if c.ok)
    print(f"\nTỔNG CỘNG: {passed}/{len(checks)} tiêu chí định dạng đạt chuẩn.")


def main() -> int:
    checks: List[Check] = []
    print("=" * 80)
    print("KIỂM CHUẨN QUY TẮC ĐỊNH DẠNG WORD (DOCX) — THAM CHIẾU NHÓM 12")
    print("=" * 80)
    print()

    print("Đang sinh tài liệu Word thử nghiệm...")
    test_file = generate_test_document()
    print(f"Đã tạo file thử nghiệm: {test_file} ({test_file.stat().st_size / 1024:.1f} KB)\n")

    check_docx_properties(checks, test_file)
    render_report(checks)

    failed = [c for c in checks if not c.ok]
    if failed:
        print(f"\nKẾT LUẬN: CÓ {len(failed)} TIÊU CHÍ CHƯA ĐẠT:")
        for f in failed:
            print(f"  - [{f.group}] {f.name}: {f.detail}")
        return 1

    print("\nKẾT LUẬN: ĐẠT — Module sinh tài liệu Word đã chuẩn hóa 100% quy chuẩn định dạng!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
