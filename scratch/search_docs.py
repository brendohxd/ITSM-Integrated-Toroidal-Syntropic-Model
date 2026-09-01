import os
import re

docs_dir = 'docs'
pattern = re.compile(r'(Freeze α|alpha\.13|UVIR-003|MAT-001|STAT-001|Theoretical Core|Cleared|0\.62|8\.57|zero free parameter)', re.IGNORECASE)

with open('scratch/docs_search.log', 'w', encoding='utf-8') as out:
    for root, _, files in os.walk(docs_dir):
        for f in files:
            if f.endswith('.html'):
                path = os.path.join(root, f)
                with open(path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                    for i, line in enumerate(lines):
                        if pattern.search(line):
                            out.write(f'{f}:{i+1}: {line.strip()}\n')
