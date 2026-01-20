#!/usr/bin/env python3
"""
🍍 Pineapple Resume Generator
A sweet and tart resume generator that converts Markdown to beautiful PDF resumes.
"""

import sys
import argparse
import re
from pathlib import Path
from typing import Dict, List
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

# Get the directory where this script is located for font paths
_SCRIPT_DIR = Path(__file__).parent

# Register Atkinson Hyperlegible Next font family
def _register_fonts():
    """Register custom fonts with ReportLab."""
    font_dir = _SCRIPT_DIR / 'fonts'
    
    pdfmetrics.registerFont(TTFont(
        'AtkinsonHyperlegible', 
        str(font_dir / 'AtkinsonHyperlegibleNext-Regular.ttf')
    ))
    pdfmetrics.registerFont(TTFont(
        'AtkinsonHyperlegible-Bold', 
        str(font_dir / 'AtkinsonHyperlegibleNext-Bold.ttf')
    ))
    pdfmetrics.registerFont(TTFont(
        'AtkinsonHyperlegible-Italic', 
        str(font_dir / 'AtkinsonHyperlegibleNext-Italic.ttf')
    ))
    pdfmetrics.registerFont(TTFont(
        'AtkinsonHyperlegible-BoldItalic', 
        str(font_dir / 'AtkinsonHyperlegibleNext-BoldItalic.ttf')
    ))
    
    # Register font family for automatic bold/italic handling in markup
    registerFontFamily(
        'AtkinsonHyperlegible',
        normal='AtkinsonHyperlegible',
        bold='AtkinsonHyperlegible-Bold',
        italic='AtkinsonHyperlegible-Italic',
        boldItalic='AtkinsonHyperlegible-BoldItalic'
    )

# Register fonts at module load time
_register_fonts()


