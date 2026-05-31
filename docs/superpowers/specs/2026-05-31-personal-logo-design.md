# Personal Brand Logo — "Node-H" — Design Spec

**Date:** 2026-05-31
**Owner:** Hygor X. Araújo
**Status:** Approved (design), implementing

## Goal
A personal-brand logo for the Quarto personal site, cohesive with the existing
**"Monograph"** design system (emerald editorial + recurring knowledge-graph motif).
Replace the placeholder `assets/favicon.ico` and add scalable logo assets.

## Concept: "Node-H"
The letter **H** takes the role of the hero's emphasized "hot center node": an emerald
node-chip carrying a serif **H**, surrounded by a small asymmetric knowledge-graph
constellation (satellite nodes + edges) echoing the hero SVG and post-header banners.

## Design tokens (from `custom.scss`)
- paper `#FAFAF7`, ink `#13171A`
- emerald `#0B7A52`, emerald-deep `#075037`, emerald-tint `#E9F3EE`, rule `#E5E3DC`
- dark: emerald `#34C088`, highlight `#6FE0AD`, paper `#14161A`

## Mark geometry (100×100 viewBox)
- Central node: rounded-square chip, emerald fill, serif **H** in paper, ~45% of canvas.
- 5 satellite nodes: filled circles r∈[3,6], asymmetric placement (not a ring).
- Edges: thin emerald lines, reduced opacity, center→satellite + 2 satellite→satellite.
- Light variant: emerald on transparent. Dark variant: brighter emerald `#34C088`.

## Deliverables (→ `assets/`)
| File | Notes |
|------|-------|
| `logo.svg`, `logo-dark.svg` | Vector source; `font-family: Newsreader, Georgia, serif` |
| `logo-512.png`, `logo-256.png`, `logo-512-dark.png` | Raster, transparent bg |
| `apple-touch-icon-180.png` | Solid paper bg for iOS |
| `favicon.ico` | Multi-res 16/32/48; **simplified** mark (H-node + 3 dots) |
| `logo-wordmark.svg`, `logo-wordmark.png` | Mark + "Hygor X. Araújo" in serif |

## Build pipeline
System has ImageMagick + Pillow but **no SVG rasterizer** (no librsvg/inkscape).
- SVG = hand-authored vector source (web uses Newsreader, already loaded by Quarto).
- PNG + ICO = **rendered by Pillow** (shapes + serif H), not by rasterizing the SVG —
  avoids the missing-renderer problem and gives pixel-perfect favicon control.
- Serif font: fetch OFL Newsreader TTF for raster fidelity; fall back to system Noto Serif.
- Generator script: `src/scripts/generate_logo.py` (entry point `gen-logo`, mirrors `gen-header`).

## Favicon simplification rationale
A 16×16 favicon (~256px) cannot carry 5 satellites + edges legibly. The ICO uses a
reduced mark (central H-node + 3 dots) so it stays readable at navbar/tab size.

## Out of scope
- No `_quarto.yml` navbar logo swap unless requested (current uses `profile.jpg`).
- favicon.ico path already wired in `_quarto.yml`; replacing the file is sufficient.
