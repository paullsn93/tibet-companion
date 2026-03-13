import urllib.request
from bs4 import BeautifulSoup
import re

url = "https://wannavegtour.com/product/0326cz/"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    
    # 阿玩官網行程是在 class 包含 toggle-container 或類似的地方
    # 我們找所有的 h3
    headings = soup.find_all('h3')
    
    mapping = {}
    for h in headings:
        text = h.get_text().strip()
        m = re.search(r'^第(\d+)天', text)
        if m:
            day_num = int(m.group(1))
            # 找到標籤的父 div 等
            parent = h.find_parent('div', class_=re.compile(r'elementor-accordion|faq|toggle', re.I))
            
            # 或者直接找他最近帶有 id 的父元素
            p = h.parent
            id_val = None
            while p and p.name != 'body':
                if p.get('id'):
                    id_val = p.get('id')
                    break
                p = p.parent
            
            mapping[day_num] = id_val

    for d in sorted(mapping.keys()):
        print(f"Day {d}: {mapping[d]}")
except Exception as e:
    print(f"Error: {e}")
