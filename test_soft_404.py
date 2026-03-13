import urllib.request
import ssl

def check_content(url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        response = urllib.request.urlopen(req, timeout=10, context=ctx)
        body = response.read().decode('utf-8', errors='ignore')
        print(f"URL: {url}")
        print(f"Status: {response.getcode()}")
        print(f"Body length: {len(body)}")
        if '不存在' in body or '404' in body or 'Not Found' in body:
            print("WARNING: Page content indicates it might not exist!")
        else:
            print(f"Content preview: {body[:200].strip()}")
    except Exception as e:
        print(f"Error: {e}")

check_content('https://www.chinatibet.tw/jingdian/yalinzangbujiang.html')
