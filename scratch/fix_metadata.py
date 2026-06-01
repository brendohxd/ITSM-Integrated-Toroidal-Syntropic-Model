import os, sys, requests, json, datetime
import urllib3
urllib3.disable_warnings()

ACCESS_TOKEN = 'y4Ht4vMx2SuaXKXKahmly4Mk7vPjVuekxPlfTIb3fOsTHl1IhS3ab52hron0'
draft_id = '20480821'
params = {'access_token': ACCESS_TOKEN}
headers = {'Content-Type': 'application/json'}

print("[*] Fetching draft...")
r = requests.get(f'https://zenodo.org/api/deposit/depositions/{draft_id}', verify=False, params=params)
deposition = r.json()
metadata = deposition['metadata']

print("[*] Fixing metadata...")
metadata['version'] = 'v9.8.1'
metadata['publication_date'] = datetime.date.today().isoformat()
if 'dates' in metadata:
    del metadata['dates']

print('[*] Updating metadata...')
metadata_url = f'https://zenodo.org/api/deposit/depositions/{draft_id}'
r = requests.put(metadata_url, verify=False, params=params, data=json.dumps({'metadata': metadata}), headers=headers)
if r.status_code == 200:
    print('[+] SUCCESS! Draft assembled: https://zenodo.org/deposit/' + str(draft_id))
else:
    print('[!] Metadata update failed:', r.json())
