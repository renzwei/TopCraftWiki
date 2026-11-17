"""Build the player equipment reference from the installed server configuration.

Usage: python -X utf8 scripts/build_equipment.py C:/Users/10740/Documents/top-craft2
Only the wiki is written. Sample templates are never used as catalog entries.
"""
from pathlib import Path
from collections import defaultdict
import sys, json, re, html, hashlib, shutil
import yaml

ROOT = Path(__file__).resolve().parents[1]
SERVER = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / 'top-craft2'
MI = SERVER / 'plugins/MMOItems'
sources = set()
def read(path):
    path = Path(path)
    sources.add(path.relative_to(SERVER).as_posix())
    return yaml.safe_load(path.read_text(encoding='utf-8-sig')) or {}
def write(path, value):
    dest = ROOT / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(value, encoding='utf-8', newline='\n')
def clean(text):
    return re.sub(r'\s+', ' ', re.sub(r'[\ue000-\uf8ff]|[&§][0-9a-fklmnor]|<[^>]+>', '', str(text), flags=re.I)).strip()
def esc(s): return html.escape(str(s), quote=True)
def fmt(n): return f'{float(n):.4f}'.rstrip('0').rstrip('.')
def slug(s): return re.sub(r'[^a-z0-9-]+', '-', s.lower().replace('_', '-')).strip('-')
def link(route, label): return f'<a href="#/{route}">{esc(label)}</a>'
def page(path, title, lead, body):
    crumb='' if path=='overview' else link('equipment/overview','装备总览')
    if path.startswith('types/'): crumb+=' / '+link('equipment/catalog','装备图鉴')
    if path.startswith('sets/'): crumb+=' / '+link('equipment/sets','套装图鉴')
    if crumb: crumb='<nav class="eq-breadcrumb" aria-label="当前位置">'+crumb+'</nav>\n\n'
    write('equipment/' + path + '.md', f'<p class="eyebrow">TOPCRAFT / 装备与道具</p>\n\n{crumb}# {title}\n\n<p class="lead">{lead}</p>\n\n{body}\n\n<div class="page-end">TopCraft 玩家手册 · 装备资料 · 2026-11-15</div>\n')

types = dict(zip(['剑','斧','锤','匕首','矛','权杖','魔杖','法书','盾牌','头盔','胸甲','护腿','靴子','项链','戒指','腰带','护符'], ['sword','axe','hammer','dagger','spear','scepter','wand','tome','shield','helmet','chestplate','leggings','boots','necklace','ring','belt','charm']))
items = {}
for path in sorted((MI/'item').glob('*.yml')):
    for key, obj in read(path).items():
        if isinstance(obj, dict) and isinstance(obj.get('base'), dict):
            items[(path.stem.upper(), str(key))] = obj
def item(t, i): return items[(t.upper(), i)]
def name(t, i): return clean(item(t, i)['base'].get('name', i))
mods = {}
for path in sorted((MI/'modifiers').glob('*.yml')): mods.update(read(path))
base_config = read(MI/'weapon-base-stats.yml')
base = base_config['weapons']
drops = read(MI/'equipment-drops.yml')
market = read(SERVER/'plugins/TopCraftProfessionMarket/config.yml')
lang = read(MI/'language/stats.yml')
custom = read(MI/'custom-stats.yml')
labels = {}
units = {}
for k, v in lang.items():
    if not isinstance(v, str): continue
    label = re.sub(r'\{[^}]+\}', '', clean(v)).strip(' %:：■+-')
    label = re.sub(r'^[^\u4e00-\u9fffA-Za-z]+', '', label)
    labels[k] = label
    units[k] = '%' if '{value}%' in v else ''
for k, v in custom.items():
    if isinstance(v, dict) and v.get('name'): labels.setdefault(k.lower().replace('_', '-'),clean(v['name']))
labels.update({'max-durability':'最大耐久','required-level':'使用等级','max-health':'生命上限','max-mana':'法力上限','critical-strike-chance':'暴击几率','critical-strike-power':'暴击伤害','health-regeneration':'生命恢复','mana-regeneration':'法力恢复','cooldown-reduction':'技能冷却缩减','custom-attackspeedbouns':'攻击速度'})
labels['custom-mana-cost-reduction-percent']='法力消耗降低'
for monster,zh in [('normal','普通怪物'),('elite','精英'),('lord','领主'),('boss','首领')]:
    labels['custom-'+monster+'-monster-damage-reduction-percent']=zh+'伤害减免'
for k in labels:
    if k.endswith('-percent') or k in ['critical-strike-chance','critical-strike-power','cooldown-reduction','custom-attackspeedbouns','spell-vampirism','additional-experience']: units[k] = '%'
def label(k):
    if k not in labels: raise ValueError('Missing player label: '+k)
    return labels[k]
stat_icons={}
for path in (SERVER/'plugins/ItemsAdder/contents/topcraft/configs/font_icons').glob('*.yml'):
    for obj in read(path).get('font_images',{}).values():
        texture=obj.get('path',''); symbol=obj.get('symbol')
        asset='assets/server/'+texture+('' if texture.endswith('.png') else '.png')
        if symbol and (ROOT/asset).is_file():
            for key,text in lang.items():
                if isinstance(text,str) and symbol in text: stat_icons[key]=asset
