# Session 5 — Battle! Part 1: Taking Turns

## Goal
Build the `Battle` class so that battles start from trainer encounters and grass patches. By the end of today, you can walk into tall grass, fight a battle, select attacks, and see monsters taking turns.

## What you are building today
- `battle.py` — the core battle system (setup, turn order, input, AI)
- `main.py` — wire battles to trainer dialogs and grass encounters

## Key concepts
- **Game states**: the game switches between "overworld mode" and "battle mode"
- **Initiative system**: monsters fill up a bar based on their speed — faster monsters get turns sooner (instead of strict alternating turns like in classic Pokemon)
- **match/case**: Python's pattern matching — a cleaner way to write big if/elif chains
- **Sprite groups**: using different groups to separate player monsters from opponent monsters

---

## Why an initiative system instead of alternating turns?

In a simple RPG, you and the enemy just alternate turns — you go, they go, repeat. But that feels boring and predictable. With an initiative bar, a level-50 Gulfin (speed 2.0) will get its turn TWICE before a slow Charmadillo (speed 1.1) gets one turn. This makes speed a meaningful stat and battles feel dynamic.

Think of it like a racing game — monsters are constantly filling their bar, and whoever fills it first goes next.

---

## Step-by-step

### Step 1 — Build `__init__` in `battle.py`
You receive 8 parameters. Store them all. Then create:
- Three sprite groups: `BattleSprites()`, and two `pygame.sprite.Group()`
- Control variables: `current_monster`, `selection_mode`, `selected_attack`, `selection_side`, `battle_over`
- An `indexes` dict with 5 keys all set to 0
- A `timers` dict with one entry: `'opponent delay'`
- Then call `self.setup()`

### Step 2 — Build `setup()`
Loop through `self.monster_data` for both `'player'` and `'opponent'`. For each side, only process monsters with key <= 2 (first 3 slots). Call `create_monster()` for each. After placing the opponent monsters, delete their entries from `monster_data['opponent']` — they are now on-screen sprites.

### Step 3 — Build `create_monster()`
This function places one monster on screen with all its UI. The hints in the file walk you through it in order:
1. Set `monster.paused = False`
2. Get frames, flip horizontally if entity == 'player'
3. Pick position from `BATTLE_POSITIONS`
4. Pick groups based on entity
5. Create `MonsterSprite`, then `MonsterOutlineSprite`, name, level, stats sprites

### Step 4 — Build `check_active()`
Loop all player and opponent sprites. If any monster's initiative >= 100:
- Call `update_all_monsters('pause')` to freeze everything
- Reset that monster's initiative to 0
- Call `set_highlight(True)` to flash it
- Store it as `self.current_monster`
- If it's a player monster: set `selection_mode = 'general'`
- If it's an opponent: activate the `'opponent delay'` timer

### Step 5 — Build `update_all_monsters(option)`
One loop through all sprites in both groups. Set `monster.paused` based on the option.

### Step 6 — Build `input()` (fight + attacks modes first)
The structure is already there with the match/case. Focus on getting these working:

**K_DOWN and K_UP**: change the current index with wrapping (`% limiter`)

**K_SPACE in 'general' mode**:
- Index 0 (fight): switch to `'attacks'` mode
- Index 1 (defend): set `monster.defending = True`, resume all, clear `current_monster`
- Index 2 (switch): switch to `'switch'` mode (EXTENSION)
- Index 3 (catch): switch to `'target'` mode, set side to `'opponent'` (EXTENSION)

**K_SPACE in 'attacks' mode**:
- Get the selected ability name from `get_abilities(include_all=False)`
- Switch to `'target'` mode
- Set `selected_attack` to that ability
- Set `selection_side` from `ATTACK_DATA[attack]['target']`

**K_SPACE in 'target' mode**:
- Get the target sprite based on `selection_side`
- Call `current_monster.activate_attack(target_sprite, selected_attack)`
- Clear `selected_attack`, `current_monster`, `selection_mode` to None

**K_ESCAPE**: go back to `'general'` if in attacks, switch, or target mode

**Reset indexes** to 0 after any confirmed action.

### Step 7 — Build `opponent_attack()`
Pick a random ability using `choice(self.current_monster.monster.get_abilities())`. Check `ATTACK_DATA[ability]['target']` — if it's `'player'`, the AI attacks the player's own monster (wait, that doesn't make sense... unless the AI uses heal!). More commonly it attacks `player_sprites`. Use `choice()` to pick a random target sprite.

### Step 8 — Add `end_dialog` battle launching in `main.py`
Find the YOUR CODE Step 8 block. Replace the simple `unblock()` with the full logic:
1. If nurse: heal all monsters, unblock
2. If trainer not defeated: stop music, start battle music, create `Battle(...)`, set tint
3. If already defeated: just unblock

### Step 9 — Add `end_battle` in `main.py`
Stop battle music, set transition to `'level'`, set tint mode. If there's a character: mark defeated and show dialog. Otherwise: unblock player and restart overworld music.

### Step 10 — Add `monster_encounter` in `main.py`
Check if the player is touching a grass patch and moving. If so, create a Battle with random-level monsters from that patch.

---

## Testing

1. Run `main.py`
2. Walk into a trainer's line of sight — dialog should appear, then battle should start
3. In battle: press DOWN to cycle through choices, SPACE to select FIGHT
4. Select an attack with DOWN/SPACE
5. Select a target with SPACE — the attack animation should play!
6. Watch the opponent's bar fill up and their turn happen automatically

---

## What you should see when done

- Battles start from trainer encounters and grass patches
- Turn order is based on speed (watch the initiative bars at the bottom of each monster)
- You can select FIGHT → pick an attack → pick a target
- The opponent takes a turn automatically after a short delay
- The battle ends and returns to the overworld (even though damage isn't full yet — that's Session 6!)

---

## Extension ideas
- Implement the SWITCH action in `input()` — look at `draw_switch()` for how the menu works
- Implement the DEFEND action (it's actually quite simple — just set `monster.defending = True`)
- Add a "catch" action that calls `delayed_kill` on the opponent if it's low health
- Make the AI smarter: pick a healing move if health is below 50%
