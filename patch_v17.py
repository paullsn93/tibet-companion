c = open('index.html', 'r', encoding='utf-8').read()

# 舊字串：搜尋路徑格式（不正確）
OLD = '`https://map.baidu.com/search/${encodeURIComponent(currentDay.stay)}/`'

# 新字串：百度地圖 web 版正確 query 格式
# https://map.baidu.com/?newmap=1&ie=utf-8&s=s%26wd%3D{hotel}
# s= 是搜尋參數，%26wd%3D 是 &wd= 的雙重編碼 (百度自己的格式)
NEW = "'https://map.baidu.com/?newmap=1&ie=utf-8&s=s%26wd%3D' + encodeURIComponent(currentDay.stay)"

if OLD in c:
    c2 = c.replace(OLD, NEW, 1)
    open('index.html', 'w', encoding='utf-8').write(c2)
    print('OK - replaced successfully')
    # verify
    if NEW in c2:
        print('Verified: new URL in file')
    remaining = c2.count('baidu.com/search/')
    print('Remaining /search/ paths (route map, expected 1):', remaining)
else:
    print('NOT FOUND')
    # dump nearby for debug
    idx = c.find('baidu.com')
    while idx != -1:
        print('pos', idx, repr(c[max(0,idx-50):idx+150]))
        print()
        idx = c.find('baidu.com', idx+1)