def statroute(k):
    if k in ['required-level','max-durability']: return ''
    if 'summon' in k: return 'combat/summons'
    if 'shield' in k: return 'combat/shield'
    if 'cooldown' in k or 'mana-cost' in k or 'attackspeed' in k: return 'combat/attributes'
    if any(x in k for x in ['resistance','armor','reduction','dodge','lifesteal','healing','regeneration']): route='combat/defense'
    elif any(x in k for x in ['damage','critical','attackspeed']): route='combat/damage'
    else: route='combat/attributes'
    return route
def statlink(k):
    route=statroute(k)
    image=f'<img class="eq-stat-icon" src="{stat_icons[k]}" alt="">' if k in stat_icons else ''
    return image+(link(route,label(k)) if route else esc(label(k)))
def statvalue(k, v, level=0):
    if isinstance(v, dict):
        center = v.get('base',0)+v.get('scale',0)*level
        spread = v.get('max-spread',0)
        val = f'{fmt(center*(1-spread))}–{fmt(center*(1+spread))}' if spread else fmt(center)
    else: val=fmt(v)
    return val+units.get(k,'')

# Match original assets by material AND model id, then resolve model texture references.
ia = {}; assets = {}; missing_icons = []
for path in sorted((SERVER/'plugins/ItemsAdder/contents').rglob('*.yml')):
    cfg=read(path)
    if not isinstance(cfg, dict): continue
    ns=cfg.get('info',{}).get('namespace',path.parts[-3])
    for key, obj in cfg.get('items',{}).items():
        if not isinstance(obj,dict): continue
        res=obj.get('resource',{})
        if 'model_id' in res:
            slot=obj.get('specific_properties',{}).get('armor',{}).get('slot')
            material=res.get('material') or {'head':'LEATHER_HELMET','chest':'LEATHER_CHESTPLATE','legs':'LEATHER_LEGGINGS','feet':'LEATHER_BOOTS'}.get(slot)
            if material: ia[(material.upper(),int(res['model_id']))]=(ns,res)
texture_roots={}
for path in (SERVER/'plugins/ItemsAdder/contents').glob('*/resourcepack/assets/*'):
    if path.is_dir(): texture_roots[path.name]=path
def resource_path(ref, ns, folder, suffix):
    if ':' in ref: ns,ref=ref.split(':',1)
    return texture_roots.get(ns,Path('__missing__'))/folder/(ref+suffix)
def icon(t, i):
    b=item(t,i)['base']; match=ia.get((b['material'].upper(),int(b.get('custom-model-data',-1))))
    if not match: return ''
    ns,res=match; textures=res.get('textures',[]); ref=textures[0] if textures else None
    if not ref and res.get('model_path'):
        model=resource_path(res['model_path'],ns,'models','.json')
        if model.is_file():
            m=json.loads(model.read_text(encoding='utf-8-sig')); tx=m.get('textures',{})
            ref=tx.get('layer0') or tx.get('0') or tx.get('particle') or next(iter(tx.values()),None)
            visited=set()
            while ref and ref.startswith('#') and ref not in visited:
                visited.add(ref);ref=tx.get(ref[1:])
    if not ref: return ''
    src=resource_path(ref,ns,'textures','.png')
    if not src.is_file(): return ''
    # These are unmodified registered inventory textures, never invented screenshots.
    digest=hashlib.sha256(src.read_bytes()).hexdigest()
    dest='assets/server/equipment/'+digest[:16]+'.png'
    (ROOT/dest).parent.mkdir(parents=True,exist_ok=True)
    if not (ROOT/dest).exists(): shutil.copyfile(src,ROOT/dest)
    assets[dest]={'source':src.relative_to(SERVER).as_posix(),'sha256':digest,'kind':'server-original'}
    return dest
def pic(t,i):
    path=icon(t,i)
    return f'<img class="eq-icon" src="{path}" alt="{esc(name(t,i))}" loading="lazy">' if path else ''

def parse_item(text):
    m=re.search(r'mmoitems?\{([^}]+)\}',text,re.I)
    if not m: return None
    p=dict(re.findall(r'(\w+)\s*=\s*([^,;]+)',m[1]))
    if 'type' not in p or 'id' not in p: return None
    return (p['type'].upper(),p['id'],float(p.get('amount',1)))
prof={'smithing':'锻造','smelting':'冶炼','cooking':'烹饪','alchemy':'炼药','fishing':'垂钓','mining':'挖掘','farming':'采集','woodcutting':'伐木'}
stations=['smithing','cooking','alchemy','alchemy-extracting','gem-cutting','smelting','purification','bait-making']
recipes=defaultdict(list); uses=defaultdict(list)
for station in stations:
    cfg=read(MI/'crafting-stations'/f'{station}.yml')
    for key,r in cfg.get('recipes',{}).items():
        out=parse_item(r.get('output',''))
        if not out or out[:2] not in items: continue
        cond=' '.join(r.get('conditions',[])); cm=re.search(r'profession=([^,}]+),level=(\d+)',cond)
        ings=[]
        for s in r.get('ingredients',[]):
            ing=parse_item(s)
            if ing:
                if ing[:2] not in items: raise ValueError('Missing ingredient: '+str(ing))
                ings.append(ing)
            else: raise ValueError('Unsupported ingredient: '+s)
        xp=re.search(r'exp give %player% \w+ (\d+)',' '.join(r.get('triggers',[])))
        entry={'station':clean(cfg['name']),'id':key,'profession':prof.get(cm[1],cm[1]) if cm else '', 'level':int(cm[2]) if cm else 0,'time':r.get('crafting-time',0),'xp':int(xp[1]) if xp else 0,'amount':out[2],'ingredients':ings}
        recipes[out[:2]].append(entry)
        for t,i,amount in ings: uses[(t,i)].append((out[0],out[1],amount))

