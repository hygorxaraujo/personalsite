#!/usr/bin/env python3
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime
import re


def slugify(text):
    return re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")


def create_post(title):
    if not title:
        raise ValueError("Title cannot be empty.")

    template = Path("templates/post-template.ipynb")
    if not template.exists():
        raise FileNotFoundError("Template file not found.")

    target_dir = Path("posts")
    target_dir.mkdir(parents=True, exist_ok=True)

    current_date = datetime.now().strftime("%Y-%m-%d")
    slug = slugify(title)
    target_file = target_dir / f"{current_date}-{slug}.ipynb"

    if target_file.exists():
        raise FileExistsError("Post with the same title already exists.")

    # Load template
    with open(template, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Modify raw cell for frontmatter and first markdown cell for title
    found_markdown = False
    for cell in data.get("cells", []):
        if cell.get("cell_type") == "raw":
            source = cell.get("source", [])
            new_source = []
            for line in source:
                line = line.replace('"Title"', f'"{title}"')
                line = line.replace('"YYYY-MM-DD"', f'"{current_date}"')
                new_source.append(line)
            cell["source"] = new_source
        elif not found_markdown and cell.get("cell_type") == "markdown":
            source = cell.get("source", [])
            new_source = []
            for line in source:
                new_source.append(line.replace("# Title", f"# {title}"))
            cell["source"] = new_source
            found_markdown = True

    # Save modified notebook
    with open(target_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1)

    print(f"Post created at: {target_file}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: Invalid number of arguments.")
        print("Usage: new_post.py <title>")
        sys.exit(1)
    create_post(sys.argv[1])
