"""Refresh social query data and original icons. Only writes the Wiki checkout."""
from pathlib import Path
import json, shutil, hashlib, sys, yaml
root=Path(__file__).resolve().parents[1]
server=Path(sys.argv[1]) if len(sys.argv)>1 else root.parent/'top-craft2'
def read(path):return yaml.safe_load((server/path).read_text(encoding='utf-8-sig'))
core=read('plugins/MMOCore/config.yml')
classes=[read('plugins/MMOCore/classes/'+p+'.yml')['max-level'] for p in ['战士','法师','牧师']]
assert len(set(classes))==1, 'Update calculator for unequal class level caps'
data={'maxMembers':core['party']['max-players'],'maxSpread':core['party']['max-level-difference'],'maxLevel':classes[0]}
(root/'assets/data/social.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
icons={'create':'party_menu/create','invite':'party_menu/invite','leave':'party_menu/leave','hall':'party_recruitment/hall','recruit':'party_recruitment/recruit_on','travel':'party_recruitment/travel','trade':'profile/trade','friend':'profile/friend','identity':'profile/identity','like':'profile/appreciation','gift':'invite/gift','milestone':'invite/milestone'}
manifest={}
for name,texture in icons.items():
    src=server/('plugins/ItemsAdder/contents/topcraft/resourcepack/assets/topcraft/textures/gui/'+texture+'.png')
    if not src.exists():raise FileNotFoundError(src)
    dest='assets/server/social/'+name+'.png'
    (root/dest).parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,root/dest)
    manifest[dest]={'source':src.relative_to(server).as_posix(),'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'kind':'server-original'}
(root/'_maintenance/social-assets.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
routes=['/']
for section in ['combat','guide','equipment','world','quests','dungeons','life','social']:routes.extend('/'+p.relative_to(root).with_suffix('').as_posix() for p in sorted((root/section).rglob('*.md')))
(root/'assets/search-paths.js').write_text('window.TopCraftSearchPaths = '+json.dumps(routes,ensure_ascii=False,indent=2)+';\n',encoding='utf-8')
print(json.dumps({'icons':len(manifest),'party':data}))
