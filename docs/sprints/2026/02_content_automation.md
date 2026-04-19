---
name: plan
description: Sprint Plan for April 2026 - Content Pipeline Automation
---

# Sprint: Content Pipeline Automation (April 2026)

## Overview
This sprint focuses on streamlining the content creation and deployment pipeline for the blog. With the visual identity established in March, we now need to automate the workflow for drafting, rendering, and publishing to minimize manual effort and ensure consistency.

## Goals
1. **Automation:** Implement a `Taskfile.yml` driven workflow for local development and deployment.
2. **Efficiency:** Configure Quarto to use `_freeze` effectively to reduce build times.
3. **Content Organization:** Establish a robust directory structure for future posts and drafts.
4. **Integration:** Ensure the local dev environment is fully synced with `uv`.

## Tasks

### 1. Workflow Automation
- [x] Create `Taskfile.yml` tasks for:
    - `dev`: Start live reload server.
    - `build`: Render site to `_site/` directory.
    - `clean`: Remove `_site/` and `_freeze/` folders.
    - `sync`: Sync python dependencies.

### 2. Quarto Optimization
- [x] Verify `_quarto.yml` configuration for `execute` settings (use `freeze: true`).
    - [x] Add `_freeze/` to `.gitignore`.
    - [x] Test incremental builds to ensure performance.

### 3. Content Infrastructure
- [x] Keep current post directory structure.
- [x] Create a templates directory (`templates/`) with a `post-template.ipynb` containing boilerplate YAML metadata in the first cell.
- [x] Automate new post creation from template and validate generation.

### 4. Validation & Testing
- [ ] Verify all existing content renders correctly with the new automation.
- [ ] Run a test build to confirm `_freeze` is working.

## Risks & Open Questions
- **Complexity:** Keeping the `Taskfile.yml` simple enough for easy maintenance.
- **Environment:** Ensuring `uv` and Quarto versions are aligned across different environments.

## Success Criteria
- A single `task` command handles the full build/preview lifecycle.
- Build times are significantly reduced through `_freeze`.
- Content creation is standardized via templates.
