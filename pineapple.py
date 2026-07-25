#!/usr/bin/env python3
"""
🍍 Pineapple Resume Generator
A sweet and tart resume generator that converts Markdown to beautiful PDF resumes.
"""

import sys
import argparse
import re
from pathlib import Path
from typing import Dict, List, Optional
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle,
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

_SCRIPT_DIR = Path(__file__).parent

# Page geometry
_LEFT_MARGIN   = 0.875 * inch
_RIGHT_MARGIN  = 0.875 * inch
_TOP_MARGIN    = 0.65  * inch
_BOTTOM_MARGIN = 0.65  * inch
# 8.5" letter minus both margins
_CONTENT_WIDTH = 8.5 * inch - _LEFT_MARGIN - _RIGHT_MARGIN


def _register_fonts():
    font_dir = _SCRIPT_DIR / 'fonts'
    pdfmetrics.registerFont(TTFont(
        'AtkinsonHyperlegible',
        str(font_dir / 'AtkinsonHyperlegibleNext-Regular.ttf'),
    ))
    pdfmetrics.registerFont(TTFont(
        'AtkinsonHyperlegible-Bold',
        str(font_dir / 'AtkinsonHyperlegibleNext-Bold.ttf'),
    ))
    pdfmetrics.registerFont(TTFont(
        'AtkinsonHyperlegible-Italic',
        str(font_dir / 'AtkinsonHyperlegibleNext-Italic.ttf'),
    ))
    pdfmetrics.registerFont(TTFont(
        'AtkinsonHyperlegible-BoldItalic',
        str(font_dir / 'AtkinsonHyperlegibleNext-BoldItalic.ttf'),
    ))
    registerFontFamily(
        'AtkinsonHyperlegible',
        normal='AtkinsonHyperlegible',
        bold='AtkinsonHyperlegible-Bold',
        italic='AtkinsonHyperlegible-Italic',
        boldItalic='AtkinsonHyperlegible-BoldItalic',
    )


_register_fonts()


