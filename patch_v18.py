"""
patch_v18.py - 四項修正：
1. 修正 Day 10 官網連結 (index.html)：改用 「第N天｜」含全形豎線，唯一性更高
2. Day 10/12 隱藏百度地圖 (JSON: show_hotel_map: false)
3. 補全所有缺少連結的景點 URL (JSON: highlights[].url)
"""
import json

# ============================================================
# 1. 修正 index.html 官網連結錨點
# ============================================================
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

OLD_ANCHOR = "'https://wannavegtour.com/product/0326cz/#:~:text=' + encodeURIComponent('第' + currentDay.day + '天')"
NEW_ANCHOR = "'https://wannavegtour.com/product/0326cz/#:~:text=' + encodeURIComponent('第' + currentDay.day + '天｜')"

if OLD_ANCHOR in html:
    html = html.replace(OLD_ANCHOR, NEW_ANCHOR, 1)
    print("✅ 1. 官網連結錨點改為 第N天｜")
else:
    # 找現有的 encodeURIComponent 部分確認格式
    import re
    m = re.search(r"encodeURIComponent\('[^']+'\)", html)
    if m:
        print("❌ 精確字串不符，找到:", repr(m.group(0)))
    else:
        print("❌ 找不到 encodeURIComponent 模式")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# ============================================================
# 2 & 3. 修改 itinerary_data.json
# ============================================================
with open('itinerary_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# ── 各景點最佳連結 ──────────────────────────────────────
NEW_URLS = {
    # Day 2
    "雅尼濕地玻璃觀景台": "https://www.chinatibet.tw/jingdian/yalinzangbujiang.html",
    # Day 3
    "林拉景觀大道": "https://www.chinatibet.tw/xizangzixingche/llinzhi.html",
    # Day 4
    "八廓街轉經道": "https://www.tibet.tw/gonglue/383.html",
    "布達拉宮夜景 (晴天限定)": "https://www.findchina.tw/2021/12/potala-palace.html",
    # Day 5
    "崗巴拉山口": "https://www.chinatibet.tw/jingdian/yanghucuo.html",
    # Day 7
    "珠峰日出": "https://www.tibet.tw/gonglue/tibet-ebc-accommodation.html",
    "加烏拉山口 (五座八千米群峰)": "https://www.greattibettour.com/tw/tibet-attractions/gawu-la-pass.html",
    # Day 8
    "藏北草原風光": "https://www.greattibettour.com/tw/tibet-attractions/northern-tibet-grassland.html",
    "當雄 (納木措門戶)": "https://www.chinatibet.tw/jingdian/130.html",
    # Day 9
    "那根拉山口 (5190m)": "https://www.chinatibet.tw/jingdian/namucuo.html",
    # Day 11
    "青海湖遠眺 (車窗風景)": "https://www.greattibettour.com/tw/tibet-attractions/qinghai-lake.html",
    "麒麟灣公園": "https://www.eztravel.com.tw/scenic/c_xining/",
    "水井巷商圈 (伴手禮)": "https://www.eztravel.com.tw/scenic/c_xining/",
}

# ── Day 10, 12 不顯示百度地圖 ─────────────────────────────
NO_MAP_DAYS = {10, 12}

changes = []
for day_data in data:
    day_num = day_data['day']

    # 補景點連結
    for h in day_data.get('highlights', []):
        label = h.get('label', '')
        if label in NEW_URLS and 'url' not in h:
            h['url'] = NEW_URLS[label]
            changes.append(f"  Day {day_num} [{label}] → {NEW_URLS[label]}")

    # 設置 show_hotel_map
    if day_num in NO_MAP_DAYS:
        day_data['show_hotel_map'] = False
        changes.append(f"  Day {day_num} show_hotel_map = False")

print("✅ 2/3. 景點連結 + show_hotel_map 修改:")
for c in changes:
    print(c)

with open('itinerary_data.json', 'w', encoding='utf-8', newline='\r\n') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\n✅ itinerary_data.json 已儲存")
print("接著需執行 sync_json_to_index.py，再修改 HTML template 判斷 show_hotel_map")
