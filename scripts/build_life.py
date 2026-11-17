"""Export the player profession handbook. Only writes the Wiki checkout.
Run after build_equipment.py to reuse existing item entries and images.
"""
from pathlib import Path
from collections import defaultdict
import json,re,html,sys,hashlib,shutil
import yaml
ROOT=Path(__file__).resolve().parents[1]
SERVER=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT.parent/'top-craft2'
sources=set(); assets={}; missing=[]
def read(p):
    p=Path(p);sources.add(p.relative_to(SERVER).as_posix());return yaml.safe_load(p.read_text(encoding='utf-8-sig')) or {}
def write(p,s):
    p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8',newline='\n')
def esc(s):return html.escape(str(s),quote=True)
def clean(s):return re.sub(r'[&§][0-9a-fklmnor]|<[^>]+>|[\ue000-\uf8ff]','',str(s),flags=re.I).strip()
def slug(s):return re.sub(r'[^a-z0-9-]+','-',s.lower().replace('_','-')).strip('-')
def fmt(n):return f'{float(n):.4f}'.rstrip('0').rstrip('.')
def link(p,s):return f'<a href="#/{p}">{esc(s)}</a>'
def table(head,rows):return '<div class="life-table"><table><thead><tr>'+''.join('<th>'+h+'</th>' for h in head)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+str(v)+'</td>' for v in r)+'</tr>' for r in rows)+'</tbody></table></div>\n\n'
def page(p,title,lead,body):write('life/'+p+'.md',f'<p class="eyebrow">TOPCRAFT / 生活职业</p>\n\n<nav class="life-breadcrumb" aria-label="当前位置">{link("life/overview","生活职业")}</nav>\n\n# {title}\n\n<p class="lead">{lead}</p>\n\n{body}\n\n<div class="page-end">TopCraft 玩家手册 · 生活职业 · 2026-11-16</div>\n')
def cards(rows):return '<div class="entry-grid">'+''.join(f'<a class="entry-card" href="#/{p}"><strong>{t}</strong><span>{d}</span></a>' for p,t,d in rows)+'</div>\n\n'
prof={'farming':'采集','mining':'挖掘','woodcutting':'伐木','fishing':'垂钓','cooking':'烹饪','alchemy':'炼药','smithing':'锻造','smelting':'冶炼'}
market=read(SERVER/'plugins/TopCraftProfessionMarket/config.yml')
quests=read(SERVER/'plugins/TopCraftLifeQuests/config.yml')
herbs=read(SERVER/'plugins/TopCraftHerbs/config.yml')
blocks=read(SERVER/'plugins/BlockRegen/Blocklist.yml')
items={}
for p in (SERVER/'plugins/MMOItems/item').glob('*.yml'):
    for k,v in read(p).items():
        if isinstance(v,dict) and isinstance(v.get('base'),dict):items[(p.stem.upper(),str(k))]=v['base']
def name(t,i):return clean(items[(t.upper(),i)].get('name',i))
eq={}; icons={}
for p in (ROOT/'equipment').rglob('*.md'):
    for card in re.findall(r'<article\b.*?</article>',p.read_text(encoding='utf-8'),re.S):
        ident=re.search(r'\bid="([^"]+)"',card);img=re.search(r'<img[^>]*class="eq-icon"[^>]*src="([^"]+)"',card)
        if ident:
            eq[ident[1]]=p.relative_to(ROOT).with_suffix('').as_posix()+'?id='+ident[1]
            if img:icons[ident[1]]=img[1]
def itemkey(t,i):return (slug(t)+'-' if slug(t) and t.upper() not in ['GEM_STONE'] else '')+slug(i)
def itemroute(t,i):
    key=itemkey(t,i)
    return eq.get(key) or eq.get(slug(i)) or ''
# Copy additional fish and tackle textures using the same material/model identity as in game.
ia={}; roots={}
for p in (SERVER/'plugins/ItemsAdder/contents').glob('*/resourcepack/assets/*'):
    if p.is_dir():roots[p.name]=p
for p in (SERVER/'plugins/ItemsAdder/contents').rglob('*.yml'):
    cfg=read(p)
    if not isinstance(cfg,dict):continue
    ns=cfg.get('info',{}).get('namespace','')
    for v in cfg.get('items',{}).values():
        if not isinstance(v,dict):continue
        r=v.get('resource',{})
        if r.get('material') and 'model_id' in r:ia[(r['material'].upper(),int(r['model_id']))]=(ns,r)
def assetpath(ref,ns,folder,suffix):
    if ':' in ref:ns,ref=ref.split(':',1)
    return roots.get(ns,Path('__missing__'))/folder/(ref+suffix)
def icon(t,i):
    found=icons.get(itemkey(t,i)) or icons.get(slug(i))
    if found:return found
    b=items[(t.upper(),i)];match=ia.get((b.get('material','').upper(),int(b.get('custom-model-data',-1))))
    if not match:return ''
    ns,r=match;tx=r.get('textures',[]);ref=tx[0] if tx else None
    if not ref and r.get('model_path'):
        path=assetpath(r['model_path'],ns,'models','.json')
        if path.is_file():
            textures=json.loads(path.read_text(encoding='utf-8-sig')).get('textures',{});ref=textures.get('layer0') or textures.get('0') or next(iter(textures.values()),None)
            seen=set()
            while ref and ref.startswith('#') and ref not in seen:seen.add(ref);ref=textures.get(ref[1:])
    if not ref:return ''
    src=assetpath(ref,ns,'textures','.png')
    if not src.is_file():return ''
    digest=hashlib.sha256(src.read_bytes()).hexdigest();dest='assets/server/life/'+digest[:16]+'.png'
    (ROOT/dest).parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,ROOT/dest)
    assets[dest]={'source':src.relative_to(SERVER).as_posix(),'sha256':digest,'kind':'server-original'};icons[itemkey(t,i)]=dest
    return dest
