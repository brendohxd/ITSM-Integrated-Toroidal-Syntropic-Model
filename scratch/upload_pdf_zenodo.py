import os, sys, requests
import urllib3
urllib3.disable_warnings()

ACCESS_TOKEN = 'y4Ht4vMx2SuaXKXKahmly4Mk7vPjVuekxPlfTIb3fOsTHl1IhS3ab52hron0'
draft_id = '20480821'
params = {'access_token': ACCESS_TOKEN}

print("[*] Fetching draft...")
r = requests.get(f'https://zenodo.org/api/deposit/depositions/{draft_id}', verify=False, params=params)
deposition = r.json()
bucket_url = deposition['links']['bucket']

filename = 'Manuscript/Main.pdf'
print(f'[*] Uploading {filename} as preview...')
with open(filename, 'rb') as fp:
    r = requests.put(f'{bucket_url}/Main.pdf', verify=False, data=fp, params=params)

if r.status_code == 201:
    print(f'[+] Main.pdf uploaded successfully! Zenodo will automatically set it as the preview.')
else:
    print(f'[!] Upload failed: {r.status_code} {r.json()}')
