"""
Utility script to download Pantheon+ dataset for supernova cosmology analysis.
Downloads the distance moduli and covariance matrices directly from the official GitHub release.
"""
import os
import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

out_dir = os.path.join(os.path.dirname(__file__), '..', 'Assets', 'Pantheon_Data')
os.makedirs(out_dir, exist_ok=True)

urls = {
    'Pantheon_SH0ES.dat': 'https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/main/Pantheon%2B_Data/4_DISTANCES_AND_COVAR/Pantheon%2BSH0ES.dat',
    'Pantheon_SH0ES_STAT_SYS.cov': 'https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/main/Pantheon%2B_Data/4_DISTANCES_AND_COVAR/Pantheon%2BSH0ES_STAT%2BSYS.cov'
}

for name, url in urls.items():
    out_path = os.path.join(out_dir, name)
    print(f'Downloading {name}...')
    try:
        urllib.request.urlretrieve(url, out_path)
        print(f'Saved to {out_path} ({os.path.getsize(out_path)/1024/1024:.2f} MB)')
    except Exception as e:
        print(f"Error downloading {name}: {e}")
