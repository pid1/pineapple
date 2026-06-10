# Writing a Winning Resume with Pineapple

This guide tells you — human or AI — exactly how to write resume Markdown that
Pineapple renders into a beautiful, ATS-proof, AI-parsable PDF. Follow the format
spec precisely; the generator's visual polish depends on it.

If you are an AI assistant generating a resume: treat the **Format Specification**
as hard syntax rules and the **Content Playbook** as strong guidance. When the user
gives you a target job description, mirror its language per the keyword rules below.

---

## Format Specification

### Document header (required, in this exact order)

```markdown
# Full Name
Professional Title

email@example.com · (555) 123-4567 · City, ST
[LinkedIn](https://linkedin.com/in/handle) · [GitHub](https://github.com/handle)
```

Rules:

- `# Name` must be the **first** heading. It becomes the 28pt centered title and
  the PDF's author/title metadata.
- The **first plain line after the name is the professional title.** It renders as
  gold tracked uppercase and is embedded in PDF Subject metadata. Make it match the
  target job title as closely as honesty allows ("Senior Software Engineer", not
  "Code Wizard").
- Subsequent plain lines before the first `##` are contact lines (small, muted,
  centered). Use `·` as a separator, not `|`.
- Keep contact to 2 lines maximum. Include: email, phone, city/state, LinkedIn,
  GitHub or portfolio. Recruiters expect a location even for remote roles.

### Sections

```markdown
## Section Name
```

Renders as a gold uppercase header with a hairline rule. **Use these exact names** —
ATS platforms (Workday, Greenhouse, Taleo, Lever) map content to fields by header:

| Use exactly this | Never this |
|---|---|
| Professional Summary | About Me, My Story, Profile |
| Introduction Video | Video, Media, Watch This |
| Work Experience | Career Journey, Employment |
| Education | Academic Background |
| Skills | Competencies, Toolkit |
| Projects | Work Samples |
| Certifications | Credentials |
| Awards & Recognition | Honors |

Recommended order: Professional Summary → Introduction Video → Work Experience →
Education → Skills → Projects → Certifications → Awards & Recognition. Drop any
section you can't fill with strong content — a thin section is worse than none.

### Roles (jobs, degrees)

```markdown
### Job Title
**Company Name** | City, ST | Jan 2022 – Present

- Achievement bullet
- Achievement bullet
```

Rules:

- The `**Company** | Location | Dates` line **must immediately follow** the `###`
  heading and **must use `|` separators**. Pineapple detects it and renders dates
  right-aligned on the title line — the signature layout of the design.
- The last `|` segment must contain a year, "Present", or "Current".
- Date format: `Mon YYYY – Mon YYYY` (e.g., `Jan 2022 – Present`). Always
  month + year; ATS parsers compute tenure from these.
- Education uses the same pattern: `### Degree` then `**University** | City, ST | 2013 – 2017`.

### Introduction Video

```markdown
## Introduction Video

One sentence telling the reader what they'll get and how long it takes:
[Watch a 60-second introduction](https://youtube.com/watch?v=VIDEO_ID)
```

Renders as a cream card with a gold border. Rules:

- Host as an **unlisted** YouTube video. 45–60 seconds. Structure: who you are
  (10s) → two or three achievements relevant to the target role (35s) → what
  you're looking for (10s).
- The body should be 1–2 lines: a hook plus the link. Don't summarize the whole
  video visibly — that's what the hidden AI block is for (below).

### Hidden AI metadata block

```markdown
<!-- AI:
Two to ten sentences written FOR machine readers: a transcript-level summary of
the introduction video, target roles, seniority, location/remote preferences,
core strengths, and ideal team or company profile.
-->
```

Rules:

- Invisible in the PDF; embedded verbatim in the PDF's `/Keywords` metadata,
  which AI screeners and PDF parsers read.
- Write it as flowing prose in third person, dense with the same keywords a
  recruiter would search. Include the video's key points — this is how the video's
  content becomes parsable.
- Place it near the end of the file. One block only.
- Keep it honest. It must never contradict the visible resume.

### Inline formatting

- `**bold**` for company names, skill-category labels, and project names
- `*italic*` sparingly, for publication titles or genuine emphasis
- `[text](url)` for links — they render in navy with underlines
- Bullets start with `- `. No nested bullets, no tables, no images, no HTML.

---

## Content Playbook

### Professional Summary (2–3 sentences, never more)

Formula: **[seniority + title] + [years] + [2–3 domains] + [what you're known for]**.
No first person ("I"), no objective statements, no "seeking a challenging role."
Front-load it with the keywords from the job description — many ATS rankers weight
the summary heaviest.

### Achievement bullets — the heart of the resume

Every bullet: **strong past-tense verb + what you did + quantified outcome.**

- Weak: `- Responsible for improving API performance`
- Strong: `- Reduced API p95 latency 40% by introducing Redis caching and query batching`

Rules:

- 3–5 bullets for recent roles, 2–3 for older ones. Most impressive bullet first.
- Quantify everything you can: %, $, time saved, users served, team size. If you
  can't quantify, name the concrete artifact you shipped.
- Vary the verbs: Led, Built, Reduced, Shipped, Designed, Automated, Scaled,
  Mentored, Drove, Eliminated. Never start two adjacent bullets with the same verb.
- Current role bullets in present tense; all past roles in past tense.
- End each role with a `- Technologies: ...` bullet listing the stack — it's a
  keyword anchor ATS parsers reliably pick up.

### Keyword strategy (this is where ATS battles are won)

- Target **15–25 keywords** mirrored from the specific job description. Fewer
  reads sparse; more trips NLP spam detection.
- Use the **exact phrasing** of the posting. If it says "Kubernetes
  administration," write that — not "container orchestration."
- Include both acronym and full form once each: "Infrastructure as Code (IaC)".
- Weave keywords into achievement bullets, not just the Skills list. A skill that
  appears inside a quantified achievement scores higher than one in a list.
- Never stuff keywords in white text or repeat them unnaturally — modern parsers
  flag it and humans reject it.

### Skills section

Group with `### ` subheadings (e.g., "Programming Languages", "Technologies &
Tools") and bold category labels:

```markdown
- **Proficient:** Python, Go, TypeScript, SQL
- **Familiar:** Rust, Java
```

Honesty matters: "Proficient" means you can interview on it today.

### Length and cutting

- **One page** for under ~10 years of experience; **two pages** absolute maximum.
- Cut in this order: oldest-role bullets → Awards → older Projects → coursework →
  roles older than 15 years entirely.
- Every line must earn its place. When in doubt, cut.

### Tailoring per application (the real advantage)

Keep one master Markdown file with everything. For each application:

1. Copy it, then prune to the most relevant roles/bullets.
2. Rewrite the title line and summary to mirror the posting.
3. Swap keywords per the keyword strategy above.
4. Update the AI block's "seeking" sentence to name the role.
5. Regenerate: `python pineapple.py resume_company.md -o lastname_resume.pdf`

Ten tailored resumes beat a hundred generic ones.

### What never to include

- Photos, graphics, skill bars, columns, or tables (ATS poison)
- "References available upon request" (assumed; wastes a line)
- Full street address, birthdate, marital status
- GPA below 3.5, or any GPA after your first job
- Pronouns in the title line (put them in your email signature instead if desired)
