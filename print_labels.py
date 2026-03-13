import json
with open('itinerary_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
with open('labels_out.txt', 'w', encoding='utf-8') as out:
    for d in data:
        if 'highlights' in d:
            for a in d['highlights']:
                url = a.get('url', 'NO_URL')
                out.write(f"{a['label']} | {url}\n")
