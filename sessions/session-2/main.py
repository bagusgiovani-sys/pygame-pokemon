import pygame
from sys import exit
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE, COLORS, WORLD_LAYERS
from support import all_character_import
from sprites import Sprite, CollidableSprite
from entities import Player
from groups import AllSprites

# ┌─────────────────────────────────────────────────────────┐
# │ SESSION 2 — STUDENT FILE                                │
# │ Updated Session 2 uses a TEMPORARY PRACTICE MAP.         │
# │                                                         │
# │ Why:                                                    │
# │ - We keep the real camera-follow system                  │
# │ - Students can see walls, paths, flags, and obstacles    │
# │ - Speed creativity feels obvious and testable            │
# │ - Real TMX/Tiled map loading still comes in Session 3    │
# └─────────────────────────────────────────────────────────┘

class Game:
	def __init__(self):
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		pygame.display.set_caption('Monster Game - Session 2 Temporary Map')
		self.clock = pygame.time.Clock()
		self.font = pygame.font.Font(None, 34)
		self.small_font = pygame.font.Font(None, 24)

		# Sprite groups
		self.all_sprites = AllSprites()
		self.collision_sprites = pygame.sprite.Group()

		# Temporary map size in pixels.
		# Bigger than the window, so the camera has something to follow.
		self.map_width = 2200
		self.map_height = 1500

		self.import_assets()
		self.setup()

	def import_assets(self):
		self.overworld_frames = {
			'characters': all_character_import('..', '..', 'graphics', 'characters'),
		}

	def make_surface(self, size, color):
		"""Create a simple colored Surface for temporary map tiles/objects."""
		surf = pygame.Surface(size)
		surf.fill(color)
		return surf

	def make_text_sprite(self, text, pos, color='white', bg=None):
		"""Create a text sprite inside the scrolling world."""
		if bg:
			surf = self.small_font.render(text, True, color, bg)
		else:
			surf = self.small_font.render(text, True, color)

		Sprite(
			pos=pos,
			surf=surf,
			groups=self.all_sprites,
			z=WORLD_LAYERS['top'],
		)

	def create_temporary_map(self):
		# ┌─────────────────────────────────────────────────────┐
		# │ YOUR CODE — Step 12a: Floor tiles                   │
		# │ Create a checker floor from 0 to map_width/map_height│
		# │ using TILE_SIZE. Each tile should be a Sprite on bg. │
		# └─────────────────────────────────────────────────────┘
		# TODO: your code here
		pass  # remove this when you're done

		# ┌─────────────────────────────────────────────────────┐
		# │ YOUR CODE — Step 12b: Visible border walls           │
		# │ Use CollidableSprite so walls are visible AND solid. │
		# │ Create top, bottom, left, and right walls.           │
		# └─────────────────────────────────────────────────────┘
		# TODO: your code here
		pass  # remove this when you're done

		# ┌─────────────────────────────────────────────────────┐
		# │ YOUR CODE — Step 12c: Speed test track               │
		# │ Add a visible path and labels: START, MID, FINISH.   │
		# │ This lets students compare walk/sprint/dash speed.   │
		# └─────────────────────────────────────────────────────┘
		# TODO: your code here
		pass  # remove this when you're done

		# ┌─────────────────────────────────────────────────────┐
		# │ YOUR CODE — Step 12d: Landmark flags                 │
		# │ Add several flag sprites along the track.            │
		# │ Flags make speed differences easy to see.            │
		# └─────────────────────────────────────────────────────┘
		# TODO: your code here
		pass  # remove this when you're done

		# ┌─────────────────────────────────────────────────────┐
		# │ YOUR CODE — Step 12e: Obstacle course                │
		# │ Add visible CollidableSprite rocks.                  │
		# │ This is where students test collision.               │
		# └─────────────────────────────────────────────────────┘
		# TODO: your code here
		pass  # remove this when you're done

		# ┌─────────────────────────────────────────────────────┐
		# │ YOUR CODE — Step 12f: Decorative zones               │
		# │ Add non-collidable Trainer Base and Water Area.      │
		# │ These make the practice map feel less empty.         │
		# └─────────────────────────────────────────────────────┘
		# TODO: your code here
		pass  # remove this when you're done

		# ─────────────────────────────────────────────────────
		# CREATIVITY OPTION 1 — Add more rocks
		# To activate after the main map works, remove the #.
		# ─────────────────────────────────────────────────────
		# extra_rocks = [(900, 1100), (980, 1100), (1060, 1100)]
		# for pos in extra_rocks:
		# 	rock_surf = self.make_surface((70, 70), '#444444')
		# 	CollidableSprite(pos, rock_surf, (self.all_sprites, self.collision_sprites))

		# ─────────────────────────────────────────────────────
		# CREATIVITY OPTION 2 — Add a danger zone
		# This is visual only, not collidable.
		# ─────────────────────────────────────────────────────
		# danger_surf = self.make_surface((260, 160), COLORS['fire'])
		# Sprite((900, 1050), danger_surf, self.all_sprites, WORLD_LAYERS['bg'])
		# self.make_text_sprite('DANGER ZONE', (960, 1110), 'white')

	def setup(self):
		# ┌─────────────────────────────────────────────────────┐
		# │ YOUR CODE — Step 13: Setup the world                 │
		# │ 1. Call self.create_temporary_map()                  │
		# │ 2. Create the Player at the speed track start.       │
		# └─────────────────────────────────────────────────────┘
		# TODO: your code here
		pass  # remove this when you're done

	def draw_hud(self):
		# HUD is drawn directly on the screen, so it does not move with the camera.
		# This helps students see the current speed when testing creativity.
		lines = [
			f'Speed: {int(self.player.speed)}',
			'Arrow Keys = Move',
			'Creativity in entities.py: WASD / Shift sprint / Ctrl sneak / Space dash',
		]

		for index, line in enumerate(lines):
			text_surf = self.font.render(line, True, 'white')
			text_rect = text_surf.get_frect(topleft=(24, 20 + index * 34))
			pygame.draw.rect(self.display_surface, '#000000', text_rect.inflate(18, 10))
			self.display_surface.blit(text_surf, text_rect)

	def run(self):
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
			self.draw_hud()

			pygame.display.update()


if __name__ == '__main__':
	game = Game()
	game.run()
