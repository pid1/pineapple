# 🍍 Pineapple

A sweet and tart resume generator. Great on a pizza.

**Pineapple** is a minimalist Python 3.13 application that converts Markdown files into beautifully designed, modern PDF resumes that are easily parsable by AI tools and ATS systems.

## Features

- ♿ **Accessibility-First Design** - WCAG AA compliant colors and Atkinson Hyperlegible font
- 🤖 **ATS & AI Optimized** - Clean structure that parses perfectly in Applicant Tracking Systems
- 📝 **Markdown-Based** - Write your resume in simple, readable Markdown
- 🚀 **Minimal Dependencies** - Only uses well-maintained, popular libraries
- 🔧 **Nix Environment** - Automated setup with devenv for reproducible builds

## Why Pineapple Resumes Are Better

### ♿ Accessibility

Pineapple generates resumes that are readable by everyone:

- **Atkinson Hyperlegible Next Font** - Designed by the Braille Institute specifically for maximum legibility. Features distinctive letterforms that reduce confusion between similar characters (1/l/I, 0/O, etc.), making your resume readable for people with low vision or dyslexia.

- **WCAG AA Color Contrast** - All text meets or exceeds the Web Content Accessibility Guidelines minimum contrast ratio of 4.5:1. Primary text uses near-black (#1a1a1a) at 16:1 contrast, ensuring readability in any lighting condition.

- **Underlined Links** - Links are both colored AND underlined, following accessibility best practices. This ensures clickability is obvious to colorblind users and on mobile devices where hover states don't exist.

### 🤖 ATS & AI Scanning

Pineapple resumes are engineered for machines as much as humans:

- **Single-Column Layout** - No complex tables, columns, or graphics that confuse ATS parsers. Content flows top-to-bottom in a predictable structure.

- **Semantic Structure** - Clear hierarchy with properly tagged headings, making it trivial for AI tools to extract your name, contact info, experience, and skills.

- **Standard Section Names** - Uses conventional section titles (Experience, Education, Skills) that ATS systems are trained to recognize.

- **Plain Text Extraction** - The PDF structure allows perfect text extraction—no garbled characters or merged words that plague image-based or overly-designed resumes.

- **No Hidden Text or Keyword Stuffing** - Clean, honest formatting that won't trigger ATS spam filters.

## Quick Start

### Prerequisites

- [Nix package manager](https://nixos.org/download.html) installed
- [devenv](https://devenv.sh/getting-started/) installed

### Setup

1. Clone the repository:
```bash
git clone https://github.com/pid1/pineapple.git
cd pineapple
```

2. Enter the devenv shell (this will automatically set up Python 3.13 and dependencies):
```bash
devenv shell
```

### Usage

Generate a resume from a Markdown file:

```bash
python pineapple.py example_resume.md
```

Specify a custom output file:

```bash
python pineapple.py your_resume.md -o custom_name.pdf
```

Get help:

```bash
python pineapple.py --help
```

## Markdown Format

Your resume should be structured using Markdown with the following conventions:

### Header
```markdown
# Your Name

Title | email@example.com | (555) 123-4567
[LinkedIn](https://linkedin.com/in/username) | [GitHub](https://github.com/username) | Location
```

### Sections
```markdown
## Section Name

### Subsection or Job Title
**Company Name** | Location | Dates

- Bullet point with accomplishments
- Another achievement with **bold** and *italic* text
- Use `code` for technical terms
```

See `example_resume.md` for a complete example.

## Design Philosophy

- **Accessibility First**: Every design choice prioritizes readability and inclusivity
- **Minimal Dependencies**: Uses only `reportlab` for PDF generation
- **Clean Code**: Simple, readable Python following best practices
- **Professional Output**: Modern color palette with WCAG AA compliant contrast ratios
- **Machine Readable**: Semantic structure optimized for ATS and AI parsing

## License

BSD 3-Clause License - see [LICENSE](LICENSE) file for details.
