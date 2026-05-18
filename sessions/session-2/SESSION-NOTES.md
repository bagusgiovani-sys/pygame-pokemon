# Session 2 — "Making the Player Walk"

## Goal
By the end of this session students will have a player sprite that walks in all four directions, animates correctly, and cannot leave the screen. They will also build the `Timer` class from scratch.

---

## Files you are working on today
| File | What you do |
|---|---|
| `timer.py` | Steps 1-4 — build the whole Timer class |
| `entities.py` | Steps 5-9 — animate(), Player.__init__, input, move, collisions |
| `sprites.py` | Steps 10-12 — Sprite, BorderSprite, CollidableSprite |
| `main.py` | Step 13 — setup() with player and walls |
| `settings.py` | Already complete — no changes needed |
| `support.py` | Already complete — no changes needed |
| `groups.py` | Already complete — no changes needed |

---

## How to run
```
cd sessions\session-2
python main.py
```

**Note:** Because `entities.py` imports from `timer.py`, finish `timer.py` first. Then do `entities.py`. Then `sprites.py`. Then `main.py`.

---

## Step-by-step instructions

### Step 1 — timer.py `__init__`
```python
def __init__(self, duration, repeat=False, autostart=False, func=None):
    self.duration   = duration
    self.start_time = 0
    self.active     = False
    self.repeat     = repeat
    self.func       = func
    if autostart:
        self.activate()
```

### Step 2 — timer.py `activate()`
```python
def activate(self):
    self.active     = True
    self.start_time = get_ticks()
```

### Step 3 — timer.py `deactivate()`
```python
def deactivate(self):
    self.active     = False
    self.start_time = 0
    if self.repeat:
        self.activate()
```

### Step 4 — timer.py `update()`
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

### Step 5 — entities.py `Entity.animate(dt)`
```python
def animate(self, dt):
    self.frame_index += ANIMATION_SPEED * dt
    state = self.get_state()
    self.image = self.frames[state][int(self.frame_index % len(self.frames[state]))]
```

---

### Step 6 — entities.py `Player.__init__`
```python
def __init__(self, pos, frames, groups, facing_direction, collision_sprites):
    super().__init__(pos, frames, groups, facing_direction)
    self.collision_sprites = collision_sprites
    self.noticed = False
```

### Step 7 — entities.py `Player.input()`
```python
def input(self):
    keys = pygame.key.get_pressed()
    input_vector = vector()
    if keys[pygame.K_UP]:    input_vector.y -= 1
    if keys[pygame.K_DOWN]:  input_vector.y += 1
    if keys[pygame.K_LEFT]:  input_vector.x -= 1
    if keys[pygame.K_RIGHT]: input_vector.x += 1
    self.direction = input_vector.normalize() if input_vector else input_vector
```

### Step 8 — entities.py `Player.move(dt)`
```python
def move(self, dt):
    self.rect.centerx += self.direction.x * self.speed * dt
    self.hitbox.centerx = self.rect.centerx
    self.collisions('horizontal')
    self.rect.centery += self.direction.y * self.speed * dt
    self.hitbox.centery = self.rect.centery
    self.collisions('vertical')
```

### Step 9 — entities.py `Player.collisions(axis)`
```python
def collisions(self, axis):
    for sprite in self.collision_sprites:
        if sprite.hitbox.colliderect(self.hitbox):
            if axis == 'horizontal':
                if self.direction.x > 0: self.hitbox.right = sprite.hitbox.left
                if self.direction.x < 0: self.hitbox.left  = sprite.hitbox.right
                self.rect.centerx = self.hitbox.centerx
            else:
                if self.direction.y > 0: self.hitbox.bottom = sprite.hitbox.top
                if self.direction.y < 0: self.hitbox.top    = sprite.hitbox.bottom
                self.rect.centery = self.hitbox.centery
```

---

### Step 10 — sprites.py `Sprite.__init__`
```python
def __init__(self, pos, surf, groups, z=WORLD_LAYERS['bg']):
    super().__init__(groups)
    self.image  = surf
    self.rect   = self.image.get_frect(topleft=pos)
    self.hitbox = self.rect.copy()
    self.y_sort = self.rect.centery
    self.z      = z
```

