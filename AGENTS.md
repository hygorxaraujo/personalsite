# Project Context: Personal Site

## Project Overview
This project is the personal website and blog of Hygor, built using [Quarto](https://quarto.org/). It is a static site that renders content from Markdown (`.qmd`) and Jupyter Notebook (`.ipynb`) files. The project uses Python for notebook execution and manages dependencies with `uv`.

## Constraints
- **No content generation:** The agent must not write blog posts, articles, or documentation. It acts as a technical assistant only.

## Technology Stack
- **Framework:** Quarto (Static Site Generator)
- **Language:** Python 3.12 (managed by `uv`)
- **Theme:** `zephyr` (light) / `darkly` (dark) + custom SCSS
- **Key Python Libraries:** `pandas`, `matplotlib`, `plotly`, `seaborn`, `polars`, `scipy`, `pdfplumber`, `jupyterlab`
- **Dev Tools:** `ruff` (linting), `pytest` (testing)

## Development Workflow

### Prerequisites
- Quarto CLI installed
- Python installed
- `uv` package manager installed
- Task (for automation)

### Common Commands
Use `Taskfile.yml` for automation.

**Install/Sync Dependencies:**
```bash
uv sync
```

**Run Development Server (Preview):**
```bash
task dev
```

**Render Site (Build):**
Build the static site to the `_site/` directory.
```bash
task build
```

**Clean Generated Files:**
```bash
task clean
```

**Scaffold New Post:**
```bash
task new_post TITLE="My New Post"
```

**Publish:**
Publish the site to GitHub Pages.
```bash
task publish
```

**Inject Jupyter Notebook SEO:**
Run helper utility to insert description/title metadata safely inside `.ipynb` JSON cells.
```bash
python3 scripts/add_post_seo.py posts/my-post.ipynb "My post description snippet." "Optional Title"
```

**Generate Header:**
Generate gem mesh SVG header (entry point in pyproject.toml).
```bash
gen-header
```

## Project Structure
- **`_quarto.yml`**: Main configuration file for the Quarto website (theme, navigation, metadata).
- **`posts/`**: Contains the blog posts. Supports `.qmd` and `.ipynb` files. Named `YYYY-MM-DD-slug.ipynb` or `.qmd`.
  - **`posts/_metadata.yml`**: Shared post defaults (author, default header image, freeze).
- **`index.qmd`**: The homepage of the site (blog listing).
- **`about.qmd`**: The "About" page.
- **`pyproject.toml`**: Python project configuration and dependency definitions.
- **`uv.lock`**: Lock file for reproducible Python environments.
- **`custom.scss`**: Shared custom styles (light + dark modes).
- **`custom-dark.scss`**: Dark-mode-only overrides.
- **`assets/`**: Images, favicon, profile photos, and generated headers.
- **`templates/`**: Template files (e.g., `post-template.ipynb` used by `task new_post`).
- **`scripts/`**: Automation scripts (e.g., `new_post.py`).
- **`src/scripts/`**: Source scripts for project tools (e.g., `generate_gem_mesh_svg.py`).
- **`docs/`**: Documentation directory.
  - **`docs/adrs/`**: Architectural Decision Records (MADRs format).
  - **`docs/sprints/`**: Sprint plans (e.g., `<number>_<name>.md`).
  - **`docs/plans/`**: Implementation plans.
- **`_freeze/`**: Stores computational results to avoid re-executing notebooks unnecessarily.
- **`_site/`**: The generated static website (output directory).

## Conventions
- **Planning:** We will always plan what should be done first as sprints in the `docs/sprints/<current_year>` directory. Follow the file name convention "<sprint_number>_<sprint_name>.md" and always save the planning to this location. No changes will be made to ClickUp until the plan has been reviewed and approved by you.
- **Project changes:** Structural changes should be first documented as Architectural Decision Records (ADRs) on `docs/adrs` following the file name convention and using the Markdown Architectural Decision Records (MADRs) template.
- **Execution:** Quarto executes code cells in `.ipynb` files during rendering. Ensure the Python environment (managed by `uv`) is active or accessible to Quarto.

## Gotchas / Quirks
- **Styles:** `styles.css` does NOT exist. Use `custom.scss` (shared) and `custom-dark.scss` (dark mode overrides).
- **SEO Preview Images:** Social media crawlers (LinkedIn, X, Slack, Facebook) do **NOT** support SVG images for social previews. The global fallback image in `_quarto.yml` is set to `assets/profile.jpg` (JPEG) to prevent broken social cards while retaining dynamic SVGs on-site.
- **Notebook Edits:** Jupyter Notebooks (`.ipynb`) are JSON files with embedded raw cells. Do not attempt direct regex/string edits as they are structurally blocked. Use `scripts/add_post_seo.py` for safe parsing and updates.
- **Notebook caching:** The `_freeze/` directory caches notebook output. Run `task clean` if outputs seem stale or aren't updating.
- **Environment:** Quarto needs the `uv` environment active to run cells during render.
