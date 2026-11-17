"""Export read-only combat data from the server checkout. Requires PyYAML.

Usage: python scripts/export_combat.py C:/path/to/top-craft2
Editorial pages are maintained separately; this only updates data and reused assets.
"""
import sys, json, re, hashlib, shutil
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
SERVER = Path(sys.argv[1]).resolve()
IA = SERVER / 'plugins/ItemsAdder/contents/topcraft'
TEXTURES = IA / 'resourcepack/assets/topcraft/textures'
MODELS = IA / 'resourcepack/assets/topcraft/models'
def read(path):
    return yaml.safe_load(path.read_text(encoding='utf-8-sig')) or {}
def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')

items = {}
for path in (IA / 'configs').rglob('*.yml'):
    for name, item in read(path).get('items', {}).items():
        r = item.get('resource', {})
        if 'model_id' in r:
            texture = (r.get('textures') or [None])[0]
            if not texture and r.get('model_path'):
                p = MODELS / (r['model_path']+'.json')
                if p.exists():
                    model = json.loads(p.read_text(encoding='utf-8-sig'))
                    texture = model.get('textures', {}).get('layer0')
            if texture: items[int(r['model_id'])] = texture.replace('topcraft:', '')

copied = {}
def asset(texture):
    texture = texture.removesuffix('.png') + '.png'
    src = TEXTURES / texture
    if not src.exists(): raise ValueError('Missing texture: '+str(src))
    dst = ROOT / 'assets/server' / texture
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    copied[dst.relative_to(ROOT).as_posix()] = {'source':src.relative_to(SERVER).as_posix(), 'sha256':hashlib.sha256(src.read_bytes()).hexdigest()}
    return dst.relative_to(ROOT).as_posix()
def icon(cmd):
    if int(cmd) not in items: raise ValueError('Missing CMD: '+str(cmd))
    return asset(items[int(cmd)])
font_icons = {}
for path in (IA / 'configs/font_icons').glob('*.yml'):
    for name, image in read(path).get('font_images', {}).items():
        texture = image.get('path', '')
        if image.get('symbol') and texture.startswith(('abilities/', 'stats/', 'status_effects/')):
            font_icons[image['symbol']] = texture
used_font_icons = {}

def clean(s, keep_icons=False):
    s = re.sub(r'<#[0-9a-fA-F]{6}>|&[0-9a-fk-orA-FK-OR]', '', str(s))
    # Keep content icons in rich lore; remove game-only padding and tooltip frames.
    def glyph(match):
        char = match.group()
        if keep_icons and char in font_icons:
            if char not in used_font_icons: used_font_icons[char] = asset(font_icons[char])
            return char
        return ''
    s = re.sub(r'[\ue000-\uf8ff\u1000-\u1fff\ua000-\ud7ff\u0c00-\u0cff\u3100-\u31ff\uff61-\uff9f丮ロぁデト]', glyph, s)
    return s.strip()

def rich_lore(node, override):
    original = {str(k):[clean(x, True) for x in ls if clean(x)] for k,ls in node.get('lores',{}).items()}
    if not override: return original
    # Editorial corrections retain matching source icons without restoring old text.
    result = {}
    for level, lines in override.items():
        source = original.get(level, original.get('0', []))
        result[level] = []
        for line in lines:
            label = re.split('[：:]', line)[0]
            match = next((raw for raw in source if clean(raw) == line or (re.search('[：:]', line) and re.split('[：:]', clean(raw))[0] == label)), '')
            icons = ''.join(c for c in match if c in used_font_icons)
            result[level].append((icons+' ' if icons else '')+line)
    return result

data = {'date':'2026-11-13', 'classes':{}, 'skills':{}, 'assets':{}}
corrections=json.loads((ROOT/'_maintenance/combat-corrections.json').read_text(encoding='utf-8'))
editorial=json.loads((ROOT/'_maintenance/combat-lore-copy.json').read_text(encoding='utf-8'))
for cls in ['战士','法师','牧师']:
    c = read(SERVER / f'plugins/MMOCore/classes/{cls}.yml')
    data['classes'][cls] = {'attributes':c['attributes'], 'skills':list(c['skills'])}
    for name, unlock in sorted(c['skills'].items(), key=lambda pair:pair[1]['level']):
        source = f'plugins/MythicLib/skill/{name}.yml'
        s = read(SERVER / source)[name]
        tsource = f'plugins/MMOCore/skill-trees/{name}技能树.yml'
        tree = read(SERVER / tsource)
        skill = {'name':name, 'class':cls, 'unlock':unlock['level'], 'maxLevel':unlock['max-level'],
                 'parameters':{k:v['player'] for k,v in s['parameters'].items() if 'player' in v},
                 'lore':[clean(x) for x in s.get('lore',[]) if clean(x)],
                 'icon':icon(str(s['icon']).split(':')[-1]), 'budget':tree['max-point-spent'], 'nodes':[],
                 'sources':[source,tsource,f'plugins/MythicMobs/skills/职业技能/{cls}/{name}.yml']}
        # Preserve nearby Chinese parameter comments as human-readable reference labels.
        comments=[]; labels={}
        for line in (SERVER/source).read_text(encoding='utf-8-sig').splitlines():
            if line.lstrip().startswith('#'): comments.append(line.lstrip()[1:].strip())
            elif re.match(r'^    [\w-]+:$', line):
                labels[line.strip()[:-1]]='；'.join(comments); comments=[]
            elif line.strip(): comments=[]
        skill['parameterNotes']=labels
        for nid,n in tree['nodes'].items():
            coords=[int(x) for x in n['coordinates'].split(',')]
            parents=n.get('parents',{}).get('strong',{})
            skill['nodes'].append({'id':nid,'name':clean(n['name']),'x':coords[0],'y':coords[1],
                'max':n['max-level'],'cost':n.get('point-consumed',1),'root':n.get('root',False),
                'icon':icon(n['display']['unlocked']['custom-model-data']),
                'lockedIcon':icon(n['display']['locked']['custom-model-data']),
                'lore':editorial.get(name,{}).get(nid) or {str(k):[clean(x) for x in ls if clean(x)] for k,ls in n.get('lores',{}).items()},
                'richLore':rich_lore(n, editorial.get(name,{}).get(nid)),
                'parents':[{'id':p,'level':v.get('level',0),'path':[[int(x) for x in str(xy).split(',')] for xy in v.get('paths',[])]} for p,v in parents.items()],
                'buffs':n.get('experience-table',{}), 'executionNote':corrections.get(name,{}).get(nid,'')})
        data['skills'][name]=skill
data['assets']['background']=asset('gui/skilltree_gui')
data['assets']['paths']={}
for code,shape in {20:'up',60:'right',54:'right',8:'up_right',56:'up_left',24:'down_right',72:'down_left'}.items():
    data['assets']['paths'][str(code)]=asset('gui/skilltree/skilltree_path_unlocked_'+shape)
for code in [26,62,74,78,80]:
    data['assets']['paths'][str(code)]=icon(28000+code)
for key in ['arrow_up','arrow_down','arrow_left','arrow_right','reset','skilllocked','skillunlock']:
    data['assets'][key]=asset('gui/'+key)
for p in (TEXTURES/'stats').glob('*.png'): asset(p.relative_to(TEXTURES).as_posix())
data['assets']['loreIcons']=used_font_icons
write(ROOT/'assets/data/combat.json',data)
write(ROOT/'_maintenance/combat-assets.json',copied)
print(f"Exported {len(data['skills'])} skills, {sum(len(s['nodes']) for s in data['skills'].values())} nodes, {len(copied)} original assets.")
