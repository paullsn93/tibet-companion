"""
從 index.html 精確提取需要修改的 template 段落
"""
import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

sections = {}

# 找 highlights 渲染區塊 (v-for highlight)
for label, keyword in [
    ('highlights_vfor', 'v-for'),
    ('day_stay', 'day.stay'),
    ('map_url', 'day.map_url'),
    ('official_btn', '0326cz'),
    ('web_anchor', 'web_anchor'),
    ('baidu', 'baidu'),
    ('hotel', 'hotel'),
    ('tips_section', 'day.tips'),
]:
    idx = content.find(keyword)
    if idx >= 0:
        snippet = content[max(0,idx-300):idx+600]
        sections[label] = snippet
    else:
        sections[label] = 'NOT FOUND'

with open('sections.txt', 'w', encoding='utf-8') as f:
    for k, v in sections.items():
        f.write(f'\n{"="*60}\n{k}\n{"="*60}\n{v}\n')

print('done')