def pic(t,i):
    src=icon(t,i);return f'<img class="life-icon" src="{src}" alt="" loading="lazy">' if src else ''
def item(t,i):
    route=itemroute(t,i);return pic(t,i)+(link(route,name(t,i)) if route else esc(name(t,i)))
def parse(s):
    m=re.search(r'mmoitems?\{([^}]+)\}',s,re.I)
    if not m:raise ValueError('Unsupported item '+s)
    v=dict(re.findall(r'([\w-]+)\s*=\s*([^,;]+)',m[1]));return v['type'].upper(),v['id'],float(v.get('amount',1))

stations={'cooking':'cooking','alchemy':'alchemy','alchemy-extracting':'alchemy','smithing':'smithing','smelting':'smelting','gem-cutting':'smelting','bait-making':'fishing','purification':'fishing'}
recipes=[];bykey={};uses=defaultdict(list)
for station,skill in stations.items():
    cfg=read(SERVER/f'plugins/MMOItems/crafting-stations/{station}.yml')
    for key,r in cfg['recipes'].items():
        t,i,n=parse(r['output']);conditions=' '.join(r.get('conditions',[]));m=re.search(r'profession\{profession=([^,}]+),level=(\d+)',conditions)
        if m and m[1]!=skill:raise ValueError((station,key,m[1]))
        xp=re.search(r'exp give %player% \w+ ([\d.]+)',' '.join(r.get('triggers',[])))
        ings=[parse(x) for x in r.get('ingredients',[])];cost=re.findall(r'(?:money|currency)\{([^}]+)\}',conditions)
        obj={'id':station+'-'+key,'key':station+':'+key,'skill':skill,'station':clean(cfg['name']),'level':int(m[2]) if m else 1,'type':t,'item':i,'name':name(t,i),'amount':n,'seconds':r.get('crafting-time',0),'xp':float(xp[1]) if xp else 0,'ingredients':ings,'conditions':r.get('conditions',[])}
        recipes.append(obj);bykey[obj['key']]=obj
        for a,b,c in ings:uses[(a,b)].append(obj)
def rlink(r):return link('life/recipes?id='+r['id'],r['name'])
def use_links(t,i):
    rs=uses[(t.upper(),i)]
    extra={'PIRATE_COIN':link('life/market?profession=fishing','向芬恩兑换鱼竿'),'LOST_TACKLE_BOX':link('life/tackle','开启获得随机渔具部件'),'FLORAL_UNDERPANTS':'可佩戴于头部。'}
    if i in extra:return extra[i]
    if rs:return '、'.join(rlink(r) for r in rs)
    if t.upper()=='垂钓':return link('life/market?profession=fishing','出售给芬恩')
    return '暂无制作配方。'
def milestones(skill):
    groups=defaultdict(list)
    for r in recipes:
        if r['skill']==skill:groups[r['level']].append(r)
    if not groups:return ''
    return '## 配方与等级解锁\n\n'+table(['职业等级','新配方','查询'],[[f'{lv} 级','、'.join(r['name'] for r in rs[:3])+('等 '+str(len(rs))+' 项' if len(rs)>3 else ''),link(f'life/recipes?profession={skill}&level={lv}','查看已解锁配方')] for lv,rs in sorted(groups.items())])

npcs=read(SERVER/'plugins/Citizens/saves.yml')['npc'];npcs={str(k):v for k,v in npcs.items()}
npc_ids={'farming':12,'mining':16,'woodcutting':14,'fishing':17,'cooking':11,'alchemy':15,'smithing':13,'smelting':18}
def npcintro(skill):
    n=npcs[str(npc_ids[skill])];loc=n['traits']['location'];coord=' / '.join(fmt(round(loc[k],1)) for k in ('x','y','z'))
    return f'<div class="life-npc"><strong>主城 · {n["name"]}</strong><span>X / Y / Z：{coord}</span>{link("world/town","查看主城服务地图")}</div>\n\n'
def tools(skill):
    rows=[]
    shop=market['markets'][skill]['tool-shop']['items']
    stats={'fishing-strength':('垂钓强度','%'),'critical-fishing-chance':('暴击垂钓几率','%'),'critical-fishing-failure-chance':('失败垂钓几率','%'),'chance':('垂钓幸运',''),'custom-fishing-speed-percent':('咬钩速度','%')}
    for sk,zh in [('farming','采集'),('mining','挖掘'),('woodcutting','伐木')]:
        stats.update({f'custom-{sk}-speed-percent':(zh+'速度','%'),f'custom-{sk}-double-drop-chance':('双倍掉落几率','%'),f'custom-{sk}-experience-percent':(zh+'经验','%')})
    stats['custom-farming-extra-harvest-amount']=('额外收获','')
    for ident,b in sorted(((i,b) for (t,i),b in items.items() if t=='工具' and i.startswith(skill.upper()+'_') and not i.startswith('FISHING_ODD_')),key=lambda row:row[1].get('profession-'+skill,0)):
        source=[]
        if ident in shop:
            entry=shop[ident];cur=entry.get('currency');source.append((f'{cur["amount"]} {cur["name"]}' if cur else fmt(entry['price'])+' 金币')+' · '+link('life/market?profession='+skill,'工具商店'))
        source.extend(rlink(r) for r in recipes if r['type']=='工具' and r['item']==ident)
        if not source:continue
        bonuses=[label+' '+('+' if b[k]>0 else '')+fmt(b[k])+unit for k,(label,unit) in stats.items() if k in b and isinstance(b[k],(int,float)) and b[k]!=0]
        rows.append([item('工具',ident),str(b.get('profession-'+skill,1))+' 级',fmt(b.get('max-durability',0)),'<br>'.join(bonuses) or '无额外属性','；'.join(source)])
    return '## 工具与获取\n\n'+table(['工具','使用要求','耐久','工具加成','获取'],rows)