class ResumeGenerator:
    """Generate beautiful, luxury PDF resumes from Markdown."""

    # Luxury warm-gold palette — deep accent on near-black body
    COLORS = {
        'primary':      '#1A1A1A',  # near-black body text
        'secondary':    '#4A4A4A',  # medium gray subtitles
        'muted':        '#6B6B6B',  # muted contact info
        'accent':       '#7A5C0A',  # deep warm gold — section headers
        'rule':         '#C4A853',  # lighter gold — rules / dividers
        'link':         '#1B4B8A',  # deep navy — hyperlinks
        'video_bg':     '#F9F6EE',  # warm cream — video card background
        'video_border': '#C4A853',  # gold — video card border
    }

    # Markdown section titles that trigger the video-card renderer
    _VIDEO_SECTION_KEYS = frozenset({
        'video introduction', 'introduction video',
        'video intro', 'intro video', 'watch introduction',
    })

    def __init__(self, markdown_file: Path, output_file: Optional[Path] = None):
        self.markdown_file = markdown_file
        self.output_file = output_file or markdown_file.with_suffix('.pdf')
        self.candidate_name: Optional[str] = None
        self.candidate_title: Optional[str] = None
        self.ai_metadata: Optional[str] = None
        self.styles = self._create_styles()

    def _create_styles(self) -> Dict:
        base = getSampleStyleSheet()
        C = self.COLORS

        return {
            'Title': ParagraphStyle(
                'CustomTitle',
                parent=base['Title'],
                fontSize=28,
                fontName='AtkinsonHyperlegible-Bold',
                textColor=colors.HexColor(C['primary']),
                alignment=TA_CENTER,
                spaceAfter=4,
                spaceBefore=0,
                leading=32,
                charSpace=1.0,
            ),
            'Subtitle': ParagraphStyle(
                'CustomSubtitle',
                parent=base['Normal'],
                fontSize=10.5,
                fontName='AtkinsonHyperlegible-Bold',
                textColor=colors.HexColor(C['accent']),
                textTransform='uppercase',
                alignment=TA_CENTER,
                spaceAfter=6,
                leading=15,
                charSpace=3.0,
            ),
            'Contact': ParagraphStyle(
                'CustomContact',
                parent=base['Normal'],
                fontSize=9,
                fontName='AtkinsonHyperlegible',
                textColor=colors.HexColor(C['muted']),
                alignment=TA_CENTER,
                spaceAfter=2,
                leading=13,
                linkUnderline=True,
            ),
            'Heading1': ParagraphStyle(
                'CustomHeading1',
                parent=base['Heading1'],
                fontSize=9,
                fontName='AtkinsonHyperlegible-Bold',
                textColor=colors.HexColor(C['accent']),
                textTransform='uppercase',
                charSpace=2.5,
                spaceAfter=2,
                spaceBefore=0,
                leading=12,
            ),
            'Heading2': ParagraphStyle(
                'CustomHeading2',
                parent=base['Heading2'],
                fontSize=11,
                fontName='AtkinsonHyperlegible-Bold',
                textColor=colors.HexColor(C['primary']),
                spaceAfter=2,
                spaceBefore=8,
                leading=14,
            ),
            'Normal': ParagraphStyle(
                'CustomNormal',
                parent=base['Normal'],
                fontSize=10,
                fontName='AtkinsonHyperlegible',
                textColor=colors.HexColor(C['primary']),
                spaceAfter=5,
                leading=14,
                linkUnderline=True,
            ),
            'Bullet': ParagraphStyle(
                'CustomBullet',
                parent=base['Normal'],
                fontSize=10,
                fontName='AtkinsonHyperlegible',
                textColor=colors.HexColor(C['primary']),
                leftIndent=16,
                spaceAfter=3,
                leading=13,
                bulletIndent=6,
                linkUnderline=True,
            ),
            'RoleDates': ParagraphStyle(
                'RoleDates',
                parent=base['Normal'],
                fontSize=9,
                fontName='AtkinsonHyperlegible',
                textColor=colors.HexColor(C['muted']),
                alignment=TA_RIGHT,
                leading=14,
            ),
            'RoleCompany': ParagraphStyle(
                'RoleCompany',
                parent=base['Normal'],
                fontSize=10,
                fontName='AtkinsonHyperlegible',
                textColor=colors.HexColor(C['secondary']),
                spaceAfter=4,
                leading=13,
            ),
            'Footer': ParagraphStyle(
                'Footer',
                parent=base['Normal'],
                fontSize=7.5,
                fontName='AtkinsonHyperlegible',
                textColor=colors.HexColor(C['muted']),
                alignment=TA_CENTER,
                charSpace=1.5,
            ),
            'VideoBody': ParagraphStyle(
                'VideoBody',
                parent=base['Normal'],
                fontSize=10,
                fontName='AtkinsonHyperlegible',
                textColor=colors.HexColor(C['secondary']),
                alignment=TA_CENTER,
                spaceAfter=4,
                leading=14,
                linkUnderline=True,
            ),
            'VideoCTA': ParagraphStyle(
                'VideoCTA',
                parent=base['Normal'],
                fontSize=11,
                fontName='AtkinsonHyperlegible-Bold',
                textColor=colors.HexColor(C['link']),
                alignment=TA_CENTER,
                leading=15,
                linkUnderline=True,
            ),
        }

    def parse_markdown(self) -> List:
        with open(self.markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()

        elements: List = []
        lines = content.split('\n')
        i = 0
        passed_first_section = False
        in_video_section = False
        video_body: List = []
        ai_lines: List[str] = []
        in_ai_block = False

        while i < len(lines):
            line = lines[i].strip()

            if not line:
                i += 1
                continue

            # ── Hidden AI metadata block  <!-- AI: ... --> ────────────────
            # Invisible to human readers; embedded in PDF Keywords metadata.
            if in_ai_block:
                if '-->' in line:
                    before = line[:line.index('-->')].strip()
                    if before:
                        ai_lines.append(before)
                    in_ai_block = False
                else:
                    ai_lines.append(line)
                i += 1
                continue

            if line.lower().startswith('<!-- ai'):
                in_ai_block = True
                after = re.sub(r'^<!--\s*ai\s*:?\s*', '', line, flags=re.IGNORECASE).strip()
                after = after.rstrip('-').rstrip('>').strip()
                if after:
                    ai_lines.append(after)
                if '-->' in line:
                    in_ai_block = False
                i += 1
                continue

            # ── Name (# heading) ──────────────────────────────────────────
            if line.startswith('# '):
                text = line[2:].strip()
                if not passed_first_section:
                    self.candidate_name = text
                    elements.append(Paragraph(text, self.styles['Title']))
                else:
                    elements.append(Paragraph(f'<b>{text}</b>', self.styles['Heading2']))

            # ── Section header (## heading) ───────────────────────────────
            elif line.startswith('## '):
                # Flush any pending video section
                if in_video_section:
                    elements.extend(self._render_video_section(video_body))
                    video_body = []
                    in_video_section = False

                # Thin centered gold divider closes the contact header block
                if not passed_first_section:
                    elements.append(Spacer(1, 0.07 * inch))
                    elements.append(HRFlowable(
                        width='30%',
                        thickness=0.75,
                        color=colors.HexColor(self.COLORS['rule']),
                        hAlign='CENTER',
                        spaceAfter=0.04 * inch,
                    ))
                    passed_first_section = True

                section_name = line[3:].strip()

                if section_name.lower() in self._VIDEO_SECTION_KEYS:
                    in_video_section = True
                else:
                    elements.append(Spacer(1, 0.06 * inch))
                    elements.append(Paragraph(section_name, self.styles['Heading1']))
                    elements.append(HRFlowable(
                        width='100%',
                        thickness=0.75,
                        color=colors.HexColor(self.COLORS['rule']),
                        spaceAfter=6,
                        spaceBefore=1,
                    ))

            # ── Sub-heading (### heading) ─────────────────────────────────
            elif line.startswith('### '):
                text = line[4:].strip()
                if in_video_section:
                    video_body.append(Paragraph(text, self.styles['VideoBody']))
                else:
                    # Look ahead: a "**Company** | Location | Dates" line right
                    # after a role heading renders as a structured role header
                    # with right-aligned dates.
                    j = i + 1
                    while j < len(lines) and not lines[j].strip():
                        j += 1
                    meta = lines[j].strip() if j < len(lines) else ''
                    role = self._try_role_header(text, meta)
                    if role is not None:
                        elements.extend(role)
                        i = j  # consume the company/dates line
                    else:
                        elements.append(Paragraph(text, self.styles['Heading2']))

            # ── Bold standalone line ──────────────────────────────────────
            elif line.startswith('**') and line.endswith('**'):
                text = line[2:-2]
                if in_video_section:
                    video_body.append(Paragraph(f'<b>{text}</b>', self.styles['VideoBody']))
                else:
                    elements.append(Paragraph(f'<b>{text}</b>', self.styles['Normal']))

            # ── Bullet point ──────────────────────────────────────────────
            elif line.startswith('- ') or line.startswith('* '):
                text = self._process_inline_markdown(line[2:].strip())
                bullet = f'<font color="{self.COLORS["rule"]}">•</font>'
                p = Paragraph(f'{bullet} {text}', self.styles['Bullet'])
                (video_body if in_video_section else elements).append(p)

            # ── Pre-section header (subtitle / contact info) ──────────────
            elif not passed_first_section:
                text = self._process_inline_markdown(line)
                # The line immediately after the name is the professional title
                if len(elements) == 1:
                    self.candidate_title = line
                    elements.append(Paragraph(text, self.styles['Subtitle']))
                else:
                    elements.append(Paragraph(text, self.styles['Contact']))

            # ── Regular paragraph ─────────────────────────────────────────
            else:
                text = self._process_inline_markdown(line)
                if in_video_section:
                    # A standalone link renders as a centered call-to-action
                    if re.fullmatch(r'\[[^\]]+\]\([^\)]+\)', line):
                        video_body.append(Paragraph(text, self.styles['VideoCTA']))
                    else:
                        video_body.append(Paragraph(text, self.styles['VideoBody']))
                else:
                    elements.append(Paragraph(text, self.styles['Normal']))

            i += 1

        # Flush any trailing video section
        if in_video_section and video_body:
            elements.extend(self._render_video_section(video_body))

        # Store collected AI metadata for embedding in PDF Keywords field
        if ai_lines:
            self.ai_metadata = ' '.join(ai_lines)

        return elements

    def _try_role_header(self, title: str, meta_line: str) -> Optional[List]:
        """Build a structured role header if meta_line looks like
        '**Company** | Location | Dates'. Returns None if it doesn't match."""
        if '|' not in meta_line or meta_line.startswith(('#', '- ', '* ')):
            return None

        parts = [p.strip() for p in meta_line.split('|')]
        if len(parts) < 2:
            return None
        # The last segment must look like a date range
        if not re.search(r'(19|20)\d{2}|Present|Current', parts[-1], re.IGNORECASE):
            return None

        dates = parts[-1]
        company = self._process_inline_markdown('  ·  '.join(parts[:-1]))

        row = Table(
            [[
                Paragraph(title, self.styles['Heading2']),
                Paragraph(dates, self.styles['RoleDates']),
            ]],
            colWidths=[_CONTENT_WIDTH * 0.70, _CONTENT_WIDTH * 0.30],
        )
        row.setStyle(TableStyle([
            ('LEFTPADDING',   (0, 0), (-1, -1), 0),
            ('RIGHTPADDING',  (0, 0), (-1, -1), 0),
            ('TOPPADDING',    (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ('VALIGN',        (0, 0), (-1, -1), 'BOTTOM'),
        ]))

        return [
            Spacer(1, 0.04 * inch),
            row,
            Paragraph(company, self.styles['RoleCompany']),
        ]

    def _render_video_section(self, body_elements: List) -> List:
        """Render the video introduction as a contained, centered cream card."""
        C = self.COLORS

        rows = [[el] for el in body_elements]

        card = Table(rows, colWidths=[_CONTENT_WIDTH])
        card.setStyle(TableStyle([
            ('BACKGROUND',    (0, 0),  (-1, -1), colors.HexColor(C['video_bg'])),
            ('LEFTPADDING',   (0, 0),  (-1, -1), 16),
            ('RIGHTPADDING',  (0, 0),  (-1, -1), 16),
            ('TOPPADDING',    (0, 0),  (0, 0),   12),
            ('TOPPADDING',    (0, 1),  (-1, -1), 6),
            ('BOTTOMPADDING', (0, -1), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0),  (-1, -2), 2),
            # Even gold border on all four sides — a self-contained box
            ('BOX',           (0, 0),  (-1, -1), 0.75, colors.HexColor(C['video_border'])),
        ]))

        return [
            Spacer(1, 0.06 * inch),
            Paragraph('Introduction Video', self.styles['Heading1']),
            HRFlowable(
                width='100%',
                thickness=0.75,
                color=colors.HexColor(C['rule']),
                spaceAfter=6,
                spaceBefore=1,
            ),
            card,
        ]

    def _process_inline_markdown(self, text: str) -> str:
        """Convert inline Markdown (links, bold, italic, code) to ReportLab XML."""
        lc = self.COLORS['link']
        text = re.sub(
            r'\[([^\]]+)\]\(([^\)]+)\)',
            rf'<a href="\2" color="{lc}">\1</a>',
            text,
        )
        text = re.sub(r'\*\*([^\*]+)\*\*', r'<b>\1</b>', text)
        text = re.sub(r'__([^_]+)__', r'<b>\1</b>', text)
        text = re.sub(r'(?<!\*)\*(?!\*)([^\*]+)\*(?!\*)', r'<i>\1</i>', text)
        text = re.sub(r'(?<!_)_(?!_)([^_]+)_(?!_)', r'<i>\1</i>', text)
        text = re.sub(r'`([^`]+)`', r'<font face="Courier" color="#6B6B6B">\1</font>', text)
        return text

    def _on_first_page(self, canvas, doc):
        """Set document language for screen readers and AI parsers."""
        from reportlab.pdfbase.pdfdoc import PDFString
        canvas._doc.Catalog.Lang = PDFString('en-US')

    def _on_later_pages(self, canvas, doc):
        """Draw a small identifying footer on continuation pages."""
        name = self.candidate_name or ''
        if not name:
            return
        canvas.saveState()
        canvas.setFont('AtkinsonHyperlegible', 7.5)
        canvas.setFillColor(colors.HexColor(self.COLORS['muted']))
        canvas.drawCentredString(
            letter[0] / 2,
            0.35 * inch,
            f'{name}  ·  Page {doc.page}',
        )
        canvas.restoreState()

    def generate_pdf(self):
        """Parse the Markdown then build and save the PDF."""
        elements = self.parse_markdown()

        subject = 'Professional Resume'
        if self.candidate_title:
            subject = f'Professional Resume — {self.candidate_title}'

        doc = SimpleDocTemplate(
            str(self.output_file),
            pagesize=letter,
            topMargin=_TOP_MARGIN,
            bottomMargin=_BOTTOM_MARGIN,
            leftMargin=_LEFT_MARGIN,
            rightMargin=_RIGHT_MARGIN,
            title=self.candidate_name or 'Resume',
            author=self.candidate_name or '',
            subject=subject,
            creator='Pineapple Resume Generator',
            keywords=self.ai_metadata or '',
        )
        doc.build(
            elements,
            onFirstPage=self._on_first_page,
            onLaterPages=self._on_later_pages,
        )
        print(f"✅ Resume generated successfully: {self.output_file}")


def main():
    parser = argparse.ArgumentParser(
        description='🍍 Pineapple Resume Generator - Convert Markdown to beautiful PDF resumes',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python pineapple.py resume.md
  python pineapple.py resume.md -o john_doe_resume.pdf
  python pineapple.py --help

For more information, visit: https://github.com/pid1/pineapple
        """,
    )
    parser.add_argument('markdown_file', type=Path, help='Input Markdown resume file')
    parser.add_argument(
        '-o', '--output',
        type=Path,
        help='Output PDF file (default: same name as input with .pdf extension)',
    )
    args = parser.parse_args()

    if not args.markdown_file.exists():
        print(f"❌ Error: File '{args.markdown_file}' not found", file=sys.stderr)
        sys.exit(1)

    try:
        generator = ResumeGenerator(args.markdown_file, args.output)
        generator.generate_pdf()
    except Exception as e:
        print(f"❌ Error generating resume: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
