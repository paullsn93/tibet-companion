import json
import re
import os

def sync():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, 'itinerary_data.json')
    html_path = os.path.join(base_dir, 'index.html')
    
    if not os.path.exists(json_path) or not os.path.exists(html_path):
        print("Error: Missing files")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Match the block between our new markers
    pattern = re.compile(r'(// --- DO NOT REMOVE THIS LINE: itineraryData Start ---\s+const itineraryData = )\[.*?\];', re.DOTALL)
    
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    
    # Safe substitution using lambda
    new_html_content = pattern.sub(lambda m: m.group(1) + json_str + ';', html_content)

    if new_html_content == html_content:
        print("Warning: No changes made to index.html. Pattern not found with markers.")
        # Fallback to old pattern if markers are missing
        alt_pattern = re.compile(r'(const itineraryData = )\[.*?\];', re.DOTALL)
        new_html_content = alt_pattern.sub(lambda m: m.group(1) + json_str + ';', html_content)
        if new_html_content != html_content:
             with open(html_path, 'w', encoding='utf-8') as f:
                f.write(new_html_content)
             print("Successfully synced itineraryData (Fallback Pattern)")
             return

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_html_content)
    print("Successfully synced itineraryData (Marker Mode)")

if __name__ == "__main__":
    sync()
