# SEO and Social Sharing Optimization Design

This document details the design specifications for improving the Search Engine Optimization (SEO) and social media sharing card preview capabilities for the personal website of Hygor X. Araújo.

---

## 1. Goal

The objective is to resolve gaps in metadata, Open Graph headers, Twitter Cards, and compatible share images to ensure:
* Search engines index descriptive and professional snippets for all pages and posts.
* Social media platforms (LinkedIn, X/Twitter, Slack, Facebook) display visually correct, rich preview cards when links are shared.
* Maintain the on-site aesthetic appeal (dynamic Delaunay triangulation graph SVGs) without breaking social media preview crawlers (which do not support SVG images).

---

## 2. Current Status & Findings

1. **Non-Supported Social Card Images (SVG Format):** 
   The default post listing header and banner image configured in `posts/_metadata.yml` is `default_header.svg`. Social media platforms do not render SVG files for `og:image` or `twitter:image`. Shared links have broken/missing social preview images.
2. **Missing Twitter Card Schema:** 
   `_quarto.yml` has `open-graph: true` but lacks any `twitter-card` configuration blocks.
3. **Under-Optimized Page Descriptions:**
   * **Homepage (`index.qmd`):** Uses the Pandoc-specific `description-meta` instead of the standard Quarto `description` field.
   * **About Page (`about.qmd`):** Lacks any description metadata entirely.
   * **Blog Posts (`posts/*.ipynb`):** All active and draft posts lack a `description` field in their frontmatter, resulting in search engines extracting arbitrary code blocks or raw cell text.

---

## 3. Proposed Changes

### 3.1. Global Configuration (`_quarto.yml`)

We will configure global fallbacks for Open Graph and Twitter Card schema.
We will set the professional high-resolution JPEG profile image `assets/profile.jpg` as the fallback `image` for both Open Graph and Twitter.

```yaml
website:
  # ... (existing properties)
  open-graph:
    true
    image: assets/profile.jpg
    locale: en_US
    site-name: "Hygor X. Araújo"
  twitter-card:
    true
    image: assets/profile.jpg
    card: summary_large_image
```

### 3.2. Homepage & About Page Upgrades

#### `index.qmd`
Standardize the description metadata from `description-meta` to the standard `description` field to automatically populate social cards.

```yaml
title: "Hygor X. Araújo"
pagetitle: "Hygor X. Araújo — Data Science & ML Engineering"
description: "Writing on data science, machine learning engineering, and agentic workflows by Hygor X. Araújo, a data scientist and systems engineer specializing in production-grade AI solutions."
```

#### `about.qmd`
Introduce a descriptive and professional snippet to the YAML header:

```yaml
title: "About"
pagetitle: "About — Hygor X. Araújo"
description: "Learn about Hygor X. Araújo, a Data Scientist and Systems Architect bridging the gap between complex software systems and intelligent reasoning, with an M.Sc. in Computational Intelligence and USP AI MBA."
```

### 3.3. Individual Blog Posts & Drafts

We will update the YAML frontmatter inside the first raw/markdown cell of each Jupyter Notebook (`.ipynb`) in `posts/` to add `description: "..."`.

#### 1. How to check missing values in pandas (`posts/2018-06-30-pandas-check-nan.ipynb`)
```yaml
description: "A practical guide on how to check, count, and analyze missing (NaN) values in a pandas DataFrame using Python's NumPy and pandas library."
```

#### 2. Explaining the Fogg Behavior Model (`posts/2020-03-08-explaining-the-fogg-behavior-model.ipynb`)
```yaml
description: "An explanation of the Fogg Behavior Model (B=MAP) with a visual graph plotted in Python using NumPy and Matplotlib."
```

#### 3. Installing TensorFlow 2.19 with GPU support on Fedora 42 (`posts/2025-05-03-installing_tensorflow2.19_on_fedora42.ipynb`)
```yaml
description: "A step-by-step technical guide to installing TensorFlow 2.19 with GPU support, including GCC 13.3 compilation and CUDA toolkit setup on Fedora 42."
```

#### 4. How to set up Google Drive sync on Linux with rcloud (`posts/2025-07-27-how-to-set-up-Google-Drive-sync-on-Linux-with-rcloud.ipynb`) [Draft]
```yaml
description: "A technical guide on how to set up robust Google Drive file synchronization on Linux using the rcloud utility."
```

#### 5. Model Context Protocol and Agent Skills (`posts/2026-02-05-mcp_and_agent_skills.ipynb`) [Draft]
```yaml
description: "An exploration of Anthropic's Model Context Protocol (MCP) and the Agent Skills specification, comparing their architectures, features, and use cases."
```

---

## 4. Verification Plan

### 4.1. Automated Rendering Verification
After modifying the source files, we will rebuild the static website to ensure Quarto compiles the tags correctly:
```bash
task build
```
This builds the site to the `_site/` directory.

### 4.2. Local Meta-Tag Checks
Verify that the output HTML files contain the expected `<meta>` tags.
For example, we will check that:
* `_site/index.html` has `<meta name="description" ...>`, `<meta property="og:description" ...>`, `<meta name="twitter:description" ...>`, and the corresponding `image` and `card` tags.
* `_site/about.html` has matching descriptions and meta properties.
* `_site/posts/*.html` have their unique, specific summaries and properties.

We can run standard tests/greps on `_site/` to verify:
```bash
grep -q '<meta name="description"' _site/index.html
grep -q 'property="og:image"' _site/index.html
```
