import json
import urllib.request
import urllib.error
import ssl

def check_url(url):
    if not url:
        return True
        
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        response = urllib.request.urlopen(req, timeout=15, context=ctx)
        if response.getcode() != 200:
            return False
            
        # Check for soft 404
        body = response.read().decode('utf-8', errors='ignore')
        
        # known error phrases on chinatibet.tw or others
        error_keywords = ['不存在', '404', 'Not Found', 'not found', '無法找到']
        
        # If the page is very small, or clearly an error page
        # Some normal pages might have "404" as a number, so be careful.
        # "頁面不存在" is a very strong indicator.
        if '頁面不存在' in body or '请求的页面不存在' in body or '<title>404' in body or '404 Not Found' in body:
            return False
            
        return True
    except Exception as e:
        print(f"Error checking {url}: {e}")
        return False

def main():
    with open('itinerary_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    removed = 0
    for day in data:
        if 'highlights' in day:
            for attr in day['highlights']:
                url = attr.get('url')
                if url:
                    print(f"Checking {attr['label']} - {url}")
                    if not check_url(url):
                        print(f"-> REMOVING soft/hard 404 URL for {attr['label']}")
                        del attr['url']
                        removed += 1
                    else:
                        print(f"-> OK")

    if removed > 0:
        with open('itinerary_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"\nSuccessfully removed {removed} invalid links.")
    else:
        print("\nAll links were OK.")

if __name__ == '__main__':
    main()
