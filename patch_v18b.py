"""
patch_v18b.py - 修正官網連結 + show_hotel_map template 邏輯
"""
c = open('index.html', 'r', encoding='utf-8').read()
original = c

# ─── 修正 1：Template 中 :href （pos~31202）─────────────────
# 舊: `https://wannavegtour.com/product/0326cz/#:~:text=${encodeURIComponent(\'第\' + currentDay.day + \'天\')}`
# 新: 加 ｜
OLD1 = "`https://wannavegtour.com/product/0326cz/#:~:text=${encodeURIComponent(\\'第\\' + currentDay.day + \\'天\\')}`"
# escape 在 repr 中，實際字串是：
OLD1_ACTUAL = "`https://wannavegtour.com/product/0326cz/#:~:text=${encodeURIComponent('第' + currentDay.day + '天')}`"
NEW1_ACTUAL = "`https://wannavegtour.com/product/0326cz/#:~:text=${encodeURIComponent('第' + currentDay.day + '天｜')}`"

if OLD1_ACTUAL in c:
    c = c.replace(OLD1_ACTUAL, NEW1_ACTUAL, 1)
    print("✅ 修正1: Template :href 加 ｜")
else:
    print("❌ Template href 找不到:", repr(OLD1_ACTUAL[:60]))

# ─── 修正 2：JavaScript 函數中 fallback（pos~115100）────────
# 舊: const anchor = day && day.web_anchor ? day.web_anchor : `第${dayNum}天`;
# 新: fallback 加 ｜，且 web_anchor 也修改為只取 「第N天｜」 前段
#     但最好讓 anchor 統一用「第N天｜」前幾個字即可
OLD2 = "const anchor = day && day.web_anchor ? day.web_anchor : `第${dayNum}天`;"
NEW2 = "const anchor = `第${dayNum}天｜`;"
# 解釋：不再使用 web_anchor（太長太特殊），統一用 「第N天｜」 唯一性足夠

if OLD2 in c:
    c = c.replace(OLD2, NEW2, 1)
    print("✅ 修正2: JS anchor 改為 第N天｜")
else:
    print("❌ JS anchor 找不到:", repr(OLD2[:60]))

# ─── 修正 3：show_hotel_map 條件邏輯 ─────────────────────────
# 找到飯店卡片顯示的 v-if 條件（目前可能是 v-if="currentDay.stay"）
# 需要改為 v-if="currentDay.stay && currentDay.show_hotel_map !== false"
import re
OLD3 = 'v-if="currentDay.stay"'
NEW3 = 'v-if="currentDay.stay && currentDay.show_hotel_map !== false"'

count = c.count(OLD3)
if count > 0:
    c = c.replace(OLD3, NEW3, 1)  # 只換第一個（住宿卡片的那個）
    print(f"✅ 修正3: show_hotel_map 條件 (共{count}處，替換第1處)")
else:
    # 找到實際的 v-if hotel 條件
    for m in re.finditer(r'v-if="currentDay\.stay[^"]*"', c):
        print("現有 hotel v-if:", repr(m.group(0)[:100]))

# 最終驗證
checks = [
    ('Template 天｜', "encodeURIComponent('第' + currentDay.day + '天｜')" in c),
    ('JS anchor 天｜', '第${dayNum}天｜' in c),
    ('show_hotel_map 條件', 'show_hotel_map !== false' in c),
]
print("\n📊 驗證:")
for name, ok in checks:
    print(f"  {'✅' if ok else '❌'} {name}")

if c != original:
    open('index.html', 'w', encoding='utf-8').write(c)
    print("\n✅ index.html 已儲存")
else:
    print("\n⚠️ 未發生改變")
