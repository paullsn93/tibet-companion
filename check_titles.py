import json
import urllib.request
import urllib.error
import ssl
import re

def get_title(body):
    match = re.search(r'<title>(.*?)</title>', body, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return "NO TITLE"

def main():
    with open('itinerary_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    with open('titles_out.txt', 'w', encoding='utf-8') as out:
        for d in data:
            if 'highlights' in d:
                for a in d['highlights']:
                    url = a.get('url')
                    if url:
                        try:
                            req = urllib.request.Request(
                                url, 
                                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
                            )
                            response = urllib.request.urlopen(req, timeout=10, context=ctx)
                            body = response.read().decode('utf-8', errors='ignore')
                            title = get_title(body)
                            out.write(f"OK | {a['label']} | {title[:40]} | {url}\n")
                        except Exception as e:
                            out.write(f"FAIL | {a['label']} | {str(e)} | {url}\n")

if __name__ == '__main__':
    main()