def common_tail(skill):return f'\n\n[查询 {prof[skill]} 升级经验](life/overview.md) · [生活委托](life/commissions.md?profession={skill}) · [出售收获与维修](life/market.md?profession={skill})\n'

curves={}
for sk in prof:
    cfg=read(SERVER/f'plugins/MMOCore/professions/{sk}.yml');p=SERVER/f'plugins/MMOCore/exp-curves/{cfg["exp-curve"]}.txt';sources.add(p.relative_to(SERVER).as_posix());curves[sk]=[int(v) for v in p.read_text(encoding='utf-8-sig').splitlines() if v.strip() and not v.startswith('#')]
page('overview','生活职业与升级','采集原料、加工材料、制作装备与补给。八项职业各自积累经验，最高 100 级。',cards([('life/'+sk,zh,desc) for (sk,zh),desc in zip(prof.items(),['作物、草药与采集锄','矿石、粗矿与挖掘镐','木材、副产物与伐木斧','鱼获、鱼饵与渔具改装','恢复食物与属性料理','恢复药水、药剂与药材提取','武器、防具、饰品与专用工具','矿物加工与宝石切割'])])+'''## 等级与经验查询

在游戏内点击<strong>背包 → 主菜单 → 生活技能</strong>，悬停对应职业图标，查看自己的等级、经验与相关属性。

各职业使用独立的升级经验。选择职业与当前等级，可查询升到下一级所需经验，以及到达目标等级的总需求。

<div class="life-calculator" data-life-xp><label>职业<select data-xp-prof>'''+''.join(f'<option value="{sk}">{zh}</option>' for sk,zh in prof.items())+'''</select></label><label>当前等级<input data-xp-level type="number" min="1" max="100" value="1"></label><label>目标等级<input data-xp-target type="number" min="1" max="100" value="25"></label><div class="life-result" role="status" data-xp-result></div></div>

总需求按当前等级经验为 0 计算；已经积累的经验可以从结果中扣除。达到职业等级后，便可使用满足要求的工具、制作相应配方。

## 经验从哪里来

'''+table(['职业','主要经验来源'],[['采集','成功收获作物与野生草药'],['挖掘','成功采出资源矿物'],['伐木','成功砍伐资源原木'],['垂钓','成功收获鱼获、制作鱼饵、提纯鱼获与渔具改装'],['烹饪、炼药、锻造、冶炼','制作对应职业的物品'],['全部职业',link('life/commissions','领取每日与每周委托奖励')]])+'''## 从原料到成品

<div class="life-chain"><span>矿石 → 粗矿</span><b>→</b><span>冶炼 → 锭与宝石</span><b>→</b><span>锻造 → 装备与工具</span></div>
<div class="life-chain"><span>作物、草药、鱼获</span><b>→</b><span>提取、提纯与食材采购</span><b>→</b><span>烹饪与炼药 → 战斗补给</span></div>

'''+cards([('life/recipes','配方检索','按职业、制作等级和成品名称查用料、产量、耗时与经验'),('life/market','商人、收购与维修','购买工具与食材，按职业等级查询资源卖价'),('life/commissions','生活委托','每日与每周目标、可计数活动与经验奖励')]))

resource_names={'COAL_ORE':'煤矿石','COPPER_ORE':'铜矿石','IRON_ORE':'铁矿石','GOLD_ORE':'金矿石','REDSTONE_ORE':'红石矿石','LAPIS_ORE':'青金石矿石','DIAMOND_ORE':'钻石矿石','EMERALD_ORE':'绿宝石矿石','NETHER_QUARTZ_ORE':'下界石英矿石','NETHER_GOLD_ORE':'下界金矿石','AMETHYST_CLUSTER':'紫水晶簇','ANCIENT_DEBRIS':'远古残骸','OBSIDIAN':'黑曜石'}
def resource_table(sk):
    rows=[];typ=prof[sk]
    for material,v in market[sk+'-harvest'].items():
        if material.startswith('DEEPSLATE_') or material=='KELP_PLANT':continue
        p=blocks[v['preset']];allowed=set(x.strip() for x in p['tool-required'].split(','));candidates=[]
        for (t,i),b in items.items():
            if t=='工具' and i.startswith(sk.upper()+'_') and b['material'] in allowed and material in b.get('can-break',[]):candidates.append((b.get('profession-'+sk,1),name(t,i)))
        gate=min(candidates)[0] if candidates else None
        if gate is None:raise ValueError('No valid tool '+material)
        res=resource_names.get(material,name(typ,v['item']))
        if 'DEEPSLATE_'+material in market[sk+'-harvest']:res+='／深层矿石'
        rows.append([res,item(typ,v['item'])+' ×'+str(v['amount']),fmt(v['experience']),f'{gate} 级工具起',str(p['regen-delay'])+' 秒'])
    return table(['采集目标','基础收获','经验','工具门槛','恢复时间'],rows)
