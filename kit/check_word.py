#!/usr/bin/env python3
"""python3 kit/check_word.py "MEK HASTE" "BRUK POCKET" -> says OK or BLOCKED (Daily Word) for each."""
import hashlib, sys, os
B=set(l.strip() for l in open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'daily_blocklist.txt')) if l.strip() and not l.startswith('#'))
for w in sys.argv[1:]:
    h=hashlib.sha256(w.replace(' ','').upper().encode()).hexdigest()[:16]
    print(('BLOCKED (Daily Word, do not post)' if h in B else 'OK'), w)
