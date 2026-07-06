import pygame
from sys import exit
from os.path import join
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE, WORLD_LAYERS, COLORS
from support import (
	tmx_importer, import_folder, coast_importer, all_character_import,
	import_folder_dict, check_connections
)
from sprites import Sprite, AnimatedSprite, MonsterPatchSprite, BorderSprite, CollidableSprite, TransitionSprite
from entities import Player, Character
from groups import AllSprites
from dialog import DialogTree
from timer import Timer

# ┌─────────────────────────────────────────────────────────┐
# │ PRE-SCAFFOLD — teacher walks through this, you use it   │
# │                                                         │
# │ This session we connect the player to a REAL map.       │
# │ The map is stored as a .tmx file (a Tiled map file).    │
# │ tmx_importer() loads it; setup() reads each layer and   │
# │ creates sprites. You'll write setup() yourself.         │
# │                                                         │
# │ We also add a screen-tint transition effect and a basic  │
# │ dialog system so NPCs can speak.                        │
# └─────────────────────────────────────────────────────────┘

# ┌─────────────────────────────────────────────────────────┐
# │ PRE-SCAFFOLD — game_data contains NPC dialog + teams    │
# │ We inline a minimal version here so session 3 runs      │
# │ without importing game_data (that file uses Monster     │
# │ which isn't fully wired up until session 4).            │
# └─────────────────────────────────────────────────────────┘
TRAINER_DATA = {
	'o1': {
		'dialog': {
			'default':  ['Hey there, traveller!', 'The world is full of monsters.'],
			'defeated': ['You beat me!'],
		},
		'directions':   ['down'],
		'look_around':  False,
		'defeated':     False,
		'biome':        'forest',
	},
	'Nurse': {
		'dialog': {
			'default':  ['Welcome to the clinic!', 'Your monsters are healed.'],
			'defeated': ['Come back anytime!'],
		},
		'directions':   ['down'],
		'look_around':  False,
		'defeated':     False,
		'biome':        'forest',
	},
}


