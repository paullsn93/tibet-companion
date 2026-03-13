import re
c = open('index.html','r',encoding='utf-8').read()
idx = c.find('wannavegtour')
results = []
while idx != -1:
    segment = c[max(0,idx-200):idx+300]
    results.append((idx, segment))
    idx = c.find('wannavegtour', idx+1)
with open('wanna_debug.txt','w',encoding='utf-8') as f:
    for pos, seg in results:
        f.write(f'=== pos {pos} ===\n')
        f.write(repr(seg) + '\n\n')
print(f'Found {len(results)} occurrences')
