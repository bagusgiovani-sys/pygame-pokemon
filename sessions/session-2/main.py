import pygame
from sys import exit
from os.path import join
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE, COLORS, WORLD_LAYERS
from support import all_character_import
from sprites import Sprite, BorderSprite, CollidableSprite, AnimatedSprite
from entities import Player
from groups import AllSprites

# ┌─────────────────────────────────────────────────────────┐
# │ PRE-SCAFFOLD — teacher walks through this, you use it   │
# │                                                         │
# │ main.py has grown since session 1. We now have:         │
# │   - import_assets() to load character frames            │
# │   - setup() to place the player and walls (you write)   │
# │   - Two sprite groups: all_sprites and collision_sprites │
# │                                                         │
# │ Compare this __init__ to session 1's — notice how       │
# │ import_assets() and setup() keep it tidy.               │
# └─────────────────────────────────────────────────────────┘

class Game:
	def __init__(self):
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		pygame.display.set_caption('Monster Game')
		self.clock = pygame.time.Clock()

		# sprite groups
		self.all_sprites       = AllSprites()
		self.collision_sprites = pygame.sprite.Group()

		self.import_assets()
		self.setup()

	# ┌─────────────────────────────────────────────────────────┐
	# │ PRE-SCAFFOLD — teacher walks through this, you use it   │
	# │                                                         │
	# │ import_assets() loads the player's walk cycle from      │
	# │ the graphics folder. all_character_import returns a     │
	# │ nested dict:  frames['player']['down'] = [surf, ...]    │
	# │                                                         │
	# │ The path starts with '..', '..' because this file runs  │
	# │ in sessions/session-2/ and assets are two levels up.    │
	# └─────────────────────────────────────────────────────────┘
	def import_assets(self):
		self.overworld_frames = {
			'characters': all_character_import('..', '..', 'graphics', 'characters'),
		}

	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 13: setup()                            │
	# │ Place the player and four border walls.                 │
	# │                                                         │
	# │ 1. Create the player:                                   │
	# │      self.player = Player(                              │
	# │          pos=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2),    │
	# │          frames=self.overworld_frames['characters']     │
	# │                     ['player'],                         │
	# │          groups=self.all_sprites,                       │
	# │          facing_direction='down',                       │
	# │          collision_sprites=self.collision_sprites)      │
	# │                                                         │
	# │ 2. Create four BorderSprites — one for each screen edge:│
	# │    Top wall:                                            │
	# │      BorderSprite((0, 0),                               │
	# │          pygame.Surface((WINDOW_WIDTH, 20)),            │
	# │          self.collision_sprites)                        │
	# │    Bottom wall: pos (0, WINDOW_HEIGHT - 20)             │
	# │    Left wall:   size (20, WINDOW_HEIGHT)                │
	# │    Right wall:  pos (WINDOW_WIDTH - 20, 0),             │
	# │                 size (20, WINDOW_HEIGHT)                │
	# │ Hint: BorderSprite does NOT go in all_sprites —         │
	# │       it only needs to be in collision_sprites.         │
	# └─────────────────────────────────────────────────────────┘
	def setup(self):
		# TODO: your code here
		pass  # remove this when you're done

	def run(self):
		# ┌─────────────────────────────────────────────────────────┐
		# │ PRE-SCAFFOLD — teacher walks through this, you use it   │
		# │                                                         │
		# │ run() has the same structure as session 1 but now:      │
		# │   - all_sprites.update(dt) advances every sprite        │
		# │   - all_sprites.draw(player) uses the camera offset     │
		# └─────────────────────────────────────────────────────────┘
		while True:
			dt = self.clock.tick() / 1000

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()

			# update
			self.all_sprites.update(dt)

			# draw
			self.display_surface.fill(COLORS['dark'])
			self.all_sprites.draw(self.player)

			pygame.display.update()


if __name__ == '__main__':
	game = Game()
	game.run()

# ┌─────────────────────────────────────────────────────────┐
# │ EXTENSION — bonus challenge!                            │
# │ Ideas: In setup(), add a coloured square obstacle:      │
# │          obs_surf = pygame.Surface((64, 64))            │
# │          obs_surf.fill(COLORS['fire'])                  │
# │          CollidableSprite((400, 300), obs_surf,         │
# │              (self.all_sprites, self.collision_sprites))│
# │        Does the player collide with it?                 │
# │        Try changing the player's speed (in entities.py).│
# └─────────────────────────────────────────────────────────┘
