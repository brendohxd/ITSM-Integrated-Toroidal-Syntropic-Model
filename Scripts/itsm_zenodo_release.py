import os
import sys
import requests
import json

ACCESS_TOKEN = 'y4Ht4vMx2SuaXKXKahmly4Mk7vPjVuekxPlfTIb3fOsTHl1IhS3ab52hron0'
DEPOSITION_ID = '18808348'

print(f"[*] Starting Zenodo release automation for base ID: {DEPOSITION_ID}")

params = {'access_token': ACCESS_TOKEN}
headers = {"Content-Type": "application/json"}

# 1. Create a new version
print("[*] Creating a new version draft...")
url = f"https://zenodo.org/api/deposit/depositions/{DEPOSITION_ID}/actions/newversion"
r = requests.post(url, verify=False, params=params)
if r.status_code != 201:
    print(f"[!] Failed to create new version: {r.json()}")
    sys.exit(1)

new_version_url = r.json()['links']['latest_draft']

# 2. Get the new deposition details
print("[*] Retrieving new version details...")
r = requests.get(new_version_url, verify=False, params=params)
new_deposition = r.json()
new_id = new_deposition['id']
bucket_url = new_deposition['links']['bucket']

print(f"[*] New deposition ID created: {new_id}")

# 3. Clear existing files in the draft (so we can replace with fresh ones)
print("[*] Clearing legacy files from the draft...")
files_url = f"https://zenodo.org/api/deposit/depositions/{new_id}/files"
r = requests.get(files_url, verify=False, params=params)
for f in r.json():
    print(f"    - Deleting {f['filename']}...")
    del_r = requests.delete(f['links']['self'], verify=False, params=params)

# 4. Upload the payload files
files_to_upload = {
    "ITSM_Computational_Engines_v10.0.0.zip": "ITSM_Computational_Engines_v10.0.0.zip",
    "ITSM_Main_Manuscript.pdf": "Manuscript/Main.pdf"
}

for dest_name, src_path in files_to_upload.items():
    print(f"[*] Uploading {dest_name}...")
    if not os.path.exists(src_path):
        print(f"[!] Could not find {src_path}. Skipping.")
        continue
    with open(src_path, "rb") as fp:
        upload_url = f"{bucket_url}/{dest_name}"
        r = requests.put(upload_url, verify=False, data=fp, params=params)
        if r.status_code == 201:
            print(f"    [+] {dest_name} uploaded successfully!")
        else:
            print(f"    [!] File upload failed: {r.json()}")

# 5. Update the metadata for the new version
print("[*] Updating metadata to v10.0.0 and injecting contact info...")
metadata_url = f"https://zenodo.org/api/deposit/depositions/{new_id}"
existing_metadata = new_deposition['metadata']
existing_metadata['version'] = 'v10.0.0'

original_desc = existing_metadata.get('description', '')
contact_html = "<p><strong>🌐 Official Model Explorer & Interactive Data:</strong> <a href=\"https://www.itsm-cosmology.org\">www.itsm-cosmology.org</a><br><strong>📧 Contact the Author:</strong> brendon.boyd@itsm-cosmology.org</p>"
if "itsm-cosmology.org" not in original_desc:
    existing_metadata['description'] = contact_html + original_desc

data = {'metadata': existing_metadata}
r = requests.put(metadata_url, verify=False, params=params, data=json.dumps(data), headers=headers)
if r.status_code == 200:
    print("[*] Metadata updated successfully.")
else:
    print(f"[!] Metadata update failed: {r.json()}")

print(f"\n[+] SUCCESS! The new v10.0.0 draft has been fully assembled.")
print(f"    You can review the draft and click 'Publish' here:")
print(f"    https://zenodo.org/deposit/{new_id}\n")
