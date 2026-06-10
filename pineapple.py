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
                fontSize=12,
                fontName='AtkinsonHyperlegible',
                textColor=colors.HexColor(C['secondary']),
                alignment=TA_CENTER,
                spaceAfter=4,
                leading=16,
                charSpace=1.5,
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
            'VideoBody': ParagraphStyle(
                'VideoBody',
                parent=base['Normal'],
                fontSize=10,
                fontName='AtkinsonHyperlegible',
                textColor=colors.HexColor(C['secondary']),
                spaceAfter=4,
                leading=14,
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

        while i < len(lines):
            line = lines[i].strip()

            if not line:
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
                target = video_body if in_video_section else elements
                target.append(Paragraph(text, self.styles['VideoBody' if in_video_section else 'Heading2']))

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
                p = Paragraph(f'• {text}', self.styles['Bullet'])
                (video_body if in_video_section else elements).append(p)

            # ── Pre-section header (subtitle / contact info) ──────────────
            elif not passed_first_section:
                text = self._process_inline_markdown(line)
                # The line immediately after the name is the professional title
                if len(elements) == 1:
                    elements.append(Paragraph(text, self.styles['Subtitle']))
                else:
                    elements.append(Paragraph(text, self.styles['Contact']))

            # ── Regular paragraph ─────────────────────────────────────────
            else:
                text = self._process_inline_markdown(line)
                if in_video_section:
                    video_body.append(Paragraph(text, self.styles['VideoBody']))
                else:
                    elements.append(Paragraph(text, self.styles['Normal']))

            i += 1

        # Flush any trailing video section
        if in_video_section and video_body:
            elements.extend(self._render_video_section(video_body))

        return elements

    def _render_video_section(self, body_elements: List) -> List:
        """Render the video introduction as a warm cream card with gold border."""
        C = self.COLORS

        rows = [[el] for el in body_elements]

        card = Table(rows, colWidths=[_CONTENT_WIDTH])
        card.setStyle(TableStyle([
            ('BACKGROUND',    (0, 0),  (-1, -1), colors.HexColor(C['video_bg'])),
            ('LEFTPADDING',   (0, 0),  (-1, -1), 14),
            ('RIGHTPADDING',  (0, 0),  (-1, -1), 14),
            ('TOPPADDING',    (0, 0),  (0, 0),   12),
            ('TOPPADDING',    (0, 1),  (-1, -1), 3),
            ('BOTTOMPADDING', (0, -1), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0),  (-1, -2), 2),
            ('LINEABOVE',  (0, 0),  (-1, 0),  2,   colors.HexColor(C['video_border'])),
            ('LINEBELOW',  (0, -1), (-1, -1), 0.5, colors.HexColor(C['video_border'])),
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

    def generate_pdf(self):
        """Parse the Markdown then build and save the PDF."""
        elements = self.parse_markdown()

        doc = SimpleDocTemplate(
            str(self.output_file),
            pagesize=letter,
            topMargin=_TOP_MARGIN,
            bottomMargin=_BOTTOM_MARGIN,
            leftMargin=_LEFT_MARGIN,
            rightMargin=_RIGHT_MARGIN,
            title=self.candidate_name or 'Resume',
            author=self.candidate_name or '',
            subject='Professional Resume',
            creator='Pineapple Resume Generator',
        )
        doc.build(elements)
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
