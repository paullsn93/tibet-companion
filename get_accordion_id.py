from bs4 import BeautifulSoup

with open("wanna.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

for item in soup.find_all(class_="elementor-accordion-item"):
    title_div = item.find(class_="elementor-tab-title")
    if title_div and "第2天" in title_div.text:
        print("FOUND DAY 2 ACCORDION ITEM:")
        print(f"Parent Class: {item.get('class')}")
        
        print("\n--- Title Section ---")
        print(f"Tag: {title_div.name}, ID: {title_div.get('id')}, Class: {title_div.get('class')}")
        a_tag = title_div.find('a')
        if a_tag:
            print(f"  Anchor Tag: {a_tag.name}, ID: {a_tag.get('id')}, Class: {a_tag.get('class')}")
            
        content_div = item.find(class_="elementor-tab-content")
        print("\n--- Content Section ---")
        if content_div:
            print(f"Tag: {content_div.name}, ID: {content_div.get('id')}, Class: {content_div.get('class')}")
            
        break
