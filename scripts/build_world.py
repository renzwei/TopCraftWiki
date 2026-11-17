"""Build the world atlas from installed server data. Writes only to the wiki.

Usage: python -X utf8 scripts/build_world.py [server-directory]
Editorial descriptions are kept here; coordinates, encounters and loot are read
from the server. Merely existing mob/world files are not public destinations.
"""
from pathlib import Path
from collections import defaultdict
import sys, re, json, html, hashlib, shutil
import yaml

ROOT = Path(__file__).resolve().parents[1]
SERVER = Path(sys.argv[1]) if len(sys.argv)>1 else ROOT.parent/'top-craft2'
MM = SERVER/'plugins/MythicMobs'
sources=set(); assets={}
def read(p):
    p=Path(p); sources.add(p.relative_to(SERVER).as_posix())
    return yaml.safe_load(p.read_text(encoding='utf-8-sig')) or {}
def write(p,s):
    p=ROOT/p; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(s,encoding='utf-8',newline='\n')
def esc(s): return html.escape(str(s),quote=True)
def clean(s): return re.sub(r'[&§][0-9a-fklmnor]|[\ue000-\uf8ff]', '',str(s),flags=re.I).strip()
def link(p,s): return f'<a href="#/{p}">{esc(s)}</a>'
def table(head,rows): return '\n| '+' | '.join(head)+' |\n| '+' | '.join(['---']*len(head))+' |\n'+''.join('| '+' | '.join(map(str,r))+' |\n' for r in rows)+'\n'
def page(route,title,lead,body):
    crumb=link('world/overview','世界探索')
    if route.startswith('regions/'): crumb+=' / '+link('world/forest','落日森林')
    if route.startswith('bosses/'): crumb+=' / '+link('world/bosses','野外领主')
    write('world/'+route+'.md',f'<p class="eyebrow">TOPCRAFT / 世界探索</p>\n\n<nav class="world-breadcrumb" aria-label="当前位置">{crumb}</nav>\n\n# {title}\n\n<p class="lead">{lead}</p>\n\n{body}\n\n<div class="page-end">TopCraft 玩家手册 · 世界资料 · 2026-11-16</div>\n')
def coords(p): return ' / '.join(f'{p[k]:.1f}'.rstrip('0').rstrip('.') for k in ('x','y','z'))
def copy(p):
    dest='assets/server/world/'+p.name; (ROOT/dest).parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(p,ROOT/dest); assets[dest]={'source':p.relative_to(SERVER).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'kind':'server-original'}
    return dest
def mapbox(which='forest',selected=''):
    return f'<div class="world-map" data-map="{which}" data-selected="{selected}"><p>正在加载区域示意图。下方的地区目录与坐标表也可直接查询位置。</p></div>\n\n'
def cards(rows):
    return '<div class="entry-grid">'+''.join(f'<a class="entry-card" href="#/{p}"><strong>{esc(t)}</strong><span>{esc(d)}</span></a>' for p,t,d in rows)+'</div>\n\n'

region_names={'df_mxzyd':'冒险者营地','df_clly':'璨蓝林野','df_fspy':'符石平原','df_rydk':'日影洞窟','df_ywsg':'遗忘山谷','df_lrzs':'落日之森','df_yxjy':'余响交椅','df_hyjt':'回音祭坛','df_djt':'断剑台'}
slugs=dict(zip(region_names,['camp','blue-woods','runestone-plains','sunshadow-cave','forgotten-valley','sunset-woods','echo-seat','echo-altar','broken-sword-terrace']))
introductions={
'df_mxzyd':'落日森林的落脚点。营地中的玛蕾、阿缇和托宾提供森林前段任务，其他驻员可交谈了解营地与遗迹。',
'df_clly':'晶蓝史莱姆与野兔出没的林野，也是「东路的第一趟」与「巡查补给」的狩猎地点。',
'df_fspy':'符文怪物聚集的平原。骑士、亡灵和灵狼近身攻击，术士远程施法；东南侧还有带领狼群的符文驯兽师。',
'df_rydk':'位于地下的狭长洞窟。黯日石傀能治疗附近同伴，磷穴幽偶则靠近目标攻击。',
'df_ywsg':'白骨骷髅和弓箭手出没的山谷，位于符石平原以东。苍白骨片是这里的主要掉落。',
'df_lrzs':'虎头蜂魂灵与低等级符文怪物共同出没的森林。这里的敌人等级跨度较大，蜂魂露可从虎头蜂魂灵身上取得。',
'df_yxjy':'失魂掠夺者、战灵、巫师和守卫聚集的区域。敌人等级为 25–29，掉落回响魂灰与灵魂结晶。',
'df_hyjt':'破碎魂灵的挑战地点。祭坛骷髅头结束倒计时后，攻击它即可唤醒领主。',
'df_djt':'区域事件「昔日幻影」的战场。集结后清剿残阳军势，再迎战残阳君主罗斯特·席尔德。'}
regions=[]
wg=read(SERVER/'plugins/WorldGuard/worlds/duskforest/regions.yml')['regions']
for rid,name in region_names.items():
    r=wg[rid]
    points=[[p['x'],p['z']] for p in r['points']] if 'points' in r else [[r['min']['x'],r['min']['z']],[r['max']['x'],r['min']['z']],[r['max']['x'],r['max']['z']],[r['min']['x'],r['max']['z']]]
    regions.append({'id':rid,'name':name,'points':points,'route':'world/regions/'+slugs[rid],'description':introductions[rid], 'underground':rid=='df_rydk'})

