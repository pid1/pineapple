# Writing a Winning Resume with Pineapple

This guide tells you — human or AI — exactly how to write resume Markdown that
Pineapple renders into a beautiful, ATS-proof, AI-parsable PDF. Follow the format
spec precisely; the generator's visual polish depends on it.

If you are an AI assistant generating a resume: treat the **Format Specification**
as hard syntax rules and the **Content Playbook** as strong guidance. When the user
gives you a target job description, mirror its language per the keyword rules below.

---

## Quick Start

Paste this skeleton, fill in your content, run `python pineapple.py resume.md`, done.

```markdown
# Your Full Name
Your Professional Title

your.email@example.com · (555) 123-4567 · City, ST
[linkedin.com/in/yourhandle](https://linkedin.com/in/yourhandle) · [github.com/yourhandle](https://github.com/yourhandle) · [yourname.dev](https://yourname.dev)

## Professional Summary

Two to three sentences. Seniority + domain + what you're known for. Mirror the
exact language of the job posting you're targeting.

## Introduction Video

Watch a 60-second introduction — background, key achievements, and what I'm looking for next: [Watch on YouTube](https://youtube.com/watch?v=YOUR_VIDEO_ID)

## Work Experience

### Job Title
**Company Name** | City, ST | Mon YYYY – Present

- Strong past-tense verb + what you did + quantified outcome
- Reduced API latency 40% by introducing Redis caching and query batching
- Technologies: Python, Go, PostgreSQL, Kubernetes

### Earlier Job Title
**Previous Company** | City, ST | Mon YYYY – Mon YYYY

- Achievement with a number in it
- Another achievement

## Education

### Degree Name
**University Name** | City, ST | YYYY – YYYY

- GPA: X.X/4.0 (omit if below 3.5 or more than ~5 years ago)

## Skills

### Programming Languages
- **Proficient:** Language A, Language B
- **Familiar:** Language C

### Technologies & Tools
- **Category:** Tool A, Tool B, Tool C

## Certifications

- Certification Name (YYYY)

<!-- AI:
[Replace this with 3–8 sentences for AI screeners: who you are, what the video
covers, target role and seniority, location/remote preference, core strengths,
ideal team profile. Third person, dense with keywords from your target postings.]
-->
```

The rest of this guide explains every rule behind that skeleton and how to make
the content as strong as the format.

---



### Document header (required, in this exact order)

