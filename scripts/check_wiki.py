"""Validate authored routes, image references and copied server assets. No dependencies."""
from pathlib import Path
import json, re, hashlib, sys
from urllib.parse import unquote, urlsplit

root=Path(__file__).resolve().parents[1]
errors=[]; refs=0
pages=[p for p in root.rglob('*.md') if not any(x in p.parts for x in ('.git','.work','_maintenance','vendor'))]
for page in pages:
    text=page.read_text(encoding='utf-8-sig')
    if '\ufffd' in text: errors.append(f'{page.relative_to(root)}: invalid replacement character')
    links=re.findall(r'\[[^\]]*\]\(([^)]+)\)',text)
    links+=re.findall(r'(?:src|href)="([^"]+)"',text)
    for link in links:
        if link.startswith(('http:','https:','mailto:','data:')): continue
        if link.startswith('#/'):
            target=link[2:].split('?')[0].split('#')[0]
            target=(target+'.md') if target and not Path(target).suffix else target
        elif link.startswith('#'): continue
        else: target=urlsplit(link).path.lstrip('/')
        if not target: target='README.md'
        target=unquote(target)
        refs+=1
        if not (root/target).is_file(): errors.append(f'{page.relative_to(root)} -> {target}')
    if re.search(r'</(?:div|figure)>\n(?:#{1,6} |\| |\d+\. |\[)',text):
        errors.append(f'{page.relative_to(root)}: missing blank line after HTML block')
manifest=json.loads((root/'_maintenance/assets.json').read_text(encoding='utf-8'))
combat_manifest=root/'_maintenance/combat-assets.json'
if combat_manifest.exists(): manifest.update(json.loads(combat_manifest.read_text(encoding='utf-8')))
equipment_manifest=root/'_maintenance/equipment-assets.json'
if equipment_manifest.exists(): manifest.update(json.loads(equipment_manifest.read_text(encoding='utf-8')))
world_manifest=root/'_maintenance/world-assets.json'
if world_manifest.exists(): manifest.update(json.loads(world_manifest.read_text(encoding='utf-8')))
life_manifest=root/'_maintenance/life-assets.json'
if life_manifest.exists(): manifest.update(json.loads(life_manifest.read_text(encoding='utf-8')))
social_manifest=root/'_maintenance/social-assets.json'
if social_manifest.exists(): manifest.update(json.loads(social_manifest.read_text(encoding='utf-8')))
guide_manifest=root/'_maintenance/guide-assets.json'
if guide_manifest.exists(): manifest.update(json.loads(guide_manifest.read_text(encoding='utf-8')))
dungeon_manifest=root/'_maintenance/dungeon-assets.json'
if dungeon_manifest.exists(): manifest.update(json.loads(dungeon_manifest.read_text(encoding='utf-8')))
for path,meta in manifest.items():
    dest=root/path
    if not dest.is_file(): errors.append(f'Missing asset: {path}')
    elif 'sha256' in meta and hashlib.sha256(dest.read_bytes()).hexdigest()!=meta['sha256']:
        errors.append(f'Copied image changed: {path}')
for p in ['index.html','them.css','assets/wiki.js','assets/combat.js','assets/combat.css','assets/data/combat.json','assets/vendor/docsify-4.13.1.min.js','assets/vendor/search-topcraft.js','assets/vendor/LICENSE-docsify']:
    if not (root/p).is_file(): errors.append('Missing site file: '+p)
print(json.dumps({'markdown_files':len(pages),'local_references':refs,'assets':len(manifest),'errors':errors},ensure_ascii=False,indent=2))
sys.exit(bool(errors))