def material_anchor(t,i): return slug(t)+'-'+slug(i) if slug(t) else slug(i)
def itemroute(t,i):
    setid=item(t,i)['base'].get('set')
    if setid and i.startswith('DF_SUNSET_'): return 'equipment/sets/'+slug(setid)+'?id='+slug(i)
    if t in types: return 'equipment/types/'+types[t]+'?id='+slug(i)
    if t=='GEM_STONE': return 'equipment/gems?id='+slug(i)
    if t in ['工具','饵料']: return 'equipment/tools?id='+slug(i)
    if t=='食物' and i in market['cooking']['foods'] or t=='药水': return 'equipment/consumables?id='+slug(i)
    return 'equipment/materials?id='+material_anchor(t,i)
def ingredient(t,i,n): return link(itemroute(t,i),name(t,i))+' ×'+fmt(n)
def recipe_html(t,i):
    result=[]
    for r in recipes.get((t,i),[]):
        requirement=esc(r['profession'])+' '+str(r['level'])+' 级'
        heading=('<b>'+requirement+'</b>') if r['station']==r['profession'] else '<b>'+esc(r['station'])+'</b> · '+requirement
        result.append(f'<div class="eq-recipe"><p>{heading} · {fmt(r["time"])} 秒 · 产出 {fmt(r["amount"])} 个 · 经验 +{r["xp"]}</p><p>'+ '、'.join(ingredient(*a) for a in r['ingredients'])+'</p></div>')
    return ''.join(result)
def stats_html(b):
    rows=[]
    for k,v in b.items():
        if k in labels and isinstance(v,(int,float,dict)) and not isinstance(v,bool):
            if isinstance(v,dict) and not any(x in v for x in ['base','scale']): continue
            if v==0 or isinstance(v,dict) and v.get('base',0)==0 and v.get('scale',0)==0: continue
            rows.append(f'<div><dt>{statlink(k)}</dt><dd>{statvalue(k,v)}</dd></div>')
    return '<dl class="eq-stats">'+''.join(rows)+'</dl>'
def card(t,i,extra='',description=''):
    b=item(t,i)['base']; ident=slug(i) if t in types or t in ['GEM_STONE','食物','药水'] else material_anchor(t,i)
    tier={'COMMON':'普通','MAGICAL':'魔法','RARE':'稀有','LEGENDARY':'传奇','SET':'套装','UNIQUE':'独特'}.get(b.get('tier'))
    badge=(' · '+tier) if tier and t in types else ''
    return f'<article class="eq-item" id="{ident}" data-eq-search="{esc(name(t,i))}"><div class="eq-item-head">{pic(t,i)}<div><span class="eq-kicker">{esc(t if t!="GEM_STONE" else "宝石")}{badge}</span><h3>{esc(name(t,i))}</h3></div></div>{description}{stats_html(b) if t in types or t in ["工具","饵料"] else ""}{extra}{recipe_html(t,i)}</article>'
def table(headers,rows): return '\n| '+' | '.join(headers)+' |\n| '+' | '.join('---' for _ in headers)+' |\n'+''.join('| '+' | '.join(map(str,r))+' |\n' for r in rows)+'\n'
def cards(entries): return '<div class="eq-grid">\n'+ '\n'.join(entries)+'\n</div>\n'
def entry(route,title,text,image=''): return f'<a class="entry-card" href="#/equipment/{route}">{image}<strong>{title}</strong><span>{text}</span><b aria-hidden="true">↗</b></a>'
def searchbox(): return '<label class="eq-search">按名称筛选 <input type="search" data-eq-filter placeholder="输入装备或材料名"></label><p class="eq-filter-status" aria-live="polite"></p>\n\n'

# Validate all growth definitions against the loaded modifiers, not just the source table.
data={'types':{},'affixes':{},'labels':labels,'units':units,'links':{k:'#/'+statroute(k) for k in labels if statroute(k)},'icons':stat_icons}
for t,cfg in base.items():
    if t not in types: continue
    mod=mods[cfg['modifier']]
    loaded={}
    for child in mod.get('modifiers',{}).values(): loaded.update(child.get('stats',{}))
    for k,v in cfg['candidates'].items():
        assert loaded.get(k)==v,(t,k,'base growth differs from loaded modifier')
    data['types'][types[t]]={'name':t,'stats':cfg['candidates'],'guaranteed':cfg.get('guaranteed',[]),'durability':mod['stats'].get('max-durability')}
