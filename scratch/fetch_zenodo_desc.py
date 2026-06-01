import os, requests
import urllib3
urllib3.disable_warnings()

ACCESS_TOKEN = 'y4Ht4vMx2SuaXKXKahmly4Mk7vPjVuekxPlfTIb3fOsTHl1IhS3ab52hron0'
draft_id = '20480821'
params = {'access_token': ACCESS_TOKEN}

r = requests.get(f'https://zenodo.org/api/deposit/depositions/{draft_id}', verify=False, params=params)
metadata = r.json().get('metadata', {})
with open('scratch/zenodo_desc.txt', 'w', encoding='utf-8') as f:
    f.write(metadata.get('description', 'No description found.'))