page('farming','采集','使用采集锄收获成熟作物，或在野外寻找草药。收获可用于烹饪、炼药和鱼饵制作。',npcintro('farming')+'''## 开始采集

在欧文处购买采集锄，手持工具左键采集作物。小麦、胡萝卜、马铃薯、甜菜、可可和下界疣需要成熟后才能收获。采集锄有独立的职业等级要求与耐久。

## 作物与资源恢复

恢复时间从成功采集后开始计算。甘蔗、竹子、仙人掌和海带可以连同上方相连部分一并收获，各段分别产出资源与经验。

'''+resource_table('farming')+'''## 收获与经验加成

<p><img class="life-stat" src="assets/server/stats/extra_harvest.png" alt="">额外收获直接增加基础产量；双倍掉落先对基础产量判定，再加固定额外收获。基础产量 1、额外收获 +1 时，普通收获为 2，触发双倍时为 3。</p>

采集经验加成提高每次活动获得的经验。作物采集还可能获得蚯蚓，几率 **12%**，可加工成鱼饵。

'''+cards([('life/herbs','野生草药图鉴','草药种类、出现环境、经验与配方用途')])+tools('farming')+common_tail('farming'))
page('mining','挖掘','使用挖掘镐采集矿物，获得粗矿、晶体与冶炼原料。',npcintro('mining')+'''## 开始挖掘

向多里安购买挖掘镐，手持工具开采矿石。工具等级与可采方块共同决定能否开采；普通石头不等同于有产出和经验的矿物资源点。

## 矿物与资源恢复

矿石采出后暂时变为不可继续开采的方块，恢复后可以再次采集。普通与对应深层矿石的收获相同。

'''+resource_table('mining')+'''## 工具属性

<p><img class="life-stat" src="assets/server/stats/mining_speed.png" alt="">挖掘速度提高采掘效率；双倍掉落有几率使本次矿物产量翻倍，经验加成单独提高获得的挖掘经验。</p>

粗铜、粗铁、粗金需要[冶炼](life/smelting.md)后加工成锭；宝石原料也可通过宝石切割加工。

'''+tools('mining')+common_tail('mining'))
woodrows=[]
for key,b in blocks.items():
    mat=b.get('target-material','')
    if not key.startswith('tc_forest_') or mat.startswith('STRIPPED_') or not (mat.endswith('_LOG') or mat.endswith('_STEM')):continue
    drops=[]
    for command in b.get('console-commands',[]):
        m=re.match(r'([\d.]+);mi give (\S+) (\S+) %player% (\d+)',command)
        if m:drops.append(item(m[2],m[3])+' ×'+m[4]+'（'+m[1]+'%）')
    woodrows.append([item('伐木',mat)+' ×1','2',str(b['regen-delay'])+' 秒','、'.join(drops)])
page('woodcutting','伐木','使用伐木斧收获木材，并取得树液、树脂与制作鱼饵的木蠹虫。',npcintro('woodcutting')+'''## 开始伐木

向罗温购买伐木斧，手持工具砍伐原木。去皮原木也按对应木材产出；每次成功采集获得基础 **2 点伐木经验**。

## 木材与副产物

'''+table(['基础木材收获','经验','恢复时间','额外掉落'],woodrows)+'''伐木另有 **10%** 几率获得木蠹虫，可用于制作鱼饵。副产物分别判定；木材双倍掉落不会让副产物再判定一次。

## 工具属性

<p><img class="life-stat" src="assets/server/stats/woodcutting_speed.png" alt="">伐木速度提高原木采集效率；双倍掉落使本次木材由 1 份变为 2 份。经验加成提高基础 2 点经验，与双倍掉落分别生效。</p>

'''+tools('woodcutting')+common_tail('woodcutting'))

ground={'GRASS_BLOCK':'草方块','DIRT':'泥土','COARSE_DIRT':'砂土','PODZOL':'灰化土','MOSS_BLOCK':'苔藓块','ROOTED_DIRT':'缠根泥土','MYCELIUM':'菌丝','SAND':'沙子','SOUL_SOIL':'灵魂土','MUD':'泥巴','SNOW_BLOCK':'雪块'}
herbcards=[]
for key,h in herbs['herbs'].items():
    if not h.get('enabled'):continue
    t,i=h['mmoitems-type'],h['mmoitems-id'];rare=h.get('rare',False)
    herbcards.append(f'<article class="life-entry" id="herb-{slug(i)}"><h3>{item(t,i)}</h3><p>{"稀有" if rare else "普通"}草药 · 基础每株 {h["amount"]} 份 · {herbs["harvest"]["rare-experience" if rare else "normal-experience"]} 采集经验</p><p>地面：'+ '、'.join(ground.get(g,g) for g in h['ground'])+f'。自然停留 {h["lifetime-min-seconds"]//60}–{h["lifetime-max-seconds"]//60} 分钟。</p><p>用途：{use_links(t,i)}</p></article>')
page('herbs','野生草药','留意野外的金色粒子，使用采集锄收获药草，交给炼药工艺加工。','''## 寻找与采集

草药会在主城以外的适宜地面出现，没有固定采集坐标。探索时留意金色粒子，手持采集锄，在 **5 格**内左键破坏草药。

普通草药提供 **10 经验**，稀有草药提供 **30 经验**。草药采集另有 **20%** 几率获得红虫。草药在野外停留一段时间后会消失；离开后再次返回，也可能出现在不同位置。采集锄的双倍掉落、额外收获和经验加成同样作用于草药，背包需有足够空间才能收获。

## 草药种类与用途

<div class="life-grid">'''+''.join(herbcards)+'</div>\n\n[药材提取与炼药配方](life/recipes.md?profession=alchemy) · [采集工具](life/farming.md)')