mobs={}; mob_paths={}
for p in sorted((MM/'mobs/落日森林').rglob('*.yml')):
    for k,v in read(p).items():
        if isinstance(v,dict): mobs[k]=v; mob_paths[k]=p
encounters=defaultdict(list)
for p in sorted((MM/'randomspawns').glob('落日森林*.yml')):
    for obj in read(p).values():
        rid=re.search(r'region\{r=([^}]+)',str(obj.get('Conditions',[]))).group(1)
        encounters[rid].extend(t.split()[0] for t in obj['Types'])
encounters['df_fspy'].append('符文驯兽师')
encounters['df_hyjt']=['破碎魂灵']
encounters['df_djt']=['残阳斥候','残阳弩手','残阳祭司','残阳血卫','残阳幼龙','残阳君主']
active=list(dict.fromkeys(n for rid in region_names for n in encounters[rid]))
mob_ids={n:'monster-'+str(i+1) for i,n in enumerate(active)}
# Stable IDs are based on server identifiers, not list order.
mob_ids={n:'mob-'+hashlib.sha1(n.encode()).hexdigest()[:10] for n in active}
def levels(n):
    skills=' '.join(str(s) for s in mobs[n].get('Skills',[]))
    m=re.search(r'setlevel\{[^}]*l=<random\.(\d+)-(\d+)>',skills)
    if m:return f'{m[1]}–{m[2]}'
    m=re.search(r'setlevel\{[^}]*l=(\d+)',skills)
    return m[1] if m else '—'
def moblink(n):
    p={'破碎魂灵':'world/bosses/shattered-soul','残阳君主':'world/bosses/sunset-lord'}.get(n,'world/monsters?id='+mob_ids[n])
    return link(p,n)

items={}
for p in (SERVER/'plugins/MMOItems/item').glob('*.yml'):
    for k,v in read(p).items():
        if isinstance(v,dict) and isinstance(v.get('base'),dict): items[(p.stem.upper(),k)]=clean(v['base'].get('name',k))
materials=(ROOT/'equipment/materials.md').read_text(encoding='utf-8')
mat_images={}
for card in re.findall(r'<article\b.*?</article>',materials,re.S):
    ident=re.search(r'id="([^"]+)"',card); img=re.search(r'<img[^>]+src="([^"]+)"',card)
    if ident and img: mat_images[ident[1]]=img[1]
drop_tables=read(MM/'droptables/落日森林_材料掉落.yml')
def loot(n,compact=False):
    rows=[]
    for line in drop_tables.get('落日森林_材料_'+n,{}).get('Drops',[]):
        m=re.match(r'mmoitems\{type=([^;]+);id=([^;}]+)[^}]*\}\s+(\S+)\s+([\d.]+)',line)
        if not m: raise ValueError(line)
        typ,ident,qty,chance=m.groups(); slug=ident.lower().replace('_','-'); name=items[(typ.upper(),ident)]
        if 'to' in qty:
            lo,hi=map(float,qty.split('to')); qty=f'{int(lo+.5)}–{int(hi-.5)}'
        img=mat_images.get(slug)
        icon=f'<img class="world-item-icon" src="{img}" alt="" loading="lazy">' if img else ''
        rows.append([icon+link('equipment/materials?id='+slug,name),qty,f'{float(chance)*100:g}%'])
    if compact: return '、'.join(r[0] for r in rows)
    return table(['材料','数量','掉落几率'],rows)

