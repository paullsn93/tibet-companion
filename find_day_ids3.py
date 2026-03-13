import urllib.request
from bs4 import BeautifulSoup
import re

url = "https://wannavegtour.com/product/0326cz/"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    
    # 阿玩的行程通常在 div class="elementor-accordion" 裡面
    # 每個 item 會有一個 id="elementor-tab-title-XXXX" 或 href="#elementor-tab-content-XXXX"
    
    # 我們找所有的 a 標籤或 div 標籤，看屬性或文字
    for el in soup.find_all(lambda tag: tag.name in ['div', 'a', 'h1', 'h2', 'h3'] and tag.get_text() and '第' in tag.get_text() and '天' in tag.get_text()):
        text = el.get_text().strip()
        m = re.match(r'^第(\d+)天', text)
        if m:
            day = m.group(1)
            # Find closest ID
            p = el
            closest_id = None
            while p and p.name != 'body':
                if p.get('id'):
                    closest_id = p.get('id')
                    break
                p = p.parent
            if closest_id:
                print(f"Day {day} -> {closest_id}  ({text[:15]})")
except Exception as e:
    print(f"Error: {e}")