craftintro={
'cooking':('烹饪','将作物、鱼获与食材制成恢复食物和属性料理。','伊芙琳','烹饪界面可进入食材商店购买鸡蛋、牛奶、油、糖等原料。食物共享 5 秒冷却；恢复量、增益与叠加规则见[食物与药水](equipment/consumables.md)。'),
'alchemy':('炼药','提取草药精华，制作生命药水、法力药水和各类药剂。','瑟琳','炼药界面可进入药材提取。恢复药水的制作等级为 1 / 25 / 60，分别恢复 15% / 30% / 45% 生命或法力，生命与法力恢复药水共享 15 秒冷却。[药剂效果与共存规则](equipment/consumables.md)'),
'smithing':('锻造','将金属、木材与野外材料制作成武器、防具、饰品和专用工具。','加雷特','锻造界面可切换武器、防具、饰品、副手与工具分类。制作等级决定能否使用配方，成品的装备等级与穿戴要求见[装备图鉴](equipment/catalog.md)。制作专用鱼竿会得到满耐久、未装饵料的新鱼竿。'),
'smelting':('冶炼','把粗矿加工成金属锭，或切割宝石，供锻造与镶嵌使用。','奥尔登','冶炼界面可进入宝石切割。粗矿、煤炭与晶体等原料来自[挖掘](life/mining.md)，成品继续用于锻造、配方和[宝石镶嵌](equipment/gems.md)。')}
for sk,(title,lead,npc,extra) in craftintro.items():
    page(sk,title,lead,npcintro(sk)+f'''## 如何制作

与{npc}交互打开制作界面，选择配方查看材料与等级要求，确认后开始制作。需要时间的配方进入队列，完成后点击领取成品；取消尚未完成的制作会返还材料。各工作台最多有 **5 个队列位置**，即时配方直接完成。

{extra}

'''+milestones(sk)+cards([('life/recipes?profession='+sk,'完整'+title+'配方','按名称与等级筛选，查看每份产量、材料、耗时与经验'),('equipment/materials','材料与用途','查询原料来源和其他制作用途')])+common_tail(sk))

fishcfg=read(SERVER/'plugins/MMOCore/professions/fishing.yml');fish=[]
for line in fishcfg['on-fish']['default']['items']:
    t,i,n=parse(line);tu=int(re.search(r'tugs=(\d+)',line)[1]);xp=int(re.search(r'experience=(\d+)',line)[1]);weight=float(line.split()[-1]);fish.append({'type':t,'item':i,'name':name(t,i),'tugs':tu,'xp':xp,'weight':weight})
total=sum(f['weight'] for f in fish)
fishrows=[]
for f in fish:
    sell=next((v['base-price'] for v in market['markets']['fishing']['items'].values() if v.get('mmoitems',{}).get('id')==f['item']),None)
    fishrows.append(f'<tr class="life-fish" id="fish-{slug(f["item"])}" data-life-row data-name="{esc(f["name"])}" data-weight="{f["weight"]}"><td>{item(f["type"],f["item"])}</td><td>{f["tugs"]}</td><td>{f["xp"]}</td><td data-fish-prob>{f["weight"]/total*100:.3f}%</td><td>{fmt(sell)+" 金币" if sell else "不收购"}</td><td>{use_links(f["type"],f["item"])}</td></tr>')
page('fish','鱼获图鉴','查看鱼获、珍品与渔具箱的基础拉竿次数、垂钓经验、出现几率和加工用途。','''<div class="life-controls" data-life-filter><label>查找鱼获<input type="search" data-life-search placeholder="输入鱼获名称"></label><label>垂钓幸运<input type="number" min="0" max="1000" value="0" data-fish-luck></label><p data-life-count role="status"></p></div>

几率按当前通用鱼池和输入的垂钓幸运计算，表示本轮抽中该鱼获的几率；最终获得物品还需要完成收竿。基础拉竿次数会被垂钓强度降低。收购栏为未加职业等级加价的基础价格，可在[收购查询](life/market.md?profession=fishing)查看你的实际卖价。

<div class="life-table"><table><thead><tr><th>鱼获</th><th>基础拉竿</th><th>经验</th><th>出现几率</th><th>基础收购价</th><th>用途</th></tr></thead><tbody>'''+''.join(fishrows)+'</tbody></table></div>\n\n<p class="life-empty" hidden>没有符合条件的鱼获，请调整名称。</p>\n\n这些鱼获共用鱼池，没有按淡水、海水分开；名称中的海域、河流字样不限制垂钓地点。\n\n[垂钓操作与属性](life/fishing.md) · [鱼饵与渔具改装](life/tackle.md)')
page('fishing','垂钓','抛竿等待咬钩，连续拉竿完成收获，再将鱼获出售、烹饪或提纯。',npcintro('fishing')+'''## 抛竿与收竿

1. 在芬恩处购买鱼竿，手持鱼竿朝水面右键抛竿。
2. 咬钩后右键收竿，进入拉竿过程。
3. 连续右键直到完成所需拉竿次数；两次有效拉竿之间超过 **1 秒**会失去本轮鱼获。

鱼获抽中后，仍可能在普通收竿结算时失败并把玩家拖向水面；暴击垂钓会立即完成拉竿，并跳过这次失败判定。

## 垂钓属性

'''+table(['属性','作用'],[['<img class="life-stat" src="assets/server/stats/fishing_strength.png" alt="">垂钓强度','减少需要的拉竿次数，普通鱼竿最高按 40% 计算。基础 8 次、强度 25% 时需要 6 次；计算结果向下取整。'],['<img class="life-stat" src="assets/server/stats/critical_fishing_chance.png" alt="">暴击垂钓几率','第一次拉竿时判定，成功后立即完成。基础 5%，普通鱼竿最高 70%。'],['失败垂钓几率','普通收竿结束时判定，基础 30%，最低 1%。暴击垂钓不会触发这次失败。'],['<img class="life-stat" src="assets/server/stats/fishing_luck.png" alt="">垂钓幸运','改变鱼池中各鱼获的相对几率；增加幸运可提高低权重鱼获的机会。可在鱼获图鉴输入幸运值查询。'],['<img class="life-stat" src="assets/server/stats/fishing_bite_speed.png" alt="">咬钩速度','缩短咬钩前等待时间。速度 +50% 时，等待区间缩短为原来的 1 ÷ 1.5；不减少拉竿次数。']])+cards([('life/fish','鱼获图鉴','鱼、珍品、海盗币与渔具箱的出现几率和用途'),('life/tackle','鱼饵与渔具改装','装饵、部件、旧鱼竿与改造规则')])+tools('fishing')+milestones('fishing')+common_tail('fishing'))
tackle=read(SERVER/'plugins/TopCraftDivineDescent/fishing-tackle.yml')['rewards']
parts=[('STRONG_FISHING_LINE','钓线',2,'垂钓强度 +10%'),('STEEL_FISHING_HOOK','鱼钩',1,'失败垂钓几率 −5%'),('SENSITIVE_FLOAT','浮漂',1,'暴击垂钓几率 +5%'),('SEA_BLESSED_SINKER','钓坠',1,'垂钓幸运 +10')]
baitrows=[]
for r in recipes:
    if r['key'].startswith('bait-making:'):
        b=items[(r['type'],r['item'])];baitrows.append([item(r['type'],r['item']),f'{r["level"]} 级',fmt(b.get('custom-fishing-speed-percent',0))+'%',rlink(r)])
