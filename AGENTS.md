# Gemini Project Context: Personal Site

## Project Overview
This project is the personal website and blog of Hygor, built using [Quarto](https://quarto.org/). It is a static site that renders content from Markdown (`.qmd`) and Jupyter Notebook (`.ipynb`) files. The project uses Python for notebook execution and manages dependencies with `uv`.

## Technology Stack
- **Framework:** Quarto (Static Site Generator)
- **Language:** Python 3.12
- **Package Manager:** `uv`
- **Key Python Libraries:** `pandas`, `matplotlib`, `plotly`, `seaborn`, `jupyterlab`

## Development Workflow

### Constraints
- **No content generation:** The agent must not write blog posts, articles, or documentation. It acts as a technical assistant only.

### Prerequisites
- Quarto CLI installed
- Python installed
- `uv` package manager installed
- Task (for automation)

### Common Commands
Use `Taskfile.yml` for automation.

**Install Dependencies:**
```bash
uv sync
```

**Run Development Server (Preview):**
```bash
task preview
```

**Render Site (Build):**
Build the static site to the `_site/` directory.
```bash
task render
```

**Publish:**
Publish the site to GitHub Pages.
```bash
task publish
```

## Project Structure

- **`_quarto.yml`**: Main configuration file for the Quarto website (theme, navigation, metadata).
- **`posts/`**: Contains the blog posts. Supports `.qmd` and `.ipynb` files.
- **`index.qmd`**: The homepage of the site.
- **`about.qmd`**: The "About" page.
- **`pyproject.toml`**: Python project configuration and dependency definitions.
- **`uv.lock`**: Lock file for reproducible Python environments.
- **`styles.css`**: Custom CSS for styling the website.
- **`_freeze/`**: Stores computational results to avoid re-executing notebooks unnecessarily.
- **`_site/`**: The generated static website (output directory).

## Conventions
- **Planning:** We will always plan what should be done first as sprints in the `docs/sprints/<current_year>` directory. Follow the file name convention "<sprint_number>_<sprint_name>.md" and always save the planning to this location. No changes will be made to ClickUp until the plan has been reviewed and approved by you.
- **Project changes:** Structural changes should be first documented as Architectural Decision Records (ADRs) on `docs/adrs` following the file name convention and using the Markdown Architectural Decision Records (MADRs) template.
- **Content:** Blog posts are located in the `posts/` directory. Each post is typically its own folder or file.
- **Execution:** Quarto executes code cells in `.ipynb` files during rendering. Ensure the Python environment (managed by `uv`) is active or accessible to Quarto.
- **Theme:** The site uses the `flatly` theme for light mode and `darkly` for dark mode, configured in `_quarto.yml`.
