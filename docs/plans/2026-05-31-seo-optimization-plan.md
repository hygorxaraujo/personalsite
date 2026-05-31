# SEO and Social Sharing Optimization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Configure global social card headers (Open Graph & Twitter Summary Large Card) using compatible JPEG banners, standardize page summaries, and add high-quality search descriptions to all blog posts.

**Architecture:** We will declare the global default fallback sharing assets in `_quarto.yml`, convert Pandoc-specific attributes to official Quarto fields in `.qmd` files, and update `.ipynb` notebooks via direct JSON adjustments to their raw frontmatter metadata cells.

**Tech Stack:** Quarto Static Site Generator, JSON syntax, Markdown, Bash.

---

### Task 1: Global Site Metadata Configuration

**Files:**
- Modify: `_quarto.yml`

- [ ] **Step 1: Edit `_quarto.yml` to declare Open Graph and Twitter Card schemas**

Modify `/home/hygor/code-projects/personalsite/_quarto.yml` by updating the `website` section around line 24.

Target content in `/home/hygor/code-projects/personalsite/_quarto.yml`:
```yaml
  bread-crumbs: true
  open-graph: true
  cookie-consent:
```

Replacement content:
```yaml
  bread-crumbs: true
  open-graph:
    true
    image: assets/profile.jpg
    locale: en_US
    site-name: "Hygor X. Araújo"
  twitter-card:
    true
    image: assets/profile.jpg
    card: summary_large_image
  cookie-consent:
```

- [ ] **Step 2: Verify `_quarto.yml` changes do not break YAML syntax**
Run standard yaml verification check or render test (compiles project configuration).
Run: `quarto inspect`
Expected: Successful JSON inspection output containing project configuration, no syntax errors.

- [ ] **Step 3: Commit global configuration changes**
Run:
```bash
git add _quarto.yml
git commit -m "chore: configure global Open Graph and Twitter Card fallbacks"
```

---

### Task 2: Homepage SEO Upgrades

**Files:**
- Modify: `index.qmd`

- [ ] **Step 1: Replace Pandoc `description-meta` with standard Quarto `description`**

Modify `/home/hygor/code-projects/personalsite/index.qmd` around line 4.

Target content in `/home/hygor/code-projects/personalsite/index.qmd`:
```yaml
title: "Hygor X. Araújo"
pagetitle: "Hygor X. Araújo — Data Science & ML Engineering"
description-meta: "Writing on data science, ML engineering, and agentic workflows by Hygor X. Araújo."
page-layout: full
```

Replacement content:
```yaml
title: "Hygor X. Araújo"
pagetitle: "Hygor X. Araújo — Data Science & ML Engineering"
description: "Writing on data science, machine learning engineering, and agentic workflows by Hygor X. Araújo, a data scientist and systems engineer specializing in production-grade AI solutions."
page-layout: full
```

- [ ] **Step 2: Commit homepage changes**
Run:
```bash
git add index.qmd
git commit -m "seo: standardize homepage description to standard Quarto format"
```

---

### Task 3: About Page SEO Upgrades

**Files:**
- Modify: `about.qmd`

- [ ] **Step 1: Add a description to the About page frontmatter**

Modify `/home/hygor/code-projects/personalsite/about.qmd` around line 4.

Target content in `/home/hygor/code-projects/personalsite/about.qmd`:
```yaml
title: "About"
pagetitle: "About — Hygor X. Araújo"
page-layout: full
```

Replacement content:
```yaml
title: "About"
pagetitle: "About — Hygor X. Araújo"
description: "Learn about Hygor X. Araújo, a Data Scientist and Systems Architect bridging the gap between complex software systems and intelligent reasoning, with an M.Sc. in Computational Intelligence and USP AI MBA."
page-layout: full
```

- [ ] **Step 2: Commit about page changes**
Run:
```bash
git add about.qmd
git commit -m "seo: add descriptive meta tags to the about page"
```

---

### Task 4: Blog Post 1 SEO Updates ("How to check missing values in pandas")

**Files:**
- Modify: `posts/2018-06-30-pandas-check-nan.ipynb`

- [ ] **Step 1: Edit raw frontmatter inside `pandas-check-nan.ipynb` to insert description**

Modify `/home/hygor/code-projects/personalsite/posts/2018-06-30-pandas-check-nan.ipynb` around line 18.

Target content in `/home/hygor/code-projects/personalsite/posts/2018-06-30-pandas-check-nan.ipynb`:
```json
     "date: '2018-06-30'\n",
     "image: /assets/headers/2018-06-30-pandas-check-nan.svg\n",
     "title: How to check missing values in pandas\n",
     "toc: true\n",
     "---"
```

