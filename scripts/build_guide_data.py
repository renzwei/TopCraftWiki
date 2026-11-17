"""Refresh starter-guide icons and configuration data; never writes the server."""
from pathlib import Path
import hashlib, json, shutil, sys, yaml
root = Path(__file__).resolve().parents[1]
server = Path(sys.argv[1]) if len(sys.argv)>1 else root.parent/'top-craft2'
gui = 'plugins/ItemsAdder/contents/topcraft/resourcepack/assets/topcraft/textures/gui/'
icons = {f'inventory-{n}':gui+'player_inventory/'+n+'.png' for n in ['personal_info','backpack','skills','class_select','main_menu','coin']}
icons.update({f'menu-{n}':gui+'main_menu/'+n+'.png' for n in ['quests','commissions','professions','party','builds','announcements']})
icons.update({f'reward-{n}':gui+'rewards/'+n+'.png' for n in ['daily','weekly','monthly','daily_wait','weekly_wait','monthly_wait','settings_icon','switch_on','switch_off']})
icons['inventory-panel']='plugins/ItemsAdder/contents/topcraft/resourcepack/assets/minecraft/textures/gui/container/inventory.png'
for n in ['health_fill','mana_fill','shield_fill','resource_track','experience_track','experience_fill','skill_plate','skill_fireball','skill_frame','skill_cooldown_mask','skill_mana_mask','skill_empty_mark','skill_ready','mana_warning']:
    icons['hud-'+n]='plugins/BetterHud/assets/mainhud_'+n+'.png'
manifest={}
for name,source in icons.items():
    src=server/source; dest='assets/server/guide/'+name+'.png'
    (root/dest).parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(src,root/dest)
    manifest[dest]={'source':source,'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'kind':'server-original'}
(root/'_maintenance/guide-assets.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
reward=yaml.safe_load((server/'plugins/DailyRewards/config.yml').read_text(encoding='utf-8'))['config']
data={'address':'topcraft.cc','clientVersion':'1.21','connectionSource':'User confirmation, 2026-11-16','rewardPlayMinutes':reward['first-time-join-required-play-time'],'rewards':{}}
for kind in ['daily','weekly','monthly']:
    data['rewards'][kind]={'hours':reward[kind+'-cooldown'],'availableOnFirstJoin':reward[kind+'-available-after-first-join'],'actions':reward[kind+'-rewards']}
(root/'assets/data/guide.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
routes=['/']
for section in ['combat','guide','equipment','world','quests','dungeons','life','social']:
    routes.extend('/'+p.relative_to(root).with_suffix('').as_posix() for p in sorted((root/section).rglob('*.md')))
(root/'assets/search-paths.js').write_text('window.TopCraftSearchPaths = '+json.dumps(routes,ensure_ascii=False,indent=2)+';\n',encoding='utf-8')
print(json.dumps({'icons':len(manifest),'rewardPlayMinutes':data['rewardPlayMinutes'],'cooldowns':{k:v['hours'] for k,v in data['rewards'].items()}}))
