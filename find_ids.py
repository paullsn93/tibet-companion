import urllib.request
from bs4 import BeautifulSoup
import re

url = "https://wannavegtour.com/product/0326cz/"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    
    soup = BeautifulSoup(html, 'html.parser')
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div'])
    
    results = []
    for h in headings:
        text = h.get_text().strip()
        if re.search(r'^第\d+天', text):
            # 找自己或父元素的 ID
            current = h
            found_id = None
            while current and current.name != 'body':
                if current.get('id'):
                    found_id = current.get('id')
                    break
                current = current.parent
            if found_id and found_id not in [r['id'] for r in results]:
                results.append({'text': text[:20], 'id': found_id, 'tag': h.name})
    
    for r in results:
        print(f"Day Info: {r['text']:<15} | ID: {r['id']}")

except Exception as e:
    print(f"Error: {e}")
