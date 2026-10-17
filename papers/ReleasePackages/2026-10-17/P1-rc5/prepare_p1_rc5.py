"""Exclusive-create local P1 rc5 package/verification artifacts; no release."""
import argparse
import hashlib
import json
import math
import re
import shutil
import subprocess
import zipfile
from pathlib import Path

from pypdf import PdfReader

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
P1 = ROOT / 'papers/P1-Scale-Matching-Reconstruction'
P2 = ROOT / 'papers/P2-Rectangular-T3-Casimir'
WORK = ROOT / '.local/p1-rc5'
STEM = 'Boyd_2026_Present-Epoch_Scale_Matching_Cobs_Hygiene_v0.2.0-rc5'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def emit(path, data):
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(data, stream, sort_keys=True, indent=2)
        stream.write('\n')


def anchor(path):
    with path.with_name(path.name + '.sha256').open('x', encoding='ascii', newline='\n') as stream:
        stream.write(f'{sha(path)}  {path.name}\n')


def text(path):
    reader = PdfReader(path)
    return re.sub(r'\s+', ' ', ' '.join(page.extract_text() for page in reader.pages)), len(reader.pages)


def prepare():
    assert sha(HERE / 'preserved_rc4/main.tex') == '2dddcba884df60dd8f990ee03a65e219b831540817569927af1164f9e099f8f8'
    old = P1 / 'Boyd_2026_Present-Epoch_Scale_Matching_Cobs_Hygiene_v0.2.0-rc4.pdf'
    assert sha(old) == '7420175e4d8bc0f776ca89d7e77d388aa5bf7a535c5eb19614d4baedc23aeee5'
    assert sha(P2 / 'main.tex') == '28cdc396e9a09221ac92b850e048f58f08837aba2efaec0a68033d3e8ac7c51a'
    protected = [old, old.with_name(old.name + '.sha256')]
    protected += [p for p in (HERE.parent / 'P1_P2_rc4').rglob('*') if p.is_file()]
    protected += [p for p in P2.rglob('*') if p.is_file() and p.suffix in {'.tex', '.bib', '.md', '.txt', '.pdf', '.sha256'}]
    protected += [P2 / 'VERSION']
    emit(HERE / 'preservation_baseline.json', {str(p.relative_to(ROOT)): sha(p) for p in protected})
    portable = HERE / 'portable'
    (portable / 'figures').mkdir(parents=True, exist_ok=False)
    source = (P1 / 'main.tex').read_text(encoding='utf-8')
    normalized, count = re.subn(r'\\graphicspath\{[^\n]*\}', lambda _: r'\graphicspath{{figures/}}', source)
    assert count == 1
    with (portable / 'main.tex').open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(normalized)
    for name in ('references.bib', 'VERSION'):
        shutil.copy2(P1 / name, portable / name)
    shutil.copy2(P1 / 'figures/itsm_t3_fundamental_domain.pdf', portable / 'figures/itsm_t3_fundamental_domain.pdf')
    print('PREPARED P1 rc5 portable source and preservation baseline')


def build(portable, compiler):
    project = HERE / 'portable' if portable else P1
    output = WORK / ('portable-build' if portable else 'build')
    output.mkdir(parents=True, exist_ok=True)
    result = subprocess.run([compiler, '-X', 'compile', '--untrusted',
                             '--keep-logs', '--keep-intermediates', '--outdir',
                             str(output), 'main.tex'], cwd=project, check=False)
    raise SystemExit(result.returncode)