npcs=read(SERVER/'plugins/Citizens/saves.yml')['npc']
npcs={str(k):v for k,v in npcs.items()}
services=read(SERVER/'plugins/TopCraftProfessionMarket/profession-npcs.yml')['npcs']
service_links={'烹饪':('life/crafting','制作食物'),'炼药':('life/crafting','制作药水'),'锻造':('equipment/catalog','锻造装备与工具'),'冶炼':('life/crafting','加工矿石与材料'),'采集':('life/market','采集工具与资源收购'),'伐木':('life/market','伐木工具与资源收购'),'挖掘':('life/market','挖掘工具与资源收购'),'垂钓':('life/market','钓竿、鱼饵与鱼获收购')}
camp_roles={0:('leader','营地领队','接取「东路的第一趟」并报告探索进展。'),1:('repairer','整备员','「巡查补给」：收集 8 张柔软兽皮并交付。'),2:('scribe','记录员','交谈了解营地与森林。'),4:('scout','斥候','「核对林野旧路」与「平原入口的威胁」相关任务。'),5:('apothecary','药剂师','营地补给与药剂相关对话。'),6:('researcher','研究员','符石与遗迹相关对话。'),7:('coachman','驿站车夫','可以交谈；传送服务尚未开放。'),8:('guild_delegate','公会派驻员','可以交谈；尚未提供委托领取与结算。')}
markers=[]; camp_cards=[]
for key,(portrait,role,desc) in camp_roles.items():
    npc=npcs[str(key)]; pos=npc['traits']['location']; name=npc['name']; image=copy(SERVER/f'plugins/LuxDialogues/Pack/Images/df_camp_{portrait}.png')
    markers.append({'id':'npc-'+str(key),'name':name,'x':pos['x'],'z':pos['z'],'y':pos['y'],'kind':'npc','description':role+' · '+desc,'route':'world/regions/camp?id=npc-'+str(key)})
    camp_cards.append(f'<article class="world-npc" id="npc-{key}"><img src="{image}" alt="{name}的游戏内对话头像" loading="lazy"><div><h3>{name} · {role}</h3><p class="world-coord">X / Y / Z：{coords(pos)}</p><p>{desc}</p></div></article>')
for key,portrait,role in [(9,'leader','学者领队'),(10,'epigrapher','铭文学者')]:
    npc=npcs[str(key)]; pos=npc['traits']['location']; image=copy(SERVER/f'plugins/LuxDialogues/Pack/Images/df_scholar_{portrait}.png')
    markers.append({'id':'npc-'+str(key),'name':npc['name'],'x':pos['x'],'y':pos['y'],'z':pos['z'],'kind':'npc','description':role+' · 位于营地西南方的遗迹附近。','route':'world/forest?id=学者驻地'})
town_markers=[]; town_rows=[]
for key,v in services.items():
    npc=npcs[str(key)]; pos=npc['traits']['location']; name=v['display-name']; role=v['profession-name']
    route,desc=service_links.get(role,('guide/rewards','领取每日、每周、每月奖励'))
    town_rows.append([name,role,coords(pos),link(route,desc)])
    town_markers.append({'id':'service-'+str(key),'name':name,'x':pos['x'],'y':pos['y'],'z':pos['z'],'kind':'npc','description':role+' · '+desc,'route':route})
worlds=read(SERVER/'plugins/Multiverse-Core/worlds.yml')['worlds']
spawn=worlds['duskforest']['spawnLocation']; town_spawn=worlds['lobby']['spawnLocation']
markers.append({'id':'arrival','name':'森林抵达点','kind':'arrival',**{k:float(spawn[k]) for k in ('x','y','z')},'description':'抵达位置；主城往返入口尚未开放。','route':'world/overview'})
for file,name,kind,route in [('落日森林_夜巡驯兽师.yml','符文驯兽师','elite','world/monsters?id='+mob_ids['符文驯兽师']),('破碎魂灵.yml','破碎魂灵','boss','world/bosses/shattered-soul'),('事件管理器_断剑台.yml','昔日幻影','event','world/events/past-phantoms')]:
    obj=next(iter(read(MM/'spawners'/file).values()))
    # Spawner locations use capitalized field names.
    markers.append({'id':kind,'name':name,'kind':kind,'x':obj['X'],'y':obj['Y'],'z':obj['Z'],'route':route,'description':{'elite':'15–17 级精英 · 带领两只灵狼','boss':'25 级领主 · 攻击就绪的祭坛骷髅头召唤','event':'区域事件 · 集结、清剿与残阳君主'}[kind]})
data={'forest':{'name':'落日森林','bounds':[-245,-350,720,590],'regions':regions,'markers':markers},'town':{'name':'主城','bounds':[-85,-20,145,115],'regions':[],'markers':town_markers+[{'id':'town-arrival','name':'主城抵达点','kind':'arrival',**{k:float(town_spawn[k]) for k in ('x','y','z')},'description':'主城的抵达位置。','route':'world/overview'}]},'camp':{'name':'冒险者营地','bounds':[100,-277,100,65],'regions':[],'markers':[m for m in markers if m['id'].startswith('npc-') and int(m['id'][4:])<9]+[next(m for m in markers if m['id']=='arrival')]}}
write('assets/data/world.json',json.dumps(data,ensure_ascii=False,indent=2)+'\n')

