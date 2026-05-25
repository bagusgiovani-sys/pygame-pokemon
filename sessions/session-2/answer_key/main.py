import pygame
from sys import exit
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE, COLORS, WORLD_LAYERS
from support import all_character_import
from sprites import Sprite, CollidableSprite
from entities import Player
from groups import AllSprites


# ┌─────────────────────────────────────────────────────────┐
# │ SESSION 2 — ANSWER KEY V2: TEMPORARY PRACTICE MAP        │
# │                                                         │
# │ Why this version is better for Session 2:               │
# │ - Still uses the real project camera                    │
# │ - But adds a temporary visible map                      │
# │ - Borders are visible, not invisible                    │
# │ - Students can compare slow / normal / sprint / dash    │
# │   because there are landmarks, paths, and obstacles     │
# │                                                         │
# │ No TMX map yet. Real Tiled map loading comes in Session 3│
# └─────────────────────────────────────────────────────────┘


class Game:
	def __init__(self):
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		pygame.display.set_caption('Monster Game - Session 2 Temporary Map')
		self.clock = pygame.time.Clock()
		self.font = pygame.font.Font(None, 34)
		self.small_font = pygame.font.Font(None, 24)

		# sprite groups
		self.all_sprites = AllSprites()
		self.collision_sprites = pygame.sprite.Group()

		# temporary map size in pixels
		# Bigger than the window, so the camera can follow the player.
		self.map_width = 2200
		self.map_height = 1500

		self.import_assets()
		self.setup()

	def import_assets(self):
		self.overworld_frames = {
			'characters': all_character_import('..', '..', '..', 'graphics', 'characters'),
		}

	def make_surface(self, size, color):
		"""Create a simple colored Surface for temporary map tiles/objects."""
		surf = pygame.Surface(size)
		surf.fill(color)
		return surf

	def make_text_sprite(self, text, pos, color='white', bg=None):
		"""Create text inside the scrolling world, useful for signs/labels."""
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
		# ─────────────────────────────────────────────────────
		# 1. Floor tiles
		# A visible tile floor makes movement distance easier to see.
		# ─────────────────────────────────────────────────────
		for x in range(0, self.map_width, TILE_SIZE):
			for y in range(0, self.map_height, TILE_SIZE):
				# checker variation so the world does not look empty
				color = '#2f4032' if (x // TILE_SIZE + y // TILE_SIZE) % 2 == 0 else '#344a36'
				floor_surf = self.make_surface((TILE_SIZE, TILE_SIZE), color)
				Sprite(
					pos=(x, y),
					surf=floor_surf,
					groups=self.all_sprites,
					z=WORLD_LAYERS['bg'],
				)

		# ─────────────────────────────────────────────────────
		# 2. Visible border walls
		# These walls are visible AND collidable.
		# Students can clearly see where collision happens.
		# ─────────────────────────────────────────────────────
		wall = '#7a7a7a'
		wall_thickness = 64

		walls = [
			# top
			((0, 0), (self.map_width, wall_thickness)),
			# bottom
			((0, self.map_height - wall_thickness), (self.map_width, wall_thickness)),
			# left
			((0, 0), (wall_thickness, self.map_height)),
			# right
			((self.map_width - wall_thickness, 0), (wall_thickness, self.map_height)),
		]

		for pos, size in walls:
			wall_surf = self.make_surface(size, wall)
			CollidableSprite(
				pos=pos,
				surf=wall_surf,
				groups=(self.all_sprites, self.collision_sprites),
			)

		# ─────────────────────────────────────────────────────
		# 3. A visible path / speed test track
		# This gives students reference points for comparing speed.
		# ─────────────────────────────────────────────────────
		path_color = '#5b4b36'
		for x in range(128, 1900, TILE_SIZE):
			path_surf = self.make_surface((TILE_SIZE, TILE_SIZE), path_color)
			Sprite((x, 320), path_surf, self.all_sprites, WORLD_LAYERS['bg'])
			Sprite((x, 384), path_surf, self.all_sprites, WORLD_LAYERS['bg'])

		self.make_text_sprite('SPEED TEST TRACK: compare walk / sprint / dash here', (180, 260), 'white')
		self.make_text_sprite('START', (150, 450), 'white')
		self.make_text_sprite('MID', (900, 450), 'white')
		self.make_text_sprite('FINISH', (1700, 450), 'white')

		# Landmark flags along the track
		flag_positions = [(220, 250), (600, 250), (1000, 250), (1400, 250), (1800, 250)]
		for index, pos in enumerate(flag_positions, start=1):
			flag_surf = self.make_surface((40, 90), COLORS['fire'] if index % 2 else COLORS['water'])
			Sprite(pos, flag_surf, self.all_sprites, WORLD_LAYERS['main'])
			self.make_text_sprite(f'Flag {index}', (pos[0] - 8, pos[1] - 28), 'white')

		# ─────────────────────────────────────────────────────
		# 4. Obstacle course
		# Visible collidable blocks = better collision lesson.
		# ─────────────────────────────────────────────────────
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

		# ─────────────────────────────────────────────────────
		# 5. Decorative zones
		# These are non-collidable, just to make the map feel alive.
		# ─────────────────────────────────────────────────────
		base_surf = self.make_surface((320, 200), COLORS['plant'])
		Sprite((280, 1050), base_surf, self.all_sprites, WORLD_LAYERS['bg'])
		self.make_text_sprite('TRAINER BASE', (360, 1120), 'white')

		water_surf = self.make_surface((360, 220), COLORS['water'])
		Sprite((1500, 980), water_surf, self.all_sprites, WORLD_LAYERS['bg'])
		self.make_text_sprite('WATER AREA', (1600, 1070), 'white')

		# ─────────────────────────────────────────────────────
		# CREATIVITY OPTION 1 — Add more rocks
		# To activate: remove the # symbols below.
		# ─────────────────────────────────────────────────────

		# extra_rocks = [(900, 1100), (980, 1100), (1060, 1100)]
		# for pos in extra_rocks:
		# 	rock_surf = self.make_surface((70, 70), '#444444')
		# 	CollidableSprite(pos, rock_surf, (self.all_sprites, self.collision_sprites))

		# ─────────────────────────────────────────────────────
		# CREATIVITY OPTION 2 — Add a danger zone
		# To activate: remove the # symbols below.
		# ─────────────────────────────────────────────────────

		# danger_surf = self.make_surface((260, 160), COLORS['fire'])
		# Sprite((900, 1050), danger_surf, self.all_sprites, WORLD_LAYERS['bg'])
		# self.make_text_sprite('DANGER ZONE', (960, 1110), 'white')

	def setup(self):
		# Create the temporary practice map first.
		self.create_temporary_map()

		# Create the player after the map so the player draws on top.
		self.player = Player(
			pos=(180, 380),
			frames=self.overworld_frames['characters']['player'],
			groups=self.all_sprites,
			facing_direction='down',
			collision_sprites=self.collision_sprites,
		)

	def draw_hud(self):
		# HUD is drawn directly on the screen, so it does not move with camera.
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
