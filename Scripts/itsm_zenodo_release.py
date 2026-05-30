import os
import sys
import requests
import json

ACCESS_TOKEN = 'y4Ht4vMx2SuaXKXKahmly4Mk7vPjVuekxPlfTIb3fOsTHl1IhS3ab52hron0'
DEPOSITION_ID = '20174582'

print(f"[*] Starting Zenodo release automation for base ID: {DEPOSITION_ID}")

params = {'access_token': ACCESS_TOKEN}
headers = {"Content-Type": "application/json"}

# 1. Create a new version
print("[*] Creating a new version draft...")
url = f"https://zenodo.org/api/deposit/depositions/{DEPOSITION_ID}/actions/newversion"
r = requests.post(url, params=params)
if r.status_code != 201:
    print(f"[!] Failed to create new version: {r.json()}")
    sys.exit(1)

new_version_url = r.json()['links']['latest_draft']

# 2. Get the new deposition details
print("[*] Retrieving new version details...")
r = requests.get(new_version_url, params=params)
new_deposition = r.json()
new_id = new_deposition['id']
bucket_url = new_deposition['links']['bucket']

print(f"[*] New deposition ID created: {new_id}")

# 3. Clear existing files in the draft (so we can replace with fresh ones)
print("[*] Clearing legacy files from the draft...")
files_url = f"https://zenodo.org/api/deposit/depositions/{new_id}/files"
r = requests.get(files_url, params=params)
for f in r.json():
    print(f"    - Deleting {f['filename']}...")
    del_r = requests.delete(f['links']['self'], params=params)

# 4. Upload the new zip file
print("[*] Uploading new ITSM_arXiv_Submission.zip archive...")
filename = "ITSM_Computational_Engines_v9.5.2.zip"
# Assuming script is run from project root: Scripts/itsm_zenodo_release.py
path = "ITSM_Computational_Engines_v9.5.2.zip" 

if not os.path.exists(path):
    print(f"[!] Could not find {path} at root directory. Make sure you run from project root.")
    sys.exit(1)

with open(path, "rb") as fp:
    upload_url = f"{bucket_url}/{filename}"
    r = requests.put(upload_url, data=fp, params=params)

if r.status_code == 201:
    print("[*] File uploaded successfully!")
else:
    print(f"[!] File upload failed: {r.json()}")

# 5. Update the metadata for the new version
print("[*] Updating metadata to v9.5.1...")
metadata_url = f"https://zenodo.org/api/deposit/depositions/{new_id}"
existing_metadata = new_deposition['metadata']
existing_metadata['version'] = 'v9.5.2'

data = {'metadata': existing_metadata}
r = requests.put(metadata_url, params=params, data=json.dumps(data), headers=headers)
if r.status_code == 200:
    print("[*] Metadata updated.")
else:
    print(f"[!] Metadata update failed: {r.json()}")

print(f"\n[+] SUCCESS! The new draft has been fully assembled.")
print(f"    You can review the draft and click 'Publish' here:")
print(f"    https://zenodo.org/deposit/{new_id}\n")
