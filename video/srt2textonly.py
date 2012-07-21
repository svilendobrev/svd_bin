line=''
state=0
import sys
for s in sys.stdin:
    s= s.strip()
    if not s:
        print line
        line = ''
        state=0
        continue
    if state==0:
        state=1
        continue
    if state==1:
        state=2
        continue
    if state==2:
        line += ' '+s

if line:
    print line