class ResumeGenerator:
    """Generate beautiful, modern PDF resumes from Markdown."""

    def __init__(self, markdown_file: Path, output_file: Path = None):
        self.markdown_file = markdown_file
        self.output_file = output_file or markdown_file.with_suffix('.pdf')
        self.styles = self._create_styles()
        
    # Color palette for consistent styling
    COLORS = {
        'primary': '#1a1a1a',      # Near-black for main text
        'secondary': '#333333',     # Dark gray for secondary text
        'accent': '#2563eb',        # Blue accent for section underlines
        'link': '#0056b3',          # Accessible blue for links (7.5:1 contrast)
    }

    def _create_styles(self) -> Dict:
        """Create custom styles for the resume."""
        base_styles = getSampleStyleSheet()
        
        styles = {
            'Title': ParagraphStyle(
                'CustomTitle',
                parent=base_styles['Title'],
                fontSize=24,
                textColor=colors.HexColor(self.COLORS['primary']),
                spaceAfter=6,
                alignment=TA_CENTER,
                fontName='AtkinsonHyperlegible-Bold',
            ),
            'Subtitle': ParagraphStyle(
                'CustomSubtitle',
                parent=base_styles['Normal'],
                fontSize=11,
                textColor=colors.HexColor(self.COLORS['secondary']),
                spaceAfter=12,
                alignment=TA_CENTER,
                fontName='AtkinsonHyperlegible',
                linkUnderline=True,
            ),
            'Heading1': ParagraphStyle(
                'CustomHeading1',
                parent=base_styles['Heading1'],
                fontSize=13,
                textColor=colors.HexColor(self.COLORS['primary']),
                spaceAfter=4,
                spaceBefore=16,
                fontName='AtkinsonHyperlegible-Bold',
                textTransform='uppercase',
            ),
            'Heading2': ParagraphStyle(
                'CustomHeading2',
                parent=base_styles['Heading2'],
                fontSize=11,
                textColor=colors.HexColor(self.COLORS['primary']),
                spaceAfter=4,
                spaceBefore=8,
                fontName='AtkinsonHyperlegible-Bold',
            ),
            'Normal': ParagraphStyle(
                'CustomNormal',
                parent=base_styles['Normal'],
                fontSize=10,
                textColor=colors.HexColor(self.COLORS['primary']),
                spaceAfter=6,
                fontName='AtkinsonHyperlegible',
                leading=14,
                linkUnderline=True,
            ),
            'Bullet': ParagraphStyle(
                'CustomBullet',
                parent=base_styles['Normal'],
                fontSize=10,
                textColor=colors.HexColor(self.COLORS['primary']),
                leftIndent=20,
                spaceAfter=4,
                fontName='AtkinsonHyperlegible',
                bulletIndent=10,
                leading=13,
                linkUnderline=True,
            ),
            'Contact': ParagraphStyle(
                'CustomContact',
                parent=base_styles['Normal'],
                fontSize=10,
                textColor=colors.HexColor(self.COLORS['secondary']),
                alignment=TA_CENTER,
                spaceAfter=2,
                fontName='AtkinsonHyperlegible',
                linkUnderline=True,
            ),
        }
        
        return styles

    def parse_markdown(self) -> List:
        """Parse markdown file and convert to PDF elements."""
        with open(self.markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        elements = []
        lines = content.split('\n')
        i = 0
        in_list = False
        
        while i < len(lines):
            line = lines[i].strip()
            
            # Skip empty lines but add small spacer
            if not line:
                if in_list:
                    in_list = False
                i += 1
                continue
            
            # Title (# heading at start or standalone bold text)
            if line.startswith('# '):
                text = line[2:].strip()
                elements.append(Paragraph(text, self.styles['Title']))
                in_list = False
                
            # Contact info or subtitle (lines right after title)
            elif i > 0 and not line.startswith('#') and not line.startswith('*') and not line.startswith('-') and len(elements) <= 3:
                # Clean up common markdown link syntax for display
                text = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', line)
                elements.append(Paragraph(text, self.styles['Contact']))
                
            # Heading 2 (## heading) - Section headers with underline
            elif line.startswith('## '):
                text = line[3:].strip()
                elements.append(Spacer(1, 0.1*inch))
                elements.append(Paragraph(text, self.styles['Heading1']))
                # Add thin accent-colored rule beneath section header
                elements.append(HRFlowable(
                    width='100%',
                    thickness=1.5,
                    color=colors.HexColor(self.COLORS['accent']),
                    spaceAfter=8,
                    spaceBefore=2,
                ))
                in_list = False
                
            # Heading 3 (### heading)
            elif line.startswith('### '):
                text = line[4:].strip()
                elements.append(Paragraph(text, self.styles['Heading2']))
                in_list = False
                
            # Bold standalone line (job title, degree, etc.)
            elif line.startswith('**') and line.endswith('**'):
                text = line[2:-2]
                elements.append(Paragraph(f'<b>{text}</b>', self.styles['Normal']))
                in_list = False
                
            # Bullet point or list item
            elif line.startswith('- ') or line.startswith('* '):
                text = line[2:].strip()
                # Handle nested markdown (bold, italic, links)
                text = self._process_inline_markdown(text)
                elements.append(Paragraph(f'• {text}', self.styles['Bullet']))
                in_list = True
                
            # Regular paragraph
            else:
                # Process inline markdown
                text = self._process_inline_markdown(line)
                elements.append(Paragraph(text, self.styles['Normal']))
                in_list = False
            
            i += 1
        
        return elements

    def _process_inline_markdown(self, text: str) -> str:
        """Process inline markdown formatting (bold, italic, links)."""
        # Links: [text](url) -> <a href="url">text</a> with accessible link color
        link_color = self.COLORS['link']
        text = re.sub(
            r'\[([^\]]+)\]\(([^\)]+)\)', 
            rf'<a href="\2" color="{link_color}">\1</a>', 
            text
        )
        
        # Bold: **text** or __text__ -> <b>text</b>
        # Process double markers first to avoid conflicts with single markers
        text = re.sub(r'\*\*([^\*]+)\*\*', r'<b>\1</b>', text)
        text = re.sub(r'__([^_]+)__', r'<b>\1</b>', text)
        
        # Italic: *text* or _text_ -> <i>text</i>
        # Use negative lookahead/lookbehind to avoid matching double markers
        text = re.sub(r'(?<!\*)\*(?!\*)([^\*]+)\*(?!\*)', r'<i>\1</i>', text)
        text = re.sub(r'(?<!_)_(?!_)([^_]+)_(?!_)', r'<i>\1</i>', text)
        
        # Code: `text` -> <font face="Courier">text</font>
        text = re.sub(r'`([^`]+)`', r'<font face="Courier" color="#c7254e">\1</font>', text)
        
        return text

    def generate_pdf(self):
        """Generate the PDF resume."""
        # Create PDF document
        doc = SimpleDocTemplate(
            str(self.output_file),
            pagesize=letter,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch,
            leftMargin=0.75*inch,
            rightMargin=0.75*inch,
        )
        
        # Parse markdown and get elements
        elements = self.parse_markdown()
        
        # Build PDF
        doc.build(elements)
        print(f"✅ Resume generated successfully: {self.output_file}")


def main():
    """Main entry point for the resume generator."""
    parser = argparse.ArgumentParser(
        description='🍍 Pineapple Resume Generator - Convert Markdown to beautiful PDF resumes',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python pineapple.py resume.md
  python pineapple.py resume.md -o john_doe_resume.pdf
  python pineapple.py --help

For more information, visit: https://github.com/pid1/pineapple
        """
    )
    
    parser.add_argument(
        'markdown_file',
        type=Path,
        help='Input Markdown resume file'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=Path,
        help='Output PDF file (default: same name as input with .pdf extension)'
    )
    
    args = parser.parse_args()
    
    # Validate input file exists
    if not args.markdown_file.exists():
        print(f"❌ Error: File '{args.markdown_file}' not found", file=sys.stderr)
        sys.exit(1)
    
    # Generate resume
    try:
        generator = ResumeGenerator(args.markdown_file, args.output)
        generator.generate_pdf()
    except Exception as e:
        print(f"❌ Error generating resume: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
