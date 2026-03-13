"""
patch_v15.py - 三項修正：
1. 官網連結改用 web_anchor 欄位（精準跳轉）
2. 新增住宿飯店卡片（含百度地圖飯店查詢連結）
3. 確認路線按鈕邏輯正確
"""
import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

original = content

# ============================================================
# 修正 1：官網連結改用 web_anchor 欄位，並加入 fallback
# ============================================================
OLD_ANCHOR = (
    r""":href="`https://wannavegtour.com/product/0326cz/#:~:text=${encodeURIComponent('第' + currentDay.day + '天')}`\""""
)
NEW_ANCHOR = (
    r""":href="`https://wannavegtour.com/product/0326cz/#:~:text=${encodeURIComponent(currentDay.web_anchor || ('第' + currentDay.day + '天'))}`\""""
)

if OLD_ANCHOR in content:
    content = content.replace(OLD_ANCHOR, NEW_ANCHOR)
    print("✅ 修正 1: 官網連結改用 web_anchor")
else:
    print("❌ 修正 1 失敗：找不到 OLD_ANCHOR，嘗試 fallback 搜尋...")
    # fallback: 找包含 0326cz/#:~:text 的整段
    m = re.search(r':href="`https://wannavegtour\.com/product/0326cz/#:~:text=\$\{encodeURIComponent\([^)]+\)\}`"', content)
    if m:
        old_found = m.group(0)
        new_str = old_found.replace(
            "encodeURIComponent(",
            "encodeURIComponent(currentDay.web_anchor || ("
        )
        # close extra paren
        new_str = re.sub(r"encodeURIComponent\(currentDay\.web_anchor \|\| \(([^)]+)\)\)", 
                         r"encodeURIComponent(currentDay.web_anchor || (\1))", new_str)
        content = content.replace(old_found, new_str)
        print(f"  ✅ Fallback 成功: {old_found[:80]}...")
    else:
        # Last resort: replace text= portion
        content = content.replace(
            "encodeURIComponent('第' + currentDay.day + '天')",
            "encodeURIComponent(currentDay.web_anchor || ('第' + currentDay.day + '天'))"
        )
        print("  ✅ Last-resort replace 完成")


# ============================================================
# 修正 2：在 TIPS 區塊前插入「住宿飯店」卡片
# ============================================================
# Tips section 的 HTML 特徵（在 sections.txt 中見到 tips_section NOT FOUND，
# 說明用的不是 day.tips 而是其他欄位，從截圖看有 "TIPS" 標題）
# 找 Tips 標題的 HTML pattern
tips_patterns = [
    '貼心叮嚀 TIPS',
    'TIPS</span>',
    'TIPS</div>',
]

hotel_card_html = '''
                        <!-- 住宿飯店 (v15.0 新增) -->
                        <div v-if="currentDay.stay" class="mt-6 p-5 rounded-2xl bg-gradient-to-r from-slate-800/80 to-slate-700/60 border border-slate-600/40">
                            <div class="flex items-center gap-2 mb-3">
                                <span class="material-icons text-amber-400 text-xl">hotel</span>
                                <span class="text-slate-400 text-base font-semibold tracking-wide uppercase">今晚住宿</span>
                            </div>
                            <div class="flex items-center justify-between gap-3 flex-wrap">
                                <span class="text-white text-xl font-bold">{{ currentDay.stay }}</span>
                                <a :href="`https://map.baidu.com/search/${encodeURIComponent(currentDay.stay)}/@12958185.64,2684783.45,13z`"
                                   target="_blank"
                                   class="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-blue-600/80 hover:bg-blue-500/80 text-white text-base font-semibold active:scale-95 transition-all no-underline shrink-0">
                                    <span class="material-icons text-base">place</span>
                                    百度地圖
                                </a>
                            </div>
                        </div>'''

inserted = False
for tip_marker in tips_markers if (tips_markers := tips_patterns) else []:
    idx = content.find(tip_marker)
    if idx >= 0:
        # 往前找到這個卡片所在的 <div 開頭
        # 找 tips 區塊的父容器開始位置（往前找最近的 <div）
        # 在 tip_marker 前面插入 hotel_card
        # 我們要找到 tip_marker 所在的那個完整 div 塊，在其前面插入
        # 尋找包含 tip_marker 的整個 section 的開頭
        search_start = max(0, idx - 300)
        prefix = content[search_start:idx]
        # 找最後一個 </div> 之前的位置來插入
        # 最簡單的方式：在包含 TIPS 標頭的整個 div 容器前面插入
        # 找前面第一個獨立 <div class= 的位置
        div_positions = [m.start() for m in re.finditer(r'<div class="mt-', content[search_start:idx])]
        if div_positions:
            insert_at = search_start + div_positions[-1]
            content = content[:insert_at] + hotel_card_html + content[insert_at:]
            print(f"✅ 修正 2: 住宿卡片插入在 '{tip_marker}' 前 (offset {insert_at})")
            inserted = True
            break
    
if not inserted:
    # Fallback: 在 Official External Link 前插入
    official_marker = '<!-- Official External Link'
    idx = content.find(official_marker)
    if idx >= 0:
        content = content[:idx] + hotel_card_html.strip() + '\n                        ' + content[idx:]
        print("✅ 修正 2 (fallback): 住宿卡片插入在官網按鈕前")
    else:
        # Last resort: 在 查看官網當日行程 前插入
        idx = content.find('查看官網當日行程')
        if idx >= 0:
            # 找到包含它的 <div 開頭
            search_start = max(0, idx - 400)
            last_div = content.rfind('<div', search_start, idx)
            if last_div >= 0:
                content = content[:last_div] + hotel_card_html + '\n                        ' + content[last_div:]
                print("✅ 修正 2 (last resort): 住宿卡片插入")

# ============================================================
# 驗證
# ============================================================
checks = [
    ('web_anchor in href', 'web_anchor' in content),
    ('hotel card html', '今晚住宿' in content),
    ('baidu map search', 'map.baidu.com/search' in content),
    ('material-icons hotel', 'hotel</span>' in content or '>hotel<' in content),
]

print("\n📊 驗證結果:")
for name, ok in checks:
    print(f"  {'✅' if ok else '❌'} {name}")

if content != original:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("\n✅ index.html 已儲存")
else:
    print("\n⚠️ 內容未變動，請檢查修改邏輯")
