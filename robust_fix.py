import os

path = os.path.join(os.getcwd(), 'index.html')
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Define the old function as a literal string. 
# I'll use a slightly more flexible approach by searching for the start and end.
start_marker = '                const openMap = (day) => {'
end_marker = '                };'
# Find the specific openMap function that contains "mapUrl = baseUrl + params;"
start_idx = content.find(start_marker, content.find('mapButtonInfo')) # Search after mapButtonInfo
if start_idx != -1:
    end_idx = content.find(end_marker, start_idx) + len(end_marker)
    if end_idx != -1:
        new_func = """                const openMap = (day) => {
                    if (mapButtonInfo.value && mapButtonInfo.value.url) {
                        window.open(mapButtonInfo.value.url, '_blank');
                    }
                };"""
        new_content = content[:start_idx] + new_func + content[end_idx:]
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Successfully replaced openMap")
    else:
        print("Could not find end marker")
else:
    print("Could not find start marker")
