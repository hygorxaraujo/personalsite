# Search Engine Optimization (SEO) & Social Sharing Previews

This document outlines how SEO, Open Graph (OG), and Twitter Card sharing previews are configured for this Quarto-based website, as well as instructions for maintaining them when publishing new content.

---

## 1. Global Configurations (`_quarto.yml`)

Global fallbacks for metadata are configured directly in `_quarto.yml` under the `website` mapping. This ensures that any page or post shared on social media (LinkedIn, X/Twitter, Slack, Facebook) has a professional, consistent fallback preview card.

### Key Global Settings:
* **Open Graph (`open-graph`):** Sets the default sharing locale (`en_US`), site name (`Hygor X. Araújo`), and default sharing preview image.
* **Twitter Card (`twitter-card`):** Sets the global Twitter sharing preview image and card type (`summary_large_image`).
* **The SVG Gotcha (Crucial):** Social media crawlers (LinkedIn, X, Slack, Facebook) **do not support SVG format images** for preview cards (`og:image` and `twitter:image`). Even though on-site banner listing headers use SVGs, we use the highly compatible JPEG profile photo (`assets/profile.jpg`) as our global fallback preview image to prevent broken or missing social card visuals.

```yaml
website:
  # ...
  open-graph:
    image: assets/profile.jpg
    locale: en_US
    site-name: "Hygor X. Araújo"
  twitter-card:
    image: assets/profile.jpg
```

---

## 2. Page-Level Configurations (`.qmd`)

Static pages (like `index.qmd` and `about.qmd`) have standard Quarto `description` tags configured in their YAML frontmatter.

* **Homepage (`index.qmd`):** Uses the `description` key (not the Pandoc-specific `description-meta`) to automatically populate `<meta name="description" ...>`, `og:description`, and `twitter:description` standard headers.
* **About Page (`about.qmd`):** Features a tailored descriptive summary of your academic background and domain consulting expertise.

Example frontmatter:
```yaml
---
title: "About"
pagetitle: "About — Hygor X. Araújo"
description: "Learn about Hygor X. Araújo, a Data Scientist and Systems Architect..."
---
```

---

## 3. Jupyter Notebook Blog Posts (`posts/*.ipynb`)

Blog posts authored inside Jupyter Notebooks (`.ipynb`) have their metadata embedded inside their first raw JSON cell in the notebook structure. 

To ensure search engines display clean, hand-crafted summaries in search result listings (and that social platforms capture a custom description snippet), every post must include a `description: "..."` key.

### Safe Metadata Editing Utility:
Because `.ipynb` notebooks are structurally validated JSON, you should **never** attempt direct regex or raw string edits, as they are extremely fragile and prone to breaking syntax. 

Instead, use the included Python automation helper script:
```bash
python3 scripts/add_post_seo.py <notebook-path> "<description-text>" "[optional-title-override]"
```

**Example Usage:**
```bash
python3 scripts/add_post_seo.py posts/2026-02-05-mcp_and_agent_skills.ipynb "An exploration of Anthropic's Model Context Protocol (MCP) and the Agent Skills specification."
```

This utility automatically:
1. Loads the notebook as JSON.
2. Navigates to the raw frontmatter metadata cell.
3. Injects or updates the `description` and `title` keys safely.
4. Correctly escapes JSON-invalid characters.
5. Saves the notebook with standard indentation.

---

## 4. Verification

Whenever changes are made to the site's metadata configurations, you can run a static compilation to inspect the output:
```bash
task build
```
Verify that the generated HTML files in `_site/` have standard meta headers by running:
```bash
grep -o '<meta name="description"[^>]*>' _site/index.html
grep -o '<meta property="og:[^>]*>' _site/index.html
```
