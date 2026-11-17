'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const data = JSON.parse(fs.readFileSync(path.join(root, 'assets/data/equipment.json'), 'utf8'));
const { range, upgrade } = require('../assets/equipment.js');
const near = (actual, expected) => assert.ok(Math.abs(actual - expected) < 1e-8, `${actual} != ${expected}`);
// Known server values: sword at level 1 and 25, boots' guaranteed speed, accessory pool sizes.
near(range(data.types.sword.stats['custom-physical-damage-bonus'], 1).center, 8.5);
near(range(data.types.sword.stats['custom-physical-damage-bonus'], 25).min, 25.96);
near(range(data.types.sword.stats['custom-physical-damage-bonus'], 25).max, 33.04);
assert.deepEqual(data.types.boots.guaranteed, ['custom-movement-speed-bonus-percent']);
for (const name of ['necklace', 'ring', 'belt', 'charm']) assert.equal(Object.keys(data.types[name].stats).length, 1);
near(upgrade(20, 0), 20);
near(upgrade(20, 1), 21);
near(upgrade(20, 5), 25.52563125);
near(upgrade(20, 15), 41.57856358822738);
assert.equal(data.labels['custom-mana-cost-reduction-percent'], '法力消耗降低');
let samples = 0;
for (const type of Object.values(data.types)) {
  for (const stat of Object.values(type.stats)) {
    for (const level of [1, 10, 25, 30, 60, 80, 100]) {
      const r = range(stat, level);
      assert.ok(Number.isFinite(r.min) && r.min <= r.center && r.center <= r.max);
      samples++;
    }
  }
}
for (const pool of Object.values(data.affixes)) {
  for (const [key, stat] of Object.entries(pool.stats)) {
    assert.ok(data.labels[key] && /[\u4e00-\u9fff]/.test(data.labels[key]));
    assert.ok(range(stat.growth, 25).min >= 0);
    samples++;
  }
}
console.log(`PASS: ${samples} equipment/affix samples; known growth values, accessory counts and native compounding upgrade examples.`);
