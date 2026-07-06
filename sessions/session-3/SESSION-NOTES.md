# Session 3 — "Building the Map"

## Goal
By the end of this session students will have a scrolling tile-based world loaded from a real TMX map file. Water and coast tiles animate. The player can walk between areas using transition zones. NPCs can be talked to using SPACE.

---

## Files you are working on today
| File | What you do |
|---|---|
| `sprites.py` | Steps 14-16 — AnimatedSprite, MonsterPatchSprite, TransitionSprite |
| `main.py` | Step 17 — setup() reads the TMX map; Step 18 — transition_check() |
| All other files | Already complete — no changes needed |

---

## How to run
```
cd sessions\session-3
python main.py
```

The world should load, the camera should follow the player, and water should animate. Walk to a doorway to transition to a new area.

---

## Step-by-step instructions

### Step 14 — sprites.py `AnimatedSprite`

```python
class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, z=WORLD_LAYERS['main']):
        self.frame_index = 0
        self.frames      = frames
        super().__init__(groups)
        self.image  = self.frames[0]
        self.rect   = self.image.get_frect(topleft=pos)
        self.z      = z
        self.hitbox = self.rect.copy()
        self.y_sort = self.rect.centery

    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]

    def update(self, dt):
        self.animate(dt)
```

---

### Step 15 — sprites.py `MonsterPatchSprite`

```python
class MonsterPatchSprite(AnimatedSprite):
    def __init__(self, pos, frames, groups, biome, monsters, level):
        z = WORLD_LAYERS['main'] if biome != 'sand' else WORLD_LAYERS['bg']
        super().__init__(pos, frames, groups, z)
        self.y_sort  -= 40
        self.biome    = biome
        self.monsters = monsters.split(',')
        self.level    = level
```

Note: the `frames` parameter here is the tile image from Tiled (passed as a single Surface). For the AnimatedSprite base class to work it needs a list. The MonsterPatchSprite in the real game passes a list of frames — if your Tiled layer gives a single surface, wrap it: `[obj.image]`.

---

### Step 16 — sprites.py `TransitionSprite`

```python
class TransitionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, size, target, groups):
        super().__init__(groups)
        surf         = pygame.Surface(size)
        self.image   = surf
        self.rect    = self.image.get_frect(topleft=pos)
        self.target  = target
        self.hitbox  = self.rect.copy()
        self.z       = WORLD_LAYERS['bg']
        self.y_sort  = self.rect.centery
```

---

### Step 17 — main.py `setup()`

Work through each sub-step in the scaffolded skeleton. Here are the complete solutions:

**17a — Clear groups:**
```python
for group in (self.all_sprites, self.collision_sprites,
              self.transition_sprites, self.character_sprites):
    group.empty()
```

**17b — Terrain tiles:**
```python
for layer in ['Terrain', 'Terrain Top']:
    for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
        Sprite((x * TILE_SIZE, y * TILE_SIZE), surf,
               self.all_sprites, WORLD_LAYERS['bg'])
```

**17c — Water:**
```python
for obj in tmx_map.get_layer_by_name('Water'):
    for x in range(int(obj.x), int(obj.x + obj.width), TILE_SIZE):
        for y in range(int(obj.y), int(obj.y + obj.height), TILE_SIZE):
            AnimatedSprite((x, y), self.overworld_frames['water'],
                           self.all_sprites, WORLD_LAYERS['water'])
```

**17d — Coast:**
```python
for obj in tmx_map.get_layer_by_name('Coast'):
    terrain = obj.properties['terrain']
    side    = obj.properties['side']
    AnimatedSprite((obj.x, obj.y),
                   self.overworld_frames['coast'][terrain][side],
                   self.all_sprites, WORLD_LAYERS['bg'])
```

**17e — Objects:**
```python
for obj in tmx_map.get_layer_by_name('Objects'):
    if obj.name == 'top':
        Sprite((obj.x, obj.y), obj.image,
               self.all_sprites, WORLD_LAYERS['top'])
    else:
        CollidableSprite((obj.x, obj.y), obj.image,
                         (self.all_sprites, self.collision_sprites))
```

**17f — Transitions:**
```python
for obj in tmx_map.get_layer_by_name('Transition'):
    TransitionSprite(
        (obj.x, obj.y),
        (obj.width, obj.height),
        (obj.properties['target'], obj.properties['pos']),
        self.transition_sprites)
```

**17g — Collisions:**
```python
for obj in tmx_map.get_layer_by_name('Collisions'):
    BorderSprite((obj.x, obj.y),
                 pygame.Surface((obj.width, obj.height)),
                 self.collision_sprites)
```

