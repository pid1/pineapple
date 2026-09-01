# 🍍 Pineapple

A sweet and tart resume generator. Great on a pizza.

**Pineapple** converts a Markdown file into a beautifully designed, ATS-optimized,
AI-parsable PDF resume. It is engineered to pass automated screening and impress
human readers — without compromising either goal.

**Writing a resume?** See [RESUME_GUIDE.md](RESUME_GUIDE.md) for the complete
format specification and content playbook, written so an AI assistant can generate
strong resume Markdown for you from scratch.

---

## Features

|                         |                                                                                                         |
| ----------------------- | ------------------------------------------------------------------------------------------------------- |
| ♿ Accessibility-first  | Atkinson Hyperlegible font, WCAG AA color contrast, PDF language tagging                                |
| 🤖 ATS & AI parsability | Single-column layout, standard section names, clean text extraction                                     |
| 🪄 Hidden AI metadata   | `<!-- AI: ... -->` blocks embed content in PDF metadata — invisible to humans, readable by AI screeners |
| 🎬 Introduction Video   | Dedicated section renders as a styled card linking to your video                                        |
| 🏆 Luxury design        | Warm gold accents, tracked uppercase headers, right-aligned dates                                       |
| 📄 PDF metadata         | Title, author, subject, language, and keywords fields all populated                                     |
| 📝 Markdown-based       | Write once, tailor per application, regenerate in seconds                                               |
| 🚀 Minimal dependencies | `reportlab` only                                                                                        |
| 🔧 Nix environment      | Reproducible builds via devenv                                                                          |

---

## Quick Start

### Prerequisites

- [Nix package manager](https://nixos.org/download.html)
- [devenv](https://devenv.sh/getting-started/)

### Setup and usage

```bash
git clone https://github.com/pid1/pineapple.git
cd pineapple
devenv shell

python pineapple.py your_resume.md              # outputs your_resume.pdf
python pineapple.py your_resume.md -o jane.pdf  # custom output name
python pineapple.py --help
```

---

## Markdown Format

See [RESUME_GUIDE.md](RESUME_GUIDE.md) for the complete specification.
What follows is a quick reference.

### Header

```markdown
# Your Name

Professional Title

email@example.com · (555) 123-4567 · City, ST
[LinkedIn](https://linkedin.com/in/handle) · [GitHub](https://github.com/handle)
```

- The name becomes the PDF's title and author metadata.
- The first line after the name is your professional title — it renders as gold
  tracked uppercase and is embedded in the PDF Subject field.
- Use `·` as a separator on contact lines, not `|`.

### Section headers

```markdown
## Professional Summary

## Introduction Video

## Work Experience

## Education

## Skills

## Projects

## Certifications

## Awards & Recognition
```

These exact names are what ATS platforms (Workday, Greenhouse, Taleo, Lever) map
to their structured fields. See RESUME_GUIDE.md for the full canonical list.

### Role headers — right-aligned dates

```markdown
### Senior Software Engineer

**TechCorp Inc.** | San Francisco, CA | Jan 2022 – Present
```

When a `**Company** | Location | Dates` line immediately follows a `###` heading,
Pineapple detects it and renders the job title with the date range right-aligned
on the same line, and the company and location on a muted line below. The last
segment must contain a year, "Present", or "Current".

### Introduction Video section

```markdown
## Introduction Video

One-sentence hook and link: [Watch a 60-second introduction](https://youtube.com/watch?v=VIDEO_ID)
```

Renders as a warm cream card with a gold border. Host the video as an unlisted
YouTube video, 45–60 seconds. See RESUME_GUIDE.md for video content guidance.

### Hidden AI metadata

```markdown
<!-- AI:
Write a dense prose summary here for AI screeners: video transcript summary,
target roles, seniority, location preferences, and core strengths. This is
completely invisible in the PDF viewer but embedded in the PDF's /Keywords
metadata field, which AI parsers and document indexers read.
-->
```

This is the honest alternative to keyword stuffing. The content is never rendered
in the document body, never shown to human readers, and does not affect the visual
layout. One block per file, placed anywhere (conventionally at the end).

### Inline formatting

```markdown
**bold** for company names, skill labels, project names
_italic_ sparingly, for publication titles or genuine emphasis
[text](url) for links — rendered in navy with underlines
`code` for technical terms inline

- bullet starts each achievement line
```

No nested bullets, no tables, no images.

---

## Why Pineapple Resumes Pass ATS

### Single-column layout

Every major ATS platform linearizes the PDF DOM top-to-bottom. Multi-column PDFs
scramble the parse order, causing skills to appear inside job descriptions and
dates to detach from roles. Pineapple uses strict single-column flow.

### Standard section names

ATS platforms score resumes by mapping parsed content to structured fields using
section header matching. Using "Career Journey" instead of "Work Experience" can
result in experience content being discarded entirely. Pineapple's canonical
section names match what Workday, Greenhouse, Taleo, and Lever expect.

### Clean text extraction

The PDF is built from real text elements — not images, not flattened glyphs.
Every character is extractable with perfect fidelity. No garbled words, no merged
tokens, no missing spaces. This matters for both traditional ATS (regex/keyword
matching) and AI-based screening (LLM parsing).

### PDF metadata

Pineapple populates all standard PDF document info fields:

| PDF Field   | Content                                   |
| ----------- | ----------------------------------------- |
| `/Title`    | Candidate name                            |
| `/Author`   | Candidate name                            |
| `/Subject`  | "Professional Resume — [title]"           |
| `/Creator`  | Pineapple Resume Generator                |
| `/Keywords` | Contents of your `<!-- AI: ... -->` block |
| `/Lang`     | `en-US` (PDF catalog)                     |

AI tools that process PDFs — including Claude, GPT-4, and resume-parsing APIs —
read these fields in addition to extracting body text. The `/Keywords` field is
how your video transcript summary travels with the PDF without appearing on the page.

### No ATS anti-patterns

Pineapple deliberately omits: tables, text boxes, graphics, skill-rating bars,
multi-column layouts, headers/footers with contact info (ATS parsers skip them),
and hidden white-on-white body text (modern parsers penalize this specifically).

---

## Accessibility

- **Atkinson Hyperlegible Next** — designed by the Braille Institute for maximum
  legibility; reduces confusion between similar characters (1/l/I, 0/O).
- **WCAG AA contrast** — all text meets or exceeds 4.5:1. Primary text (#1a1a1a)
  achieves 16:1.
- **PDF language tag** — `/Lang (en-US)` in the catalog enables correct
  screen-reader pronunciation and AI language detection.
- **Underlined links** — colored and underlined, so clickability is obvious to
  colorblind readers and in printed copies.
- **Continuation page footer** — multi-page resumes include a `Name · Page N`
  footer so separated pages are never anonymous.

---

## Design Philosophy

- **Honest** — the AI metadata feature surfaces information through legitimate
  PDF metadata channels, not invisible body text. Nothing in the document
  misleads a reader or an ATS.
- **Accessible before beautiful** — every font, contrast, and layout choice
  serves readability first.
- **Machine-readable before decorative** — visual refinements (gold accents,
  tracked headers, right-aligned dates) are layered on top of a structure that
  parses cleanly with all decoration stripped.
- **Minimal** — one Python file, one dependency, plain Markdown input.

---

## License

BSD 3-Clause License — see [LICENSE](LICENSE) for details.
