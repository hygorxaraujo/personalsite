# Improve new_post.py substitution Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Modify `scripts/new_post.py` to automatically substitute `title` and `date` values into the newly created notebook file based on the template.

**Architecture:**
1. Read the newly copied `.ipynb` file.
2. Use Python's `json` module to parse the content.
3. Locate the `raw` cell containing the YAML frontmatter.
4. Replace the "Title" and "YYYY-MM-DD" placeholders with the actual values.
5. Save the updated JSON back to the target file.

**Tech Stack:** Python, `json`, `pathlib`, `datetime`.

---

### Task 1: Update scripts/new_post.py to read and update the template content

**Objective:** Enhance `create_post` to parse the notebook as JSON, update frontmatter, and save it.

**Files:**
- Modify: `scripts/new_post.py`

**Step 1: Modify `scripts/new_post.py`**

```python
import json

def update_frontmatter(file_path, title, date):
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Locate frontmatter cell
    for cell in data.get('cells', []):
        if cell.get('cell_type') == 'raw':
            source = cell.get('source', [])
            new_source = []
            for line in source:
                line = line.replace('Title', title)
                line = line.replace('YYYY-MM-DD', date)
                new_source.append(line)
            cell['source'] = new_source
            break
            
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=1)
```

And update `create_post` to call this function.

**Step 2: Commit**

```bash
git add scripts/new_post.py
git commit -m \"feat: add frontmatter substitution to new_post.py\"
```

---

**Plan complete. Shall I proceed with implementation using subagent-driven-development?**