page('overview','世界地图与旅行','从主城服务、森林地区到野外领主，按目的地查找位置、敌人和奖励。',f'''<div class="notice"><strong>旅行入口尚未开放。</strong>主城与落日森林的往返传送计划通过 NPC 提供，目前还不能通过 NPC、菜单或旅行指令往返。</div>

{cards([('world/town','主城与服务','锻造、炼药、烹饪、生活商人和周期奖励'),('world/forest','落日森林','9 个地区、区域示意图、NPC 与遭遇战'),('world/bosses','野外领主','破碎魂灵与残阳君主的召唤、招式和掉落'),('world/events','区域事件','昔日幻影：集结、清剿、首领战与冷却')])}
## 抵达位置

坐标依次为 **X / Y / Z**。X 向东增大，Z 向南增大，Y 表示高度。

{table(['目的地','抵达坐标','周边'],[['主城',coords(town_spawn),link('world/town','职业服务与商人')],['落日森林',coords(spawn),link('world/regions/camp','冒险者营地')]])}
## 队伍同行

主城与落日森林之间的队长跨世界移动会带上仍在出发世界的在线队员，队员抵达目的地的固定抵达点。队员自行换世界不会带走队伍；身处其他世界的队员也不会被召集。

死亡、正在骑乘或载有乘客的队员不会自动跟随。这套同行规则不提供旅行入口；往返 NPC 开放后才能通过该入口使用。[组队与队伍大厅](social/party.md)

## 秘境

秘境的入口、钥匙和计时规则见[秘境挑战](dungeons/overview.md)。落日森林的野外领主与区域事件在森林地图内进行。
''')
page('town','主城与服务','按 NPC 名称、服务类型与坐标寻找主城设施。',mapbox('town')+'## NPC 与服务\n\n接近下列 NPC 后与其交互即可打开对应服务。\n\n'+table(['NPC','服务','X / Y / Z','查看详情'],town_rows)+'''## 常用查询

制作前可先查[材料图鉴](equipment/materials.md)与[装备图鉴](equipment/catalog.md)；工具维修和资源出售见[生活商人](life/market.md)。主城与落日森林的传送 NPC 尚未开放，旅行状态见[世界地图与旅行](world/overview.md)。
''')

region_rows=[]
for r in regions:
    ns=encounters[r['id']]; ranges=[int(v) for n in ns for v in levels(n).split('–') if v.isdigit()]
    lv=('—' if not ranges else str(min(ranges)) if min(ranges)==max(ranges) else f'{min(ranges)}–{max(ranges)}')
    r['level']=lv
    region_rows.append([link(r['route'],r['name']),lv,'、'.join(moblink(n) for n in ns) if ns else '营地 NPC 与任务'])
page('forest','落日森林','以冒险者营地为落脚点，探索符文遗迹、地下洞窟与失魂魔物的栖地。',mapbox()+'''区域示意图按坐标绘制，显示地区边界与已知地点；不表示道路、地形或可通行路线。点击地区查看详情，点击标记查看坐标。

## 地区目录

下表为各地出现的怪物等级。落日之森同时存在 7–15 级怪物与 23–26 级虎头蜂魂灵。

'''+table(['地区','怪物等级','主要遭遇'],region_rows)+'''## 学者驻地

伊蕾娜与诺菈在营地西南方的遗迹附近，位置不在冒险者营地边界内。学者对话随森林任务推进。

'''+table(['NPC','身份','X / Y / Z'],[[f'<img class="world-scholar-portrait" src="assets/server/world/df_scholar_{portrait}.png" alt="" loading="lazy"> '+npcs[str(k)]['name'],role,coords(npcs[str(k)]['traits']['location'])] for k,role,portrait in [(9,'学者领队','leader'),(10,'铭文学者','epigrapher')]])+'''## 任务与材料

营地的[森林任务](quests/forest.md)会引导你前往璨蓝林野与符石平原。击败敌人获得的材料可在[材料图鉴](equipment/materials.md)查询用途与配方；具体来源、数量和几率列在[怪物图鉴](world/monsters.md)中。
''')

