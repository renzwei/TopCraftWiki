<nav class="wiki-breadcrumb" aria-label="当前位置"><span>战斗机制</span><span>›</span><span>防御与恢复</span></nav>

# 防御与恢复

<p class="lead">查看护甲与抗性的减伤效果，以及举盾、护盾、躲闪和治疗如何保护角色。</p>

<nav class="mechanics-tabs" aria-label="战斗机制"><a href="#/combat/attributes">角色属性</a><a href="#/combat/damage">伤害与暴击</a><a href="#/combat/defense" aria-current="page">防御与恢复</a><a href="#/combat/status-effects">状态与控制</a></nav>

<nav class="entry-nav" aria-label="本页条目"><a href="#/combat/defense?id=armor">护甲与抗性</a><a href="#/combat/defense?id=reduction">百分比减伤</a><a href="#/combat/defense?id=block">举盾格挡</a><a href="#/combat/defense?id=perfect-block">完美格挡</a><a href="#/combat/defense?id=shield">护盾</a><a href="#/combat/defense?id=dodge">躲闪</a><a href="#/combat/defense?id=healing">治疗与吸血</a></nav>

## <img class="pixel-icon" src="assets/server/stats/defense.png" alt=""> 护甲与元素抗性 :id=armor

护甲降低物理伤害，单元素抗性降低对应元素伤害。计算公式为：

<div class="formula">实际护甲 = 护甲 ×（1 + 总护甲% ÷ 100）<br>护甲后物理伤害 = 物理伤害 × 1000 ÷（1000 + 实际护甲）<br>抗性后元素伤害 = 该元素伤害 × 1000 ÷（1000 + 该元素抗性）</div>

| 护甲或单元素抗性 | 对应伤害减免 | 受到 100 点伤害时实际承受 |
| --- | --- | --- |
| 100 | 9.09% | 90.91 |
| 250 | 20% | 80 |
| 500 | 33.33% | 66.67 |
| 1000 | 50% | 50 |
| 2000 | 66.67% | 33.33 |
| 4000 | 80% | 20 |

摔落、溺水、虚空伤害不受护甲减免。混合伤害的各元素分别计算，例如物理部分受护甲减免，火焰部分受火焰抗性减免。

## <img class="pixel-icon" src="assets/server/stats/all_element_resistance.png" alt=""> 全元素抗性与最终减伤 :id=reduction

全元素抗性降低经过单元素抗性减免后的火焰、冰霜、雷电、毒素伤害。总护甲百分比则提高护甲数值。

对应怪物品阶减伤和通用最终伤害减免再分别乘剩余比例，均限制在 0～100%。例如 100 点火焰伤害，火抗 1000、全元素抗性 20%、对应品阶减伤 10%、最终减伤 15%：

`100 × 1000/2000 × 0.8 × 0.9 × 0.85 = 30.6`

关卡的承伤倍率在上述减免之后计算。不同种类的减伤按剩余伤害相乘：例如 20% 全元素抗性与 15% 最终伤害减免，合计减伤为 `1 − 0.8 × 0.85 = 32%`。

## <img class="pixel-icon" src="assets/server/stats/block.png" alt=""> 举盾格挡 :id=block

将盾牌装备在主手或副手，按住使用物品键（默认右键）举盾，可以完全抵挡一次击中类攻击。临近受击时举盾可触发<strong>完美格挡</strong>，免除本次耐久消耗。普通格挡和完美格挡成功后都会放下盾牌，并进入冷却。

| 规则 | 效果 |
| --- | --- |
| 能格挡的伤害 | 符合击中条件的攻击 |
| 无法格挡的伤害 | 持续伤害、摔落、溺水等非击中伤害 |
| 普通格挡耐久消耗 | 按护甲与抗性减伤前的伤害扣除，最多扣完剩余耐久 |
| 完美格挡耐久消耗 | 不消耗耐久 |
| 耐久不足 | 只要盾牌仍有耐久，就能完整抵挡本次攻击；耐久耗尽后无法继续举盾，也无法触发完美格挡 |
| 冷却 | 默认 5 秒，由正在使用的盾牌自身“盾牌冷却缩减”降低 |
| 修理 | 耐久为 0 时盾牌仍保留，可修理后继续使用 |

