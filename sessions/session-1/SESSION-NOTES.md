# Session 1 — "Getting the Window Open"

## Goal
By the end of this session students will have a working Pygame window with a coloured rectangle in the centre that they can close cleanly. This is the foundation every other session builds on.

---

## Files you are working on today
| File | What you do |
|---|---|
| `settings.py` | Step 1 — fill in the four game constants |
| `main.py` | Step 2 — initialise pygame; Step 3 — write the game loop |
| `timer.py` | Read only — you build this yourself in session 2 |
| `support.py` | Read only — will grow in later sessions |

---

## How to run the game
Open a terminal, navigate to this folder, then run:

```
cd sessions\session-1
python main.py
```

A 1280×720 window should open showing a green rectangle in the centre. Close it by clicking the X button.

---

## Step-by-step instructions

### Step 1 — settings.py
Open `settings.py`. Find the four lines that say `???` and replace each one:

```python
WINDOW_WIDTH  = 1280
WINDOW_HEIGHT = 720
TILE_SIZE     = 64
ANIMATION_SPEED = 6
```

Save the file. You won't see anything different yet — these are just numbers we'll use in `main.py`.

---

### Step 2 — main.py `__init__`
Open `main.py`. Inside `__init__`, replace the `pass` with:

```python
pygame.init()
self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Monster Game')
self.clock = pygame.time.Clock()
```

**What each line does:**
- `pygame.init()` — starts all of Pygame's internal systems (fonts, sounds, display, etc.). You must call this before anything else.
- `set_mode(...)` — asks the OS to open a window of the given size. The return value is a Surface that represents the whole screen. We store it as `self.display_surface`.
- `set_caption(...)` — sets the window title bar text.
- `Clock()` — a timer object we'll use to control frame rate and measure delta time.

---

### Step 3 — main.py `run()`
Inside `run()`, replace the `pass` with:

```python
while True:
    dt = self.clock.tick() / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    self.display_surface.fill('black')
    self.display_surface.blit(self.player_surf, self.player_rect)
    pygame.display.update()
```

---

## Key concepts explained

### What is a game loop?
A game loop is a `while True:` loop that runs once per frame. Each time around the loop the game:
1. Checks for input (keyboard, mouse, window close)
2. Updates the game state (move things, check collisions)
3. Draws everything to the screen

This happens 60+ times per second — so fast the player sees smooth motion.

### What is delta time (dt)?
`clock.tick()` returns how many **milliseconds** passed since the last frame. We divide by 1000 to get **seconds**.

Why does this matter? If the game runs at 30fps on a slow PC and 120fps on a fast one, moving a character by `5 pixels per frame` would make them move at different speeds on each machine. Moving by `300 * dt` (pixels per second) means the same distance regardless of frame rate.

### Why `pygame.init()`?
Pygame is split into sub-modules: display, font, sound, joystick, etc. `pygame.init()` starts all of them at once. Without it, most functions will crash with confusing errors.

### What is `blit`?
`blit` means "draw this surface onto that surface at this position". Think of it like stamping one image onto another. We blit the green rectangle (`player_surf`) onto the screen (`display_surface`).

### Why `pygame.display.update()`?
Pygame draws everything to an invisible back-buffer first. `update()` flips that buffer to the screen all at once, which prevents flickering.

---

## What you should see when done
- A 1280×720 black window opens instantly
- A green rectangle appears in the exact centre of the window
- Clicking the X button closes the window cleanly (no crash)

---

## Extension challenges

1. **Change the colour** — In `main.py`, change `COLORS['plant']` to `COLORS['fire']` or any other key from the COLORS dict in `settings.py`.

2. **Add a text label** — After the `blit` call, add:
   ```python
   font = pygame.font.Font(None, 48)
   text = font.render('Hello!', True, 'white')
   self.display_surface.blit(text, (100, 100))
   ```

3. **Move the rectangle** — Make the rectangle move right a little each frame by adding `self.player_rect.x += 1` inside the loop (before the blit). What happens when it goes off screen?

4. **Change the window size** — Try setting `WINDOW_WIDTH = 800` and `WINDOW_HEIGHT = 600` in settings.py. Does everything still work?
