"""Check the rendered equipment catalog's cross references and content invariants."""
from pathlib import Path
import re, json, sys
from urllib.parse import unquote, parse_qs
root=Path(__file__).resolve().parents[1]
pages={p.relative_to(root).with_suffix('').as_posix():p.read_text(encoding='utf-8') for p in (root/'equipment').rglob('*.md')}
errors=[]; anchors=0; cards=0; gaps=[]
for route,text in pages.items():
    ids=re.findall(r'\bid="([^"]+)"',text)
    if len(ids)!=len(set(ids)): errors.append(route+': duplicate id')
    for dest,query in re.findall(r'href="#/(equipment/[^?"#]+)\?([^"]+)"',text):
        target=parse_qs(query).get('id',[''])[0]
        anchors+=1
        if f'id="{target}"' not in pages.get(dest,''): errors.append(f'{route} -> {dest}#{target}')
    for card in re.findall(r'<article\b.*?</article>',text,re.S):
        cards+=1
        if '获取地点尚未收录' in card: gaps.append(re.search(r'<h3>(.*?)</h3>',card)[1])
    for forbidden in ['TEST_STATS','UNIQUE_T2D','MMOItems','AttackSpeedBouns','undefined','NaN']:
        if forbidden in text: errors.append(route+': developer/sample text '+forbidden)
    if re.search(r'<a[^>]*></a>',text): errors.append(route+': empty link label')
data=json.loads((root/'assets/data/equipment.json').read_text(encoding='utf-8'))
used={key for t in data['types'].values() for key in t['stats']} | {key for a in data['affixes'].values() for key in a['stats']}
for key in used:
    if not re.search(r'[\u4e00-\u9fff]',data['labels'].get(key,'')): errors.append('Missing Chinese stat label: '+key)
print(json.dumps({'pages':len(pages),'cards':cards,'item_links':anchors,'unresolved_material_sources':gaps,'errors':errors},ensure_ascii=False,indent=2))
sys.exit(bool(errors))
