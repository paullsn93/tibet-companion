import urllib.request
from bs4 import BeautifulSoup
import re

url = "https://wannavegtour.com/product/0326cz/"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    
    soup = BeautifulSoup(html, 'html.parser')
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    
    print("Found headings matching '第X天':")
    for h in headings:
        text = h.get_text().strip()
        if re.search(r'第\d+天', text):
            # Find the closest parent with an ID
            parent_id = None
            parent = h.parent
            while parent and parent.name != 'body':
                if parent.get('id'):
                    parent_id = parent.get('id')
                    break
                parent = parent.parent
            print(f"- Text: '{text[:40]}...', ID: '{h.get('id')}', Parent ID: '{parent_id}', Tag: {h.name}")
except Exception as e:
    print(f"Error fetching {url}: {e}")