oddrows=[]
for ident,stat,lo,hi,dl,dh in [('FRAYED','垂钓强度',91.7,99.3,5,13),('BLURRED','暴击垂钓几率',78.6,92.4,7,16),('BENT','失败垂钓几率',-28.9,-27.4,29,50),('SCRAWLED','垂钓幸运',73.6,116.8,6,14),('SOUR','咬钩速度',164.3,237.8,8,23)]:
    oddrows.append([item('工具','FISHING_ODD_'+ident),stat+' '+fmt(lo)+'–'+fmt(hi)+('' if ident=='SCRAWLED' else '%'),f'{dl}–{dh}'])
page('tackle','鱼饵与渔具改装','用鱼饵缩短等待，用部件调整拉竿、暴击与幸运。',npcintro('fishing')+'''## 鱼饵原料与装饵

成功采集作物有 **12%** 几率获得蚯蚓，采集草药有 **20%** 几率获得红虫，伐木有 **10%** 几率获得木蠹虫。原料加工成鱼饵后，才能安装到鱼竿上。

在芬恩的界面进入鱼饵制作。将成品鱼饵拖放到具有空闲「饵料」槽的鱼竿上，消耗鱼饵并安装其加成。安装后持续生效，不按每次抛竿消耗一份；没有空闲饵料槽时无法再安装。

'''+table(['鱼饵','制作等级','咬钩速度增加','配方'],baitrows)+'''## 渔具部件

垂钓可能获得遗失的渔具箱，使用后得到 **1 个部件**。四类部件的开箱几率如下。

'''+table(['部件','部位','每次改造用量','改造效果','开箱几率'],[[item('渔具部件',i),p,n,e,f'{tackle[i]/sum(tackle.values())*100:g}%'] for i,p,n,e in parts])+'''## 如何改造

从芬恩的界面进入渔具改装，将鱼竿放在中央，并在对应位置放入足量部件，确认完成改造。每改造一个部位花费 **100 金币**，获得 **20 垂钓经验**；同时完成四个部位需 400 金币，获得 80 经验。

每个部位只能改造一次，已改造部位不能重复安装或替换。未改造的其他部位可以以后继续添加；鱼竿原有耐久与已装饵料会保留。

## 奇怪的旧鱼竿

成功收获时另有 **0.3%** 几率捞起一把旧鱼竿，五种旧鱼竿等概率。它们带有随机属性与少量剩余耐久，无法维修或进行部件改造；每次成功收获消耗 1 点耐久，失败或中止不消耗。

'''+table(['旧鱼竿','随机属性','初始剩余耐久'],oddrows)+'''强度型旧鱼竿按自身强度计算拉竿次数，最低仍需 1 次；暴击型旧鱼竿按基础 5% 加自身暴击属性计算，最高 100%。这两类旧鱼竿不使用普通鱼竿的 40% 强度与 70% 暴击上限。
''')

recipe_cards=[]
for r in sorted(recipes,key=lambda r:(list(prof).index(r['skill']),r['level'],r['name'])):
    ing=''.join(f'<li>{item(t,i)} <b>×{fmt(n)}</b></li>' for t,i,n in r['ingredients'])
    conditions=[]
    for cond in r['conditions']:
        if cond.startswith('profession{'):continue
        m=re.match(r'(?:money|currency)\{(?:amount|value)=([\d.]+)',cond)
        if m:conditions.append(fmt(m[1])+' 金币')
        else:raise ValueError('Unmapped recipe condition '+cond)
    recipe_cards.append(f'<article class="life-recipe" id="{r["id"]}" data-life-row data-profession="{r["skill"]}" data-level="{r["level"]}" data-name="{esc(r["name"])}"><header>{pic(r["type"],r["item"])}<div><h3>{esc(r["name"])}</h3><p>{prof[r["skill"]]} {r["level"]} 级 · {r["station"]}</p></div></header><div class="life-recipe-facts"><span>产量 <b>×{fmt(r["amount"])}</b></span><span>耗时 <b>{fmt(r["seconds"])+" 秒" if r["seconds"] else "即时"}</b></span><span>经验 <b>+{fmt(r["xp"])}</b></span></div><ul class="life-ingredients">{ing}</ul>'+('<p>额外费用：'+'、'.join(conditions)+'</p>' if conditions else '')+(f'<p>{link(itemroute(r["type"],r["item"]),"查看成品效果与用途")}</p>' if itemroute(r['type'],r['item']) else '')+'</article>')