def seal():
    baseline = json.loads((HERE / 'preservation_baseline.json').read_text(encoding='utf-8'))
    assert all(sha(ROOT / rel) == expected for rel, expected in baseline.items())
    h0 = 70 * 1000 / 3.085677581491367e22
    a0 = 299792458 * h0 / (2 * math.pi)
    same_scale = math.sqrt(2 / 3)
    empirical_scale = ((4 * a0 / 9) / 1.2e-10) ** 0.25
    assert math.isclose(same_scale ** 4, 4 / 9, rel_tol=1e-14)
    assert round(100 * (1 - same_scale), 2) == 18.35
    assert round(100 * (1 - empirical_scale), 2) == 20.43
    assert round(same_scale, 4) == 0.8165 and round(empirical_scale, 4) == 0.7957
    assert (P1 / 'references.bib').read_bytes() == (HERE / 'preserved_rc4/references.bib').read_bytes()
    source = (P1 / 'main.tex').read_text(encoding='utf-8')
    old_source = (HERE / 'preserved_rc4/main.tex').read_text(encoding='utf-8')
    action_pattern = r'\\begin\{align\}\s*S_\{\\mathrm\{WF\}\}.*?\\label\{eq:SWF\}.*?\\end\{align\}'
    assert re.search(action_pattern, source, re.S).group() == re.search(action_pattern, old_source, re.S).group()
    canonical_text, pages = text(WORK / 'build/main.pdf')
    portable_text, portable_pages = text(WORK / 'portable-build/main.pdf')
    assert canonical_text == portable_text and pages == portable_pages
    assert '0.2.0-rc5' in canonical_text and '??' not in canonical_text
    assert not re.search(r'\[\s*\?', canonical_text)
    log_warnings = {}
    for build in ('build', 'portable-build'):
        log = (WORK / build / 'main.log').read_text(encoding='utf-8', errors='replace')
        for failure in ('undefined', 'Overfull', 'Missing character', '! LaTeX Error'):
            assert failure not in log, (build, failure)
        log_warnings[build] = {'underfull': log.count('Underfull'), 'float_warning': 'float is stuck' in log,
                               'log_sha256': sha(WORK / build / 'main.log')}
    portable = HERE / 'portable'
    shutil.copy2(WORK / 'portable-build/main.bbl', portable / 'main.bbl')
    pdf = P1 / (STEM + '.pdf')
    if pdf.exists():
        raise FileExistsError(pdf)
    shutil.copy2(WORK / 'build/main.pdf', pdf)
    anchor(pdf)
    archive = HERE / 'ITSM_P1_source_v0.2.0-rc5_2026-10-17.zip'
    with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED) as bundle:
        for path in sorted(portable.rglob('*')):
            if path.is_file():
                info = zipfile.ZipInfo(path.relative_to(portable).as_posix(), (2026, 10, 17, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                bundle.writestr(info, path.read_bytes())
    with zipfile.ZipFile(archive) as bundle:
        assert bundle.testzip() is None
        assert bundle.read('main.tex') == (portable / 'main.tex').read_bytes()
    anchor(archive)
    record = {'version': '0.2.0-rc5', 'local_validation_pass': True,
              'physics_pass': False, 'publication_ready': False,
              'author_final_verification': 'PENDING', 'independent_review': 'PENDING',
              'pages': pages, 'canonical_portable_text_identical': True,
              'preserved_artifact_count': len(baseline), 'p2_unchanged': True,
              'source_sha256': sha(P1 / 'main.tex'), 'pdf_sha256': sha(pdf),
              'source_zip_sha256': sha(archive), 'verification_script_sha256': sha(Path(__file__)),
              'preservation_baseline_sha256': sha(HERE / 'preservation_baseline.json'),
              'a0_at_H0_70_m_s2': a0, 'a_eff_m_s2': 4 * a0 / 9,
              'same_a0_velocity_ratio': same_scale, 'same_a0_velocity_reduction_percent': 100 * (1 - same_scale),
              'empirical_scale_velocity_ratio': empirical_scale,
              'empirical_scale_velocity_reduction_percent': 100 * (1 - empirical_scale),
              'action_bibliography_unchanged': True, 'build_warnings': log_warnings,
              'members': {str(p.relative_to(portable)): sha(p) for p in portable.rglob('*') if p.is_file()}}
    emit(HERE / 'P1_RC5_MANIFEST.json', record)
    anchor(HERE / 'P1_RC5_MANIFEST.json')
    print(json.dumps({'local_validation_pass': True, 'pages': pages, 'p2_unchanged': True,
                      'physics_pass': False, 'publication_ready': False}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage', choices=('prepare', 'build', 'portable-build', 'seal'))
    parser.add_argument('--compiler')
    args = parser.parse_args()
    if args.stage == 'prepare':
        prepare()
    elif args.stage == 'seal':
        seal()
    else:
        assert args.compiler is not None
        build(args.stage == 'portable-build', args.compiler)
