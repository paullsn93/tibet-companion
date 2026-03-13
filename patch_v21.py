import re

html_path = "index.html"
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Pattern 1: HTML template link
# <a :href="`https://wannavegtour.com/product/0326cz/#:~:text=${encodeURIComponent(anchor + '天｜')}`"
pattern_template = r'<a\s+:href="`https://wannavegtour\.com/product/0326cz/#:~:text=\$\{encodeURIComponent\(anchor \+ \'天｜\'\)\}`"'
replacement_template = r'<a :href="`https://wannavegtour.com/product/0326cz/#itinerary-answer-${currentDayIndex + 1}`"'
html_content, c1 = re.subn(pattern_template, replacement_template, html_content)

# Pattern 2: JS fallback link
# const url = `https://wannavegtour.com/product/0326cz/#:~:text=${encodeURIComponent(anchor)}`;
pattern_js = r'const url = `https://wannavegtour\.com/product/0326cz/#:~:text=\$\{encodeURIComponent\(anchor\)\}`;'
replacement_js = r'const url = `https://wannavegtour.com/product/0326cz/#itinerary-answer-${currentDayIndex.value + 1}`;'
html_content, c2 = re.subn(pattern_js, replacement_js, html_content)


if c1 > 0 or c2 > 0:
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Fixed {c1} template links and {c2} JS links.")
else:
    print("Failed to replace links! Check the regex.")