def controls(kind,levels=True):
    return '<div class="life-controls" data-life-filter><label>查找'+kind+'<input type="search" data-life-search placeholder="输入'+kind+'名称"></label><label>职业<select data-life-prof><option value="">全部职业</option>'+''.join(f'<option value="{sk}">{zh}</option>' for sk,zh in prof.items())+'</select></label>'+('<label>当前等级<input type="number" min="1" max="100" value="100" data-life-level></label><label class="life-check"><input type="checkbox" data-life-eligible>只显示当前可用</label>' if levels else '')+'<p data-life-count role="status"></p></div>\n\n'
page('recipes','生活配方检索','按职业、名称与等级查找完整用料。每张配方卡列出一次制作的产量、耗时和职业经验。',controls('成品')+'<div class="life-grid">'+''.join(recipe_cards)+'</div>\n\n<p class="life-empty" hidden>没有符合条件的配方，请调整名称、职业或等级。</p>')

taskcards=[]
for ident,t in quests['tasks'].items():
    reqs=[]
    for req in t['requirements']:
        choices=[]
        for key in req['keys']:
            if req['kind']=='craft' and key not in bykey:raise ValueError('Missing commission recipe '+key)
            if req['kind']=='craft' and key in bykey:
                r=bykey[key];count_level=quests['resource-levels'][key]
                choices.append(f'<span class="life-choice" data-choice-level="{count_level}" data-craft-level="{r["level"]}">{rlink(r)}（制作需要 {prof[r["skill"]]} {r["level"]} 级）<small data-choice-status></small></span>')
            elif req['kind']=='fish':choices.append(item('垂钓',key))
        reqs.append('<li>'+esc(req['label'])+' <b>×'+str(req['amount'])+'</b>'+('<details><summary>可计数的'+('配方' if req['kind']=='craft' else '鱼获')+'</summary><p>'+''.join(choice if 'data-choice-level' in choice else '<span class="life-choice">'+choice+'</span>' for choice in choices)+'</p></details>' if choices else '')+'</li>')
    taskcards.append(f'<article class="life-quest" id="{ident}" data-life-row data-name="{esc(t["title"])}" data-profession="{t["skill"]}" data-cycle="{t["cycle"]}" data-level="{t["min_level"]}" data-max-level="{t["max_level"]}"><h3>{t["title"]}</h3><p>{prof[t["skill"]]} · {"每日" if t["cycle"]=="daily" else "每周"} · {t["min_level"]}–{t["max_level"]} 级</p><ul>{"".join(reqs)}</ul><p class="life-reward" data-reward>经验奖励按职业等级查询</p></article>')
page('commissions','每日与每周生活委托','接取生活活动目标，完成后领取对应职业经验。','''## 接取、领取与刷新

点击<strong>背包 → 主菜单 → 生活委托</strong>进入，再通过界面中的每日／每周按钮切换委托。每日名额 **2 项**，每周 **1 项**，八项职业共用名额。

每日在 **06:00** 刷新，每周在**周一 06:00** 刷新，均按 UTC+8 计算。各职业从符合等级的任务中抽取本期目标，图鉴展示的是可能出现的任务。完成后返回界面左键领取；跨周期后旧任务与未领取奖励不保留。

未产生进度时可取消接取并换职业目标；已有进度后不能切换。奖励按本期任务生成时的职业等级确定，本期内升级不会改变已经生成的奖励。

## 哪些操作计数

'''+table(['活动','计数规则'],[['采集、挖掘、伐木','接取后成功采集指定资源才计数；额外产量不额外增加活动次数。'],['垂钓','成功获得指定鱼获才计数；普通失误、提前收竿或超时不计数。'],['制作','成功加入指定制作队列或完成即时制作时计数；按制作操作计数，不按成品件数累计。领取队列成品不会再计一次。'],['持有或购买材料','不计入活动进度；这类委托要求完成活动，不是交付库存。']])+'''## 目标与奖励查询

输入本期任务生成时的职业等级，查询奖励与可计数的配方。部分委托会在配方解锁前出现，接取后仍需达到相应制作等级才能完成；展开卡片可查看具体要求。

'''+controls('委托').replace('value="100" data-life-level','value="1" data-life-level').replace('<p data-life-count','<label>周期<select data-life-cycle><option value="">每日与每周</option><option value="daily">每日</option><option value="weekly">每周</option></select></label><p data-life-count')+'<div class="life-grid">'+''.join(taskcards)+'</div>\n\n<p class="life-empty" hidden>没有符合条件的委托，请调整筛选。</p>')

