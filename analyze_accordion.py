from bs4 import BeautifulSoup
import re

html_path = "wanna.html"
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# Find the itinerary section. Look for headers like "第2天"
headers = soup.find_all(lambda tag: tag.name and 'h' in tag.name and '第2天' in tag.text)
for h in headers:
    print("--- Found Header for Day 2 ---")
    print(f"Tag: {h.name}")
    print(f"Text: {h.text.strip()}")
    print(f"Attributes: {h.attrs}")
    
    # Print its parent structure up to 3 levels to see the accordion logic
    parent = h.parent
    for i in range(3):
        if parent:
            print(f"Parent {i+1}: {parent.name} | id: {parent.get('id', '')} | class: {parent.get('class', [])}")
            parent = parent.parent

# Also let's find the exact accordion container
items = soup.find_all(class_=re.compile(r'accordion|elementor-tab|tour-itinerary'))
if items:
    print("\n--- Example Accordion Item ---")
    # print the first item that contains "第2天"
    for item in items:
        if '第2天' in item.text:
            print(f"Item Tag: {item.name}")
            print(f"Item ID: {item.get('id', '')}")
            print(f"Item Class: {item.get('class', [])}")
            # print direct children
            for child in item.children:
                if child.name:
                    print(f"  Child: {child.name} | id: {child.get('id','')} | class: {child.get('class',[])}")
            break