Replacement content:
```json
     "date: '2018-06-30'\n",
     "image: /assets/headers/2018-06-30-pandas-check-nan.svg\n",
     "title: How to check missing values in pandas\n",
     "description: \"A practical guide on how to check, count, and analyze missing (NaN) values in a pandas DataFrame using Python's NumPy and pandas library.\"\n",
     "toc: true\n",
     "---"
```

- [ ] **Step 2: Verify JSON syntax validity**
Run: `python3 -c "import json; json.load(open('posts/2018-06-30-pandas-check-nan.ipynb'))"`
Expected: Clean exit (no syntax errors).

- [ ] **Step 3: Commit post changes**
Run:
```bash
git add posts/2018-06-30-pandas-check-nan.ipynb
git commit -m "seo: add post description to pandas-check-nan notebook"
```

---

### Task 5: Blog Post 2 SEO Updates ("Explaining the Fogg Behavior Model")

**Files:**
- Modify: `posts/2020-03-08-explaining-the-fogg-behavior-model.ipynb`

- [ ] **Step 1: Edit raw frontmatter inside `explaining-the-fogg-behavior-model.ipynb`**

Modify `/home/hygor/code-projects/personalsite/posts/2020-03-08-explaining-the-fogg-behavior-model.ipynb` around line 20.

Target content in `/home/hygor/code-projects/personalsite/posts/2020-03-08-explaining-the-fogg-behavior-model.ipynb`:
```json
     "image: 2020-03-08-explaining-the-fogg-behavior-model_files/figure-html/fig-bmap-output-1.png\n",
     "title: Explaining the Fogg Behavior Model\n",
     "toc: true\n",
     "format:\n",
     "  html:\n",
     "    code-fold: true\n",
     "---"
```

Replacement content:
```json
     "image: 2020-03-08-explaining-the-fogg-behavior-model_files/figure-html/fig-bmap-output-1.png\n",
     "title: Explaining the Fogg Behavior Model\n",
     "description: \"An explanation of the Fogg Behavior Model (B=MAP) with a visual graph plotted in Python using NumPy and Matplotlib.\"\n",
     "toc: true\n",
     "format:\n",
     "  html:\n",
     "    code-fold: true\n",
     "---"
```

- [ ] **Step 2: Verify JSON syntax validity**
Run: `python3 -c "import json; json.load(open('posts/2020-03-08-explaining-the-fogg-behavior-model.ipynb'))"`
Expected: Clean exit (no syntax errors).

- [ ] **Step 3: Commit post changes**
Run:
```bash
git add posts/2020-03-08-explaining-the-fogg-behavior-model.ipynb
git commit -m "seo: add post description to fogg-behavior-model notebook"
```

---

### Task 6: Blog Post 3 SEO Updates ("Installing TensorFlow 2.19 with GPU support on Fedora 42")

**Files:**
- Modify: `posts/2025-05-03-installing_tensorflow2.19_on_fedora42.ipynb`

- [ ] **Step 1: Edit raw frontmatter inside `installing_tensorflow2.19_on_fedora42.ipynb`**

Modify `/home/hygor/code-projects/personalsite/posts/2025-05-03-installing_tensorflow2.19_on_fedora42.ipynb` around line 18.

Target content in `/home/hygor/code-projects/personalsite/posts/2025-05-03-installing_tensorflow2.19_on_fedora42.ipynb`:
```json
     "title: \"Installing TensorFlow 2.19 with GPU support on Fedora 42\"\n",
     "toc: true\n",
     "format:\n",
     "  html:\n",
     "    code-fold: false\n",
     "---"
```

Replacement content:
```json
     "title: \"Installing TensorFlow 2.19 with GPU support on Fedora 42\"\n",
     "description: \"A step-by-step technical guide to installing TensorFlow 2.19 with GPU support, including GCC 13.3 compilation and CUDA toolkit setup on Fedora 42.\"\n",
     "toc: true\n",
     "format:\n",
     "  html:\n",
     "    code-fold: false\n",
     "---"
```

- [ ] **Step 2: Verify JSON syntax validity**
Run: `python3 -c "import json; json.load(open('posts/2025-05-03-installing_tensorflow2.19_on_fedora42.ipynb'))"`
Expected: Clean exit (no syntax errors).

- [ ] **Step 3: Commit post changes**
Run:
```bash
git add posts/2025-05-03-installing_tensorflow2.19_on_fedora42.ipynb
git commit -m "seo: add post description to tensorflow installation guide notebook"
```

