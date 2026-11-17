"""Refresh dungeon rules and original art from the server checkout (read-only)."""
from pathlib import Path
import hashlib, json, re, shutil, sys
import yaml

root = Path(__file__).resolve().parents[1]
server = Path(sys.argv[1]) if len(sys.argv) > 1 else root.parent / 'top-craft2'
sources = {}
def read(path):
    raw = (server / path).read_bytes()
    sources[path] = hashlib.sha256(raw).hexdigest()
    return raw.decode('utf-8-sig')

keys = yaml.safe_load(read('plugins/TopCraftDungeonKeys/config.yml'))
entrance = yaml.safe_load(read('plugins/TopCraftDungeonKeys/entrance.yml'))
season = json.loads(read('plugins/TopCraftDungeonProgress/definitions/season-1.json'))
scaling = read('plugins/MythicMobs/skills/秘境_系统技能/数值初始化.yml')
growth = float(re.search(r'value="([\d.]+)\^\(<world.var.Layer>-1\)', scaling)[1])
maps = []
for ident, slug in [('1001','mushroom'),('1003','desert'),('1004','sakura')]:
    m = keys['dungeons'][ident]
    maps.append(dict(id=ident, slug=slug, name=m['name'], limit=m['limit-seconds'], enabled=m['enabled']))
data = dict(season=season['title'], maps=maps, capacity=entrance['ready-ui']['capacity'],
            unkeyedLayer=entrance['unkeyed-layer'], readySeconds=entrance['ready-timeout-seconds'],
            rapidRatio=keys['rapid-ratio'], keyRules=keys['key-rules'], growth=growth,
            deathPenalty=15, scoreRules=season['scoreRules'], rewards=season['rewards'])
for path in ['蘑菇森林技能/全流程.yml','赤沙遗迹/场次与交互.yml','樱落溪涧技能/全流程.yml']:
    assert 'dungeonrules{deathpenalty=15;respawn=true}' in read('plugins/MythicMobs/skills/'+path)

art = 'plugins/ItemsAdder/contents/topcraft/resourcepack/assets/'
icons = {
    'key': art+'topcraft_progress/textures/buttons/key.png',
    'socket-key': art+'topcraft_progress/textures/buttons/socket_key.png',
    'white-jade': art+'topcraft/textures/dungeon/yl_white_jade.png',
    'black-jade': art+'topcraft/textures/dungeon/yl_black_jade.png',
    'fire': art+'topcraft/textures/stats/fire.png',
    'rainbow': art+'topcraft/textures/buffs/rainbow_spore.png',
}
for name in ['gold','diamond','emerald','obsidian','crying-obsidian']:
    icons[name] = 'plugin-src/topcraft-dungeon-progress/ui/badges/'+name+'.png'
manifest = {}
for name, path in icons.items():
    raw = (server/path).read_bytes()
    dest = 'assets/server/dungeons/'+name+'.png'
    (root/dest).parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(server/path, root/dest)
    manifest[dest] = dict(source=path, sha256=hashlib.sha256(raw).hexdigest(), kind='server-original')

# Retain evidence for authored mechanics without making a second server configuration.
for directory in ['蘑菇森林技能','赤沙遗迹','樱落溪涧技能']:
    for path in (server/'plugins/MythicMobs/skills'/directory).rglob('*.yml'):
        read(path.relative_to(server).as_posix())
for directory in ['蘑菇森林','赤沙遗迹','樱落溪涧']:
    for path in (server/'plugins/MythicMobs/mobs'/directory).rglob('*.yml'):
        read(path.relative_to(server).as_posix())
for path in [
    'plugin-src/topcraft-dungeon-progress/src/main/java/topcraft/progress/season/ScoreRules.java',
    'plugin-src/topcraft-dungeon-progress/src/main/java/topcraft/progress/season/ScorePoints.java',
    'plugin-src/topcraft-dungeon-progress/src/main/java/topcraft/progress/storage/ProgressStore.java',
    'plugin-src/topcraft-dungeon-progress/src/main/java/topcraft/progress/storage/LeaderboardQueries.java',
    'plugin-src/topcraft-dungeon-keys/src/main/java/topcraft/dungeons/TopCraftDungeonKeys.java',
    'plugin-src/topcraft-dungeon-keys/src/main/java/topcraft/dungeons/SeasonEntrance.java',
    'plugin-src/topcraft-dungeon-keys/src/main/java/topcraft/dungeons/DungeonRun.java',
    'plugin-src/topcraft-dungeon-keys/src/main/java/topcraft/dungeons/DungeonStore.java',
    'plugin-src/topcraft-dungeon-keys/src/main/java/topcraft/dungeons/DungeonContent.java',
    'plugin-src/topcraft-dungeon-keys/src/main/java/topcraft/dungeons/DungeonResources.java',
]: read(path)
for path, value in [('assets/data/dungeons.json',data),('_maintenance/dungeon-assets.json',manifest),('_maintenance/dungeon-sources.json',sources)]:
    (root/path).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
routes = ['/'] + sorted('/'+p.relative_to(root).with_suffix('').as_posix() for folder in ['combat','equipment','world','quests','dungeons','life','social','guide'] for p in (root/folder).rglob('*.md'))
(root/'assets/search-paths.js').write_text('window.TopCraftSearchPaths = '+json.dumps(routes,ensure_ascii=False,indent=2)+';\n',encoding='utf-8')
print(f'Dungeons: {len(maps)} maps, {len(icons)} original images, {len(sources)} sources.')