### Step 11 — sprites.py `BorderSprite.__init__`
```python
def __init__(self, pos, surf, groups):
    super().__init__(groups)
    self.image  = surf
    self.rect   = self.image.get_frect(topleft=pos)
    self.hitbox = self.rect.copy()
```

### Step 12 — sprites.py `CollidableSprite.__init__`
```python
def __init__(self, pos, surf, groups):
    super().__init__(groups)
    self.image  = surf
    self.rect   = self.image.get_frect(topleft=pos)
    self.hitbox = self.rect.inflate(-10, -10)
```

---

### Step 13 — main.py `setup()`
```python
def setup(self):
    self.player = Player(
        pos=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2),
        frames=self.overworld_frames['characters']['player'],
        groups=self.all_sprites,
        facing_direction='down',
        collision_sprites=self.collision_sprites
    )
    # top wall
    BorderSprite((0, 0), pygame.Surface((WINDOW_WIDTH, 20)), self.collision_sprites)
    # bottom wall
    BorderSprite((0, WINDOW_HEIGHT - 20), pygame.Surface((WINDOW_WIDTH, 20)), self.collision_sprites)
    # left wall
    BorderSprite((0, 0), pygame.Surface((20, WINDOW_HEIGHT)), self.collision_sprites)
    # right wall
    BorderSprite((WINDOW_WIDTH - 20, 0), pygame.Surface((20, WINDOW_HEIGHT)), self.collision_sprites)
```

---

## Key concepts

### Vectors
`Vector2` from pygame lets us store an x and y together. `vector(1, 0)` means "moving right". We can add vectors, scale them by speed, and normalise them — all in one line.

### `get_pressed()` vs `get_just_pressed()`
- `get_pressed()` — returns True every frame the key is held. Perfect for movement.
- `get_just_pressed()` — returns True only on the frame the key was pressed. Used for dialog, menu clicks, etc.

### Frame-rate-independent movement (delta time)
If we move `5 pixels per frame` and the game runs at 60fps we move 300px/s. On a slow PC at 30fps we'd move only 150px/s — the player would feel laggy.

Instead we move `speed * dt` pixels per frame. If dt=0.016s (60fps): 250 × 0.016 = 4px per frame. If dt=0.033s (30fps): 250 × 0.033 = 8px per frame. Same total distance per second regardless of frame rate.

### Why split movement into horizontal and vertical?
If we move both x and y at the same time and hit a corner, it's ambiguous which wall to push back from. By resolving horizontal first, then vertical, each collision is clean and the player slides along walls smoothly.

### The hitbox
The `hitbox` is smaller than the visible sprite. This is intentional — trees, buildings, and the player character all have visual space above their feet. The hitbox only covers the feet area so it feels natural to walk close to objects.

### `inflate()`
`rect.inflate(-10, -10)` shrinks the rect by 10px on each side (so 20px narrower total). `inflate(10, 10)` would expand it. Negative values shrink.

---

## What you should see when done
- The player sprite appears at the centre of a dark screen
- Arrow keys move the player in all four directions
- The walk animation plays while moving; idle animation plays when still
- The player cannot walk off any edge of the screen
- Diagonal movement feels the same speed as straight movement

---

## Extension challenges

1. **Add a sprint** — In `Player.input()`, check `keys[pygame.K_LSHIFT]`. If held, use `self.speed = 400`, otherwise `250`.

2. **Add an obstacle** — In `main.py setup()`, add a coloured square using `CollidableSprite`. Try adjusting the `inflate` values and feel the difference.

3. **Explain normalize()** — Remove the `if input_vector` check and always call `.normalize()`. What error do you get when no key is pressed? Why?

4. **Timer demo** — Add a `Timer(2000, func=lambda: print('2 seconds!'))` to `Game.__init__`, call `.activate()` in `__init__`, and call `.update()` every frame in `run()`. Does it print after 2 seconds?
