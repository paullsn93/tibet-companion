import re

html_path = "index.html"
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Fix HTML template
# Replace: '第' + currentDay.day + '天｜' 
# With:    '第' + currentDay.day + '天'
# Wait, let's just make sure we match the exact string from patch_v22.py
pattern_template = r"""<a :href="`https://wannavegtour.com/product/0326cz/#:~:text=\$\{encodeURIComponent\(currentDay.day === 10 \? '搭乘青藏鐵路' : '第' \+ currentDay.day \+ '天｜'\)\}`\""""
replacement_template = r"""<a :href="`https://wannavegtour.com/product/0326cz/#:~:text=${encodeURIComponent(currentDay.day === 10 ? '搭乘青藏鐵路' : '第' + currentDay.day + '天')}`\""""
html_content, c1 = re.subn(pattern_template, replacement_template, html_content)


# Fix JS logic
# `const anchor = \`第${dayNum}天｜\`;`
# Since `anchor` is used, let's just replace the definition of `anchor`
pattern_js_anchor = r'const anchor = `第\$\{dayNum\}天｜`;'
replacement_js_anchor = r'const anchor = `第${dayNum}天`;'
html_content, c2 = re.subn(pattern_js_anchor, replacement_js_anchor, html_content)


if c1 > 0 or c2 > 0:
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Removed pipe from Text Fragment: Replaced {c1} HTML template links and {c2} JS logic blocks.")
else:
    print("FAILED to replace pipe, check index.html string structure.")
