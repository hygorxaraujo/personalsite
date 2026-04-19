# Improve new_post.py substitution Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Update `scripts/new_post.py` to also substitute the title in the first markdown cell (which currently contains `# Title`).

**Architecture:**
1. Modify `scripts/new_post.py` to identify the first markdown cell.
2. Replace `# Title` with `# {title}` in that cell.

**Tech Stack:** Python, `json`.

---

### Task 1: Update scripts/new_post.py to update markdown cell

**Objective:** Enhance `create_post` to locate the first markdown cell and update the title.

**Files:**
- Modify: `scripts/new_post.py`

**Step 1: Modify `scripts/new_post.py`**

Update the logic in `create_post`:

```python
    # Modify raw cell for frontmatter AND markdown cell for title
    markdown_updated = False
    for cell in data.get('cells', []):
        if cell.get('cell_type') == 'raw':
            # ... (existing frontmatter logic) ...
            source = cell.get('source', [])
            new_source = []
            for line in source:
                line = line.replace('\"Title\"', f'\"{title}\"')
                line = line.replace('\"YYYY-MM-DD\"', f'\"{current_date}\"')
                new_source.append(line)
            cell['source'] = new_source

        elif not markdown_updated and cell.get('cell_type') == 'markdown':
            source = cell.get('source', [])
            new_source = []
            for line in source:
                line = line.replace('# Title', f'# {title}')
                new_source.append(line)
            cell['source'] = new_source
            markdown_updated = True
```

---

**Plan complete. Shall I proceed with implementation?**
