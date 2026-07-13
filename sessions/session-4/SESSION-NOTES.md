# Session 4 — Designing Your Creatures & Battling

## Goal
Build the `Monster` class, design your own monsters in `game_data.py`, and wire up a real turn-based battle system. By the end of today, you can walk into tall grass or challenge a trainer and fight an actual battle — attacks, damage, fainting, XP, and winning or losing.

## What you are building today
- `game_data.py` — the "database" of all monsters and attacks
- `monster.py` — the Python class that brings one monster to life
- `battle.py` — the turn-based battle system (menu, turn order, damage, win/lose)
- `main.py` — your player's team, plus triggering battles from NPCs and wild encounters

## Key concepts
- **Data-driven design**: storing game content in dictionaries instead of hard-coding it everywhere
- **Classes as data + behavior**: `Monster` holds data (health, stats) AND behavior (level up, take damage)
- **Stat scaling**: stats multiply by level — a level 10 monster is 10x stronger than level 1!
- **Turn order from a stat**: each monster's own speed decides how often it gets a turn — no dice rolls
- **Type effectiveness**: fire beats plant, water beats fire, plant beats water — a balanced triangle with no "best" type
- **Bench and auto-swap**: your team waits on the bench; when your active monster faints, the next one steps in automatically

---

## Why data-driven design?

Imagine you wanted to add a new monster. With hard-coded logic you would have to change the attack code, the UI code, the battle code... everywhere. With MONSTER_DATA, you just add one entry to the dictionary. The rest of the game reads from it automatically. This is how real games work — Minecraft, Pokemon, Stardew Valley all use data files like this.

---

## What's different from a "full" Pokémon-style battle

To keep this session focused, the battle system here only ever shows **one monster per side** at a time — no switching mid-battle, no catching wild monsters. When your active monster faints, your next living monster is sent in automatically. It's still a real, properly turn-based fight — attacks queue up based on speed, damage uses real type-effectiveness and defense math, and you can genuinely win or lose — just without the extra menu complexity. Switching and catching are listed as extension challenges if you want to add them yourself.

---

## Step-by-step

### Step 1 — Design your monsters in `game_data.py`
Find the `???` placeholders in `MONSTER_DATA`. You need to fill in two monsters.

Think about your monster's personality:
- Fast and fragile? High speed (2.0+), low defense (5-8)
- Slow and tanky? Low speed (1.0), high health (25+) and defense (12+)
- Magic-user? High energy (20+), lower physical attack

**Stat guide:**
| Stat | Low | Medium | High |
|------|-----|--------|------|
| max_health | 10 | 18 | 30 |
| max_energy | 5 | 15 | 25 |
| attack | 1 | 3 | 6 |
| defense | 5 | 10 | 15 |
| recovery | 1.0 | 1.5 | 2.5 |
| speed | 1.0 | 1.5 | 3.0 |

### Step 2 — Design your attacks in `game_data.py`
Fill in `spark` and `heal` in `ATTACK_DATA`:
- `spark`: fire attack, targets opponent, amount around 1.1, cost around 20
- `heal`: plant healing, targets player (yourself!), amount -1.2 (negative = healing!), cost 600

### Step 3 — Build `__init__` in `monster.py`
The `__init__` sets up a monster from a name and level. The hints tell you exactly what each line does. Key idea: `health = base_health * level` because stats scale with level!

### Step 4 — Build `get_stat(stat)`
One line! Multiply `self.base_stats[stat]` by `self.level`. That's it.

### Step 5 — Build `get_stats()`
Return a dictionary with 6 entries. Call `self.get_stat()` for each one. The keys should be: `'health'`, `'energy'`, `'attack'`, `'defense'`, `'speed'`, `'recovery'`.

### Step 6 — Build `get_abilities(include_all=True)`
Loop through `self.abilities.items()`. Each entry is `(min_level, ability_name)`. Keep it if `self.level >= min_level`. If `include_all=False`, also check that `ATTACK_DATA[ability]['cost'] < self.energy`.

Use a list comprehension — it fits in one line!

### Step 7 — Build `get_base_damage(attack)`
`return self.get_stat('attack') * ATTACK_DATA[attack]['amount']`

