import os

def fix():
    path = 'index.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Fix Official Link Anchor (removed leading zero, added encodeURIComponent)
    old_link = ':href="`https://wannavegtour.com/product/0327cz/#:~:text=第${currentDay.day<10?\'0\'+currentDay.day:currentDay.day}天`"'
    new_link = ':href="`https://wannavegtour.com/product/0327cz/#:~:text=${encodeURIComponent(\'第\' + currentDay.day + \'天\')}`"'
    
    if old_link in content:
        content = content.replace(old_link, new_link)
        print("Updated official link anchor.")
    else:
        print("Could not find old_link pattern.")

    # 2. Fix enterApp to always go to Day 1
    if 'resetToToday();' in content:
        content = content.replace('resetToToday();', 'currentIndex.value = 0; // FIXED DAY 1')
        print("Updated enterApp to Day 1.")
    else:
        print("Could not find resetToToday() pattern.")

    # 3. Increase Mobile Padding for visibility
    if 'style="padding-top: max(3.5rem, env(safe-area-inset-top));"' in content:
        content = content.replace('style="padding-top: max(3.5rem, env(safe-area-inset-top));"', 'style="padding-top: max(5.5rem, env(safe-area-inset-top));"')
        print("Increased top padding.")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    fix()
