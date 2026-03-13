"""
patch_v16.py - 修復兩個功能 bug:
1. 百度地圖飯店搜尋：移除固定座標，改用純搜尋 URL
2. 官網 Text Fragment：改用簡短唯一錨點 「第N天」
"""

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

original = content

# ============================================================
# 修復 1: 百度地圖 URL (移除固定座標)
# ============================================================
# 舊格式: map.baidu.com/search/${encodeURIComponent(currentDay.stay)}/@12958185.64,2684783.45,13z
# 新格式: map.baidu.com/search/${encodeURIComponent(currentDay.stay)}/
OLD_BAIDU = 'map.baidu.com/search/${encodeURIComponent(currentDay.stay)}/@12958185.64,2684783.45,13z'
NEW_BAIDU = 'map.baidu.com/search/${encodeURIComponent(currentDay.stay)}/'

if OLD_BAIDU in content:
    content = content.replace(OLD_BAIDU, NEW_BAIDU)
    print("✅ 修復 1: 百度地圖固定座標已移除")
else:
    # 嘗試找部分匹配
    idx = content.find('map.baidu.com/search/')
    if idx >= 0:
        snippet = content[idx:idx+200]
        print(f"❌ 精確匹配失敗，找到: {snippet[:100]}")
        # 用 re 替換
        import re
        pattern = r'map\.baidu\.com/search/\${encodeURIComponent\(currentDay\.stay\)}/[^`"\']*'
        replacement = 'map.baidu.com/search/${encodeURIComponent(currentDay.stay)}/'
        new = re.sub(pattern, replacement, content)
        if new != content:
            content = new
            print("  ✅ 正則替換成功")
        else:
            print("  ❌ 正則替換也失敗")
    else:
        print("❌ 找不到百度地圖 URL")

# ============================================================
# 修復 2: 官網連結改用短錨點 (只用 「第N天」前幾個字)
# Text Fragment: 只需足夠唯一即可，「第1天｜」這樣的格式每天唯一
# 使用 text start,text end 格式更穩定：
# #:~:text=第N天,-天 (只匹配「第」+數字+「天」)
# 最簡單但有效的方式：只用天數標題前8個字
# ============================================================
OLD_ANCHOR_EXPR = "encodeURIComponent(currentDay.web_anchor || ('第' + currentDay.day + '天'))"
# 新策略：只取 web_anchor 的前7個字（「第N天｜XX」），確保唯一且無特殊字元問題
# 或者更好： 直接用 「第」 + day + 「天」作為 textStart，讓瀏覽器只找段落起始
NEW_ANCHOR_EXPR = "encodeURIComponent('第' + currentDay.day + '天')"

if OLD_ANCHOR_EXPR in content:
    content = content.replace(OLD_ANCHOR_EXPR, NEW_ANCHOR_EXPR)
    print("✅ 修復 2: 官網連結改用簡短 「第N天」 錨點")
else:
    print(f"❌ 找不到 OLD_ANCHOR_EXPR: {OLD_ANCHOR_EXPR[:60]}...")

# ============================================================
# 驗證
# ============================================================
checks = [
    ('百度地圖純搜尋 URL', 'map.baidu.com/search/${encodeURIComponent(currentDay.stay)}/' in content and '@12958185' not in content),
    ('官網連結用 第N天', "'第' + currentDay.day + '天'" in content),
    ('無舊固定座標', '12958185' not in content),
]

print("\n📊 驗證:")
for name, ok in checks:
    print(f"  {'✅' if ok else '❌'} {name}")

if content != original:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("\n✅ index.html 已儲存")
else:
    print("\n⚠️ 沒有任何改變！")
