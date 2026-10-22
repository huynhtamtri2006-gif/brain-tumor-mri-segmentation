"""Module biên soạn và sinh báo cáo đồ án chuẩn Microsoft Word (.docx).

Tuân thủ nghiêm ngặt quy chuẩn định dạng trích xuất từ docs/Nhom12_BaoCao.docx:
- Font: Times New Roman thống nhất 100%.
- Căn lề: Top 3.0cm, Bottom 3.0cm, Left 3.0cm, Right 2.0cm.
- Normal: 13.0pt, 1.5 line spacing, Justified, space after 4pt.
- Heading 1: 15.0pt, IN HOA, IN ĐẬM, Center, space before 12pt, after 6pt.
- Heading 2: 13.5pt, Chữ thường, IN ĐẬM, Left, space before 8pt, after 0pt.
- Heading 3: 13.0pt, Chữ thường, IN NGHIÊNG, Left, space before 6pt, after 2pt.
- Bảng: Font 10.5-11.0pt, Header in đậm, Caption TRÊN bảng 11.5pt in nghiêng căn giữa.
- Hình: Căn giữa, Caption DƯỚI hình 11.5pt in nghiêng căn giữa.
"""

from __future__ import annotations

import os
import sys
from typing import List, Optional, Tuple, Any
import docx
from docx.shared import Cm, Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Cài đặt padding cho ô bảng (đơn vị dxa = 1/20 pt)."""
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def set_cell_shading(cell, color_hex="F2F2F2"):
    """Tô màu nền cho ô bảng."""
    tcPr = cell._element.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), color_hex)
    tcPr.append(shd)


def set_table_borders(table, color="B0B0B0", sz="4", val="single"):
    """Đặt đường viền mỏng, trang nhã cho toàn bộ bảng (kiểu APA/IEEE chuẩn mực)."""
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)


class ReportBuilder:
    """Lớp điều phối tạo tài liệu Word báo cáo đồ án chuẩn HUIT."""

    def __init__(self, paper_size: str = "A4"):
        self.doc = docx.Document()
        self._setup_page(paper_size)
        self._setup_styles()

    def _setup_page(self, paper_size: str):
        section = self.doc.sections[0]
        if paper_size.upper() == "LETTER":
            section.page_width = Cm(21.59)
            section.page_height = Cm(27.94)
        else:  # A4 mặc định
            section.page_width = Cm(21.0)
            section.page_height = Cm(29.7)

        # Căn lề chuẩn: Top 3.0cm, Bottom 3.0cm, Left 3.0cm, Right 2.0cm
        section.top_margin = Cm(3.0)
        section.bottom_margin = Cm(3.0)
        section.left_margin = Cm(3.0)
        section.right_margin = Cm(2.0)
        section.header_distance = Cm(1.27)
        section.footer_distance = Cm(1.27)

    def _setup_styles(self):
        # 1. Normal Style
        normal = self.doc.styles["Normal"]
        normal.font.name = "Times New Roman"
        normal.font.size = Pt(13.0)
        normal.font.color.rgb = RGBColor(0, 0, 0)
        pf = normal.paragraph_format
        pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        pf.line_spacing = 1.5
        pf.space_before = Pt(0)
        pf.space_after = Pt(4.0)

        # Đảm bảo thẻ XML rFonts có Times New Roman
        rPr = normal.element.get_or_add_rPr()
        rFonts = OxmlElement('w:rFonts')
        rFonts.set(qn('w:ascii'), 'Times New Roman')
        rFonts.set(qn('w:hAnsi'), 'Times New Roman')
        rFonts.set(qn('w:cs'), 'Times New Roman')
        rPr.append(rFonts)

        # 2. Heading 1
        h1 = self.doc.styles["Heading 1"]
        h1.font.name = "Times New Roman"
        h1.font.size = Pt(15.0)
        h1.font.bold = True
        h1.font.color.rgb = RGBColor(0, 0, 0)
        h1_pf = h1.paragraph_format
        h1_pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
        h1_pf.space_before = Pt(12.0)
        h1_pf.space_after = Pt(6.0)

        # 3. Heading 2
        h2 = self.doc.styles["Heading 2"]
        h2.font.name = "Times New Roman"
        h2.font.size = Pt(13.5)
        h2.font.bold = True
        h2.font.color.rgb = RGBColor(0, 0, 0)
        h2_pf = h2.paragraph_format
        h2_pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
        h2_pf.space_before = Pt(8.0)
        h2_pf.space_after = Pt(0.0)

        # 4. Heading 3
        h3 = self.doc.styles["Heading 3"]
        h3.font.name = "Times New Roman"
        h3.font.size = Pt(13.0)
        h3.font.bold = False
        h3.font.italic = True
        h3.font.color.rgb = RGBColor(0, 0, 0)
        h3_pf = h3.paragraph_format
        h3_pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
        h3_pf.space_before = Pt(6.0)
        h3_pf.space_after = Pt(2.0)

    def add_cover_page(
        self,
        university: str = "TRƯỜNG ĐẠI HỌC CÔNG THƯƠNG TP. HỒ CHÍ MINH",
        faculty: str = "KHOA CÔNG NGHỆ THÔNG TIN",
        department: str = "BỘ MÔN KHOA HỌC DỮ LIỆU",
        course_type: str = "BÁO CÁO ĐỒ ÁN HỌC PHẦN",
        course_name: str = "XỬ LÝ ẢNH SỐ",
        project_label: str = "ĐỀ TÀI",
        project_title: str = "PHÂN ĐOẠN VÀ PHÁT HIỆN KHỐI U NÃO TRÊN ẢNH CỘNG HƯỞNG TỪ MRI",
        dataset_note: str = "(BỘ DỮ LIỆU CHUẨN TCGA-LGG)",
        advisor: str = "ThS. Đinh Nguyễn Trọng Nghĩa",
        students: Optional[List[str]] = None,
        city_year: str = "TP. Hồ Chí Minh, Năm 2026"
    ):
        """Sinh trang bìa chuẩn mẫu khoa học kỹ thuật của Trường ĐH Công Thương TP.HCM."""
        if students is None:
            students = [
                "1. Hà Mạnh Trường — MSSV: 2045240326 — Nhóm trưởng (50%)",
                "2. Huỳnh Tâm Trí — MSSV: 2045240315 — Thành viên (50%)"
            ]

        def _p(text, size=13.0, bold=False, italic=False, space_after=6.0):
            p = self.doc.add_paragraph()
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(space_after)
            r = p.add_run(text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(size)
            r.bold = bold
            r.italic = italic
            return p

        _p(university, size=15.0, bold=True, space_after=6.0)
        _p(faculty, size=14.0, bold=True, space_after=6.0)
        _p(department, size=14.0, bold=True, space_after=18.0)

        _p(course_type, size=13.0, bold=False, space_after=4.0)
        _p(course_name, size=14.0, bold=True, space_after=24.0)

        _p(project_label, size=16.0, bold=True, space_after=4.0)
        _p(project_title, size=16.0, bold=True, space_after=6.0)
        _p(dataset_note, size=13.0, italic=True, space_after=36.0)

        _p(f"Giảng viên hướng dẫn: {advisor}", size=13.0, space_after=18.0)

        _p("Sinh viên thực hiện:", size=13.0, bold=True, space_after=6.0)
        for st in students:
            _p(st, size=13.0, bold=False, space_after=4.0)

        _p("", size=13.0, space_after=24.0)
        _p(city_year, size=13.0, bold=True, space_after=0.0)

        # Ngắt trang sau trang bìa
        self.doc.add_page_break()

    def add_page_break(self):
        """Thêm ngắt trang sang trang mới."""
        self.doc.add_page_break()

    def add_heading_1(self, text: str):
        """Thêm tiêu đề Heading 1 (Chương và mục lớn mở đầu)."""
        p = self.doc.add_paragraph(text.upper(), style="Heading 1")
        p.paragraph_format.first_line_indent = Cm(0)
        return p

    def add_heading_2(self, text: str):
        """Thêm tiêu đề Heading 2 (Tiểu mục cấp 1: X.Y)."""
        p = self.doc.add_paragraph(text, style="Heading 2")
        p.paragraph_format.first_line_indent = Cm(0)
        return p

    def add_heading_3(self, text: str):
        """Thêm tiêu đề Heading 3 (Tiểu mục cấp 2: X.Y.Z)."""
        p = self.doc.add_paragraph(text, style="Heading 3")
        p.paragraph_format.first_line_indent = Cm(0)
        return p

    def add_paragraph(
        self,
        text: str,
        indent: bool = True,
        bold_prefix: Optional[str] = None,
        italic: bool = False
    ):
        """Thêm đoạn văn bản thân (Body text)."""
        p = self.doc.add_paragraph(style="Normal")
        if indent:
            p.paragraph_format.first_line_indent = Cm(1.27)
        else:
            p.paragraph_format.first_line_indent = Cm(0)

        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.bold = True
            r_pre.font.name = "Times New Roman"
            r_pre.font.size = Pt(13.0)

        r = p.add_run(text)
        r.italic = italic
        r.font.name = "Times New Roman"
        r.font.size = Pt(13.0)
        return p

    def add_bullet(self, text: str, bold_prefix: Optional[str] = None):
        """Thêm danh sách dạng gạch đầu dòng."""
        p = self.doc.add_paragraph(style="Normal")
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.left_indent = Cm(1.27)
        r_bullet = p.add_run("• ")
        r_bullet.bold = True
        r_bullet.font.name = "Times New Roman"
        r_bullet.font.size = Pt(13.0)

        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.bold = True
            r_pre.font.name = "Times New Roman"
            r_pre.font.size = Pt(13.0)

        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(13.0)
        return p

    def add_equation(self, latex_str: str, label: str = ""):
        """Thêm công thức toán học căn giữa trang."""
        p = self.doc.add_paragraph()
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(4.0)
        p.paragraph_format.space_after = Pt(6.0)
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.first_line_indent = Cm(0)

        added = False
        try:
            from math_equation import add_math
            add_math(p, latex_str)
            if label:
                r_lbl = p.add_run(f"    ({label})")
                r_lbl.font.name = "Times New Roman"
                r_lbl.font.size = Pt(13.0)
            added = True
        except Exception:
            pass

        if not added:
            txt = f"{latex_str}    ({label})" if label else latex_str
            r = p.add_run(txt)
            r.italic = True
            r.font.name = "Times New Roman"
            r.font.size = Pt(13.0)
        return p

    def add_table(
        self,
        headers: List[str],
        data: List[List[Any]],
        caption: Optional[str] = None,
        col_widths: Optional[List[float]] = None
    ):
        """Tạo bảng biểu chuẩn mực có Caption phía trên."""
        if caption:
            p_cap = self.doc.add_paragraph()
            p_cap.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(8.0)
            p_cap.paragraph_format.space_after = Pt(4.0)
            p_cap.paragraph_format.first_line_indent = Cm(0)
            r_cap = p_cap.add_run(caption)
            r_cap.font.name = "Times New Roman"
            r_cap.font.size = Pt(11.5)
            r_cap.italic = True

        table = self.doc.add_table(rows=len(data) + 1, cols=len(headers))
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(table)

        # Hàng tiêu đề
        hdr_row = table.rows[0]
        for col_idx, h_text in enumerate(headers):
            cell = hdr_row.cells[col_idx]
            cell.text = ""
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(3.0)
            p.paragraph_format.space_after = Pt(3.0)
            p.paragraph_format.first_line_indent = Cm(0)
            r = p.add_run(str(h_text))
            r.font.name = "Times New Roman"
            r.font.size = Pt(11.0)
            r.bold = True
            set_cell_margins(cell, top=120, bottom=120, left=120, right=120)
            set_cell_shading(cell, "EAEAEA")

        # Các hàng dữ liệu
        for row_idx, row_values in enumerate(data):
            row = table.rows[row_idx + 1]
            for col_idx, val in enumerate(row_values):
                cell = row.cells[col_idx]
                cell.text = ""
                p = cell.paragraphs[0]
                val_str = str(val)
                # Nếu là số hoặc phần trăm căn giữa, chữ căn trái
                if any(c.isdigit() for c in val_str) and len(val_str) <= 15:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                p.paragraph_format.space_before = Pt(2.5)
                p.paragraph_format.space_after = Pt(2.5)
                p.paragraph_format.first_line_indent = Cm(0)
                r = p.add_run(val_str)
                r.font.name = "Times New Roman"
                r.font.size = Pt(10.5)
                # Hàng tổng cộng hoặc cột đầu in đậm
                if col_idx == 0 and len(val_str) <= 10:
                    r.bold = True
                set_cell_margins(cell, top=80, bottom=80, left=100, right=100)

        # Chỉnh độ rộng cột nếu có
        if col_widths and len(col_widths) == len(headers):
            for row in table.rows:
                for idx, w in enumerate(col_widths):
                    row.cells[idx].width = Cm(w)

        # Thêm khoảng cách sau bảng
        p_after = self.doc.add_paragraph(style="Normal")
        p_after.paragraph_format.space_before = Pt(0)
        p_after.paragraph_format.space_after = Pt(6.0)
        p_after.paragraph_format.first_line_indent = Cm(0)
        return table

    def add_figure(self, image_path: str, caption: Optional[str] = None, width: float = 14.0):
        """Chèn hình ảnh căn giữa kèm chú thích Caption phía dưới."""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Không tìm thấy ảnh tại: {image_path}")

        p_img = self.doc.add_paragraph()
        p_img.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6.0)
        p_img.paragraph_format.space_after = Pt(2.0)
        p_img.paragraph_format.first_line_indent = Cm(0)
        r_img = p_img.add_run()
        r_img.add_picture(image_path, width=Cm(width))

        if caption:
            p_cap = self.doc.add_paragraph()
            p_cap.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(4.0)
            p_cap.paragraph_format.space_after = Pt(8.0)
            p_cap.paragraph_format.first_line_indent = Cm(0)
            r_cap = p_cap.add_run(caption)
            r_cap.font.name = "Times New Roman"
            r_cap.font.size = Pt(11.5)
            r_cap.italic = True

    def add_reference(self, index: int, text: str):
        """Thêm mục tài liệu tham khảo chuẩn IEEE ([1], [2]...)."""
        p = self.doc.add_paragraph(style="Normal")
        p.paragraph_format.first_line_indent = Cm(-0.75)
        p.paragraph_format.left_indent = Cm(0.75)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(3.0)
        r_idx = p.add_run(f"[{index}] ")
        r_idx.bold = True
        r_idx.font.name = "Times New Roman"
        r_idx.font.size = Pt(13.0)
        r_txt = p.add_run(text)
        r_txt.font.name = "Times New Roman"
        r_txt.font.size = Pt(13.0)
        return p

    def save(self, output_path: str):
        """Lưu tài liệu ra file .docx."""
        out_dir = os.path.dirname(output_path)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        self.doc.save(output_path)
