import json
import re

json_path = "itinerary_data.json"
html_path = "index.html"

# Load JSON
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

json_str = json.dumps(data, ensure_ascii=False, indent=2)

# Read index.html
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# The pattern aims to match from "const itineraryData = [" exactly down to "]; // --- DO NOT REMOVE THIS LINE: itineraryData End ---"
# We'll use a precise regex that looks for the start and end markers.

start_marker = r"// --- DO NOT REMOVE THIS LINE: itineraryData Start ---\s*const itineraryData =\s*"
end_marker = r";\s*// --- DO NOT REMOVE THIS LINE: itineraryData End ---"

pattern = re.compile(f"({start_marker})\\[.*?\\]({end_marker})", re.DOTALL)

def replacer(match):
    # match.group(1) is the start marker and assignment
    # match.group(2) is the end marker
    return match.group(1) + json_str + match.group(2)

new_html, count = pattern.subn(replacer, html_content)

if count > 0:
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("SUCCESS: JSON firmly injected into index.html using defined markers.")
else:
    # Fallback if markers don't match exactly. Maybe the end marker is slightly different
    print("WARNING: Marker match failed. Trying a pure string swap method.")
    
    # Let's find exactly the index of start and end strings
    start_str = "const itineraryData = ["
    end_str = "]; // --- DO NOT REMOVE THIS LINE: itineraryData End ---"
    
    idx_start = html_content.find(start_str)
    idx_end = html_content.find(end_str)
    
    if idx_start != -1 and idx_end != -1 and idx_end > idx_start:
        prefix = html_content[:idx_start + len("const itineraryData = ")]
        suffix = html_content[idx_end:]
        final_html = prefix + json_str + suffix
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(final_html)
        print("SUCCESS: JSON injected via string slicing.")
    else:
        print("ERROR: Could not find the injection points in index.html.")