### Step 8 — Build `update_xp(amount)`
Two cases:
1. If `self.level_up - self.xp > amount`: just add the XP normally
2. Otherwise: level up! Add 1 to level. Carry over leftover XP. Recalculate `level_up = level * 150`.

### Step 9 — Build `stat_limiter()`
Use `max(0, min(value, max_value))` to clamp each stat. This stops health going below 0 or above the maximum.

### Step 10 — Create `self.player_monsters` in `main.py`
Find the Step 10 marker in `__init__`. Create a dictionary with 6-7 monsters using `Monster('Name', level)`. Then loop through and add random XP with `randint(0, monster.level * 100)`.

### Step 11 — Build `battle.py`'s setup: `__init__`, `setup()`, `create_monster()`
Three small, tightly-linked methods in `battle.py`:
- `__init__` creates the sprite groups and control variables, then calls `self.setup()`.
- `setup()` pulls the first monster off each side's bench (`monster_data`) and sends it into `create_monster()`.
- `create_monster()` builds all the on-screen pieces for one monster — the animated sprite, its outline, name tag, level badge, and stat bars — flipping the player's monster to face right.

### Step 12 — Build turn order: `check_active()`, `update_all_monsters()`
Every monster's `initiative` climbs each frame based on its speed (from `Monster.update()`, built back in Step 9's session). `check_active()` checks for any monster at 100+ initiative and gives it a turn — pausing everyone else with `update_all_monsters()` so only one monster acts at a time.

### Step 13 — Build `input()`
Reads the player's menu choices: Fight or Defend at the top level, then which attack once "Fight" is chosen. Confirming an attack calls `activate_attack()` on the current monster's sprite, which plays the animation and eventually calls back into `apply_attack()` (Step 15).

### Step 14 — Build `opponent_attack()`
The AI's turn. Picks a random ability the opponent's monster can currently afford and attacks with it — same target logic as the player's own attacks.

### Step 15 — Build `apply_attack()`
The actual damage formula: type effectiveness (2x or 0.5x depending on the fire/water/plant triangle), then a defense reduction based on the target's defense stat (and an extra reduction if it chose Defend), then subtract the result from health.

### Step 16 — Wire battles into `main.py`
Three methods work together:
- `end_dialog()` — if the NPC is the nurse, heal your team; if they're a trainer who hasn't been defeated, start a `Battle`; otherwise just end the conversation.
- `end_battle()` — called when a battle finishes. Marks a trainer defeated and shows their post-battle line, or (for a wild encounter) just returns you to walking around.
- `monster_encounter()` — checks if you're standing in tall grass and moving, and randomly starts a wild `Battle` against a team built from that patch's monster list.

---

## Testing your Monster class

After finishing `monster.py`, open a terminal in this folder and try:

```python
python
>>> from monster import Monster
>>> m = Monster('Sparchu', 5)
>>> print(m)
monster: Sparchu, lvl: 5
>>> print(m.get_stat('attack'))
15
>>> print(m.get_abilities())
['scratch', 'fire']
>>> m.update_xp(800)
>>> print(m.level)
# level_up was 5*150=750, so 800 XP pushes it to level 6
```

---

## What you should see when done

Run `main.py` — walk into tall grass or talk to a trainer who hasn't been defeated yet, and a real battle starts: choose Fight or Defend, pick an attack, watch health bars drop, and see monsters faint and your bench send in the next one. Win, and you return to the overworld with the trainer marked defeated (or just walking again, for a wild encounter). Lose your whole team, and the game ends.

If anything doesn't behave the way you expect, compare your files against the answer key in `finished/session-4/` (outside the `Python-Monsters` folder) — it's a complete, runnable version of everything in this session.

---

## Extension ideas
- Add `is_fainted()` that returns `True` if `self.health <= 0`
- Add `is_low_energy()` that returns `True` if energy is below 20% of max
- Design an evolved form for one of your monsters: add it to `MONSTER_DATA` and set `'evolve': ('EvolvedName', level)` on the base form
- Add a third custom monster — how about a water type?
- Implement a SWITCH action so you can swap your active monster mid-battle instead of waiting for it to faint
- Implement a CATCH action to capture wild monsters instead of always defeating them
