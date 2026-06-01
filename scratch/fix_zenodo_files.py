import os, sys, requests
import urllib3
urllib3.disable_warnings()

ACCESS_TOKEN = 'y4Ht4vMx2SuaXKXKahmly4Mk7vPjVuekxPlfTIb3fOsTHl1IhS3ab52hron0'
draft_id = '20480821'
params = {'access_token': ACCESS_TOKEN}

print("[*] Fetching draft files...")
files_url = f'https://zenodo.org/api/deposit/depositions/{draft_id}/files'
r = requests.get(files_url, verify=False, params=params)

if r.status_code == 200:
    files = r.json()
    for f in files:
        if f['filename'] == 'ITSM_arXiv_Submission.zip':
            print(f"[*] Deleting {f['filename']} from Zenodo...")
            del_r = requests.delete(f['links']['self'], verify=False, params=params)
            if del_r.status_code == 204:
                print("[+] Successfully deleted.")
            else:
                print(f"[!] Failed to delete: {del_r.status_code} {del_r.text}")
else:
    print(f"[!] Failed to fetch files: {r.status_code} {r.text}")
