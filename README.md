# 🍍 Pineapple

A sweet and tart resume generator. Great on a pizza.

**Pineapple** is a minimalist Python 3.13 application that converts Markdown files into beautifully designed, modern PDF resumes that are easily parsable by AI tools and ATS systems.

## Features

- ✨ **Modern Design** - Clean, professional layout with thoughtful typography and spacing
- 🤖 **AI-Parsable** - Structured output optimized for AI tools and Applicant Tracking Systems
- 📝 **Markdown-based** - Write your resume in simple, readable Markdown
- 🚀 **Minimal Dependencies** - Only uses well-maintained, popular libraries (markdown, reportlab)
- 🔧 **Nix Environment** - Automated setup with shell.nix for reproducible builds

## Quick Start

### Prerequisites

- [Nix package manager](https://nixos.org/download.html) installed

### Setup

1. Clone the repository:
```bash
git clone https://github.com/pid1/pineapple.git
cd pineapple
```

2. Enter the Nix shell (this will automatically set up Python 3.13 and dependencies):
```bash
nix-shell
```

The shell will automatically:
- Set up Python 3.13
- Create a virtual environment
- Install required dependencies

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

- **Minimal Dependencies**: Uses only `markdown` for parsing and `reportlab` for PDF generation
- **Clean Code**: Simple, readable Python following best practices
- **Professional Output**: Modern color scheme (#2c3e50, #3498db) with proper spacing
- **AI-Friendly**: Structured text with semantic HTML tags for easy parsing

## Development

### Manual Setup (without Nix)

If you prefer not to use Nix:

```bash
# Create virtual environment
python3.13 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the generator
python pineapple.py example_resume.md
```

## Dependencies

- **markdown** (3.7) - Markdown parsing
- **reportlab** (4.2.5) - PDF generation

## License

BSD 3-Clause License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Why "Pineapple"?

Because just like pineapple on pizza, this resume generator is a delightful combination that some people love and others... well, they'll come around eventually. 🍍🍕
