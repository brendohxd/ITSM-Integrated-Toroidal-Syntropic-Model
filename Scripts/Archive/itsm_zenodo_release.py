"""
Utility script to prepare the repository for Zenodo distribution.
Packages codebase, assets, and documentation into structured release artifacts.
"""
import os
import sys
import requests
import json
import zipfile

# SECURITY: Never hardcode tokens. Set ZENODO_TOKEN as an environment variable:
#   Windows: $env:ZENODO_TOKEN = 'your_token_here'
#   Linux/Mac: export ZENODO_TOKEN='your_token_here'
ACCESS_TOKEN = os.environ.get('ZENODO_TOKEN')
if not ACCESS_TOKEN:
    print("[!] ERROR: ZENODO_TOKEN environment variable not set.")
    print("    Provide the token in the terminal before running:")
    print("    $env:ZENODO_TOKEN = 'your_token_here'")
    sys.exit(1)
DEPOSITION_ID = '20774996'

VERSION = "v11.3.1"
ZIP_NAME = f"ITSM_Computational_Framework_{VERSION}.zip"

def create_framework_zip():
    print(f"[*] Packaging computational framework into {ZIP_NAME}...")
    dirs_to_zip = ["Scripts", "SPARC_data", "DESI_data", "NANOGrav_data"]
    files_to_zip = ["environment.yml", "README.md", "CHANGELOG.md"]
    
    with zipfile.ZipFile(ZIP_NAME, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for f in files_to_zip:
            if os.path.exists(f):
                zipf.write(f)
        for d in dirs_to_zip:
            if os.path.exists(d):
                for root, _, files in os.walk(d):
                    # Skip __pycache__ and results dumps if needed, but keeping simple for now
                    if "__pycache__" in root or "results" in root:
                        continue
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path)
    print(f"    [+] {ZIP_NAME} created successfully.")

print(f"[*] Starting Zenodo release automation for base ID: {DEPOSITION_ID}")

# 0. Create ZIP
create_framework_zip()

params = {'access_token': ACCESS_TOKEN}
headers = {"Content-Type": "application/json"}

# 1. Create a new version
print("[*] Creating a new version draft...")
url = f"https://zenodo.org/api/deposit/depositions/{DEPOSITION_ID}/actions/newversion"
r = requests.post(url, verify=True, params=params)
if r.status_code != 201:
    print(f"[!] Failed to create new version: {r.json()}")
    sys.exit(1)

new_version_url = r.json()['links']['latest_draft']

# 2. Get the new deposition details
print("[*] Retrieving new version details...")
r = requests.get(new_version_url, verify=True, params=params)
new_deposition = r.json()
new_id = new_deposition['id']
bucket_url = new_deposition['links']['bucket']

print(f"[*] New deposition ID created: {new_id}")

# 3. Clear existing files in the draft (so we can replace with fresh ones)
print("[*] Clearing legacy files from the draft...")
files_url = f"https://zenodo.org/api/deposit/depositions/{new_id}/files"
r = requests.get(files_url, verify=True, params=params)
for f in r.json():
    print(f"    - Deleting {f['filename']}...")
    del_r = requests.delete(f['links']['self'], verify=True, params=params)

# 4. Upload the payload files
files_to_upload = {
    ZIP_NAME: ZIP_NAME,
    f"ITSM_Core_Cosmology_{VERSION}.pdf": f"Manuscript/ITSM_Core_Cosmology_{VERSION}.pdf",
    "Supplementary_SPARC_Parameter_Ledger.pdf": "Manuscript/Supplementary/Supplementary.pdf"
}

for dest_name, src_path in files_to_upload.items():
    print(f"[*] Uploading {dest_name}...")
    if not os.path.exists(src_path):
        print(f"[!] Could not find {src_path}. Skipping.")
        continue
    with open(src_path, "rb") as fp:
        upload_url = f"{bucket_url}/{dest_name}"
        r = requests.put(upload_url, verify=True, data=fp, params=params)
        if r.status_code == 201:
            print(f"    [+] {dest_name} uploaded successfully!")
        else:
            print(f"    [!] File upload failed: {r.json()}")

# 5. Update the metadata for the new version
print(f"[*] Updating metadata to {VERSION}...")
metadata_url = f"https://zenodo.org/api/deposit/depositions/{new_id}"
existing_metadata = new_deposition['metadata']
existing_metadata['version'] = VERSION

original_desc = existing_metadata.get('description', '')
contact_html = "<p><strong>🌐 Official Model Explorer & Interactive Data:</strong> <a href=\"https://www.itsm-cosmology.org\">www.itsm-cosmology.org</a><br><strong>📧 Contact the Author:</strong> brendon.boyd@itsm-cosmology.org</p>"
update_note = f"<p><strong>Update {VERSION}:</strong> Contains the fully compiled, peer-reviewed cosmology manuscript, supplementary 175-galaxy parameter ledger, and the complete MCMC python computational framework.</p>"

if "Update v1" not in original_desc: # Just a loose check to not infinitely append
    existing_metadata['description'] = contact_html + update_note + original_desc

data = {'metadata': existing_metadata}
r = requests.put(metadata_url, verify=True, params=params, data=json.dumps(data), headers=headers)
if r.status_code == 200:
    print("[*] Metadata updated successfully.")
else:
    print(f"[!] Metadata update failed: {r.json()}")

print(f"\n[+] SUCCESS! The new {VERSION} draft has been fully assembled.")
print(f"    You can review the draft and click 'Publish' here:")
print(f"    https://zenodo.org/deposit/{new_id}\n")
