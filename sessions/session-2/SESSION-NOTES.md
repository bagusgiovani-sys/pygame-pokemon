# Session 2 — Player Movement Playground with Temporary Map

## Big idea
Session 2 is **not** the real Tiled/TMX map yet. That comes in Session 3.

In this updated Session 2, students build a **temporary practice map** so movement creativity is visible and meaningful:

- camera follows the player
- visible floor tiles
- visible border walls
- visible speed-test track
- visible flags / landmarks
- visible collision obstacle course
- HUD showing current speed
- optional creativity: WASD, sprint, sneak, dash, extra rocks, danger zone

This fixes the old issue where the border was invisible and the camera made speed changes feel unclear.

---

## Expected outcome by the end
Students should have:

1. A player sprite loaded from `graphics/characters/player.png`
2. A scrolling temporary map bigger than the window
3. A camera that follows the player
4. Visible border walls that block the player
5. A speed-test track with START / MID / FINISH markers
6. A HUD showing current speed
7. Working player movement with collision
8. At least one creative movement feature such as WASD, sprint, sneak, or dash

---

## Files for this session

| File | What students do |
|---|---|
| `timer.py` | Steps 1-4: build the Timer class |
| `entities.py` | Steps 5-10: animation, player input, movement, collision, update |
| `sprites.py` | Steps 11-12: basic visible sprites and collidable sprites |
| `main.py` | Steps 13-14: build temporary map, create player, draw HUD |
| `settings.py` | Pre-scaffold, no edits needed |
| `support.py` | Pre-scaffold, no edits needed |
| `groups.py` | Pre-scaffold camera system, no edits needed |

---

## How to run

From the project root:

```bash
cd "Python-Monsters/sessions/session-2"
c:/python313/python.exe main.py
```

Or if Python is already in PATH:

```bash
python main.py
```

Important: run the command **from inside `sessions/session-2`** because the asset paths use `..`, `..` to reach the main `graphics` folder.

---

# Teaching flow

## Step 1-4 — `timer.py`

### Step 1 — `Timer.__init__`

```python
def __init__(self, duration, repeat=False, autostart=False, func=None):
    self.duration = duration
    self.start_time = 0
    self.active = False
    self.repeat = repeat
    self.func = func
    if autostart:
        self.activate()
```

### Step 2 — `activate()`

```python
def activate(self):
    self.active = True
    self.start_time = get_ticks()
```

### Step 3 — `deactivate()`

```python
def deactivate(self):
    self.active = False
    self.start_time = 0
    if self.repeat:
        self.activate()
```

### Step 4 — `update()`

```python
def update(self):
    if self.active:
        current_time = get_ticks()
        if current_time - self.start_time >= self.duration:
            if self.func:
                self.func()
            self.deactivate()
```

---

## Step 5-10 — `entities.py`

## Step 5 — `Entity.animate(dt)`

```python
def animate(self, dt):
    state = self.get_state()
    self.frame_index += ANIMATION_SPEED * dt
    self.image = self.frames[state][int(self.frame_index % len(self.frames[state]))]
```

Teacher explanation:

> The player sprite sheet has walking animation frames. `frame_index` moves through the list. `%` loops the animation back to the start.

---

## Step 6 — `Player.__init__`

```python
def __init__(self, pos, frames, groups, facing_direction, collision_sprites):
    super().__init__(pos, frames, groups, facing_direction)
    self.collision_sprites = collision_sprites
    self.noticed = False
```

Teacher explanation:

> `super()` gives the player image, rect, hitbox, direction, speed, and animation state from `Entity`.

---

## Step 7 — `Player.input()` basic version

```python
def input(self):
    keys = pygame.key.get_pressed()
    input_vector = vector()

    if keys[pygame.K_UP]:
        input_vector.y -= 1
    if keys[pygame.K_DOWN]:
        input_vector.y += 1
    if keys[pygame.K_LEFT]:
        input_vector.x -= 1
    if keys[pygame.K_RIGHT]:
        input_vector.x += 1

    self.speed = 250
    self.direction = input_vector.normalize() if input_vector else input_vector
```

Teacher explanation:

> Keyboard input becomes direction. Direction becomes movement. `normalize()` prevents diagonal movement from being faster.