### 完美格挡 :id=perfect-block

在盾牌举起后的<strong>前 6 个游戏刻（约 0.3 秒）</strong>内挡住攻击，即为完美格挡。判定从实际举起盾牌时开始；一直按住举盾不会反复刷新这个窗口。举盾满 6 个游戏刻后挡住攻击，按普通格挡处理。

完美格挡<strong>完全抵消本次伤害，且不消耗盾牌耐久</strong>，成功时会播放更高音调的格挡音效。它同样只能抵挡击中类攻击，无法抵挡持续伤害、摔落或溺水。

例如盾牌剩余 80 点耐久，受到一次减伤前为 100 点的可格挡攻击：普通格挡能挡下全部伤害，但耐久降至 0；完美格挡同样挡下全部伤害，耐久仍为 <strong>80 点</strong>。

观察敌人的攻击动作，在攻击即将命中时举盾。过早举盾会变为普通格挡，攻击已经命中后再举盾则无法补挡。完美格挡成功后仍需等待盾牌冷却结束，才能再次举盾。

### 格挡冷却 :id=block-cooldown

普通格挡与完美格挡共用同一套冷却，完美格挡不会额外缩短冷却。

<div class="formula">举盾冷却 = 5 秒 ×（1 − 盾牌冷却缩减 ÷ 100）</div>

20% 盾牌冷却缩减将冷却缩短至 <strong>4 秒</strong>。该属性的有效范围为 0～100%，冷却按 <span data-number-raw>0.05</span> 秒向上取整。盾牌共用冷却，更换另一面盾牌不能立即再次格挡。

举盾格挡在护盾吸收之前生效；成功格挡的攻击不会继续消耗护盾。护甲、抗性和躲闪在护盾之后处理。

## <img class="pixel-icon" src="assets/server/stats/dome.png" alt=""> 护盾 :id=shield

护盾先于护甲与抗性抵消伤害。受击时仍有护盾，即可抵消本次伤害；破盾时超出的伤害不会扣除生命。护盾的获得加成、自然衰减、定时护盾与保留效果见独立条目。

<div class="mechanic-cards"><a class="mechanic-card" href="#/combat/shield"><img class="pixel-icon" src="assets/server/stats/dome.png" alt=""><strong>护盾详解</strong><span>吸收顺序、破盾、获得量与衰减</span></a></div>

## <img class="pixel-icon" src="assets/server/stats/dodge.png" alt=""> 躲闪 :id=dodge

躲闪可避开击中类技能和怪物普通攻击，不作用于持续伤害、摔落和溺水等伤害。

躲闪率的长期有效上限为 <strong>75%</strong>。连续躲闪失败时，后续成功几率逐步提高；成功躲闪后重新开始累计。单次判定几率最高为 <strong>95%</strong>。

举盾或护盾已经抵消的攻击不会再判定躲闪，也不累计躲闪失败次数。

## <img class="pixel-icon" src="assets/server/stats/healing_bonus.png" alt=""> 治疗、受到治疗与吸血 :id=healing

带治疗标签的玩家治疗使用来源的治疗提高；接收玩家再按自身受到治疗百分比增加一次。百分比治疗以<strong>每个目标自身最大生命</strong>计算。

例：1000 生命目标接受 5% 最大生命治疗，施法者治疗提高 20%、接收者受到治疗 10%，无其他状态时：`1000 × 0.05 × 1.2 × 1.1 = 66`。实际恢复不能超过已损失生命；只有明确提供溢出转盾的技能才处理溢出。

普通吸血根据击中造成的<strong>实际物理伤害</strong>；法术吸血要求法术标签，排除持续与召唤伤害。吸血使用目标减伤后实际承受的伤害，超过目标剩余生命的伤害不计入吸血。

例如一次物理法术造成 100 点伤害，目标受击前剩余 40 点生命，普通吸血为 10%、法术吸血为 5%，则恢复基数为 `40 × (0.10 + 0.05) = 6`，再受相应治疗加成影响。被护盾完全抵消的伤害不产生这类吸血。

治疗降低会减少恢复量，详见[治疗降低](#/combat/status-effects?id=healing-reduction)。

<div class="page-end">TopCraft 玩家手册 · 更新于 2026-11-16</div>
