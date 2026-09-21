import json, glob, os

def main():
    files = sorted(glob.glob('tvbox/*.json'))
    agg = {}
    all_sites = {}
    best = None
    for f in files:
        try:
            d = json.load(open(f, encoding='utf-8'))
        except Exception:
            continue
        if not isinstance(d, dict):
            continue
        n = len(d.get('sites', []) or [])
        if 'spider' in d and (best is None or n > best[1]):
            best = (f, n, d)
        for s in (d.get('sites', []) or []):
            if isinstance(s, dict) and s.get('key'):
                all_sites[s['key']] = s
    if best:
        src = best[2]
        for k in ('spider', 'logo', 'ua', 'parses', 'lives', 'rules', 'heads', 'ijk', 'parseHeader'):
            if k in src:
                agg[k] = src[k]
    agg['sites'] = list(all_sites.values())
    if 'lives' not in agg:
        agg['lives'] = []
    with open('all.json', 'w', encoding='utf-8') as fp:
        json.dump(agg, fp, ensure_ascii=False, indent=2)
    print('all.json generated, sites=', len(agg['sites']))

if __name__ == '__main__':
    main()