for r in regions:
    rid=r['id']; ns=encounters[rid]; xs=[p[0] for p in r['points']]; zs=[p[1] for p in r['points']]
    body=f'<div class="world-facts"><span>怪物等级 <b>{r["level"]}</b></span><span>X 范围 <b>{min(xs)} 至 {max(xs)}</b></span><span>Z 范围 <b>{min(zs)} 至 {max(zs)}</b></span></div>\n\n'+mapbox('camp' if rid=='df_mxzyd' else 'forest',rid)
    if rid=='df_mxzyd': body+='## 营地人物\n\n<div class="world-npc-grid">'+''.join(camp_cards)+'</div>\n\n任务接取顺序和目标见[落日森林任务](quests/forest.md)。需要装备制作、材料加工与资源出售时，可查[主城服务](world/town.md)；主城往返 NPC 目前尚未开放。\n'
    else:
        body+='## 怪物与遭遇\n\n'+table(['敌人','等级','类别'],[[moblink(n),levels(n),'领主' if n in ('破碎魂灵','残阳君主') else '精英' if n=='符文驯兽师' else '事件怪物' if rid=='df_djt' else '普通怪物'] for n in ns])
        if rid=='df_rydk': body+='洞窟位于 **Y = 6–24** 的地下空间。仅到达相同 X / Z 的地表位置，仍不在洞窟内。黯日石傀会分 3 次治疗自己与 8 格内的石傀、幽偶，每次恢复 5% 生命；先击败治疗者可减少战斗消耗。\n\n'
        if rid=='df_fspy': body+='普通符文怪物在平原 **Y < 12** 的地带出没。符文驯兽师位于 **257 / 7 / 16**，带有两只 13–15 级灵狼；击败驯兽师后灵狼消失。\n\n[平原入口的威胁](quests/forest.md)需要击败 15 只普通符文怪物。\n\n'
        if rid=='df_clly': body+='「东路的第一趟」需要击败 **8 只晶蓝史莱姆**；「巡查补给」需要 **8 张柔软兽皮**，可从野兔身上收集。接取与交付见[森林任务](quests/forest.md)。\n\n'
        if rid=='df_hyjt': body+='领主祭坛在 **−29 / 31 / −130**。等待 **300 秒**倒计时结束，出现攻击提示后连续攻击骷髅头，开启[破碎魂灵](world/bosses/shattered-soul.md)战斗。\n\n'
        if rid=='df_djt': body+='战场中心为 **136 / 25 / 152**。事件就绪后靠近即可触发集结，先在 4 分钟内击败 36 名残阳军势，再于 10 分钟内击败残阳君主。完整流程见[昔日幻影](world/events/past-phantoms.md)。\n\n'
        body+='## 掉落与用途\n\n'+''.join(f'**{n}**：{loot(n,True)}。\n\n' for n in ns)
        body+='各项掉落的数量与几率见上方敌人链接；材料页面可继续查询制作配方。\n'
    page('regions/'+slugs[rid],r['name'],introductions[rid],body)

behaviors={
'晶蓝史莱姆':'靠近目标攻击；掉落晶蓝胶质，可同时完成「东路的第一趟」。',
'野兔':'近身攻击。柔软兽皮是「巡查补给」所需材料。',
'符文骑士':'持械近战，与其他符文怪物共同出现。',
'符文亡灵':'靠近目标进行近战攻击。',
'符文灵狼':'追近目标后撕咬。也会出现在落日之森。',
'符文刺客':'近战强袭型敌人，出现在符石平原。',
'符文术士':'从远处发射魔法弹，与近战符文怪物一同出现。',
'黯日石傀':'受击时有 5% 几率施放治疗，冷却 15 秒。施法期间减速 4 秒，在第 1、2、3 秒分别恢复自身及 8 格内黯日石傀、磷穴幽偶 5% 生命。',
'磷穴幽偶':'近战强袭型敌人，可受到黯日石傀的群体治疗。',
'白骨骷髅':'近身挥击。苍白骨片的主要来源之一。',
'白骨弓箭手':'从远处射击，射击间隔 5 秒。',
'虎头蜂魂灵':'靠近目标攻击，等级明显高于同区域的史莱姆、灵狼与亡灵。掉落蜂魂露。',
'失魂掠夺者':'25–28 级近战敌人，是余响交椅中等级较低的一类。',
'失魂战灵':'27–29 级近战敌人，掉落回响魂灰与破碎的刃具。',
'失魂巫师':'远程型敌人，掉落回响魂灰、朽纹布片与魔尘。',
'失魂守卫':'铁壁型近战敌人，与掠夺者、战灵和巫师共同出现。',
'残阳斥候':'「昔日幻影」清剿阶段的近战敌人，击败后推进清剿进度。',
'残阳弩手':'「昔日幻影」清剿阶段的远程弩手。',
'残阳祭司':'「昔日幻影」清剿阶段的远程施法者，会发射火球。',
'残阳血卫':'「昔日幻影」后续波次中的铁壁型近战敌人。',
'残阳幼龙':'残阳君主的火球落点可能召来幼龙。幼龙近身攻击，出现在领主阶段。',
'符文驯兽师':'远程精英，带领两只 13–15 级符文灵狼。驯兽师死亡后，两只灵狼也会消失；召唤的灵狼不掉落物品。刷新点为 257 / 7 / 16，刷新冷却 300 秒，有玩家进入 32 格范围时才会激活刷新。'}
mob_cards=[]
for n in active:
    if n in ('破碎魂灵','残阳君主'):continue
    located=[rid for rid in region_names if n in encounters[rid]]
    grade='精英' if n=='符文驯兽师' else '普通怪物'
    body=f'<article class="world-monster" id="{mob_ids[n]}" data-regions="{" ".join(located)}" data-name="{n}"><div class="world-monster-heading"><h3>{n}</h3><span>{levels(n)} 级 · {grade}</span></div><p>{behaviors[n]}</p><p>出没：'+ '、'.join(link('world/regions/'+slugs[rid],region_names[rid]) for rid in located)+'</p>'
    rows=loot(n)
    # Raw HTML tables keep complete monster entries searchable by Docsify.
    lines=rows.strip().splitlines(); header=lines[0].strip('|').split('|')
    body+='<div class="world-loot"><table><thead><tr>'+''.join('<th>'+h.strip()+'</th>' for h in header)+'</tr></thead><tbody>'
    for line in lines[2:]: body+='<tr>'+''.join('<td>'+v.strip()+'</td>' for v in line.strip('|').split('|'))+'</tr>'
    body+='</tbody></table></div><p class="world-drop-note">随机装备掉落几率：'+('25%' if grade=='精英' else '3%')+'。<a href="#/equipment/quality">查看装备品质与词条</a></p></article>'
    mob_cards.append(body)