sale_rows=[];buy_rows=[]
for sk,m in market['markets'].items():
    for ident,v in m['items'].items():
        t,i=v['mmoitems']['type'],v['mmoitems']['id']
        sale_rows.append(f'<tr data-life-row data-name="{esc(name(t,i))}" data-profession="{sk}"><td>{item(t,i)}</td><td>{prof[sk]}</td><td>{fmt(v["base-price"])}</td><td data-sale-base="{v["base-price"]}" data-sale-bonus="{m["bonus-per-level"]}">{float(v["base-price"])*1.01:.2f}</td></tr>')
    for ident,v in m['tool-shop']['items'].items():
        cur=v.get('currency');price=f'{cur["amount"]} {cur["name"]}' if cur else fmt(v['price'])+' 金币'
        buy_rows.append([item('工具',ident),prof[sk],str(v['required-level'])+' 级',price])
page('market','商人、收购与维修','购买工具和食材，按生活职业等级查询收购价格，修复装备与工具的耐久。','''## 出售资源

欧文收购采集资源，多里安收购矿物，罗温收购木材，芬恩收购鱼获。[主城 NPC 坐标与地图](world/town.md)

收购只接受对应资源物品。单件卖价为 **基础价格 ×（1 + 职业等级 × 1%）**，等级最多计算至 100。单件价格先四舍五入保留两位小数，再乘出售数量。例如基础价 1 金币的物品，50 级卖价为 1.50 金币，100 级为 2.00 金币。

「全部出售」会出售背包中符合当前收购清单的物品，包括可用于任务与制作的材料。

'''+controls('资源',False).replace('<p data-life-count','<label>收购职业等级<input type="number" min="1" max="100" value="1" data-sale-level></label><p data-life-count')+'<div class="life-table"><table><thead><tr><th>资源</th><th>收购职业</th><th>基础价格</th><th>当前卖价／金币</th></tr></thead><tbody>'+''.join(sale_rows)+'</tbody></table></div>\n\n## 商店工具\n\n'+table(['工具','职业','使用等级','购买费用'],buy_rows)+'## 食材与瓶子\n\n烹饪界面的食材商店提供以下原料。\n\n'+table(['商品','每份价格'],[[item(v['type'],i),fmt(v['price'])+' 金币'] for i,v in market['ingredient-shop']['items'].items()])+'''## 维修

手持一件需要维修的装备或工具，输入 `/修复` 打开修理界面，确认后恢复至最大耐久。费用为 **损失耐久 × <span data-number-raw>0.05</span> 金币**，例如恢复 200 点耐久花费 10 金币。

没有可修复耐久的物品不能维修；奇怪的旧鱼竿也不能维修。耐久已满时不扣费。工具耐久耗尽可能损坏消失，需在耗尽前修理。
''')
page('gathering','采集与资源','按资源类型进入对应职业，查询工具、收获和恢复时间。',cards([('life/farming','采集','作物、采集锄与额外收获'),('life/herbs','野生草药','草药环境与炼药用途'),('life/mining','挖掘','矿物、粗矿与挖掘镐'),('life/woodcutting','伐木','木材、树液与伐木斧')]))
page('crafting','生活制作','按制作职业查找配方、材料与加工用途。',cards([('life/cooking','烹饪','食物与料理'),('life/alchemy','炼药','药材提取、恢复药水与药剂'),('life/smithing','锻造','装备与专用工具'),('life/smelting','冶炼','金属与宝石加工'),('life/recipes','全部配方','材料、产量、耗时与经验'),('equipment/consumables','补给效果','恢复数值、持续时间与共存规则')]))
data={'professions':prof,'curves':curves,'rewards':quests['reward-levels'],'fish':fish,'recipes':[{k:v for k,v in r.items() if k not in ['conditions']} for r in recipes]}
write('assets/data/life.json',json.dumps(data,ensure_ascii=False,indent=2)+'\n')
for p in (SERVER/'plugin-src/TopCraftProfessionMarket').glob('*.java'):sources.add(p.relative_to(SERVER).as_posix())
sources.update(['plugin-src/TopCraftDivineDescent/FishingBaitHandler.java','plugin-src/TopCraftDivineDescent/FishingTackleHandler.java','plugin-src/TopCraftLifeQuests/CommissionRules.java','plugin-src/TopCraftLifeQuests/TopCraftLifeQuests.java','plugin-src/TopCraftLifeQuests/WorkListeners.java','plugin-src/TopCraftHerbs/TopCraftHerbs.java','plugins/MMOCore/stats.yml','plugins/MMOCore/config.yml','plugins/BlockRegen/Settings.yml','plugins/MMOCore-1.13.1-20260531.191529-59.jar'])
write('_maintenance/life-assets.json',json.dumps(assets,ensure_ascii=False,indent=2)+'\n')
write('_maintenance/life-sources.json',json.dumps({'date':'2026-11-16','sources':sorted(sources),'counts':{'recipes':len(recipes),'fish_pool':len(fish),'commissions':len(taskcards),'herbs':len(herbcards)},'notes':['委托奖励读取 reward-levels，不使用 task.reward 的旧数值。','鱼获概率使用本地 RandomWeightedRoll 的实际权重公式；普通鱼竿与旧鱼竿的上限分别说明。','未将样例制作站视为已开放入口。','植物刷新预算不等同于固定刷新倒计时。','未启动游戏服验证。']},ensure_ascii=False,indent=2)+'\n')
routes=['/']
for section in ['combat','guide','equipment','world','quests','dungeons','life','social']:routes.extend('/'+p.relative_to(ROOT).with_suffix('').as_posix() for p in sorted((ROOT/section).rglob('*.md')))
write('assets/search-paths.js','window.TopCraftSearchPaths = '+json.dumps(routes,ensure_ascii=False,indent=2)+';\n')
print(json.dumps({'pages':len(list((ROOT/'life').glob('*.md'))),'recipes':len(recipes),'fish':len(fish),'commissions':len(taskcards),'copied_assets':len(assets)},ensure_ascii=False))
