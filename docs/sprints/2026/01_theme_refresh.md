# Sprint: Theme Refresh & Visual Identity (March 2026)

## Overview
This sprint focuses on modernizing the visual identity of the blog to better reflect its technical content (AI, Data Science, Linux, and Automation). The goal is to move away from the default Bootstrap look towards a more "technical and polished" aesthetic.

## Goals
1. **Technical Aesthetics:** Transition to a theme that feels more "precise" and "modern," suitable for a blog about AI and Data Science.
2. **Improved Readability:** Optimize typography for long-form technical reading and code snippet legibility.
3. **Visual Impact:** Replace the standard list-style homepage with a more dynamic grid layout with high-quality thumbnails.
4. **Cohesive Dark/Light Modes:** Refine the color palettes for both modes to ensure a consistent brand feel.

## Tasks

### 1. Research & Theme Selection
- [x] Evaluate Quarto base themes (`lux`, `zephyr`, `cosmo`, `yeti`). (Selected: **Zephyr** for light, **Darkly** for dark)
- [x] Select a primary accent color that represents "AI/Data Science" (Selected: **Emerald Green** `#198754`)
- [x] Research and choose typography: (Selected: **Tech-Forward**)
    - **Body:** Inter
    - **Headings:** Space Grotesk
    - **Code:** JetBrains Mono

### 2. Base Configuration Updates (`_quarto.yml`)
- [x] Update `format.html.theme` to the selected base theme.
- [x] Configure `listing` in `index.qmd` to use `type: grid` for better visual impact.
- [x] Enable `image-height: 200px` or similar for post thumbnails.
- [x] Ensure `back-to-top-navigation` and `page-navigation` are optimized.

### 3. Custom SCSS Development
- [x] Create `custom.scss` to handle Bootstrap overrides.
- [x] Implement the selected typography via Google Fonts or local imports.
- [x] Customize code block styling (colors, borders, and shadows) to make them "pop" as technical content.
- [x] Add subtle technical details:
    - [x] Subtle grid pattern background for the body or header.
    - [x] Hover effects for post cards on the listing page.
    - [x] Custom scrollbar styling for a polished look.

### 4. Homepage (Hero Section) Redesign
- [x] Add a prominent "Hero" section to `index.qmd` using a custom div class.
- [x] Include a brief, punchy description of the blog's focus (AI, Data Science, Engineering).
- [ ] (Optional) Add a "Featured Post" section above the main listing.

### 5. Post Metadata & Thumbnails
- [x] Update `posts/_metadata.yml` or individual posts to ensure all have relevant `image` metadata for the grid listing.
- [x] Standardize the display of categories/tags on the listing cards.

### 6. Validation & Testing
- [ ] Verify responsiveness on mobile, tablet, and desktop.
- [ ] Test both Light and Dark modes for accessibility and contrast.
- [ ] Check page load performance (especially with new fonts).

## Technical Implementation Notes
- **Quarto Customization:** We will use the `theme: [selected-theme, custom.scss]` syntax to allow for surgical overrides while maintaining the stability of a base Bootswatch theme.
- **Listing Type:** Switching `index.qmd` from `default` to `grid` listing will require ensuring that each post has a fallback or explicit thumbnail image.

## Success Criteria
- The blog feels distinctly "technical" rather than "generic Bootstrap."
- Code snippets are easy to read and aesthetically pleasing.
- The homepage provides a clear, visually engaging entry point for new readers.
