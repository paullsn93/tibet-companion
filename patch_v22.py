import re

html_path = "index.html"
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Fix HTML template
# <a :href="`https://wannavegtour.com/product/0326cz/#itinerary-answer-${currentDay.day}`"
pattern_template = r'<a\s+:href="`https://wannavegtour\.com/product/0326cz/#itinerary-answer-\$\{currentDay\.day\}`"'
replacement_template = r"""<a :href="`https://wannavegtour.com/product/0326cz/#:~:text=${encodeURIComponent(currentDay.day === 10 ? '搭乘青藏鐵路' : '第' + currentDay.day + '天｜')}`\""""
html_content, c1 = re.subn(pattern_template, replacement_template, html_content)


# Fix JS logic
# const url = `https://wannavegtour.com/product/0326cz/#itinerary-answer-${currentDayIndex.value + 1}`;
# We also have: const anchor = `第${dayNum}天｜`; just before it. We want to update `url`.

pattern_js = r'const url = `https://wannavegtour\.com/product/0326cz/#itinerary-answer-\$\{currentDayIndex\.value \+ 1\}`;'
replacement_js = r"const url = `https://wannavegtour.com/product/0326cz/#:~:text=${encodeURIComponent(dayNum === 10 ? '搭乘青藏鐵路' : anchor)}`;"
html_content, c2 = re.subn(pattern_js, replacement_js, html_content)


if c1 > 0 or c2 > 0:
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Successfully reverted to Text Fragment: Replaced {c1} HTML template links and {c2} JS links.")
else:
    print("FAILED to verify regex, check index.html string structure.")
