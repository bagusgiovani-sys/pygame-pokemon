# Session 4 — Designing Your Creatures

## Goal
Build the `Monster` class and design your own monsters in `game_data.py`. By the end of today, your game has a full team of creatures stored in memory, each with stats, abilities, and XP tracking.

## What you are building today
- `game_data.py` — the "database" of all monsters and attacks
- `monster.py` — the Python class that brings one monster to life
- `main.py` — updated to create your player's team at startup

## Key concepts
- **Data-driven design**: storing game content in dictionaries instead of hard-coding it everywhere
- **Classes as data + behavior**: `Monster` holds data (health, stats) AND behavior (level up, take damage)
- **Stat scaling**: stats multiply by level — a level 10 monster is 10x stronger than level 1!

---

## Why data-driven design?

Imagine you wanted to add a new monster. With hard-coded logic you would have to change the attack code, the UI code, the battle code... everywhere. With MONSTER_DATA, you just add one entry to the dictionary. The rest of the game reads from it automatically. This is how real games work — Minecraft, Pokemon, Stardew Valley all use data files like this.

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

Then fill in `spark` and `heal` in `ATTACK_DATA`:
- `spark`: fire attack, targets opponent, amount around 1.1, cost around 20
- `heal`: plant healing, targets player (yourself!), amount -1.2 (negative = healing!), cost 600

### Step 2 — Build `__init__` in `monster.py`
The `__init__` sets up a monster from a name and level. The hints tell you exactly what each line does. Key idea: `health = base_health * level` because stats scale with level!

### Step 3 — Build `get_stat(stat)`
One line! Multiply `self.base_stats[stat]` by `self.level`. That's it.

### Step 4 — Build `get_stats()`
Return a dictionary with 6 entries. Call `self.get_stat()` for each one. The keys should be: `'health'`, `'energy'`, `'attack'`, `'defense'`, `'speed'`, `'recovery'`.

### Step 5 — Build `get_abilities(include_all=True)`
Loop through `self.abilities.items()`. Each entry is `(min_level, ability_name)`. Keep it if `self.level >= min_level`. If `include_all=False`, also check that `ATTACK_DATA[ability]['cost'] < self.energy`.

Use a list comprehension — it fits in one line!

### Step 6 — Build `get_base_damage(attack)`
`return self.get_stat('attack') * ATTACK_DATA[attack]['amount']`

### Step 7 — Build `update_xp(amount)`
Two cases:
1. If `self.level_up - self.xp > amount`: just add the XP normally
2. Otherwise: level up! Add 1 to level. Carry over leftover XP. Recalculate `level_up = level * 150`.

### Step 8 — Build `stat_limiter()`
Use `max(0, min(value, max_value))` to clamp each stat. This stops health going below 0 or above the maximum.

### Step 9 — Create `self.player_monsters` in `main.py`
Find the Step 1 marker in `__init__`. Create a dictionary with 6-7 monsters using `Monster('Name', level)`. Then loop through and add random XP with `randint(0, monster.level * 100)`.

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
>>> m.update_xp(500)
>>> print(m.level)
# Should be 6 if 500 > 5*150!
```

---

## What you should see when done

Run `main.py` — the overworld runs the same as before. But now `self.player_monsters` exists in memory! In the next session you will wire up battles that use this team.

---

## Extension ideas
- Add `is_fainted()` that returns `True` if `self.health <= 0`
- Add `is_low_energy()` that returns `True` if energy is below 20% of max
- Design an evolved form for one of your monsters: add it to `MONSTER_DATA` and set `'evolve': ('EvolvedName', level)` on the base form
- Add a third custom monster — how about a water type?