filters='<div class="world-filter"><label>查找怪物<input type="search" placeholder="输入怪物名称" data-monster-search></label><label>出没地区<select data-monster-region><option value="">全部地区</option>'+''.join(f'<option value="{rid}">{region_names[rid]}</option>' for rid in region_names if encounters[rid] and rid!='df_hyjt')+'</select></label><p data-monster-count role="status"></p></div>'
page('monsters','怪物图鉴','按地区或名称查找普通怪物、精英与事件敌人的等级、招式和完整材料掉落。',filters+'\n\n各项材料分别判定掉落，一次击败可能获得多种材料。随机装备的物品等级取决于怪物等级。两名领主的战斗与奖励见[野外领主](world/bosses.md)。\n\n<div class="world-monsters">'+''.join(mob_cards)+'</div>\n\n<p class="world-empty" hidden>没有符合条件的怪物。可以清空名称或切换地区。</p>')

page('bosses','野外领主','两场领主战都发生在落日森林：回音祭坛唤醒破碎魂灵，断剑台的昔日幻影召来残阳君主。',cards([('world/bosses/shattered-soul','破碎魂灵 · 25 级','回音祭坛 · 骷髅头召唤 · 瞬移、灵魂喷发与残灵'),('world/bosses/sunset-lord','残阳君主 · 25 级','断剑台 · 区域事件首领 · 烈阳驭天与残阳守卫套装')])+table(['领主','位置 X / Y / Z','单人生命','开启方式'],[['破碎魂灵','−29 / 31 / −130','30,000','祭坛倒计时结束后攻击骷髅头'],['残阳君主','136 / 25 / 152','35,400','完成昔日幻影的清剿阶段']])+'两名领主都有 **75%** 几率掉落一件随机装备。残阳君主额外掉落一件残阳守卫套装部件和一个残阳烬核。\n')
page('bosses/shattered-soul','破碎魂灵','回音祭坛的 25 级领主。瞬移后接续不同招式，生命降至 30% 时进入狂暴。','''## 召唤与重置

前往[回音祭坛](world/regions/echo-altar.md)的 **−29 / 31 / −130**。祭坛倒计时为 **300 秒**；出现「攻击骷髅头触发战斗」后，连续攻击骷髅头直至召唤演出开始。

领主距离出生点超过 **64 格**并持续 **10 秒**会重置；在计时结束前返回范围可以中止重置。重置会清理本轮召唤物并重新开始战斗。

## 生命与人数

单人生命 **30,000**，32 格内每增加一名玩家，生命上限增加 **15,000**。战斗中每 5 秒重新统计附近人数，人数变化时保留当前生命百分比。例如 4 人时为 **75,000** 生命。

## 招式与应对

| 招式 | 效果与范围 | 应对 |
| --- | --- | --- |
| 瞬移 | 移动到附近 4–8 格的位置，随后可能接圆斩、喷发、魂灵箭或召唤；冷却 3 秒 | 跟随落点观察下一次预兆 |
| 圆斩 | 红黑圆环预兆后攻击周围 5 格，随后向四方发射最远 15 格的十字剑气；每次命中造成 10 点伤害 | 看到圆环先离开近身范围，之后避开剑气方向 |
| 灵魂喷发 | 朝周围及远处玩家发射抛射弹；落点 4 格内造成 10 点伤害，冷却 5 秒 | 持续移动，离开弹体落点 |
| 魂灵箭 | 发射追踪箭，最多追踪附近 28 格内的 2 名玩家；命中造成 10 点伤害，并散布灵魂碎片 | 观察弹道，移动躲避，并处理落地碎片 |
| 召唤失落骑士 | 在周围 4 个方向召唤骑士，冷却 35 秒 | 留出走位空间，清理追近的骑士 |
| 灵魂碎片 | 受击时可能生成地面碎片；前 4 秒内靠近至 1.75 格可将其破坏，未破坏的碎片随后生长并召出残灵 | 尽早踩掉碎片，减少残灵数量 |
| 残灵 | 出现后 5–10 秒开始闪光自爆预兆，1.5 秒后消失并放出射线；射线最远 12 格，命中造成 10 点伤害 | 看到闪光及时拉开，避开散射的白色射线 |
| 狂暴 | 生命降至 30% 时加速；狂暴喷发冷却 4 秒，爆炸后还会散布灵魂碎片 | 保持移动避开喷发，在碎片生长前靠近清除 |

伤害数值为招式伤害，实际损失受角色[防御与恢复](combat/defense.md)影响。

## 掉落

随机装备：**75%** 几率掉落一件。领主采用个人掉落，战利品分别结算。

'''+loot('破碎魂灵'))
page('bosses/sunset-lord','残阳君主','罗斯特·席尔德，断剑台的 25 级领主。「昔日幻影」清剿完成后现身。','''## 开战条件与生命

在[昔日幻影](world/events/past-phantoms.md)中击败 **36** 名残阳军势后，于 **136 / 25 / 152** 迎战领主。首领战限时 **10 分钟**。

单人生命 **35,400**，每增加一名玩家增加 **17,700**。人数在领主出现时按附近 **32 格**内的玩家统计，最高按 **8 人**计算，本轮固定。4 人为 **88,500**，8 人为 **159,300**。8 人是生命计算上限，不是参战人数上限。

## 地面战斗

| 招式 | 效果与数值 | 应对 |
| --- | --- | --- |
| 火球连射 | 冷却 20 秒；向附近抛射多枚火球，落点 4 格内造成 10 点伤害，并可能召来斥候、弩手、祭司、血卫或幼龙 | 离开火球落点，清理新出现的敌人 |
| 大跳 | 朝远处目标跃起，落地时在 4 格内造成 10 点伤害，随后向外扩散火圈 | 看到跃起便离开落点，再避开向外移动的火圈 |
| 冲锋 | 冷却 18 秒；向远处目标冲锋，最远 25 格，终点 4 格内造成 10 点伤害 | 向冲锋方向的侧面闪开 |
| 直线攻击 | 冷却 5 秒；向正前方打出最远 16 格的地面攻击，命中造成 10 点伤害并击飞 | 避开领主正前方 |
| 扩散火圈 | 沿地面向四周扩散，最远 30 格，命中造成 10 点伤害 | 留意环形火线，跳过低矮的火圈 |

每轮天空阶段结束后回到地面战斗。表中为招式伤害，实际损失受角色防御影响。

## 烈阳驭天

开战约 **120 秒**后进入首次天空阶段，之后大机制冷却 **120 秒**。屏幕出现警示及「飞向天空，吸收残阳君主的力量！」时，领主返回场中，并在机制期间免疫伤害。

天空阶段开始后，场中每隔 **3 秒**对附近 **36 格**内、**Y < 30** 的玩家造成 **10 点伤害**，并点燃 **5 秒**。保持在 Y = 30–40 的空中可以避开这项地面伤害。

获得 **12 秒**的烈阳驭天后，朝想去的方向看即可飞行：抬头上升，低头下降。飞行作用高度为 **Y = 25–40**，需要处于领主附近 **64 格**内。吸收普通球或增益球可将持续时间刷新至 12 秒。

| 天空球 | 接触效果 | 处理方式 |
| --- | --- | --- |
| 普通球 | 3.5 格内吸收，刷新烈阳驭天 | 优先收集；阶段结束时每颗剩余普通球为领主恢复 5% 生命 |
| 增益球 | 3.5 格内吸收，刷新烈阳驭天并获得 60 秒跳跃提升 | 用于续飞与提高跳跃能力 |
| 危险球（冒黑烟） | 靠近 3 格触发爆炸，4 格内造成 10 点伤害，并为领主恢复 2% 生命 | 绕开，不要撞向它 |

天空阶段结束时飞行效果消失，并获得短暂缓降。机制期间先处理天空球，回到地面后继续攻击领主。

## 掉落

每次结算掉落 **1 件[残阳守卫套装](equipment/sets/df-sunset-guard.md)**，头盔、胸甲、护腿、靴子四个部位等概率；另有 **75%** 几率掉落一件随机装备。材料中必定包含 **1 个残阳烬核**。领主采用个人掉落，战利品分别结算。

'''+loot('残阳君主'))
page('events','区域事件','落日森林的公共战斗事件，可与附近玩家共同完成。',cards([('world/events/past-phantoms','昔日幻影 · 断剑台','60 秒集结 → 4 分钟清剿 → 10 分钟领主战')])+'''## 参加方式

事件就绪时靠近断剑台会开始集结，无需在任务手册中接取。事件状态与剩余时间在战场提示中显示；冷却中的事件不能立即重新开始。

完成后可从[残阳君主](world/bosses/sunset-lord.md)获得套装、随机装备和材料。事件的详细目标、失败条件和冷却见[昔日幻影](world/events/past-phantoms.md)。
''')
page('events/past-phantoms','昔日幻影','断剑台的区域事件。清剿残阳军势后，击败罗斯特·席尔德，终结昔日战场的幻影。','''<div class="world-facts"><span>地点 <b>断剑台</b></span><span>中心 <b>136 / 25 / 152</b></span><span>敌人 <b>25–29 级</b></span><span>事件冷却 <b>4 小时</b></span></div>

## 参加与流程

事件就绪后，进入战场中心 **96 格**范围即可开始集结。创造与旁观模式不计入参战人数。集结开始后，其他玩家也可进入战场共同作战。

<ol class="world-timeline"><li><strong>集结 · 60 秒</strong><p>靠近断剑台，等待集结倒计时结束。</p></li><li><strong>清剿 · 240 秒</strong><p>在 4 分钟内累计击败 36 名残阳军势。清剿完成后，剩余小怪被清除，领主现身。</p></li><li><strong>领主 · 600 秒</strong><p>在 10 分钟内击败残阳君主。领主出现后开始计算首领战时间。</p></li><li><strong>胜利与冷却</strong><p>领取领主掉落；本轮结束后进入 4 小时冷却。</p></li></ol>

## 清剿阶段

残阳斥候近身攻击，弩手与祭司在远处射击、施法，后续波次加入残阳血卫。每隔 **20 秒**尝试补充一批敌人；场上敌人较多时暂停补充。目标是累计击败 **36 名**，无需等待固定波数。

清剿阶段的四类敌人等级均为 **25–29**。领主阶段的火球还可能召来 **残阳幼龙**。各类敌人的材料掉落与几率见[怪物图鉴](world/monsters.md)。

## 领主阶段

残阳君主出现时，根据附近玩家人数确定本轮生命。战斗中会进入「烈阳驭天」阶段：收集天空球续飞，避开危险球，并减少普通球剩余数量。完整招式与生命数值见[残阳君主攻略](world/bosses/sunset-lord.md)。

## 失败与离场

清剿或领主阶段超时，事件失败。战场中心 96 格内连续 **90 秒**没有参战玩家时，本轮中止。领主异常消失也会结束本轮；离开后重返战场不会保留已经结束的战斗进度。失败或中止同样进入冷却。

## 奖励

击败残阳君主获得 **1 件残阳守卫套装部件**、**1 个残阳烬核**，并有 **75%** 几率获得一件随机装备；其他材料见[领主掉落表](world/bosses/sunset-lord.md)。清剿小怪也有各自掉落。事件结束后没有额外的结算宝箱或任务交付奖励。

## 再次挑战

本轮结束后冷却 **4 小时**。以战场显示的剩余时间为准，倒计时结束后可以再次靠近集结。
''')

