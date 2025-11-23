# Pineapple Resume Generator Agent Guide

This guide provides context and conventions for GitHub Copilot agents working on the Pineapple resume generator project.

## Project Overview

**Pineapple** is a Python 3.13 resume generator that converts Markdown files into beautifully designed, modern PDF resumes optimized for AI parsing and ATS systems.

### Key Design Principles

1. **Minimal Dependencies**: Use only well-maintained, popular libraries
2. **Clean Code**: Simple, readable Python following best practices
3. **Professional Output**: Modern color scheme with proper spacing
4. **AI-Friendly**: Structured text with semantic formatting for easy parsing
5. **Nix-First**: Development environment managed through shell.nix

## Project Structure

```
.
├── pineapple.py           # Main application (executable)
├── example_resume.md      # Example resume demonstrating format
├── example_resume.pdf     # Generated example (committed)
├── shell.nix              # Nix environment setup
├── requirements.txt       # Python dependencies
├── README.md              # User documentation
├── LICENSE                # BSD 3-Clause License
└── .gitignore            # Excludes .venv, *.pdf (except example*.pdf)
```

## Build and Test Commands

### Environment Setup

```bash
# Using Nix (recommended)
nix-shell  # Automatically sets up Python 3.13, venv, and installs dependencies

# Manual setup (without Nix)
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Testing the Application

```bash
# Activate virtual environment
source .venv/bin/activate

# Generate resume from example
python pineapple.py example_resume.md

# Test with custom output
python pineapple.py example_resume.md -o custom_name.pdf

# Test error handling
python pineapple.py nonexistent.md  # Should show error message

# Verify AI-parsability
pdftotext example_resume.pdf -  # Should output clean, structured text
```

### Validation Checklist

Before committing changes:
- [ ] Application runs without errors
- [ ] PDF is generated successfully
- [ ] Text extraction works (pdftotext)
- [ ] Help command works
- [ ] Error handling works for invalid inputs
- [ ] No security vulnerabilities (run codeql_checker)

## Dependencies

### Current Dependencies
- **markdown** (3.7) - Markdown parsing library
  - Used for: Reference only (we implement custom parsing)
  - Why: Standard, well-maintained library
  
- **reportlab** (4.2.5) - PDF generation
  - Used for: Creating PDF documents with custom styles
  - Why: Industry standard, actively maintained, no system dependencies

### Dependency Policy

- **DO** use well-maintained, popular libraries with active communities
- **DON'T** add dependencies for simple tasks that can be done in a few lines
- **CHECK** security advisories before adding new dependencies
- **PREFER** libraries that are pure Python (no C extensions unless necessary)

## Code Conventions

### Python Style

- **Python Version**: 3.13+ (but compatible with 3.12+)
- **Type Hints**: Use type hints for function signatures
- **Docstrings**: Include docstrings for classes and public methods
- **Imports**: Keep imports clean, remove unused imports
- **Line Length**: Aim for 88 characters (Black-compatible)

### Markdown Parsing

The application uses **custom regex-based markdown parsing** with the following important details:

#### Regex Pattern Order
```python
# Process in this order to avoid conflicts:
1. Links: [text](url)
2. Bold: **text** or __text__ (double markers)
3. Italic: *text* or _text_ (single markers with negative lookahead/lookbehind)
4. Code: `text`
```

#### Important Regex Pattern
```python
# Italic patterns use negative lookahead/lookbehind to avoid conflicts with bold
text = re.sub(r'(?<!\*)\*(?!\*)([^\*]+)\*(?!\*)', r'<i>\1</i>', text)
text = re.sub(r'(?<!_)_(?!_)([^_]+)_(?!_)', r'<i>\1</i>', text)
```

**Why**: Without the negative lookahead/lookbehind, patterns like `__bold__` could be incorrectly matched by the italic pattern after bold processing completes.

### PDF Styling

#### Color Scheme
- **Primary Text**: #1a1a1a, #2c3e50, #34495e
- **Accent Color**: #3498db (links, borders)
- **Subtle Text**: #555555 (contact info)
- **Code/Technical**: #e74c3c

#### Font Choices
- **Headers**: Helvetica-Bold
- **Body**: Helvetica
- **Code**: Courier

#### Spacing
- **Page Margins**: 0.5" top/bottom, 0.75" left/right
- **Section Spacing**: 12pt after major sections
- **Line Height**: 13-14pt for readability

## Markdown Format Specification

### Resume Structure

```markdown
# Full Name
Contact Line | email@example.com | phone
[LinkedIn](url) | [GitHub](url) | Location

