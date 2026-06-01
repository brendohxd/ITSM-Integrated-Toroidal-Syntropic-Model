import os, sys, requests, json, shutil
from zipfile import ZipFile, ZIP_DEFLATED
import urllib3
urllib3.disable_warnings()

ACCESS_TOKEN = 'y4Ht4vMx2SuaXKXKahmly4Mk7vPjVuekxPlfTIb3fOsTHl1IhS3ab52hron0'
old_id = '20466198'
params = {'access_token': ACCESS_TOKEN}
headers = {'Content-Type': 'application/json'}

print("[*] Preparing arXiv Bundle...")
os.makedirs('arXiv_Bundle/Figures', exist_ok=True)
shutil.copy('Manuscript/Main.tex', 'arXiv_Bundle/Main.tex')
shutil.copy('Manuscript/Main.pdf', 'arXiv_Bundle/Main.pdf')
shutil.copy('Manuscript/MainNotes.bib', 'arXiv_Bundle/MainNotes.bib')
for f in os.listdir('Assets/Figures'):
    if f.endswith('.png'):
        shutil.copy(os.path.join('Assets/Figures', f), os.path.join('arXiv_Bundle/Figures', f))

print("[*] Zipping arXiv Bundle...")
with ZipFile('ITSM_arXiv_Submission.zip', 'w', ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk('arXiv_Bundle'):
        for f in files:
            file_path = os.path.join(root, f)
            arcname = os.path.relpath(file_path, 'arXiv_Bundle')
            zf.write(file_path, arcname)

print("[*] Zipping Computational Engines...")
ignore_dirs = {'.git', 'scratch', 'arXiv_Bundle', '__pycache__', '.tempmediaStorage'}
ignore_exts = {'.zip'}
with ZipFile('ITSM_Computational_Engines_v9.8.1.zip', 'w', ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for f in files:
            if not any(f.endswith(ext) for ext in ignore_exts):
                file_path = os.path.join(root, f)
                arcname = os.path.relpath(file_path, '.')
                zf.write(file_path, arcname)

print("[*] Creating new version on Zenodo...")
r = requests.post(f'https://zenodo.org/api/deposit/depositions/{old_id}/actions/newversion', verify=False, params=params)
if r.status_code != 201:
    print("Error creating new version:", r.json())
    sys.exit(1)

new_draft_url = r.json()['links']['latest_draft']
r = requests.get(new_draft_url, verify=False, params=params)
new_deposition = r.json()
new_id = new_deposition['id']
bucket_url = new_deposition['links']['bucket']

print(f"[*] New Draft ID: {new_id}")

print('[*] Clearing legacy files from draft...')
files_url = f'https://zenodo.org/api/deposit/depositions/{new_id}/files'
r = requests.get(files_url, verify=False, params=params)
for f in r.json():
    print(f'    - Deleting {f["filename"]}...')
    requests.delete(f['links']['self'], verify=False, params=params)

files_to_upload = ['ITSM_Computational_Engines_v9.8.1.zip', 'ITSM_arXiv_Submission.zip']
for filename in files_to_upload:
    print(f'[*] Uploading {filename}...')
    with open(filename, 'rb') as fp:
        r = requests.put(f'{bucket_url}/{filename}', verify=False, data=fp, params=params)
    if r.status_code == 201:
        print(f'    - {filename} uploaded successfully!')
    else:
        print(f'    - {filename} upload failed: {r.json()}')

print('[*] Updating metadata...')
metadata_url = f'https://zenodo.org/api/deposit/depositions/{new_id}'
new_deposition['metadata']['version'] = 'v9.8.1'
r = requests.put(metadata_url, verify=False, params=params, data=json.dumps({'metadata': new_deposition['metadata']}), headers=headers)
if r.status_code == 200:
    print('[+] SUCCESS! Draft assembled: https://zenodo.org/deposit/' + str(new_id))
else:
    print('[!] Metadata update failed:', r.json())
