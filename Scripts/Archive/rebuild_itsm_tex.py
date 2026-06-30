from pathlib import Path
import re

root = Path(__file__).resolve().parent.parent
src = root / 'papers' / 'The-Anachronistic-Archive' / 'ITSM_Metaphysical_Synthesis_FIXED.tex'
dst = root / 'papers' / 'The-Anachronistic-Archive' / 'ITSM_Metaphysical_Synthesis_REBUILT.tex'
text = src.read_text(encoding='utf-8')

m = re.search(r'^(.*?\\begin\{document\})(.*?)(\\end\{document\})$', text, flags=re.S)
if not m:
    raise SystemExit('document environment not found')

preamble = m.group(1)
body = m.group(2)
footer = m.group(3)

# Remove only debug comments and tracing directives.
body = re.sub(r'(?m)^\s*%.*$', '', body)
body = re.sub(r'(?m)^\s*\\tracingifs\s*=\s*1\s*$', '', body)
body = body.replace('\\tracingifs=1', '')

# Collapse repeated blank lines while preserving LaTeX structure.
body = re.sub(r'(?m)^[ \t]+|[ \t]+$', '', body)
body = re.sub(r'\n{3,}', '\n\n', body).strip()

output = preamble + '\n' + body + '\n' + footer + '\n'
dst.write_text(output, encoding='utf-8')
print(f'Rebuilt file created at {dst}')