for q in ['魔法','稀有','传奇']:
    m=mods['武器'+q+'词条组']
    data['affixes'][q]={'min':m['min'],'max':m['max'],'stats':{}}
    for key,v in m['modifiers'].items():
        for k,stat in v.get('stats',{}).items(): data['affixes'][q]['stats'][k]={'growth':stat,'rank':re.search(r'T\d',key)[0]}

# Real monster -> drop-table references; orphan tables are not published as sources.
mob_tables=defaultdict(list)
for path in (SERVER/'plugins/MythicMobs/mobs').rglob('*.yml'):
    cfg=read(path)
    for mob,m in cfg.items():
        if not isinstance(m,dict): continue
        for drop in m.get('Drops',[]):
            tok=str(drop).split()
            if tok: mob_tables[tok[0]].append(str(mob))
material_sources=defaultdict(list)
for path in (SERVER/'plugins/MythicMobs/droptables').glob('落日森林_材料*.yml'):
    for tab,m in read(path).items():
        if tab not in mob_tables: continue
        for s in m.get('Drops',[]):
            out=parse_item(s)
            if not out: continue
            tail=s.split('}',1)[1].strip().split()
            qty=tail[0]; prob=float(tail[1]) if len(tail)>1 else 1
            if 'to' in qty:
                lo,hi=map(float,qty.split('to')); qty=f'{int(lo+0.5)}–{int(hi-0.5)}'
            material_sources[out[:2]].append('、'.join(mob_tables[tab])+f'：{fmt(prob*100)}% 掉落 {qty} 个')
for i,obj in market.get('ingredient-shop',{}).get('items',{}).items():
    material_sources[(obj['type'].upper(),i)].append('食材商店：'+str(obj['price'])+' 金币 / 个')
herbs=read(SERVER/'plugins/TopCraftHerbs/config.yml')
def herb_sources(obj):
    if not isinstance(obj,dict): return
    if obj.get('mmoitems-id') and obj.get('enabled',True):
        key=(obj.get('mmoitems-type','采集').upper(),obj['mmoitems-id'])
        material_sources[key].append('野外采摘：每株 '+str(obj.get('amount',1))+' 个')
    for v in obj.values(): herb_sources(v)
herb_sources(herbs)

# Page composition follows the catalog, mechanics and recipe split used by ARPG wikis.
page('overview','装备与道具','查找装备属性、套装效果与制作材料，也可以从这里了解强化、镶嵌和补给。',
 '<div class="entry-grid">'+''.join(entry(*x) for x in [
 ('catalog','装备图鉴','17 类装备 · 等级数值查询 · 锻造配方'),('quality','品质与词条','基础属性与附加词条 · 各品质词条池'),('sets','套装与独特装备','13 套护甲 · 部件与套装奖励'),('upgrading','强化','四种强化石 · 成功率 · 属性成长'),('gems','宝石与镶嵌','五色宝石 · 五个档次 · 切割配方'),('identification','鉴定与修理','鉴定卷轴 · 装备耐久 · 修理费用'),('consumables','食物与药水','恢复效果 · 料理加成 · 炼药配方'),('materials','材料图鉴','怪物掉落 · 商店价格 · 制作用途')])+'</div>\n\n'+
 '## 装备从哪里来\n\n落日森林的普通怪物有 **3%** 几率掉落一件随机装备，精英为 **25%**，领主为 **75%**。残阳君主还会额外掉落一件残阳誓卫套装部件。锻造装备有固定名称、使用等级和配方，可在[装备图鉴](equipment/catalog.md)按类型查找。\n\n'+
 '## 物品等级与使用等级\n\n随机掉落装备的物品等级由怪物等级决定，影响属性数值。使用等级在物品等级前后 2 级内随机，最低 1 级、最高 30 级。\n\n'+
 '## 穿戴与搭配\n\n[武器与穿戴](equipment/slots.md)介绍防具、手持物品和五个饰品栏。[伤害与暴击](combat/damage.md)与[防御与恢复](combat/defense.md)说明各类属性的效果。')

page('slots','武器与穿戴','防具放入对应护甲栏；戒指、项链、护符和腰带有各自的饰品栏。',
 '## 栏位\n\n'+table(['装备','位置'],[['剑、斧、锤、匕首、矛、权杖、魔杖','手持武器'],['法书、盾牌','手持装备；盾牌举盾规则见[盾牌与格挡](combat/defense.md?id=block)'],['头盔、胸甲、护腿、靴子','对应的四个护甲栏'],['两枚戒指','背包第一排左起第 1、2 格'],['项链','背包第一排左起第 3 格'],['护符','背包第一排左起第 4 格'],['腰带 / 饰品','背包第一排左起第 5 格']])+
 '## 装备要求\n\n装备达到标注的使用等级后可以使用。未鉴定装备需要先用[鉴定卷轴](equipment/identification.md)鉴定；带有职业限制或灵魂绑定的装备还须符合对应条件。\n\n## 查找装备\n\n[装备图鉴](equipment/catalog.md)收录各类型的基础属性、成长范围和锻造装备。[套装图鉴](equipment/sets.md)收录四件护甲的组合效果。')