## Section Name (e.g., Summary, Experience, Education)

### Subsection (e.g., Job Title, Degree)
**Organization** | Location | Dates

- Bullet point with details
- Use **bold** for emphasis
- Use *italic* for terms
- Use `code` for technical terms
- Use [links](url) for references
```

### Supported Formatting

- **Headings**: `#` (title), `##` (major section), `###` (subsection)
- **Bold**: `**text**` or `__text__`
- **Italic**: `*text*` or `_text_`
- **Code**: `` `text` ``
- **Links**: `[text](url)`
- **Lists**: `- item` or `* item`

## Common Tasks

### Adding New Features

1. **Extend Markdown Support**
   - Add parsing logic in `_process_inline_markdown()` or `parse_markdown()`
   - Test with a minimal example first
   - Verify PDF output with pdftotext

2. **Modify PDF Styling**
   - Update styles in `_create_styles()` method
   - Maintain professional appearance
   - Test with example_resume.md

3. **Add Command-Line Options**
   - Extend argparse configuration in `main()`
   - Update help text and README
   - Add examples to --help output

### Debugging

```bash
# Enable Python debugging
python -m pdb pineapple.py example_resume.md

# Check PDF structure
pdfinfo example_resume.pdf
pdftotext example_resume.pdf -  # Extract text

# Test with minimal input
echo "# Name\n\n## Section\n\n- Item" > /tmp/test.md
python pineapple.py /tmp/test.md
```

## Known Limitations

1. **Markdown Coverage**: Only supports common formatting (no tables, images, nested lists)
2. **Page Breaks**: Automatic only, no manual control
3. **Fonts**: Limited to standard PDF fonts
4. **Layout**: Single column only

## Security Considerations

- **Input Validation**: File existence checked before processing
- **Path Handling**: Uses pathlib.Path for safe path operations
- **No Code Execution**: Markdown parsing is regex-based, no eval/exec
- **PDF Generation**: ReportLab handles escaping automatically

## Future Enhancement Ideas

Potential features for future iterations (not currently implemented):

- [ ] Multiple resume themes/templates
- [ ] Support for resume.json (JSON Resume format)
- [ ] HTML output option
- [ ] Two-column layouts
- [ ] Custom color schemes via config
- [ ] Photo/headshot support
- [ ] Multiple page layouts
- [ ] Export to other formats (DOCX, HTML)

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'reportlab'`
- **Solution**: Activate venv and install dependencies: `source .venv/bin/activate && pip install -r requirements.txt`

**Issue**: PDF is blank or incomplete
- **Solution**: Check markdown formatting, ensure sections use proper heading levels

**Issue**: Text extraction shows garbled output
- **Solution**: Verify reportlab version, check for Unicode issues in markdown

**Issue**: Nix shell fails
- **Solution**: Ensure Nix is installed and nixpkgs channel is available

## Testing Strategy

### Manual Testing
```bash
# Basic functionality
python pineapple.py example_resume.md

# Custom output
python pineapple.py example_resume.md -o test.pdf

# Error cases
python pineapple.py nonexistent.md
python pineapple.py  # Missing argument

# Format variations
# Create test files with different markdown patterns
```

### Validation
```bash
# Text extraction (AI-parsability)
pdftotext example_resume.pdf - | head -20

# PDF metadata
pdfinfo example_resume.pdf

# File size (should be reasonable)
ls -lh example_resume.pdf
```

## Git Workflow

### What to Commit
- Source code (*.py)
- Configuration (shell.nix, requirements.txt)
- Documentation (README.md, *.md)
- Example files (example_resume.md, example_resume.pdf)

### What Not to Commit (via .gitignore)
- Virtual environments (.venv/)
- Generated PDFs (*.pdf, except example*.pdf)
- Python cache (__pycache__/, *.pyc)
- Build artifacts
- IDE settings (unless project-wide)

## Contact and Resources

- **Repository**: https://github.com/pid1/pineapple
- **License**: BSD 3-Clause
- **Python Version**: 3.13+ (compatible with 3.12+)
- **Dependencies**: markdown 3.7, reportlab 4.2.5

## Version History

### v1.0.0 (Initial Release)
- Basic Markdown to PDF conversion
- Custom styling and formatting
- Shell.nix environment setup
- Example resume and documentation
- AI-parsable PDF output
