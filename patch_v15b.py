"""
patch_v15b.py - 修正 encodeURIComponent 括號問題並重新清潔 href 屬性
"""
import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 找到官網連結的 href 屬性（完整）
# 從 wannavegtour 往前找到 :href= 的起點
idx_url = content.find('wannavegtour.com/product/0326cz')
if idx_url < 0:
    print("ERROR: wannavegtour URL not found!")
    exit(1)

# 找 :href=" 的起點
href_start = content.rfind(':href=', 0, idx_url)
if href_start < 0:
    print("ERROR: :href= not found before URL!")
    exit(1)

# 找到 href 結尾（找到對應引號結尾）
# :href="`...`"  格式
href_end = content.find('"', content.find('`"', idx_url))
full_href = content[href_start:href_end+1]
print("現有 href:", full_href[:300])

# 建立正確的 href
correct_href = ':href="`https://wannavegtour.com/product/0326cz/#:~:text=${encodeURIComponent(currentDay.web_anchor || (\'第\' + currentDay.day + \'天\'))}`"'

print("\n目標 href:", correct_href)

# 替換
new_content = content[:href_start] + correct_href + content[href_end+1:]

# 驗證
check_idx = new_content.find('wannavegtour.com/product/0326cz')
context = new_content[max(0, check_idx-60):check_idx+200]
print("\n替換後 context:", context)

# 檢查括號配對
paren_open = context.count('(')
paren_close = context.count(')')
print(f"括號：( 出現 {paren_open} 次，) 出現 {paren_close} 次")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)
print("\n✅ index.html 已儲存")