**17h — Monster patches:**
```python
for obj in tmx_map.get_layer_by_name('Monsters'):
    MonsterPatchSprite(
        (obj.x, obj.y),
        obj.image,
        (self.all_sprites, self.monster_sprites),
        obj.properties['biome'],
        obj.properties['monsters'],
        obj.properties['level'])
```

**17i — Entities (two-pass approach):**
```python
# First pass: spawn the player
for obj in tmx_map.get_layer_by_name('Entities'):
    if obj.name == 'Player':
        if obj.properties['pos'] == player_start_pos:
            self.player = Player(
                pos=(obj.x, obj.y),
                frames=self.overworld_frames['characters']['player'],
                groups=self.all_sprites,
                facing_direction=obj.properties['direction'],
                collision_sprites=self.collision_sprites)

# Second pass: spawn NPCs (player must exist first)
for obj in tmx_map.get_layer_by_name('Entities'):
    if obj.name != 'Player':
        char_id = obj.properties['character_id']
        data = TRAINER_DATA.get(char_id, TRAINER_DATA['o1'])
        Character(
            pos=(obj.x, obj.y),
            frames=self.overworld_frames['characters'][obj.properties['graphic']],
            groups=(self.all_sprites, self.collision_sprites, self.character_sprites),
            facing_direction=obj.properties.get('direction', 'down'),
            character_data=data,
            player=self.player,
            create_dialog=self.create_dialog,
            collision_sprites=self.collision_sprites,
            radius=obj.properties.get('radius', 0),
            nurse=(char_id == 'Nurse'),
            notice_sound=pygame.mixer.Sound(
                join('..', '..', 'audio', 'notice.wav')))
```

Note: use `.get()` with defaults for `direction`/`radius` — the Nurse NPC in `hospital2.tmx` doesn't define either property, and a direct `['direction']` lookup crashes when that map loads.

---

### Step 18 — main.py `transition_check()`

```python
def transition_check(self):
    sprites = pygame.sprite.spritecollide(
        self.player, self.transition_sprites, False)
    if sprites:
        self.player.block()
        self.transition_target = sprites[0].target
        self.tint_mode = 'tint'
```

---

## Key concepts

### What is a camera?
The camera is an offset vector. Every sprite's position is drawn shifted by `offset`. When the player moves right, `offset.x` decreases, so all sprites slide left — giving the illusion the world is moving.

In `AllSprites.draw()`:
```python
self.offset.x = -(player.rect.centerx - WINDOW_WIDTH / 2)
```
This keeps the player locked at the screen centre.

### What is z-sorting?
In a top-down game, entities closer to the bottom of the screen should appear in front of entities higher up. We sort the main-layer sprites by `y_sort` (their feet position) before drawing. Higher y = drawn later = drawn on top.

### What is a TMX file?
TMX is the format used by the free map editor "Tiled". It stores tile layers (terrain, water), object layers (collision shapes, spawn points), and custom properties on each object. `pytmx` converts this into Python objects so we can loop over them.

### Why two passes for entities?
NPCs (Characters) need a reference to `self.player` when they're created. If we spawn NPCs and the player on the same pass, there's a risk `self.player` doesn't exist yet when the first NPC is created. By spawning the player first, we guarantee it exists for all NPCs.

### What is `spritecollide`?
`pygame.sprite.spritecollide(sprite, group, dokill)` returns a list of all sprites in `group` whose `rect` overlaps `sprite.rect`. If `dokill=True` it removes the colliding sprites. We use `False` so transition zones persist.

---

## What you should see when done
- The tile-based world loads with grass, paths, and buildings
- Water tiles animate (rippling effect)
- Coast edges animate around water boundaries
- The player walks around and collides with buildings and borders
- Walking through a doorway fades to black and loads a new area
- Press SPACE near an NPC to read their dialog; press SPACE again to advance

---

## Extension challenges

1. **Different starting room** — Change `'house'` to `'world'` in the `setup()` call in `__init__`. Explore what loads.

2. **Debug mode** — Add `print(obj.name, obj.properties)` inside the Entities loop. Look at the terminal output — what properties do NPCs have?

3. **Random water offset** — In `AnimatedSprite.__init__`, after storing `self.frame_index = 0`, change it to `self.frame_index = uniform(0, len(frames))` (import `uniform` from random). Do all water tiles still ripple in sync?

4. **Slow coast animation** — In `AnimatedSprite.animate()`, change `ANIMATION_SPEED` to `ANIMATION_SPEED * 0.5`. What does it look like?
