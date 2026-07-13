# Session 5 — Evolution: The Finale

## Goal
Wire up the evolution system so a monster that reaches the right level transforms into its stronger form, mid-game, with a real animated overlay. By the end of today your game is complete: designed monsters, real battles, and now evolution too.

## What's already done
Real audio (music, sound effects) and your custom monsters from session 4 are already wired up — there's nothing left to add there. This session is entirely about one new mechanic: evolution.

## What you are building today
- `main.py` — import and wire up the `Evolution` overlay, and two new methods: `check_evolution()` and `end_evolution()`

## Key concepts
- **Evolution as a reward moment**: a special animated overlay that plays when a monster's level matches its `evolve` threshold — celebrating progress the player earned over many battles
- **Overlays that block gameplay**: like `dialog_tree` and `battle`, `evolution` is a third overlay checked in `run()` — while it's active, the player stays blocked and the overworld pauses underneath it
- **Timers driving a sequence**: the `Evolution` class (already fully built for you in `evolution.py`) uses two `Timer`s back to back — one delay before the reveal starts, one before it ends — to pace the animation without you writing any of that logic

---

## Where evolution data already lives

Every monster in `MONSTER_DATA` already has an `'evolve'` field — either `None`, or a tuple like `('Cindrill', 15)` meaning "becomes Cindrill at level 15." You already saw this in session 4; today you make it actually *do* something.

**Important:** evolution only works between monsters that already have real artwork in `graphics/monsters/` — the custom monsters you designed in session 4 don't have art, so they can't evolve into (or be battled as) anything visual. `Sparchu → Cindrill` is a good one to test with, since both already exist in the game.

---

## Step-by-step

### Step 2a — Import `Evolution` in `main.py`
One line at the top of the file: `from evolution import Evolution`. Take a look at `evolution.py` first — it's a complete, pre-built class. You're wiring it in, not writing it.

### Step 2b — Add `self.evolution = None`
Right alongside `self.dialog_tree` and `self.battle` in `__init__` — this is the third overlay slot, storing the `Evolution` object while one is playing.

### Step 2c — Load the star animation frames
`import_assets()` needs one more line to load the sparkle particles the evolution screen plays: `self.start_animation_frames = import_folder('..', '..', 'graphics', 'other', 'star animation')`.

### Step 3 — Build `check_evolution()`
Called right after a wild battle ends (already wired up in `end_battle()` for you). Loop `self.player_monsters.items()`. For each monster: if it has an `evolve` value AND its current `level` matches that evolution's required level, that's the one — play the evolution sound, block the player, build the `Evolution` overlay, and swap that team slot for a brand-new `Monster` of the evolved species at the same level. Stop looking once you've found one (`break`) — only one evolution at a time. If nothing evolved, just restart the overworld music.

### Step 4 — Build `end_evolution()`
Called automatically by the `Evolution` overlay once its animation finishes. Four lines: clear `self.evolution`, unblock the player, stop the evolution sound, restart the overworld music.

---

## Testing quickly

The starting team includes `Sparchu` at exactly level 15 — its own evolution threshold (`('Cindrill', 15)`) — specifically so you can test this without grinding. Win your very first wild battle and evolution should trigger immediately.

```python
python
>>> from monster import Monster
>>> m = Monster('Sparchu', 15)
>>> print(m.evolution)
('Cindrill', 15)
>>> print(m.level == m.evolution[1])
True
```

---

## What you should see when done

Win a wild encounter (not a trainer battle — trainer wins show their defeat dialog instead) with a monster at its evolution level, and the screen darkens, your monster's silhouette flashes white, then reveals its new evolved form with stars and a name-change message, before returning control to you with the team permanently updated.

If anything doesn't behave the way you expect, compare your files against the answer key in `finished/session-5/` (outside the `Python-Monsters` folder).

---

## Extension ideas
- Give one of your own custom monsters from session 4 a "spirit evolution" — reuse an *existing* monster's name and art as its evolved form (thematically a stretch, but a great way to explore the data without needing new art)
- Add a second evolution stage — evolve `Cindrill` into `Charmadillo` too (the data's already there!) and watch a monster evolve twice across a long play session
- Show a small on-screen message the moment a monster is *one level away* from evolving
- Add a unique sound or extra star burst for evolutions specifically triggered by defeating a trainer, if you extend `check_evolution()` to run after trainer battles too
