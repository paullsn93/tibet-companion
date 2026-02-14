import json
import re
import os

def sync():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, 'itinerary_data.json')
    html_path = os.path.join(base_dir, 'index.html')
    
    if not os.path.exists(json_path) or not os.path.exists(html_path):
        print("Missing files")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Find the itineraryData block in HTML
    # It starts with 'const itineraryData = [' and ends with '];'
    pattern = re.compile(r'(const itineraryData = )\[.*?\];', re.DOTALL)
    
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    new_html_content = pattern.sub(rf'\1{json_str};', html_content)

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_html_content)
    
    print("Successfully synced itineraryData")

if __name__ == "__main__":
    sync()
