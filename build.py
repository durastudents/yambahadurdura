#!/usr/bin/env python3
"""Edit data.json, then run:  python3 build.py   (add --watch to rebuild on every save)
Reads data.json, checks it, and writes data.js, which index.html loads."""
import json, os, sys, time
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check(d):
    errs = []
    for k in ('book', 'extra', 'gal'):
        if k not in d: errs.append('missing top-level key: ' + k)
    if errs: return errs
    for c in d['book']:
        for k in ('n', 'title', 'pages', 'sections'):
            if k not in c: errs.append('chapter %s: missing "%s"' % (c.get('n', '?'), k))
        for s in c.get('sections', []):
            if 'title' not in s or 'page' not in s: errs.append('chapter %s: a section needs "title" and "page"' % c.get('n'))
            for p in s.get('paras', []):
                if 't' not in p and 'c' not in p: errs.append('chapter %s / %s: a paragraph needs "t" (text) or "c" (caption)' % (c.get('n'), s.get('title')))
    for g in d['extra'].get('glossary', []):
        if 'w' not in g or 'd' not in g: errs.append('glossary entry needs "w" and "d": %s' % g)
    for p in d['extra'].get('people', []):
        if not (isinstance(p, list) and len(p) == 3): errs.append('person must be [name, place, contribution]: %s' % p)
    for g in d['gal']:
        if not g['i'].startswith('data:') and not os.path.exists(g['i']): errs.append('image file not found: ' + g['i'])
    return errs

def build():
    try:
        d = json.load(open('data.json', encoding='utf-8'))
    except json.JSONDecodeError as e:
        print('data.json is not valid JSON: line %d, column %d: %s' % (e.lineno, e.colno, e.msg)); return False
    errs = check(d)
    if errs:
        print('Not built. Fix these first:'); [print('  -', e) for e in errs]; return False
    body = json.dumps(d, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    open('data.js', 'w', encoding='utf-8').write('/* AUTO-GENERATED from data.json by build.py. Do not edit; edit data.json. */\nwindow.DURA_DATA=' + body + ';\n')
    n = sum(len(c['sections']) for c in d['book'])
    print('Built data.js: %d chapters, %d topics, %d glossary words, %d people, %d photos' % (len(d['book']), n, len(d['extra']['glossary']), len(d['extra']['people']), len(d['gal'])))
    return True

if __name__ == '__main__':
    build()
    if '--watch' in sys.argv:
        print('Watching data.json (Ctrl+C to stop)...'); last = os.path.getmtime('data.json')
        while True:
            time.sleep(1)
            m = os.path.getmtime('data.json')
            if m != last: last = m; build()