---

## Step 7 Extension — creativity controls

After basic movement works, students can upgrade `Player.input()`.

### WASD controls

```python
if keys[pygame.K_w]:
    input_vector.y -= 1
if keys[pygame.K_s]:
    input_vector.y += 1
if keys[pygame.K_a]:
    input_vector.x -= 1
if keys[pygame.K_d]:
    input_vector.x += 1
```

### Sprint / sneak / dash

Replace `self.speed = 250` with:

```python
if keys[pygame.K_SPACE]:
    self.speed = 700      # dash
elif keys[pygame.K_LSHIFT]:
    self.speed = 450      # sprint
elif keys[pygame.K_LCTRL]:
    self.speed = 120      # sneak
else:
    self.speed = 250      # normal walk
```

Student challenge:

> Test each speed on the speed-test track. Which one feels balanced? Which one is too fast?

---

## Step 8 — `Player.move(dt)`

```python
def move(self, dt):
    self.rect.centerx += self.direction.x * self.speed * dt
    self.hitbox.centerx = self.rect.centerx
    self.collisions('horizontal')

    self.rect.centery += self.direction.y * self.speed * dt
    self.hitbox.centery = self.rect.centery
    self.collisions('vertical')
```

Teacher explanation:

> We move x first, then y. This makes wall collision cleaner.

---

## Step 9 — `Player.collisions(axis)`

```python
def collisions(self, axis):
    for sprite in self.collision_sprites:
        if sprite.hitbox.colliderect(self.hitbox):

            if axis == 'horizontal':
                if self.direction.x > 0:
                    self.hitbox.right = sprite.hitbox.left
                if self.direction.x < 0:
                    self.hitbox.left = sprite.hitbox.right
                self.rect.centerx = self.hitbox.centerx

            else:
                if self.direction.y > 0:
                    self.hitbox.bottom = sprite.hitbox.top
                if self.direction.y < 0:
                    self.hitbox.top = sprite.hitbox.bottom
                self.rect.centery = self.hitbox.centery
```

Teacher explanation:

> If the player overlaps a wall, we push the player back to the edge of the wall.

---

## Step 10 — `Player.update(dt)`

```python
def update(self, dt):
    if not self.blocked:
        self.input()
        self.move(dt)

    self.animate(dt)
    self.y_sort = self.rect.centery
```

Teacher explanation:

> Every frame, the player checks input, moves, animates, and updates draw order.

---

# Step 11-12 — `sprites.py`

## Step 11 — `Sprite.__init__`

```python
def __init__(self, pos, surf, groups, z=WORLD_LAYERS['main']):
    super().__init__(groups)
    self.image = surf
    self.rect = self.image.get_frect(topleft=pos)
    self.hitbox = self.rect.copy()
    self.z = z
    self.y_sort = self.rect.centery
```

---

## Step 12 — `CollidableSprite.__init__`

```python
def __init__(self, pos, surf, groups, z=WORLD_LAYERS['main']):
    super().__init__(groups)
    self.image = surf
    self.rect = self.image.get_frect(topleft=pos)
    self.hitbox = self.rect.inflate(-10, -10)
    self.z = z
    self.y_sort = self.rect.centery
```

Teacher explanation:

> `CollidableSprite` is visible and solid. This is why the Session 2 walls are no longer invisible.

---

# Step 13-14 — `main.py`

## Step 13 — `create_temporary_map()`

### 13a — Floor tiles

```python
for x in range(0, self.map_width, TILE_SIZE):
    for y in range(0, self.map_height, TILE_SIZE):
        color = '#2f4032' if (x // TILE_SIZE + y // TILE_SIZE) % 2 == 0 else '#344a36'
        floor_surf = self.make_surface((TILE_SIZE, TILE_SIZE), color)
        Sprite(
            pos=(x, y),
            surf=floor_surf,
            groups=self.all_sprites,
            z=WORLD_LAYERS['bg'],
        )
```

### 13b — Visible border walls

