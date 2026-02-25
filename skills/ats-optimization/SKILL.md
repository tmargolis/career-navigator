---
name: ats-optimization
trigger: auto
fires_when:
  - A resume is being generated or assembled
  - A resume is being edited or reviewed
  - The /cn:tailor-resume command is active
  - The /cn:resume-score command is active
  - The user pastes resume content for feedback
description: >
  Automatically checks resumes for ATS compatibility issues, keyword alignment,
  and structural problems. Surfaces fixes inline without being asked.
---

# ATS Optimization Skill

This skill fires automatically whenever a resume is being generated or reviewed. Apply all checks below and report findings inline, ordered by impact.

## 1. Formatting — ATS-Hostile Patterns

Flag any of these immediately with a specific fix:

| Pattern | Problem | Fix |
|---------|---------|-----|
| Tables | ATS parsers scramble or skip table content | Convert to plain bullet list |
| Text boxes | Content is invisible to most parsers | Move text inline |
| Columns / two-column layouts | Columns are read left-to-right across both, mangling content | Convert to single-column |
| Graphics, logos, icons | Ignored or cause parse errors | Remove entirely |
| Unusual fonts (decorative, symbol fonts) | May render as garbage characters | Use Arial, Calibri, Georgia, Times New Roman |
| Contact info in header/footer | Most ATS systems don't parse headers/footers | Move contact info to body, top of page |
| Embedded hyperlinks with anchor text | Some parsers drop the URL | Write out full URLs or remove |
| Images of text | Completely opaque to parsers | Replace with actual text |

**File format guidance**: `.docx` (plain, no macros) is the safest format. PDF is acceptable only if it has a proper text layer (not scanned). Never submit `.pages` or image-only PDFs.

## 2. Keyword Density — Match the JD

- **Use the exact language from the job description**, not synonyms. If the JD says "cross-functional collaboration," don't write "working across teams." ATS matches strings.
- Check that skills listed in the JD appear verbatim in the resume, prioritizing the top 10 keywords by frequency/prominence in the JD.
- Skills should appear in both a Skills section AND woven into experience bullets where truthful.
- Avoid keyword stuffing — each keyword should appear in a meaningful context, 1–3 times per document.
- If a required skill is genuinely absent, do not add it. Flag the gap explicitly.

**Before/after example:**
- Before: "Managed product releases and worked with engineers"
- After: "Led end-to-end product launches in collaboration with engineering teams, reducing release cycle time by 20%"

## 3. Section Order — ATS Parsing Priority

Recommended order for most ATS systems:
1. Contact information (name, email, phone, LinkedIn URL, city/state)
2. Professional summary (2–3 lines, keyword-rich)
3. Skills (flat list or categorized, no graphics)
4. Work experience (reverse chronological; company, title, dates, bullets)
5. Education
6. Certifications (if relevant and recent)
7. Optional: Projects, Publications, Volunteer work

**Never lead with a photo, objective statement, or references section.**

## 4. Experience Bullet Quality

Each bullet should follow: **[Action verb] + [what you did] + [measurable result]**

Flag bullets that:
- Start with a noun or "Responsible for" (passive, weak)
- Have no measurable outcome (add one where possible)
- Are longer than two lines (split or tighten)
- Duplicate content from another bullet

## 5. ATS Score Reporting

After checks, report:

```
ATS COMPATIBILITY CHECK
─────────────────────────────────────────
Formatting:     PASS / WARN / FAIL  [issue count]
Keyword match:  XX% against JD      [missing: skill1, skill2]
Section order:  PASS / WARN
Bullet quality: X of Y bullets flagged

Overall score: XX/100
Top fixes: [list top 3 highest-impact changes]
```

Score calculation: Formatting 30pts (deduct 5 per issue), Keyword match 40pts (proportional), Section order 10pts, Bullet quality 20pts (deduct 2 per weak bullet, max 10 deductions).
