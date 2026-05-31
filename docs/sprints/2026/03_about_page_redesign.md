---
name: plan
description: Sprint Plan for May 2026 - About Page Editorial Redesign
---

# Sprint: About Page Editorial Redesign (May 2026)

## Overview
This sprint focuses on elevating the "About Me" page from a generic Quarto template to a bespoke, editorial, and highly engaging technical portfolio page. We will maintain the established "Monograph" brand style—using emerald typography on warm paper—and add an interactive visual component (`fig. 2 — architectural alignment`) alongside a stylized academic and professional timeline.

## Goals
1. **Bespoke Editorial Design:** Move away from Quarto's default `trestles` layout to a custom asymmetrical layout.
2. **Interactive Visual Element:** Design a beautiful, custom responsive SVG diagram illustrating the synthesis between Systems Architecture and Data Science.
3. **Structured Professional Timeline:** Format Hygor's academic background and consulting pillars into an elegant, custom-styled vertical timeline.
4. **Perfect Mode Cohesion:** Ensure that all new visual assets and layout details adapt fluidly to both light (`zephyr`) and dark (`darkly`) modes.
5. **No Content Generation:** Refine and re-layout the existing bio text and academic credentials without fabricating any new content.

## Tasks

### 1. Style Overrides for Custom About Page
- [x] **Step 1: Add Custom SCSS Rules for About Page**
  Modify `custom.scss` to define layout, typography, and interactive timeline styles.
  Add classes: `.about-custom`, `.about-hero`, `.about-portrait-card`, `.about-metadata-table`, `.editorial-timeline`, and `.about-graphic`.
- [x] **Step 2: Add Dark Mode Overrides**
  Modify `custom-dark.scss` to refine shadows, timeline borders, and SVG fill states for the dark theme.

### 2. Custom Interactive SVG Design
- [x] **Step 1: Create the Synthesis SVG (`fig. 2`)**
  Design a custom vector graphic representing the Venn diagram or connected graph of Hygor's core expertise pillars: **Systems Architecture**, **Machine Learning**, and **Domain Consulting**, using CSS variables for smooth pulse animations and hover glows.

### 3. Rebuild `about.qmd` with Bespoke Layout
- [x] **Step 1: Implement HTML/Markdown Structure**
  Replace `about.qmd` content with a clean structural grid utilizing Quarto's page-layout settings. Reuse the exact existing bio texts, education dates, and social URLs.

### 4. Build and Verify
- [x] **Step 1: Render and Preview Site**
  Run `task dev` to spin up the local server, verifying layout performance, responsiveness on mobile, and theme adaptation.

---

## Technical Implementation Notes

### Hide Default Quarto Title Header
We will use CSS parent selector logic to hide the default Quarto title banners on pages carrying the `.about-custom` anchor class, giving us complete control over the layout.

```scss
body:has(.about-custom) #title-block-header { display: none; }
body:has(.about-custom) .quarto-title-banner { display: none; }
```

### Layout Grid Composition
```
┌────────────────────────────────────────────────────────┐
│                        NAVBAR                          │
├──────────────────────────┬─────────────────────────────┤
│                          │                             │
│  [Profile Image]         │  "A bridge between..."      │
│  [Metadata Grid]         │  [Biography Paragraphs]     │
│  [Interactive SVG]       │                             │
│  "fig. 2 - alignment"    │  [Vertical Timeline]        │
│                          │                             │
└──────────────────────────┴─────────────────────────────┘
```

## Success Criteria
- The "About" page feels like an extension of the beautiful editorial "Monograph" style.
- Visual alignment with the homepage (matching fonts, layout asymmetry, and animated SVGs).
- Education details are presented in a structured timeline rather than plain text list.
- Fully functional and responsive in both light and dark modes.
