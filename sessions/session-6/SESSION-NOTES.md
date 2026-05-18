# Session 6 — Battle! Part 2: Making It Hurt

## Goal
Make battles actually deal damage, faint monsters, award XP, and detect win/lose. By the end of today, you have a fully functional battle system!

## What you are building today
- `monster.py` — `update_xp()` so monsters level up after earning XP
- `battle.py` — `apply_attack()`, `check_death()`, and `check_end_battle()`

## Key concepts
- **Damage formulas**: combining attack, type effectiveness, and defense into a single number
- **Type effectiveness**: the rock-paper-scissors triangle of fire/plant/water
- **Win/lose states**: detecting when all monsters on one side have fainted
- **XP and leveling**: rewarding the player with growth after victory

---

## Why is the fire/plant/water triangle elegant?

Three types, each beats one and loses to one. It is perfectly balanced with no "best" type. This means:
- You have to think about which monster to send out
- Type decisions matter even at low levels
- It is easy to understand after hearing it once

Compare that to more complex systems with 18 types and 324 interactions — elegant design beats complex design every time.

---

## The damage formula — how does it work?

Real games use formulas like this (simplified version):

```
base_damage = attacker.attack_stat * attack.amount
type_modifier = 2.0 or 0.5 or 1.0
defense_modifier = 1 - (defense_stat / 2000)
final_damage = base_damage * type_modifier * defense_modifier
```

The defense modifier means:
- A monster with defense 100 takes `1 - (100/2000) = 0.95` of the damage (5% reduction)
- A monster with defense 500 takes `1 - (500/2000) = 0.75` (25% reduction)
- A defending monster takes 0.2 less on top of that

This creates a smooth scale where defense matters but never makes a monster invincible.

---

## Step-by-step

### Step 1 — Build `update_xp(amount)` in `monster.py`

The XP system has two cases. The hint in the file spells them out:

**Case 1**: `self.level_up - self.xp > amount`
- There is room before the next level: just add `self.xp += amount`

**Case 2**: not enough room — level up!
- Carry over the leftover: `leftover = amount - (self.level_up - self.xp)`
- Increment level: `self.level += 1`
- Set `self.xp = leftover`
- Recalculate: `self.level_up = self.level * 150`

Test it: `m = Monster('Sparchu', 5); m.update_xp(1000); print(m.level)` — should be 6 (since 5 * 150 = 750 < 1000).

### Step 2 — Build `apply_attack()` in `battle.py`

The animation and sound are already handled. You need to add the damage calculation. Follow the comments in the file:

**Get elements**:
```python
attack_element = ATTACK_DATA[attack]['element']
target_element = target_sprite.monster.element
```

**Type effectiveness** (add these if/elif checks):
```python
if attack_element == 'fire' and target_element == 'plant':
    amount *= 2
# ... (repeat pattern for the other 2 strengths and 3 weaknesses)
```

**Defense reduction**:
```python
target_defense = 1 - target_sprite.monster.get_stat('defense') / 2000
if target_sprite.monster.defending:
    target_defense -= 0.2
target_defense = max(0, min(1, target_defense))
```

**Apply damage**:
```python
target_sprite.monster.health -= amount * target_defense
```

### Step 3 — Build `check_death()` in `battle.py`

Loop all sprites in both groups. If health <= 0, figure out the replacement.

**For player monsters**:
```python
active_monsters = [(s.index, s.monster) for s in self.player_sprites.sprites()]
available = [(i, m) for i, m in self.monster_data['player'].items()
             if m.health > 0 and (i, m) not in active_monsters]
new_monster_data = (available[0][1], available[0][0], monster_sprite.pos_index, 'player') if available else None
```

**For opponent monsters**:
```python
new_monster_data = (list(self.monster_data['opponent'].values())[0],
                    monster_sprite.index, monster_sprite.pos_index, 'opponent') if self.monster_data['opponent'] else None
if self.monster_data['opponent']:
    del self.monster_data['opponent'][min(self.monster_data['opponent'])]
# Award XP
xp_amount = monster_sprite.monster.level * 100 / len(self.player_sprites)
for player_sprite in self.player_sprites:
    player_sprite.monster.update_xp(xp_amount)
```

Then: `monster_sprite.delayed_kill(new_monster_data)`

### Step 4 — Build `check_end_battle()` in `battle.py`

Two conditions:

**Win**: `len(self.opponent_sprites) == 0 and not self.battle_over`
```python
self.battle_over = True
self.end_battle(self.character)
for monster in self.monster_data['player'].values():
    monster.initiative = 0
```

**Lose**: `len(self.player_sprites) == 0`
```python
pygame.quit()
exit()
```

---

## Testing

1. Fight a trainer — your attacks should deal real damage (watch the red health bar shrink!)
2. Keep attacking — when health hits 0, the monster should have a faint animation and a new one appears
3. Defeat all opponent monsters — the battle should end and return to the overworld
4. Type test: use a fire attack on a plant monster — the damage should be noticeably higher than a normal attack
5. Open the monster index (Enter key) after a battle — check that your monsters gained XP

---

## What you should see when done

The full battle loop works:
- Attacks deal damage based on type matchups
- Monsters faint and replacements come in
- XP is awarded for defeating opponents
- Winning returns you to the overworld with the trainer defeated
- Losing exits the game (game over)

---

## Extension ideas
- Implement the SWITCH action in `input()` — let the player swap monsters mid-battle
- Implement the DEFEND action (hint: it's already tracked with `monster.defending`!)
- Catch action: when opponent health is low, add it to your team instead of defeating it
- Make the loss screen nicer: instead of quitting, show a "YOU LOST" message before exiting
- Level up message: when a monster levels up from XP, display a short notification
