# ADR 001: Visual Identity and "The Neural Network" Color Palette

**Status:** Accepted  
**Date:** 2026-03-15  
**Decider:** Hygor (User) & Gemini CLI  

## Context and Problem Statement

The personal brand and website (hygorxaraujo.com) require a cohesive visual identity that reflects its focus on technical subjects: AI, Data Science, Linux, and Agentic Workflows. The existing "Emerald Green" anchor needs a supporting palette to move away from generic "Bootstrap-style" aesthetics toward a precise, high-performance "Technical" look.

## Decision Drivers

*   **Industry Alignment:** The palette should feel "AI-native" (comparable to modern developer tools like Cursor, Vercel, or OpenAI).
*   **Accessibility:** High contrast is required for long-form technical reading and code snippet legibility.
*   **Typography Synergy:** Colors must complement the geometric nature of *Space Grotesk* and the clarity of *Inter*.
*   **Thematic Consistency:** Support both light and dark modes with a unified brand "feel."

## Considered Options

1.  **"The Neural Network" (Chosen):** High-tech, deep contrast, "Cyberpunk" professional.
2.  **"The Data Lab":** Clean, scientific, "Published Paper" aesthetic.

## Decision Outcome

Chosen Option: **"The Neural Network"**. This option was selected because it best represents the "future-forward" nature of agentic workflows and AI. It creates a distinct, "tool-like" atmosphere that separates the blog from standard lifestyle or general tech blogs.

### The Color Palette

| Role | Color Name | Hex Code | Usage |
| :--- | :--- | :--- | :--- |
| **Brand Anchor** | Emerald Tech | `#198754` | Primary identity, logos, active links, main borders. |
| **Deep Contrast** | Obsidian Indigo | `#1B1B3A` | Secondary branding, hero section accents, deep UI shadows. |
| **Highlight/Glow** | Neon Mint | `#00FF87` | Hover states, success indicators, code block accents. |
| **Dark Base** | Dark Slate | `#0F172A` | Background for dark mode, footer, code block backgrounds. |
| **Data Accent** | Electric Violet | `#7C3AED` | Tertiary accent for data visualizations or "AI" specific labels. |

## Implementation Strategy

1.  **SCSS Variables:** Define these colors as `$brand-*` variables in `custom.scss`.
2.  **Hero Section:** Update the `.hero-banner` in `index.qmd` to utilize the `Obsidian Indigo` and `Emerald Tech` gradient or border style.
3.  **Code Blocks:** Adjust syntax highlighting or code block borders to use the `Neon Mint` highlight for a "glowing" effect.
4.  **Logo/Assets:** Any future logos or social preview images should strictly adhere to this palette.

## Pros and Cons of the Chosen Option

### Pros
*   **Distinctive:** High-contrast indigo/emerald is less common than blue/gray, aiding brand recall.
*   **Technical:** Naturally evokes a "terminal" or "IDE" feel, which resonates with the target audience.
*   **Scalable:** The addition of *Electric Violet* allows for complex data visualizations that remain on-brand.

### Cons
*   **Dark-Mode Bias:** This palette is heavily optimized for dark mode; light mode implementation requires careful balancing of saturation to avoid "vibrancy fatigue."