```markdown
# Full Name
Professional Title

email@example.com · (555) 123-4567 · City, ST
[linkedin.com/in/handle](https://linkedin.com/in/handle) · [github.com/handle](https://github.com/handle) · [yourname.dev](https://yourname.dev)
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
- **Write GitHub and LinkedIn as visible URLs, not labels.** Use
  `[github.com/handle](https://github.com/handle)` not `[GitHub](https://github.com/handle)`.
  AI resume screeners extract the PDF's text layer and parse it for profile URLs —
  they never see the `href` attribute alone. A visible `github.com/handle` lets them
  fetch your profile and repositories, which can add 35+ points to your score.
  Same reasoning applies to your portfolio URL.

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
  which many AI screeners and PDF parsers read.
- Write it as flowing prose in third person, dense with the same keywords a
  recruiter would search. Include the video's key points — this is how the video's
  content becomes parsable.
- Place it near the end of the file. One block only.
- Keep it honest. It must never contradict the visible resume.
- **Important**: some AI resume screeners extract only visible page text and skip
  PDF metadata fields entirely. Do not rely on the AI block as the sole carrier of
  critical information. Your **Professional Summary** must independently state your
  seniority, domain, and key differentiators — the AI block is additive, not a
  replacement.

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

If you have open source contributions, name the projects here. AI screeners give
significant weight to contributions to external repos (vs. personal projects only),
and mentioning them in the summary ensures the context is visible even if the
screener does not reach the Projects section.

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

### Projects section

Split into two subsections using `### ` headings:

**Open Source Contributions** — contributions to repos you do not own. These are
scored separately and more generously than personal projects, because they prove
you can work within another team's standards. For each contribution, link to the
external repo and the specific merged PR:

```markdown
### Open Source Contributions
- **[Project Name](https://github.com/org/project)** — What you changed; [PR #N](https://github.com/org/project/pull/N) merged, X reactions
```

**Personal Projects** — your own work. AI evaluators heavily penalize missing
links. Every project needs at minimum a GitHub URL; a live deployment adds a
meaningful score boost. Include real-world impact metrics when you have them
(users, stars, institutional adoption):

```markdown
### Personal Projects
- **Project Name** — One-line description, impact metric · [github.com/you/project](https://github.com/you/project) · [Live: project.yourdomain.com](https://project.yourdomain.com)
```

**Link scoring impact** (typical AI evaluator behavior):
- No GitHub link, no live demo → −3 to −5 points per project
- GitHub link only, no live demo → −2 to −3 points per project
- GitHub + live demo → full score; live demo alone can add 10–20% bonus
- Broken or inaccessible links → treated the same as missing links

Aim for projects that demonstrate real-world impact, non-trivial architecture, or
user adoption — these score significantly higher than tutorial-style assignments.

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

---

## Avoiding AI Tells

If you draft with an LLM, edit the output until it stops *sounding* like an LLM.
Reviewers — human and machine — increasingly recognize generated prose, and "reads
as AI" gets resumes discarded. These patterns, distilled from the Wikipedia
[Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
field guide, are the ones that surface most in resumes. None of them is proof of AI
on its own, but stacked together they are a strong tell. Hunt them down and cut them.

### Inflated significance and legacy

LLMs puff up importance instead of stating facts. Delete sentences that explain why
your work *mattered to a broader trend* rather than what you did.

- Cut: "served as a pivotal contributor, underscoring the team's commitment to
  excellence and reflecting a broader shift toward modern engineering."
- Keep: "Cut deploy time from 40 minutes to 6 by parallelizing the CI pipeline."

Watch for: *stands/serves as a testament, plays a vital/crucial/pivotal role,
underscores/highlights the importance of, reflects a broader, marked a turning point,
evolving landscape, indelible mark.*

### Promotional / advertisement tone

Resumes should read as factual claims, not a brochure. Avoid: *boasts, vibrant, rich,
robust, seamless, cutting-edge, world-class, passionate about, committed to,
spearheaded a groundbreaking, leveraged synergies.* State the achievement and the
number; let it speak.

### Superficial "-ing" analyses

LLMs glue a trailing participle clause onto a fact to editorialize about its impact.
On a resume this reads as filler.

- Cut: "Migrated the database to Postgres, **enhancing scalability and driving
  operational efficiency across the organization**."
- Keep: "Migrated the database to Postgres; supported 3x traffic with no added latency."

### High-density "AI vocabulary"

A cluster of these words in one document is the single strongest tell. One is a
coincidence; six is a fingerprint. Prefer plain synonyms:

| AI-flavored | Plain |
|---|---|
| leverage, utilize | use |
| spearhead, helm | lead |
| facilitate | run, help |
| delve into | examine |
| showcase, highlight | show |
| crucial, pivotal, key | important (or cut) |
| robust, seamless | reliable, smooth |
| foster, cultivate | build, grow |
| testament to | proof of (or cut) |

Also overused: *additionally, moreover, intricate, tapestry, underscore, vibrant,
meticulous, garner, bolster, enduring.*

### Negative parallelisms

"Not just X, but Y" / "It's not A, it's B" constructions are a hallmark of generated
prose. Rewrite as a direct statement.

- Cut: "Not just a developer, but a force multiplier for the entire team."
- Keep: "Mentored four junior engineers; two were promoted within a year."

### Rule of three

LLMs reflexively group everything in threes ("fast, scalable, and reliable";
"designed, built, and deployed"). One or two genuine threes are fine — a resume
where *every* bullet lands a tidy triplet is a tell. Vary your structure.

### Formatting fingerprints

- **Em dashes** ( — ) used heavily, surrounded by spaces, to punch up clauses.
  Pineapple resumes rarely need them; use commas or rewrite.
- **Curly quotes/apostrophes** (' " ") inconsistently mixed with straight ones.
  Pick straight and keep it consistent.
- **Title Case On Every Heading** — use the exact section names from this guide
  instead.
- **Boldface sprayed** across whole phrases for emphasis. Bold is reserved here for
  company names, skill labels, and project names only.
- **Inline-header bullet lists** ("**Leadership:** did things; **Delivery:** did
  more things"). Write real achievement bullets instead.

### Generic, unquantified claims

The deepest tell is content, not style: LLMs default to vague, widely-applicable
statements. The fix is also the best resume advice in this guide — every bullet needs
a concrete artifact or a number. Specificity is the most reliably human signal you
can send.

> Self-check before you ship: read each bullet and ask "could this appear on a
> thousand other resumes unchanged?" If yes, it's either AI filler or weak writing —
> rewrite it with a number, a name, or a result.
