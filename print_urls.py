import json

with open('itinerary_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('urls_output.txt', 'w', encoding='utf-8') as out:
    out.write("Remaining URLs:\n")
    for d in data:
        if 'highlights' in d:
            for a in d['highlights']:
                if 'url' in a:
                    out.write(f"- {a['label']}: {a['url']}\n")
