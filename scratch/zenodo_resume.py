import os, sys, requests, json
import urllib3
urllib3.disable_warnings()
ACCESS_TOKEN = 'y4Ht4vMx2SuaXKXKahmly4Mk7vPjVuekxPlfTIb3fOsTHl1IhS3ab52hron0'
new_id = '20466198'
params = {'access_token': ACCESS_TOKEN}
headers = {'Content-Type': 'application/json'}

r = requests.get(f'https://zenodo.org/api/deposit/depositions/{new_id}', verify=False, params=params)
new_deposition = r.json()
bucket_url = new_deposition['links']['bucket']

print('[*] Clearing legacy files...')
files_url = f'https://zenodo.org/api/deposit/depositions/{new_id}/files'
r = requests.get(files_url, verify=False, params=params)
for f in r.json():
    print(f'    - Deleting {f["filename"]}...')
    requests.delete(f['links']['self'], verify=False, params=params)

print('[*] Uploading new archive...')
filename = 'ITSM_Computational_Engines_v9.6.0.zip'
with open(filename, 'rb') as fp:
    r = requests.put(f'{bucket_url}/{filename}', verify=False, data=fp, params=params)
if r.status_code == 201:
    print('[*] File uploaded successfully!')
else:
    print(f'[!] File upload failed: {r.json()}')

print('[*] Updating metadata...')
metadata_url = f'https://zenodo.org/api/deposit/depositions/{new_id}'
new_deposition['metadata']['version'] = 'v9.6.0'
r = requests.put(metadata_url, verify=False, params=params, data=json.dumps({'metadata': new_deposition['metadata']}), headers=headers)
print('[+] SUCCESS! Draft assembled: https://zenodo.org/deposit/' + new_id)
