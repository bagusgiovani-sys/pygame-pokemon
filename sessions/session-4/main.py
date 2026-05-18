import pygame
from sys import exit
from os.path import join
from random import randint
from pytmx.util_pygame import load_pygame

from settings import WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE, WORLD_LAYERS
from game_data import TRAINER_DATA
from support import (
	tmx_importer, import_folder, coast_importer, all_character_import,
	import_folder_dict, monster_importer, outline_creator, attack_importer,
	audio_importer, check_connections
)
from sprites import Sprite, AnimatedSprite, MonsterPatchSprite, BorderSprite, CollidableSprite, TransitionSprite
from entities import Player, Character
from groups import AllSprites
from dialog import DialogTree
from timer import Timer
from monster import Monster

class Game:
	def __init__(self):
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		pygame.display.set_caption('Monster Hunter')
		self.clock = pygame.time.Clock()
		self.encounter_timer = Timer(2000)

		# ┌─────────────────────────────────────────────────────────┐
		# │ YOUR CODE — Step 1: Create the player's monster team!   │
		# │ Hint: use Monster('MonsterName', level) to create each. │
		# │       Keys are 0, 1, 2, ... (one per monster).          │
		# │       After making the dict, loop through the values    │
		# │       and add randint(0, monster.level * 100) to xp.    │
		# └─────────────────────────────────────────────────────────┘
		# self.player_monsters = {
		#     0: Monster('Ivieron', 32),
		#     1: Monster('Atrox', 15),
		#     ... (add 5-7 monsters)
		# }
		# for monster in self.player_monsters.values():
		#     monster.xp += randint(0, monster.level * 100)

		# TODO: your code here
		pass  # remove this when you're done

		# groups
		self.all_sprites = AllSprites()
		self.collision_sprites = pygame.sprite.Group()
		self.character_sprites = pygame.sprite.Group()
		self.transition_sprites = pygame.sprite.Group()
		self.monster_sprites = pygame.sprite.Group()

		# transition / tint
		self.transition_target = None
		self.tint_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
		self.tint_mode = 'untint'
		self.tint_progress = 0
		self.tint_direction = -1
		self.tint_speed = 600

		self.import_assets()
		self.setup(self.tmx_maps['world'], 'house')

		# overlays
		self.dialog_tree = None
		self.index_open = False
		self.battle = None

	def import_assets(self):
		self.tmx_maps = tmx_importer('..', '..', 'data', 'maps')

		self.overworld_frames = {
			'water': import_folder('..', '..', 'graphics', 'tilesets', 'water'),
			'coast': coast_importer(24, 12, '..', '..', 'graphics', 'tilesets', 'coast'),
			'characters': all_character_import('..', '..', 'graphics', 'characters')
		}

		self.monster_frames = {
			'icons': import_folder_dict('..', '..', 'graphics', 'icons'),
			'monsters': monster_importer(4, 2, '..', '..', 'graphics', 'monsters'),
			'ui': import_folder_dict('..', '..', 'graphics', 'ui'),
			'attacks': attack_importer('..', '..', 'graphics', 'attacks')
		}
		self.monster_frames['outlines'] = outline_creator(self.monster_frames['monsters'], 4)

		self.fonts = {
			'dialog': pygame.font.Font(join('..', '..', 'graphics', 'fonts', 'PixeloidSans.ttf'), 30),
			'regular': pygame.font.Font(join('..', '..', 'graphics', 'fonts', 'PixeloidSans.ttf'), 18),
			'small': pygame.font.Font(join('..', '..', 'graphics', 'fonts', 'PixeloidSans.ttf'), 14),
			'bold': pygame.font.Font(join('..', '..', 'graphics', 'fonts', 'dogicapixelbold.otf'), 20),
		}
		self.bg_frames = import_folder_dict('..', '..', 'graphics', 'backgrounds')

		self.audio = audio_importer('..', '..', 'audio')

	def setup(self, tmx_map, player_start_pos):
		# clear the map
		for group in (self.all_sprites, self.collision_sprites, self.transition_sprites, self.character_sprites):
			group.empty()

		# terrain
		for layer in ['Terrain', 'Terrain Top']:
			for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
				Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, WORLD_LAYERS['bg'])

		# water
		for obj in tmx_map.get_layer_by_name('Water'):
			for x in range(int(obj.x), int(obj.x + obj.width), TILE_SIZE):
				for y in range(int(obj.y), int(obj.y + obj.height), TILE_SIZE):
					AnimatedSprite((x,y), self.overworld_frames['water'], self.all_sprites, WORLD_LAYERS['water'])

		# coast
		for obj in tmx_map.get_layer_by_name('Coast'):
			terrain = obj.properties['terrain']
			side = obj.properties['side']
			AnimatedSprite((obj.x, obj.y), self.overworld_frames['coast'][terrain][side], self.all_sprites, WORLD_LAYERS['bg'])

		# objects
		for obj in tmx_map.get_layer_by_name('Objects'):
			if obj.name == 'top':
				Sprite((obj.x, obj.y), obj.image, self.all_sprites, WORLD_LAYERS['top'])
			else:
				CollidableSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

		# transition objects
		for obj in tmx_map.get_layer_by_name('Transition'):
			TransitionSprite((obj.x, obj.y), (obj.width, obj.height), (obj.properties['target'], obj.properties['pos']), self.transition_sprites)

		# collision objects
		for obj in tmx_map.get_layer_by_name('Collisions'):
			BorderSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)

		# grass patches
		for obj in tmx_map.get_layer_by_name('Monsters'):
			MonsterPatchSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.monster_sprites), obj.properties['biome'], obj.properties['monsters'], obj.properties['level'])

		# entities
		for obj in tmx_map.get_layer_by_name('Entities'):
			if obj.name == 'Player':
				if obj.properties['pos'] == player_start_pos:
					self.player = Player(
						pos = (obj.x, obj.y),
						frames = self.overworld_frames['characters']['player'],
						groups = self.all_sprites,
						facing_direction = obj.properties['direction'],
						collision_sprites = self.collision_sprites)
			else:
				Character(
					pos = (obj.x, obj.y),
					frames = self.overworld_frames['characters'][obj.properties['graphic']],
					groups = (self.all_sprites, self.collision_sprites, self.character_sprites),
					facing_direction = obj.properties['direction'],
					character_data = TRAINER_DATA[obj.properties['character_id']],
					player = self.player,
					create_dialog = self.create_dialog,
					collision_sprites = self.collision_sprites,
					radius = obj.properties['radius'],
					nurse = obj.properties['character_id'] == 'Nurse',
					notice_sound = self.audio['notice'])

	# dialog system
	def input(self):
		if not self.dialog_tree and not self.battle:
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
			self.dialog_tree = DialogTree(character, self.player, self.all_sprites, self.fonts['dialog'], self.end_dialog)

	def end_dialog(self, character):
		self.dialog_tree = None
		self.player.unblock()

	# transition system
	def transition_check(self):
		sprites = pygame.sprite.spritecollide(self.player, self.transition_sprites, False)
		if sprites:
			self.player.block()
			self.transition_target = sprites[0].target
			self.tint_mode = 'tint'

	def tint_screen(self, dt):
		if self.tint_mode == 'untint':
			self.tint_progress -= self.tint_speed * dt

		if self.tint_mode == 'tint':
			self.tint_progress += self.tint_speed * dt
			if self.tint_progress >= 255:
				self.setup(self.tmx_maps[self.transition_target[0]], self.transition_target[1])
				self.tint_mode = 'untint'
				self.transition_target = None

		self.tint_progress = max(0, min(self.tint_progress, 255))
		self.tint_surf.set_alpha(self.tint_progress)
		self.display_surface.blit(self.tint_surf, (0,0))

	def run(self):
		while True:
			dt = self.clock.tick() / 1000
			self.display_surface.fill('black')

			# event loop
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()

			# update
			self.encounter_timer.update()
			self.input()
			self.transition_check()
			self.all_sprites.update(dt)

			# drawing
			self.all_sprites.draw(self.player)

			# overlays
			if self.dialog_tree: self.dialog_tree.update()

			self.tint_screen(dt)
			pygame.display.update()

if __name__ == '__main__':
	game = Game()
	game.run()
