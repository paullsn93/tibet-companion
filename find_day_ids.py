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
    
    mapping = {}
    for h in headings:
        text = h.get_text().strip()
        m = re.search(r'^第(\d+)天', text)
        if m:
            day_num = int(m.group(1))
            parent = h.parent
            while parent and parent.name != 'body':
                if parent.get('id') and 'itinerary' in parent.get('id'):
                    mapping[day_num] = parent.get('id')
                    break
                parent = parent.parent
    
    for d in sorted(mapping.keys()):
        print(f"Day {d}: {mapping[d]}")
except Exception as e:
    print(f"Error: {e}")
