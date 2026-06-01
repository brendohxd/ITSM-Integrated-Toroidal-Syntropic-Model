import os, sys, requests, json
import urllib3
urllib3.disable_warnings()

ACCESS_TOKEN = 'y4Ht4vMx2SuaXKXKahmly4Mk7vPjVuekxPlfTIb3fOsTHl1IhS3ab52hron0'
new_id = '20466198'
params = {'access_token': ACCESS_TOKEN}

r = requests.get(f'https://zenodo.org/api/deposit/depositions/{new_id}', verify=False, params=params)
if r.status_code == 200:
    data = r.json()
    print("State:", data.get('state'))
    print("Submitted:", data.get('submitted'))
    print("Title:", data.get('title', data.get('metadata', {}).get('title')))
    print("Version:", data.get('metadata', {}).get('version'))
else:
    print("Error:", r.status_code, r.text)