catalog=[]
for t,s in types.items():
    craft=[i for (ty,i) in recipes if ty==t and i.startswith('DF_FORGED_')]
    preview=pic(t,craft[0]) if craft else ''
    catalog.append(entry('types/'+s,t,'基础属性与成长 · '+str(len(craft))+' 件锻造装备',preview))
    cfg=base[t]; rows=[]
    guaranteed=cfg.get('guaranteed',[])
    for k,v in cfg['candidates'].items():
        rows.append([statlink(k)+(' · 必有' if k in guaranteed else ''),fmt(v['base']+v['scale'])+units.get(k,''),'+'+fmt(v['scale'])+(' 个百分点' if units.get(k) else ''),statvalue(k,v,25)])
    count=min(base_config['max-stats'],len(cfg['candidates']))
    content='## 随机装备\n\n'+(f'基础属性从下列候选中不重复选取 **{count} 项**。' if len(cfg['candidates'])>count else f'固定具有下列 **{count} 项**基础属性。')+('靴子的移动速度必有，另选 2 项。' if t=='靴子' else '')+'每项属性的实际数值在中心值的 **88%–112%** 之间浮动。\n\n'
    content+=f'<div class="eq-growth" data-eq-type="{s}"><label>物品等级 <input type="number" min="1" step="1" value="25" aria-label="物品等级"></label><div class="eq-growth-result" aria-live="polite"></div></div>\n\n'
    content+=table(['属性候选','1 级中心值','每级成长','25 级范围'],rows)
    dura=cfg['item-stats'].get('max-durability')
    if dura: content+='最大耐久：1 级 **'+fmt(dura['base']+dura.get('scale',0))+'**，每级 **+'+fmt(dura.get('scale',0))+'**。\n\n'
    else: content+='这类饰品没有耐久消耗。\n\n'
    content+='掉落来源：落日森林随机装备。附加词条见[品质与词条](equipment/quality.md)，护甲组合见[套装图鉴](equipment/sets.md)。\n\n'
    if craft:
        content+='## 锻造装备\n\n在锻造工作站制作。卡片列出成品的使用等级、属性范围与材料消耗。\n\n'+cards([card(t,i) for i in craft])
    page('types/'+s,t+'图鉴','随机掉落与锻造'+t+'的属性、成长和获取方式。',content)
page('catalog','装备图鉴','按类型查看基础属性与等级成长，或查找锻造装备的具体数值和配方。','[查看穿戴栏位](equipment/slots.md) · [套装图鉴](equipment/sets.md) · [生活工具与鱼饵](equipment/tools.md)\n\n<div class="entry-grid">'+''.join(catalog)+'</div>')

quality='## 品质\n\n'+table(['品质','附加词条','非套装随机掉落占比'],[['普通','无附加词条','70%'],['魔法','1–2 项，来自魔法词条池','25%'],['稀有','2–4 项，来自稀有词条池','4%'],['传奇','2–4 项，来自传奇词条池','1%'],['套装','按套装分别列出，并有穿戴件数奖励','占全部随机装备的 5%'],['独特','由具体装备决定','不在普通随机掉落品质池中']])
quality+='基础属性与附加词条分别生成。装备外观可以在不同品质间共用，品质以装备名称与品质标识为准。\n\n## 附加词条数值\n\n选择物品等级和品质，查看该品质可能出现的词条及数值范围。\n\n<div class="eq-affixes"><label>物品等级 <input type="number" min="1" step="1" value="25" aria-label="词条物品等级"></label><label>品质 <select aria-label="词条品质"><option>魔法</option><option>稀有</option><option>传奇</option></select></label><div class="eq-affix-result" aria-live="polite"></div></div>\n\n'
for q,a in data['affixes'].items():
    quality+=f'<details class="eq-details"><summary>{q}词条池 · 完整成长公式</summary>\n\n'+table(['词条','分级','1 级中心值','每级成长'],[[statlink(k),v['rank'],statvalue(k,{**v['growth'],'max-spread':0},1),fmt(v['growth'].get('scale',0))+(' 个百分点' if units.get(k) else '')] for k,v in a['stats'].items()])+'\n</details>\n\n'
quality+='## 词条怎样影响战斗\n\n[伤害与暴击](combat/damage.md) · [护甲、抗性与恢复](combat/defense.md) · [召唤物属性](combat/summons.md) · [冷却与法力消耗](combat/attributes.md)'
page('quality','品质与词条','装备类型决定基础属性候选；品质决定附加词条的数量和种类。',quality)

