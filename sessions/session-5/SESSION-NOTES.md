# Session 5 — Polish and Make It Yours

## Goal
Add music and sound effects, trigger the evolution animation, and design your own custom monster. By the end of today, you have a complete, polished game — and it has a piece of you in it.

## What you are building today
- `game_data.py` — add your own custom monster
- `main.py` — wire up real audio and the evolution system

## Key concepts
- **Audio in Pygame**: loading sound files, playing music loops, stopping sounds
- **Game feel**: how sound and animation make a game feel alive
- **Extending a codebase**: adding new features to a working system without breaking it
- **Evolution as reward**: triggering a special moment that celebrates the player's progress

---

## Why does sound matter so much?

Try this: watch any video game footage with sound, then watch the same clip on mute. The game feels completely dead without audio. Sound tells the player "your attack landed", "danger is coming", "you did it!". It communicates information AND emotion simultaneously.

Even simple games feel professional with good sound design. Adding music loops and hit sounds today will make your game feel like a real game — not just a coding exercise.

---

## Step-by-step

### Step 1 — Add your custom monster in `game_data.py`

Find the YOUR CODE placeholder at the end of `MONSTER_DATA`. Replace `'YourMonsterName'` with something creative!

**Design tips:**
- Give it a theme: lava creature? crystal insect? storm cloud?
- Match stats to its theme: a fast, fragile creature has high speed + low health; a rock creature has high defense + low speed
- Pick a type that fits: fire is aggressive, water is balanced, plant is defensive/supportive

**Stat guide:**
| Role | health | attack | defense | speed |
|------|--------|--------|---------|-------|
| Glass cannon | 10-14 | 5-6 | 5-7 | 2.5-3.0 |
| Tank | 25-30 | 2-3 | 13-15 | 1.0-1.2 |
| Balanced | 16-20 | 3-4 | 9-11 | 1.5-1.8 |

**Abilities**: stick to existing ones — `scratch`, `fire`, `spark`, `splash`, `ice`, `heal`, `explosion`, `battlecry`

After you are done: add your monster to `self.player_monsters` in `main.py` so it appears in your team!

### Step 2 — Add audio in `import_assets()`

Find the TODO comments in `import_assets()`. The temporary silent audio dict is there so the game doesn't crash before you replace it. Once you add real audio:

1. Delete or comment out the `SilentSound` block (lines starting with `self.audio = {}`)
2. Add these two lines:
```python
self.audio = audio_importer('..', '..', 'audio')
self.start_animation_frames = import_folder('..', '..', 'graphics', 'other', 'star animation')
```

The game will now have real music and sound effects!

### Step 3 — Add `from evolution import Evolution` import

At the top of `main.py`, find the YOUR CODE Step 3 comment. Uncomment the import line.

Then in `__init__`, find the other Step 3 comment and add `self.evolution = None`.

### Step 4 — Build `check_evolution()` in `main.py`

This is called after every battle ends. It checks if any monster in your team earned enough levels to evolve.

The logic (from the commented-out hints):
1. Loop through `self.player_monsters.items()`
2. If a monster has an evolution (`monster.evolution` is not None) AND its current level matches the required evolution level (`monster.level == monster.evolution[1]`):
   - Play the evolution sound: `self.audio['evolution'].play()`
   - Block the player: `self.player.block()`
   - Create the Evolution overlay and store it: `self.evolution = Evolution(...)`
   - Replace the monster in the dict with the evolved form: `self.player_monsters[index] = Monster(monster.evolution[0], monster.level)`
3. If NO evolution happened: restart overworld music

**Evolution constructor arguments:**
```python
Evolution(
    self.monster_frames['monsters'],  # all monster animation frames
    monster.name,                      # which monster is evolving FROM
    monster.evolution[0],              # which monster it becomes
    self.fonts['bold'],                # font for the text
    self.end_evolution,                # callback when animation finishes
    self.start_animation_frames)       # the star particles
```

### Step 5 — Build `end_evolution()` in `main.py`

Called when the evolution animation finishes. Four lines:
```python
self.evolution = None
self.player.unblock()
self.audio['evolution'].stop()
self.audio['overworld'].play(-1)
```

---

## Testing

1. Run the game — you should hear the overworld music!
2. Walk into tall grass — the music should switch to battle music
3. Win a battle — music should switch back to overworld
4. Level up Sparchu to level 15 (fight a few battles) — the evolution animation should trigger!
5. Open the monster index (Enter key) — check that your custom monster appears in the team

**Testing evolution quickly**: In `__init__`, temporarily set `Monster('Sparchu', 14)` with `monster.xp += 2000` — it will level up on the first battle and trigger evolution.

---

## What you see when done

You have built a complete game:
- Overworld with animated maps and characters
- Dialog system with trainers that challenge you
- Battle system with initiative turns, type matchups, and faint/replace logic
- XP and leveling system
- Evolution animation
- Full audio with music and sound effects
- Your own custom monster in the game world

---

## You built this! What's next?

Here are some ideas for where you could take this further:

### Battle polish
- Implement a SWITCH action so you can swap your active monster mid-battle instead of waiting for it to faint
- Implement a CATCH action to capture wild monsters instead of always defeating them
- Add a level-up notification in battle ("Sparchu grew to level 16!")
- Smarter AI: use type advantages when picking attacks

### Game world
- Add a second custom monster (maybe an evolution of your first?)
- Add dialog after winning a battle
- Add a "you lose" screen instead of just quitting

### Sound and feel
- Add a battle win fanfare sound
- Add a footstep sound when walking
- Make the screen flash white when a monster faints

You understand every function in this codebase. You could add any of these features yourself — and now you know how.
