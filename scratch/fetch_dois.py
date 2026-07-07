import re
import urllib.request
import urllib.parse
import json
import time

def fetch_doi(title, author):
    # Construct search query
    query = f"{title} {author}".strip()
    url = "https://api.crossref.org/works?query.bibliographic=" + urllib.parse.quote(query) + "&rows=1"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'mailto:brendon.boyd@itsm-cosmology.org'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if data['message']['items']:
                item = data['message']['items'][0]
                # Double check the title matches roughly
                crossref_title = item.get('title', [''])[0].lower()
                clean_title = title.lower().replace('{','').replace('}','')
                
                # Check for a reasonable match (e.g. at least one word from title)
                if len(set(clean_title.split()) & set(crossref_title.split())) > 1:
                    return item.get('DOI')
    except Exception as e:
        print(f"Error fetching {query}: {e}")
    return None

with open('Manuscript/references.bib', 'r', encoding='utf-8') as f:
    bib_content = f.read()

entries = re.split(r'(?=\n@)', '\n' + bib_content)[1:]

updated_bib = ""
for entry in entries:
    # Check if doi or url is missing
    if 'doi =' not in entry.lower() and 'url =' not in entry.lower():
        # Try to extract title and author
        title_match = re.search(r'title\s*=\s*[\{"](.*?)[\\}"]', entry, re.IGNORECASE | re.DOTALL)
        author_match = re.search(r'author\s*=\s*[\{"](.*?)[\\}"]', entry, re.IGNORECASE | re.DOTALL)
        
        if title_match:
            title = title_match.group(1).replace('\n', ' ').strip()
            author = author_match.group(1).replace('\n', ' ').strip() if author_match else ""
            
            # special case cleanup
            author = author.split('and')[0].strip()
            
            print(f"Fetching DOI for: {title[:50]}...")
            doi = fetch_doi(title, author)
            if doi:
                print(f"  -> Found DOI: {doi}")
                # Insert DOI before the last closing brace
                entry = re.sub(r'\n(})', f',\n  doi = {{{doi}}}\n\\1', entry)
            else:
                print("  -> No DOI found.")
            time.sleep(0.1) # rate limit
    updated_bib += entry

with open('Manuscript/references_updated.bib', 'w', encoding='utf-8') as f:
    f.write(updated_bib)

print("Updated bibliography saved to references_updated.bib")