sets=read(MI/'armor-sets.yml')['sets']; boss=read(MI/'boss-sets.yml'); loaded_sets=read(MI/'item-sets.yml')
set_cards=[]
for sid,cfg in {**sets,**boss}.items():
    assert cfg['bonuses']==loaded_sets[sid]['bonuses'],sid
    entries=[]
    for t in ['头盔','胸甲','护腿','靴子']:
        if sid in sets: iid=sid
        else: iid=next(i for ty,i in items if ty==t and item(ty,i)['base'].get('set')==sid)
        entries.append((t,iid))
    route='sets/'+slug(sid)
    set_cards.append(entry(route,cfg['name'],'2 / 3 / 4 件效果 · '+('残阳君主掉落与锻造' if sid in boss else '落日森林随机掉落'),pic(*entries[0])))
    content='## 套装效果\n\n'+table(['穿戴件数','新增效果'],[[n,'；'.join(statlink(k)+' +'+statvalue(k,v) for k,v in stats.items())] for n,stats in cfg['bonuses'].items()])
    content+='各档奖励累加，穿齐 4 件时同时获得 2、3、4 件奖励。四个部位分别为头盔、胸甲、护腿和靴子。\n\n## 获取方式\n\n'
    if sid in boss:
        content+='击败落日森林的 **残阳君主**，每次掉落一件套装部件，四个部位等概率。残阳君主还掉落 **1 个残阳烬核**；每个部件也可在 **锻造 30 级**制作。\n\n'
        content+='## 套装部件\n\n'+cards([card(t,i) for t,i in entries])
    else:
        content+='来自落日森林的随机装备掉落。每次生成随机装备有 **5%** 几率成为套装护甲；同套装的四个部位均可掉落。\n\n'
        profile=cfg['stat-profile']; q={'COMMON':'普通','MAGICAL':'魔法','RARE':'稀有','LEGENDARY':'传奇'}[profile]
        text={'COMMON':'无附加词条','MAGICAL':'1–2 项魔法池词条','RARE':'2–4 项稀有池词条','LEGENDARY':'2–4 项传奇池词条'}[profile]
        content+=f'每个部位有 3 项基础属性，{text}。基础属性随物品等级成长；点击部位可查询具体范围。\n\n'
        content+=cards([f'<article class="eq-item"><div class="eq-item-head">{pic(t,i)}<h3>{link("equipment/types/"+types[t],cfg["name"]+" · "+t)}</h3></div><p>基础属性与成长见部位图鉴；附加词条见{link("equipment/quality",q+"词条池")}。</p></article>' for t,i in entries])
    page(route,cfg['name'],'四件护甲的部件属性、套装奖励与获取方式。',content)
page('sets','套装与独特装备','套装以穿戴件数提供额外属性；各部件本身的属性与套装奖励分别生效。','## 套装图鉴\n\n<div class="entry-grid">'+''.join(set_cards)+'</div>\n\n## 独特装备\n\n独特是单独的装备品质，不会从普通随机装备的品质池中抽出。当前图鉴收录有明确获取途径的装备；独特装备尚无可列出的获取条目。')

upgrade=read(MI/'upgrade-stones.yml')['stones']
upcontent='## 如何强化\n\n在背包中拿起强化石，放到要强化的装备上。强化成功提高 1 级，最高 **+15**。失败消耗强化石，装备和强化等级保留。\n\n## 强化石\n\n'
upcards=[]
for i,cfg in upgrade.items():
    src={'TC_UPGRADE_STONE':'每周礼包 ×2','TC_UPGRADE_STONE_TIDE':'每月礼包 ×3'}.get(i,'暂无可确认的获取途径')
    upcards.append(card('CONSUMABLE',i,f'<p class="eq-effect">成功率 <b>{cfg["success"]}%</b></p><p>获取：{src}。</p>'))
upcontent+=cards(upcards)+'\n## 属性成长\n\n每次成功强化，参与强化的属性在当前数值上提高 **5%**。强化 n 级后的数值 = 初始数值 × 1.05ⁿ。例如初始物理伤害 20，+1 为 21，+5 约 25.53，+15 约 41.58。\n\n<div class="eq-upgrade"><label>初始属性 <input type="number" min="0" step="any" value="20" aria-label="初始属性"></label><label>强化等级 <input type="number" min="0" max="15" step="1" value="15" aria-label="强化等级"></label><output aria-live="polite"></output></div>\n\n'
upstats=read(MI/'upgrade-templates.yml')['topcraft-fixed']
upcontent+='## 哪些属性会提高\n\n'+ '、'.join(statlink(k) for k in upstats)+'。\n\n物品等级、使用等级、最大耐久与套装奖励不随强化提升。附加词条中未列在上述范围内的属性也不提升。宝石与强化的关系见[宝石与镶嵌](equipment/gems.md)。'
page('upgrading','强化','强化提高装备属性；四种强化石的成功率分别为 25%、50%、75% 和 100%。',upcontent)

gemcfg=read(MI/'gem-drops.yml'); gemcards=[]
gembody='## 镶嵌\n\n随机装备有 **10%** 几率带一个宝石孔，五种孔色等概率。将宝石拖放到具有同色空孔的装备上即可镶嵌；本页宝石镶嵌成功率均为 **100%**。每颗宝石提供一项固定属性，再随机获得另一项不同的属性。\n\n宝石按档次提供固定数值，不随镶嵌目标的物品等级变化。\n\n## 五色宝石\n\n'+table(['颜色','固定属性'],[[c,statlink(v['fixed-stat'])] for c,v in gemcfg['gems'].items()])
gembody+='## 切割与各档数值\n\n前往挖掘生活职业菜单的宝石切割入口，在冶炼达到配方等级后制作。卡片中的等级是制作要求。\n\n'
for color,cfg in gemcfg['gems'].items():
    gembody+='### '+color+'\n\n'
    colorcards=[]
    for tier in [10,25,40,60,80]:
        iid=cfg['template']+'_CUT_'+str(tier); b=item('GEM_STONE',iid)['base']; key=cfg['fixed-stat']
        pool=mods[f'切割宝石_{color}_{tier}']['modifiers']
        secondary={k:v for m in pool.values() for k,v in m.get('stats',{}).items()}
        desc=f'<p class="eq-effect">{statlink(key)} <b>+{statvalue(key,b[key])}</b></p>'
        desc+='<details class="eq-details"><summary>随机附加属性 · 从 '+str(len(secondary))+' 项中获得 1 项</summary><dl class="eq-stats">'+''.join(f'<div><dt>{statlink(k)}</dt><dd>+{statvalue(k,v)}</dd></div>' for k,v in secondary.items())+'</dl></details>'
        colorcards.append(card('GEM_STONE',iid,desc))
    gembody+=cards(colorcards)+'\n'