# Load the exact skill/template files cited by the editorial combat descriptions.
for folder in ['skills/落日森林技能/领主-残阳君主','skills/落日森林技能/领主-破碎魂灵','skills/落日森林技能/区域事件','mobs/生物模板','skills/生物模板技能']:
    for p in (MM/folder).rglob('*.yml'): sources.add(p.relative_to(SERVER).as_posix())
sources.update(['plugins/TopCraftPartyRecruitment/config.yml','plugin-src/TopCraftPartyRecruitment/TopCraftPartyRecruitment.java','plugins/MythicMobs/skills/落日森林技能/落日森林小怪技能/石傀_治疗.yml'])
write('_maintenance/world-assets.json',json.dumps(assets,ensure_ascii=False,indent=2)+'\n')
write('_maintenance/world-sources.json',json.dumps({'date':'2026-11-16','sources':sorted(sources),'active_monsters':active,'references':['https://lastepoch.tunklab.com/zones','https://www.diablowiki.net/Fields_of_Misery'],'notes':['用户确认：主城与森林往返入口尚未添加，计划 NPC 传送。','地图为 WorldGuard 边界与实际坐标示意，不表示地形和道路。','未将高地魔牛、遗忘的凋零骑士等未找到刷新入口的配置列为可挑战敌人。','昔日幻影第 4 波的 <=4 与 >=4 条件重叠；不将配置注释中的每波 6 人写为固定规则。','冷却减免技能没有找到调用入口，因此不发布减免玩法。','技能与掉落依据文件核对，未启动服务器做运行验收。']},ensure_ascii=False,indent=2)+'\n')
routes=['/']
for section in ['combat','guide','equipment','world','quests','dungeons','life','social']:
    routes.extend('/'+p.relative_to(ROOT).with_suffix('').as_posix() for p in sorted((ROOT/section).rglob('*.md')))
write('assets/search-paths.js','window.TopCraftSearchPaths = '+json.dumps(routes,ensure_ascii=False,indent=2)+';\n')
# Include computed level labels in map data after all region pages are built.
write('assets/data/world.json',json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'regions':len(regions),'monsters':len(active),'npc_portraits':len(assets),'world_pages':len(list((ROOT/'world').rglob('*.md')))},ensure_ascii=False))