```python
wall = '#7a7a7a'
wall_thickness = 64

walls = [
    ((0, 0), (self.map_width, wall_thickness)),
    ((0, self.map_height - wall_thickness), (self.map_width, wall_thickness)),
    ((0, 0), (wall_thickness, self.map_height)),
    ((self.map_width - wall_thickness, 0), (wall_thickness, self.map_height)),
]

for pos, size in walls:
    wall_surf = self.make_surface(size, wall)
    CollidableSprite(
        pos=pos,
        surf=wall_surf,
        groups=(self.all_sprites, self.collision_sprites),
    )
```

### 13c — Speed-test track

```python
path_color = '#5b4b36'
for x in range(128, 1900, TILE_SIZE):
    path_surf = self.make_surface((TILE_SIZE, TILE_SIZE), path_color)
    Sprite((x, 320), path_surf, self.all_sprites, WORLD_LAYERS['bg'])
    Sprite((x, 384), path_surf, self.all_sprites, WORLD_LAYERS['bg'])

self.make_text_sprite('SPEED TEST TRACK: compare walk / sprint / dash here', (180, 260), 'white')
self.make_text_sprite('START', (150, 450), 'white')
self.make_text_sprite('MID', (900, 450), 'white')
self.make_text_sprite('FINISH', (1700, 450), 'white')
```

### 13d — Landmark flags

```python
flag_positions = [(220, 250), (600, 250), (1000, 250), (1400, 250), (1800, 250)]
for index, pos in enumerate(flag_positions, start=1):
    flag_surf = self.make_surface((40, 90), COLORS['fire'] if index % 2 else COLORS['water'])
    Sprite(pos, flag_surf, self.all_sprites, WORLD_LAYERS['main'])
    self.make_text_sprite(f'Flag {index}', (pos[0] - 8, pos[1] - 28), 'white')
```

### 13e — Obstacle course

```python
rock_color = '#575757'
rock_positions = [
    (500, 650), (600, 650), (700, 650),
    (700, 750), (700, 850),
    (1000, 760), (1100, 760), (1200, 760), (1300, 760),
    (1300, 860), (1300, 960),
]

for pos in rock_positions:
    rock_surf = self.make_surface((70, 70), rock_color)
    CollidableSprite(pos, rock_surf, (self.all_sprites, self.collision_sprites))

self.make_text_sprite('OBSTACLE COURSE: test collision here', (470, 590), 'white')
```

### 13f — Decorative zones

```python
base_surf = self.make_surface((320, 200), COLORS['plant'])
Sprite((280, 1050), base_surf, self.all_sprites, WORLD_LAYERS['bg'])
self.make_text_sprite('TRAINER BASE', (360, 1120), 'white')

water_surf = self.make_surface((360, 220), COLORS['water'])
Sprite((1500, 980), water_surf, self.all_sprites, WORLD_LAYERS['bg'])
self.make_text_sprite('WATER AREA', (1600, 1070), 'white')
```

---

## Step 14 — `setup()`

```python
def setup(self):
    self.create_temporary_map()

    self.player = Player(
        pos=(180, 380),
        frames=self.overworld_frames['characters']['player'],
        groups=self.all_sprites,
        facing_direction='down',
        collision_sprites=self.collision_sprites,
    )
```

---

# What students should see

When complete, students should see:

- a scrolling green temporary map
- grey border walls
- a brown speed-test track
- START / MID / FINISH labels
- red/blue flags along the track
- grey obstacle blocks
- a speed HUD at the top-left
- a player sprite that moves and animates
- collision with rocks and walls

---

# Creativity tasks

## Must-have creativity
Each student should activate at least one:

1. WASD controls
2. Sprint with Shift
3. Sneak with Ctrl
4. Dash with Space

## Optional map creativity
Students can also customize:

1. Add more rocks
2. Add a danger zone
3. Change track color
4. Move the flags
5. Change the map size
6. Add a new landmark area

---

# Teacher framing

Use this line:

> Today we are not building the final world map yet. We are building a movement playground to test how our trainer feels. Game developers do this before building the real map.

Student showcase prompt:

> Show your trainer movement style. What speed did you choose? Is your trainer a runner, ninja, explorer, or heavy trainer?

---

# Teacher answer key

The complete runnable answer files are in:

```text
session-2/answer_key/
```

Use them as reference. The student-facing files in the main `session-2` folder intentionally contain `TODO` and `pass`.
