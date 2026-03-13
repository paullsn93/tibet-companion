"""V15.0: Remove local KML, replace with cloud link"""

def patch():
    path = 'index.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    changes = 0

    # 1. Delete allMarkers array
    marker_start = '// V14.0: All Markers for KML Export'
    marker_end_anchor = '        createApp({'
    if marker_start in content:
        start_idx = content.index(marker_start)
        end_idx = content.index(marker_end_anchor, start_idx)
        content = content[:start_idx] + content[end_idx:]
        changes += 1
        print("[1/4] Deleted allMarkers array.")

    # 2. Delete downloadKML function
    func_start = '// V14.0: KML Export'
    func_end = '// Expose resetToDayOne globally'
    if func_start in content:
        start_idx = content.index(func_start)
        end_idx = content.index(func_end, start_idx)
        content = content[:start_idx] + content[end_idx:]
        changes += 1
        print("[2/4] Deleted downloadKML function.")

    # 3. Remove downloadKML from return statement
    if 'downloadKML,' in content:
        content = content.replace('                    downloadKML,\n', '')
        changes += 1
        print("[3/4] Removed downloadKML from return.")

    # 4. Replace button with <a> link
    old_btn = '''<button @click="downloadKML"
                                    class="flex flex-col items-center justify-center p-6 bg-emerald-900/50 border border-emerald-700 rounded-2xl text-white text-lg font-bold shadow-lg hover:bg-emerald-800/70 transition-all active:scale-95">
                                    <span class="material-icons-outlined text-4xl mb-2 text-emerald-400">public</span>
                                    下載全景地圖
                                </button>'''
    new_btn = '''<a href="https://earth.google.com/earth/d/17RseOVaMtPcovzugsf9PAYKp9bvaKcJ-?usp=sharing" 
                                   target="_blank"
                                   class="flex flex-col items-center justify-center p-6 bg-emerald-900/50 border border-emerald-800 rounded-2xl text-white text-lg font-bold shadow-lg hover:bg-emerald-800/70 transition-all active:scale-95 no-underline">
                                    <span class="material-icons-outlined text-4xl mb-2 text-emerald-400">public</span>
                                    觀看全景地圖
                                </a>'''
    if old_btn in content:
        content = content.replace(old_btn, new_btn)
        changes += 1
        print("[4/4] Replaced button with cloud link.")
    else:
        print("[4/4] SKIP: Button not found as expected.")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"\nDone! {changes} patches applied.")

if __name__ == "__main__":
    patch()