gembody+='## 强化与拆卸\n\n宝石属性采用后续强化：镶嵌后再成功强化，参与强化的宝石属性也会成长；装备已有的强化等级不会追溯增加刚镶入的宝石属性。\n\n目前没有可确认的宝石拆卸道具获取途径。'
page('gems','宝石与镶嵌','五种颜色对应五项固定属性，每颗切割宝石另有一项随机属性。',gembody)

ident=pic('CONSUMABLE','TC_IDENTIFICATION_SCROLL')
page('identification','鉴定与修理','鉴定揭示装备属性；修理恢复装备和工具的耐久。',
 '## 鉴定\n\n随机掉落装备有 **10%** 几率处于未鉴定状态。将鉴定卷轴拖放到未鉴定装备上，消耗一张卷轴并显示完整属性。鉴定不会重新随机装备属性。\n\n'+cards([f'<article class="eq-item"><div class="eq-item-head">{ident}<h3>鉴定卷轴</h3></div><p>每日礼包 ×1 · 每周礼包 ×3 · 每月礼包 ×5</p></article>'])+
 '\n## 修理\n\n手持一件需要修理的装备或工具，输入 **`/修复`**。界面列出当前耐久、损失耐久和费用；点击“确认修复”后扣除金币并恢复全部耐久。\n\n每恢复 **1 点耐久消耗 <span data-number-raw>0.05</span> 金币**。例如损失 100 点耐久，修理费为 5 金币。耐久已满时不会扣费。\n\n## 耐久耗尽\n\n带有损坏规则的装备可能在耐久耗尽时损坏，应在耗尽前维修。盾牌耐久为 0 时无法举盾，仍可修复。旧鱼竿无法维修。\n\n[强化](equipment/upgrading.md)不会恢复耐久，也不会提高最大耐久。')

foodcards=[]; potioncards=[]
attributes={'dexterity':'敏捷','strength':'力量','vitality':'体质','intelligence':'智力','spirit':'精神'}
for iid,f in market['cooking']['foods'].items():
    assert ('食物',iid) in recipes,('food missing recipe',iid)
    desc=f'<p class="eq-effect">{f["regeneration-seconds"]} 秒内恢复最大生命值的 <b>{f["health-percent"]}%</b>。</p>'
    if f.get('buff'):
        b=f['buff']; desc+=f'<p>{attributes[b["attribute"]]} +{b["amount"]}，持续 {fmt(b["duration-seconds"]/60)} 分钟。</p>'
    foodcards.append(card('食物',iid,desc))
for iid,f in market['alchemy']['potions'].items():
    if f.get('legacy'): continue
    desc=f'<p class="eq-effect">立即恢复最大'+('生命值' if f['resource']=='health' else '法力值')+f'的 <b>{f["percent"]}%</b>。</p>'
    potioncards.append(card('药水',iid,desc))
for iid,f in market['alchemy']['effects'].items():
    k=f['stat'].lower().replace('_','-'); val=fmt(f['amount'])+('%' if f['mode']=='RELATIVE' else units.get(k,''))
    desc=f'<p class="eq-effect">{statlink(k)} <b>+{val}</b>，持续 {f["duration-seconds"]} 秒。</p>'
    potioncards.append(card('药水',iid,desc))
page('consumables','食物与药水','食物提供脱战恢复，料理附带属性加成；药水可在战斗中补充生命和法力。',
 '## 食用、冷却与覆盖\n\n'+table(['种类','使用时机','共享冷却','持续效果'],[['食物与料理','脱离战斗后','5 秒','新食物替换尚未完成的恢复；新料理替换原料理属性'],['生命、法力、轻步药水','可在战斗中使用','15 秒','恢复药水立即生效；轻步持续 8 秒'],['药剂与合剂','可在战斗中使用','1 秒','同时保留一种，新效果替换旧效果']])+
 '食物开始恢复后，攻击或受伤不会中断恢复。料理与药剂可以同时生效。没有属性加成的普通食物在生命已满时不能食用。料理、药剂和合剂的持续效果在死亡时移除。\n\n'+searchbox()+
 '## 食物与料理\n\n'+cards(foodcards)+'\n## 药水、药剂与合剂\n\n'+cards(potioncards))

# Finished tools and bait are separate from ingredients, but keep recipe round trips.
toolkeys=[(t,i) for t,i in recipes if t in ['工具','饵料']]
toolcards=[]
for t,i in toolkeys:
    b=item(t,i)['base']
    req=['需要'+zh+' '+fmt(b['profession-'+key])+' 级' for key,zh in prof.items() if 'profession-'+key in b]
    desc='<p>'+ '；'.join(req)+'</p>' if req else ''
    if b.get('gem-sockets'): desc+='<p>可镶嵌：'+ '、'.join(map(esc,b['gem-sockets']))+'。</p>'
    toolcards.append(card(t,i,description=desc))
