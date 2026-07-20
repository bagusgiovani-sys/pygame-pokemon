import utils.transport
import utils.session
import pygame
from sys import exit
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, COLORS

# ┌─────────────────────────────────────────────────────────┐
# │ PRE-SCAFFOLD — teacher walks through this, you use it   │
# │                                                         │
# │ We put all our game code inside a class called Game.    │
# │ __init__ sets everything up once at the start.          │
# │ run() is the loop that keeps going until you close it.  │
# └─────────────────────────────────────────────────────────┘


class Game:

    def __init__(self):
        # ┌─────────────────────────────────────────────────────────┐
        # │ YOUR CODE — Step 2: Initialise pygame                   │
        # │ You need four lines:                                     │
        # │   1. pygame.init()  — starts all pygame modules         │
        # │   2. pygame.display.set_mode(...)  — creates the window  │
        # │      pass (WINDOW_WIDTH, WINDOW_HEIGHT) as the size     │
        # │      store the result as self.display_surface           │
        # │   3. pygame.display.set_caption('Monster Game')         │
        # │   4. self.clock = pygame.time.Clock()                   │
        # │ Hint: use WINDOW_WIDTH and WINDOW_HEIGHT from settings. │
        # └─────────────────────────────────────────────────────────┘
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pokemon Game")
        self.clock = pygame.time.Clock()

        # ┌─────────────────────────────────────────────────────────┐
        # │ PRE-SCAFFOLD — teacher walks through this, you use it   │
        # │                                                         │
        # │ A placeholder(temporary) player rectangle.                         │
        # │ We'll replace this with a real animated sprite          │
        # │ in session 2, once we learn about sprite classes.       │
        # └─────────────────────────────────────────────────────────┘
        self.player_surf = pygame.Surface((48, 64))
        self.player_surf.fill(COLORS["plant"])
        self.player_rect = self.player_surf.get_frect(
            center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        )

    def run(self):
        # ┌─────────────────────────────────────────────────────────┐
        # │ YOUR CODE — Step 3: The game loop                       │
        # │ Write a while True: loop that does these things:        │
        # │   1. dt = self.clock.tick() / 1000                      │
        # │      (tick() gives milliseconds; divide by 1000         │
        # │       to get seconds — this is called "delta time")     │
        # │   2. An event loop:                                      │
        # │        for event in pygame.event.get():                 │
        # │            if event.type == pygame.QUIT:                │
        # │                pygame.quit()                            │
        # │                exit()                                   │
        # │   3. self.display_surface.fill('black')                 │
        # │   4. self.display_surface.blit(                         │
        # │          self.player_surf, self.player_rect)            │
        # │   5. pygame.display.update()                            │
        # │ Hint: dt divides by 1000 to convert ms → seconds.      │
        # │       We'll use dt in session 2 to move the player.     │
        # └─────────────────────────────────────────────────────────┘
        while True:
            dt = self.clock.tick() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # update all of the sprites to
            self.all_sprites.update(dt)

            # screen re-draw
            self.display_surface.fill(COLORS["dark"])
            self.all_sprites.draw(self.player)

            pygame.display.update()

            # Hz = screen refresh rate 30 Hz = 60 FPS >>> we end up getting 30 FPS eventually


# ┌─────────────────────────────────────────────────────────┐
# │ PRE-SCAFFOLD — teacher walks through this, you use it   │
# │                                                         │
# │ This block only runs when you execute this file         │
# │ directly (not when another file imports it).            │
# └─────────────────────────────────────────────────────────┘
if __name__ == "__main__":
    game = Game()
    game.run()

# ┌─────────────────────────────────────────────────────────┐
# │ EXTENSION — bonus challenge!                            │
# │ Ideas: Change the player color using a different        │
# │        COLORS key (try 'fire' or 'water'),              │
# │        Add a text label with pygame.font.Font and       │
# │        font.render() drawn above the rectangle,         │
# │        Make the rectangle move with arrow keys.         │
# └─────────────────────────────────────────────────────────┘
