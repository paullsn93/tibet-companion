"""
分析 index.html 找出需要修改的 template 位置，輸出到 analysis.txt
"""
import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

results = {}

# 1. 找官網按鈕的 JS 函數
patterns = [
    ('official_url', r'0326cz.{0,300}'),
    ('highlights_block', r'今日亮點.{0,500}'),
    ('tips_block', r'TIPS.{0,300}'),
    ('map_btn', r'查看路線.{0,300}'),
    ('hotel_stay', r'stay.{0,200}'),
    ('baidu', r'baidu.{0,200}'),
    ('web_anchor_js', r'web_anchor.{0,300}'),
]

with open('analysis.txt', 'w', encoding='utf-8') as out:
    for name, pattern in patterns:
        matches = re.findall(pattern, content)
        out.write(f'\n\n=== {name} ===\n')
        for m in matches[:3]:
            out.write(m[:400] + '\n---\n')
    
    # 找 stay 欄位附近的 template
    idx = content.find('day.stay')
    out.write(f'\n\n=== day.stay 位置 ===\n')
    if idx >= 0:
        out.write(content[max(0,idx-200):idx+500])
    else:
        out.write('NOT FOUND')
    
    # 找 map_url 附近
    idx2 = content.find('map_url')
    out.write(f'\n\n=== map_url 位置 ===\n')
    if idx2 >= 0:
        out.write(content[max(0,idx2-200):idx2+500])
    else:
        out.write('NOT FOUND')
    
    # 找 highlight 渲染
    idx3 = content.find('highlight')
    out.write(f'\n\n=== highlight 渲染位置 ===\n')
    if idx3 >= 0:
        out.write(content[max(0,idx3-200):idx3+600])
    else:
        out.write('NOT FOUND')

print('分析完成，輸出至 analysis.txt')
print(f'檔案大小: {len(content)} bytes')