page('tools','生活工具与鱼饵','锻造工具的耐久、使用要求和配方，以及制作鱼饵所需的材料。','采集与挖掘规则见[资源采集](life/gathering.md)，抛竿、鱼饵与鱼获规则见[垂钓](life/fishing.md)。\n\n'+searchbox()+cards(toolcards))

# Materials include all ingredients used by the published recipes, recursively.
material_keys=set(uses)|set(material_sources)|set(recipes)
material_keys={k for k in material_keys if k in items and k[0] not in types and k[0] not in ['药水','GEM_STONE','工具','饵料'] and not(k[0]=='食物' and k[1] in market['cooking']['foods'])}
material_cards=[]; material_groups=defaultdict(list)
for t,i in sorted(material_keys):
    b=item(t,i)['base']; src=material_sources.get((t,i),[])
    # Preserve explicit in-game source descriptions where no enumerated drop/shop exists.
    lore=[clean(s) for s in b.get('lore',[]) if clean(s)]
    source_lore=[s for s in lore if any(w in s for w in ['来源','采集','采矿','挖掘','伐木','钓鱼','垂钓','采摘'])]
    if t=='伐木' and i in ['BIRCH_LOG','DARK_OAK_LOG','OAK_LOG','SPRUCE_LOG']:
        source_lore=['伐木：砍伐对应树种获得']
    src=src or source_lore
    source_html='<p><b>获取</b>：'+('；'.join(esc(s) for s in src) if src else ('通过下方配方制作' if recipes.get((t,i)) else '获取地点尚未收录'))+'。</p>'
    reverse=uses.get((t,i),[])
    uses_html='<details class="eq-details"><summary>制作用途 · '+str(len(reverse))+' 项</summary><ul>'+''.join('<li>'+link(itemroute(ty,ii),name(ty,ii))+'：每次制作消耗本材料 ×'+fmt(n)+'</li>' for ty,ii,n in reverse)+'</ul></details>' if reverse else ''
    if i=='DF_SOFT_HIDE': uses_html+='<p>任务用途：'+link('quests/forest','巡查补给')+'需要 8 张柔软兽皮。</p>'
    rendered=card(t,i,source_html+uses_html)
    material_cards.append(rendered);material_groups[t].append(rendered)
material_nav='<nav class="entry-nav" aria-label="材料分类">'+''.join(link('equipment/materials?id=material-group-'+str(n),t+' · '+str(len(v))) for n,(t,v) in enumerate(material_groups.items()))+'</nav>\n\n'
material_body=''.join(f'<section class="eq-category" id="material-group-{n}"><h2>{esc(t)}</h2>{cards(v)}</section>\n\n' for n,(t,v) in enumerate(material_groups.items()))
page('materials','材料图鉴','按名称查找材料的掉落、购买价格和配方用途。点击成品名称可以查看完整配方。',material_nav+searchbox()+material_body)

write('assets/data/equipment.json',json.dumps(data,ensure_ascii=False,indent=2)+'\n')
routes=['/']
for section in ['combat','guide','equipment','world','quests','dungeons','life','social']:
    routes.extend('/'+p.relative_to(ROOT).with_suffix('').as_posix() for p in sorted((ROOT/section).rglob('*.md')))
write('assets/search-paths.js','window.TopCraftSearchPaths = '+json.dumps(routes,ensure_ascii=False)+';\n')
write('_maintenance/equipment-assets.json',json.dumps(assets,ensure_ascii=False,indent=2)+'\n')
sources.update(['plugin-src/TopCraftDivineDescent/EquipmentDropHandler.java','plugin-src/TopCraftDivineDescent/GemDropPolicy.java','plugin-src/TopCraftProfessionMarket/FoodEffects.java','plugin-src/TopCraftProfessionMarket/AlchemyPotions.java','plugin-src/TopCraftProfessionMarket/AlchemyBuffs.java','plugin-src/TopCraftProfessionMarket/PaidRepair.java','plugin-src/TopCraftProfessionMarket/plugin.yml','plugins/DailyRewards/config.yml','plugins/BlockRegen/Blocklist.yml','plugins/BetonQuest/QuestPackages/duskforest_entry/conditions.yml','plugins/BetonQuest/QuestPackages/duskforest_entry/actions.yml','plugins/MMOItems-6.10.1-20260531.191614-59.jar','plugins/MythicLib-dist-1.7.1-20260607.161447-102.jar'])
write('_maintenance/equipment-sources.json',json.dumps({'generated_by':'scripts/build_equipment.py','sources':sorted(sources),'scope':{'types':len(types),'sets':len(sets)+len(boss),'foods':len(foodcards),'potions':len(potioncards),'materials':len(material_cards),'recipes':sum(len(v) for v in recipes.values())},'unresolved':['紫曜与日辉强化石：未找到玩家获取入口','独特装备：未找到玩家获取入口','宝石拆卸：未找到玩家获取入口']},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'types':len(types),'sets':len(sets)+len(boss),'foods':len(foodcards),'potions':len(potioncards),'materials':len(material_cards),'assets':len(assets)},ensure_ascii=False))
