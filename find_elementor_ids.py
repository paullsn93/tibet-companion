from bs4 import BeautifulSoup
import re

with open('wanna.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

mapping = []
for div in soup.find_all('div', class_=re.compile(r'elementor-tab-title')):
    text = div.get_text().strip()
    m = re.match(r'^第(\d+)天', text)
    if m:
        day = int(m.group(1))
        # Find the id of the tab title or the tab content
        # elementor accordions use id on the title and aria-controls for content.
        # usually linking to #elementor-tab-title-XXXX works.
        title_id = div.get('id')
        content_id = div.get('aria-controls')
        print(f"Day {day}: Element ID -> {title_id} | Content ID -> {content_id}")
