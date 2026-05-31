#!/usr/bin/env python3
import json
import sys

def add_seo(filepath, description, title=None):
    with open(filepath, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    source = nb['cells'][0]['source']
    
    has_description = False
    has_title = False
    
    # Check existing keys and update them
    for i, line in enumerate(source):
        if line.strip().startswith('description:'):
            source[i] = f'description: "{description}"\n'
            has_description = True
        if line.strip().startswith('title:'):
            if title:
                source[i] = f'title: "{title}"\n'
            has_title = True
            
    # If not found, insert before the closing '---'
    if not has_description:
        for i in range(len(source) - 1, -1, -1):
            if source[i].strip() == '---':
                source.insert(i, f'description: "{description}"\n')
                break
                
    if title and not has_title:
        for i in range(len(source) - 1, -1, -1):
            if source[i].strip() == '---':
                source.insert(i, f'title: "{title}"\n')
                break

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
        f.write('\n')

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 add_post_seo.py <filepath> <description> [title]")
        sys.exit(1)
    
    path = sys.argv[1]
    desc = sys.argv[2]
    t = sys.argv[3] if len(sys.argv) > 3 else None
    
    add_seo(path, desc, t)
    print(f"Successfully updated SEO metadata in {path}")