---

### Task 7: Draft Post 4 SEO Updates ("How to set up Google Drive sync on Linux with rcloud")

**Files:**
- Modify: `posts/2025-07-27-how-to-set-up-Google-Drive-sync-on-Linux-with-rcloud.ipynb`

- [ ] **Step 1: Edit raw frontmatter inside `how-to-set-up-Google-Drive-sync-on-Linux-with-rcloud.ipynb`**

Modify `/home/hygor/code-projects/personalsite/posts/2025-07-27-how-to-set-up-Google-Drive-sync-on-Linux-with-rcloud.ipynb` around line 16.

Target content in `/home/hygor/code-projects/personalsite/posts/2025-07-27-how-to-set-up-Google-Drive-sync-on-Linux-with-rcloud.ipynb`:
```json
     "title: How to set up Google Drive sync on Linux with rcloud\n",
     "toc: true\n",
     "draft: true\n",
     "format:\n",
     "  html:\n",
     "    code-fold: false\n",
     "---"
```

Replacement content:
```json
     "title: How to set up Google Drive sync on Linux with rcloud\n",
     "description: \"A technical guide on how to set up robust Google Drive file synchronization on Linux using the rcloud utility.\"\n",
     "toc: true\n",
     "draft: true\n",
     "format:\n",
     "  html:\n",
     "    code-fold: false\n",
     "---"
```

- [ ] **Step 2: Verify JSON syntax validity**
Run: `python3 -c "import json; json.load(open('posts/2025-07-27-how-to-set-up-Google-Drive-sync-on-Linux-with-rcloud.ipynb'))"`
Expected: Clean exit (no syntax errors).

- [ ] **Step 3: Commit post changes**
Run:
```bash
git add posts/2025-07-27-how-to-set-up-Google-Drive-sync-on-Linux-with-rcloud.ipynb
git commit -m "seo: add post description to google-drive rcloud sync notebook"
```

---

### Task 8: Draft Post 5 SEO Updates ("Model Context Protocol and Agent Skills")

**Files:**
- Modify: `posts/2026-02-05-mcp_and_agent_skills.ipynb`

- [ ] **Step 1: Edit raw frontmatter inside `mcp_and_agent_skills.ipynb`**

Modify `/home/hygor/code-projects/personalsite/posts/2026-02-05-mcp_and_agent_skills.ipynb` around line 17.

Target content in `/home/hygor/code-projects/personalsite/posts/2026-02-05-mcp_and_agent_skills.ipynb`:
```json
     "categories:\n",
     "- agents\n",
     "- ai\n",
     "- llm\n",
     "- mcp\n",
     "---"
```

Replacement content:
```json
     "categories:\n",
     "- agents\n",
     "- ai\n",
     "- llm\n",
     "- mcp\n",
     "title: \"Model Context Protocol and Agent Skills\"\n",
     "description: \"An exploration of Anthropic's Model Context Protocol (MCP) and the Agent Skills specification, comparing their architectures, features, and use cases.\"\n",
     "---"
```

- [ ] **Step 2: Verify JSON syntax validity**
Run: `python3 -c "import json; json.load(open('posts/2026-02-05-mcp_and_agent_skills.ipynb'))"`
Expected: Clean exit (no syntax errors).

- [ ] **Step 3: Commit post changes**
Run:
```bash
git add posts/2026-02-05-mcp_and_agent_skills.ipynb
git commit -m "seo: add post title and description to mcp_and_agent_skills notebook"
```

---

### Task 9: Site Render & Verification

- [ ] **Step 1: Build the website statically**
Compile the static site to regenerate sitemaps and HTML contents with new meta headers.
Run: `task build`
Expected: Build finishes with exit code 0.

- [ ] **Step 2: Verify homepage meta headers**
Run: `grep -q '<meta name="description"' _site/index.html && grep -q 'property="og:image"' _site/index.html && grep -q 'name="twitter:card"' _site/index.html`
Expected: Returns exit code 0.

- [ ] **Step 3: Verify about page meta headers**
Run: `grep -q '<meta name="description"' _site/about.html && grep -q 'property="og:image"' _site/about.html`
Expected: Returns exit code 0.

- [ ] **Step 4: Verify built blog post meta headers**
Run: `grep -q '<meta name="description"' _site/posts/2018-06-30-pandas-check-nan.html && grep -q 'property="og:image"' _site/posts/2018-06-30-pandas-check-nan.html`
Expected: Returns exit code 0.