class Game:
	# ┌─────────────────────────────────────────────────────────┐
	# │ PRE-SCAFFOLD — teacher walks through this, you use it   │
	# └─────────────────────────────────────────────────────────┘
	def __init__(self):
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		pygame.display.set_caption('Monster Game')
		self.clock = pygame.time.Clock()

		# sprite groups
		self.all_sprites       = AllSprites()
		self.collision_sprites = pygame.sprite.Group()
		self.character_sprites = pygame.sprite.Group()
		self.transition_sprites = pygame.sprite.Group()
		self.monster_sprites   = pygame.sprite.Group()

		# transition / tint system
		self.transition_target = None
		self.tint_surf         = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
		self.tint_mode         = 'untint'
		self.tint_progress     = 0
		self.tint_speed        = 600

		# dialog
		self.dialog_tree = None

		self.import_assets()
		self.setup(self.tmx_maps['world'], 'house')

	# ┌─────────────────────────────────────────────────────────┐
	# │ PRE-SCAFFOLD — teacher walks through this, you use it   │
	# │                                                         │
	# │ import_assets loads everything from disk once at start. │
	# │ Notice all paths start with '..', '..' because this     │
	# │ file lives in sessions/session-3/ and the assets are    │
	# │ in Python-Monsters/graphics/ (two levels up).          │
	# └─────────────────────────────────────────────────────────┘
	def import_assets(self):
		self.tmx_maps = tmx_importer('..', '..', 'data', 'maps')

		self.overworld_frames = {
			'water':      import_folder('..', '..', 'graphics', 'tilesets', 'water'),
			'coast':      coast_importer(24, 12, '..', '..', 'graphics', 'tilesets', 'coast'),
			'characters': all_character_import('..', '..', 'graphics', 'characters'),
		}

		self.fonts = {
			'dialog':  pygame.font.Font(join('..', '..', 'graphics', 'fonts', 'PixeloidSans.ttf'), 30),
			'regular': pygame.font.Font(join('..', '..', 'graphics', 'fonts', 'PixeloidSans.ttf'), 18),
			'small':   pygame.font.Font(join('..', '..', 'graphics', 'fonts', 'PixeloidSans.ttf'), 14),
			'bold':    pygame.font.Font(join('..', '..', 'graphics', 'fonts', 'dogicapixelbold.otf'), 20),
		}

		# Placeholder: a simple green surface for monster patches
		# (full monster sprites come in session 4)
		self.monster_patch_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
		self.monster_patch_surf.fill(COLORS['plant'])

	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 17: setup(tmx_map, player_start_pos)   │
	# │                                                         │
	# │ This method reads every layer of the TMX map and turns  │
	# │ it into sprites. Work through each sub-step in order.  │
	# │                                                         │
	# │ How TMX layers work:                                    │
	# │   tmx_map.get_layer_by_name('Terrain').tiles()          │
	# │     → yields (col, row, surface) for each tile          │
	# │   tmx_map.get_layer_by_name('Water')                    │
	# │     → yields object rects with .x .y .width .height    │
	# │   obj.properties['key']  → reads a custom property      │
	# └─────────────────────────────────────────────────────────┘
	def setup(self, tmx_map, player_start_pos):

		# ── Step 17a: Clear all groups so the old map is gone ────────
		# Hint: call .empty() on each group.
		# TODO: your code here

		# ── Step 17b: Terrain tiles ───────────────────────────────────
		# Loop through the 'Terrain' and 'Terrain Top' layers.
		# For each tile at (x, y) call:
		#   Sprite((x * TILE_SIZE, y * TILE_SIZE), surf,
		#           self.all_sprites, WORLD_LAYERS['bg'])
		# Hint: use a for loop over ['Terrain', 'Terrain Top']
		#   then tmx_map.get_layer_by_name(layer).tiles()
		# TODO: your code here

		# ── Step 17c: Water animated sprites ─────────────────────────
		# The 'Water' layer has rectangle objects. We need to tile
		# animated water sprites across each rectangle.
		# For each obj in tmx_map.get_layer_by_name('Water'):
		#   for x in range(int(obj.x), int(obj.x + obj.width), TILE_SIZE):
		#     for y in range(int(obj.y), int(obj.y + obj.height), TILE_SIZE):
		#       AnimatedSprite((x, y), self.overworld_frames['water'],
		#                      self.all_sprites, WORLD_LAYERS['water'])
		# TODO: your code here

		# ── Step 17d: Coast animated sprites ─────────────────────────
		# Coast tiles have 'terrain' and 'side' properties.
		# For each obj in tmx_map.get_layer_by_name('Coast'):
		#   terrain = obj.properties['terrain']
		#   side    = obj.properties['side']
		#   AnimatedSprite((obj.x, obj.y),
		#                  self.overworld_frames['coast'][terrain][side],
		#                  self.all_sprites, WORLD_LAYERS['bg'])
		# TODO: your code here

		# ── Step 17e: Objects (trees, buildings, etc.) ───────────────
		# Objects named 'top' go in the WORLD_LAYERS['top'] layer
		# so they draw in FRONT of the player (e.g. treetops).
		# All other objects are collidable.
		# For each obj in tmx_map.get_layer_by_name('Objects'):
		#   if obj.name == 'top':
		#     Sprite((obj.x, obj.y), obj.image,
		#             self.all_sprites, WORLD_LAYERS['top'])
		#   else:
		#     CollidableSprite((obj.x, obj.y), obj.image,
		#                      (self.all_sprites, self.collision_sprites))
		# TODO: your code here

		# ── Step 17f: Transition sprites (doorways, cave entrances) ──
		# For each obj in tmx_map.get_layer_by_name('Transition'):
		#   TransitionSprite(
		#       (obj.x, obj.y),
		#       (obj.width, obj.height),
		#       (obj.properties['target'], obj.properties['pos']),
		#       self.transition_sprites)
		# TODO: your code here

		# ── Step 17g: Collision borders (invisible walls) ────────────
		# For each obj in tmx_map.get_layer_by_name('Collisions'):
		#   BorderSprite((obj.x, obj.y),
		#                pygame.Surface((obj.width, obj.height)),
		#                self.collision_sprites)
		# TODO: your code here

		# ── Step 17h: Monster patch sprites ──────────────────────────
		# For each obj in tmx_map.get_layer_by_name('Monsters'):
		#   MonsterPatchSprite(
		#       (obj.x, obj.y),
		#       obj.image,    ← the tile image from Tiled
		#       (self.all_sprites, self.monster_sprites),
		#       obj.properties['biome'],
		#       obj.properties['monsters'],
		#       obj.properties['level'])
		# Hint: obj.image already has the tall-grass art from Tiled.
		# TODO: your code here

		# ── Step 17i: Entities (Player + NPCs) ───────────────────────
		# For each obj in tmx_map.get_layer_by_name('Entities'):
		#   if obj.name == 'Player':
		#     Only spawn if obj.properties['pos'] == player_start_pos
		#     self.player = Player(
		#         pos=(obj.x, obj.y),
		#         frames=self.overworld_frames['characters']['player'],
		#         groups=self.all_sprites,
		#         facing_direction=obj.properties['direction'],
		#         collision_sprites=self.collision_sprites)
		#   else:
		#     char_id = obj.properties['character_id']
		#     data = TRAINER_DATA.get(char_id, TRAINER_DATA['o1'])
		#     Character(
		#         pos=(obj.x, obj.y),
		#         frames=self.overworld_frames['characters'][
		#                    obj.properties['graphic']],
		#         groups=(self.all_sprites, self.collision_sprites,
		#                 self.character_sprites),
		#         facing_direction=obj.properties.get('direction', 'down'),
		#         character_data=data,
		#         player=self.player,
		#         create_dialog=self.create_dialog,
		#         collision_sprites=self.collision_sprites,
		#         radius=obj.properties.get('radius', 0),
		#         nurse=(char_id == 'Nurse'),
		#         notice_sound=pygame.mixer.Sound(
		#             join('..', '..', 'audio', 'notice.wav')))
		# Hint: Spawn the Player BEFORE NPCs so self.player exists.
		#       Do a first pass for 'Player', then a second for NPCs.
		# Note: use .get() with defaults for 'direction'/'radius' — the
		#       Nurse NPC in hospital2.tmx doesn't define either property.
		# TODO: your code here
		pass  # remove this when you're done

	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 18: transition_check()                 │
	# │ Check if the player is standing on a transition zone.   │
	# │                                                         │
	# │ 1. Use pygame.sprite.spritecollide to find any          │
	# │    transition sprites the player overlaps. Pass a       │
	# │    collided= function that compares HITBOXES, not the   │
	# │    default rects — the player's rect is the full 128x128│
	# │    sprite frame, much bigger than the real hitbox, so    │
	# │    the door would trigger from far away (and could      │
	# │    immediately re-trigger the exit right after spawning │
	# │    inside a building):                                  │
	# │      sprites = pygame.sprite.spritecollide(             │
	# │          self.player, self.transition_sprites, False,   │
	# │          collided=lambda a, b: a.hitbox.colliderect(b.hitbox))│
	# │ 2. If sprites is non-empty:                             │
	# │      self.player.block()                                │
	# │      self.transition_target = sprites[0].target        │
	# │      self.tint_mode = 'tint'                            │
	# │ Hint: spritecollide returns a list; check with if sprites│
	# └─────────────────────────────────────────────────────────┘
	def transition_check(self):
		# TODO: your code here
		pass  # remove this when you're done

	# ┌─────────────────────────────────────────────────────────┐
	# │ PRE-SCAFFOLD — teacher walks through this, you use it   │
	# │                                                         │
	# │ tint_screen fades the screen to black (tint mode) then  │
	# │ loads the new map, then fades back in (untint mode).    │
	# └─────────────────────────────────────────────────────────┘
	def tint_screen(self, dt):
		if self.tint_mode == 'untint':
			self.tint_progress -= self.tint_speed * dt

		if self.tint_mode == 'tint':
			self.tint_progress += self.tint_speed * dt
			if self.tint_progress >= 255:
				# swap to the new map
				if self.transition_target:
					self.setup(
						self.tmx_maps[self.transition_target[0]],
						self.transition_target[1]
					)
				self.tint_mode         = 'untint'
				self.transition_target = None

		self.tint_progress = max(0, min(self.tint_progress, 255))
		self.tint_surf.set_alpha(self.tint_progress)
		self.display_surface.blit(self.tint_surf, (0, 0))

	# ┌─────────────────────────────────────────────────────────┐
	# │ PRE-SCAFFOLD — teacher walks through this, you use it   │
	# └─────────────────────────────────────────────────────────┘
	def input(self):
		if not self.dialog_tree:
			keys = pygame.key.get_just_pressed()
			if keys[pygame.K_SPACE]:
				for character in self.character_sprites:
					if check_connections(100, self.player, character):
						self.player.block()
						character.change_facing_direction(self.player.rect.center)
						self.create_dialog(character)
						character.can_rotate = False

	def create_dialog(self, character):
		if not self.dialog_tree:
			self.dialog_tree = DialogTree(
				character,
				self.player,
				self.all_sprites,
				self.fonts['dialog'],
				self.end_dialog
			)

	def end_dialog(self, character):
		# Session 3 simplified: just unblock the player.
		# Battle trigger comes in session 5.
		self.dialog_tree = None
		self.player.unblock()

	# ┌─────────────────────────────────────────────────────────┐
	# │ PRE-SCAFFOLD — teacher walks through this, you use it   │
	# └─────────────────────────────────────────────────────────┘
	def run(self):
		while True:
			dt = self.clock.tick() / 1000

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()

			# update
			self.input()
			self.transition_check()
			self.all_sprites.update(dt)

			# draw
			self.display_surface.fill('black')
			self.all_sprites.draw(self.player)

			# overlays
			if self.dialog_tree:
				self.dialog_tree.update()

			self.tint_screen(dt)
			pygame.display.update()


if __name__ == '__main__':
	game = Game()
	game.run()

# ┌─────────────────────────────────────────────────────────┐
# │ EXTENSION — bonus challenge!                            │
# │ Ideas: Change the starting position by passing a        │
# │        different string to setup() — e.g. 'world'       │
# │        instead of 'house'. What changes?                │
# │        Add print(obj.name, obj.x, obj.y) inside the     │
# │        Entities loop to see what objects are in the map.│
# └─────────────────────────────────────────────────────────┘
