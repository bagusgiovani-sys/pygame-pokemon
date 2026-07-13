import pygame
from sys import exit
from pygame.math import Vector2 as vector
from settings import BATTLE_POSITIONS, BATTLE_CHOICES, COLORS
from sprites import MonsterSprite, MonsterNameSprite, MonsterLevelSprite, MonsterStatsSprite, MonsterOutlineSprite, AttackSprite
from groups import BattleSprites
from game_data import ATTACK_DATA
from timer import Timer
from random import choice

# Only one monster is ever active per side. When it faints, the next
# monster from that side's bench (monster_data) is sent in automatically
# — there's no manual switching and no catching wild monsters.

class Battle:
	def __init__(self, player_monsters, opponent_monsters, monster_frames, bg_surf, fonts, end_battle, character, sounds):
		self.display_surface = pygame.display.get_surface()
		self.bg_surf = bg_surf
		self.monster_frames = monster_frames
		self.fonts = fonts
		self.monster_data = {'player': dict(player_monsters), 'opponent': dict(opponent_monsters)}
		self.end_battle = end_battle
		self.character = character
		self.sounds = sounds

		self.battle_sprites = BattleSprites()
		self.player_sprites = pygame.sprite.Group()
		self.opponent_sprites = pygame.sprite.Group()

		self.battle_over = False
		self.current_monster = None
		self.selection_mode = None

		self.indexes = {'general': 0, 'attacks': 0}
		self.timers = {'opponent delay': Timer(600, func=self.opponent_attack)}

		self.setup()

	def setup(self):
		for entity in ('player', 'opponent'):
			index = list(self.monster_data[entity].keys())[0]
			monster = self.monster_data[entity].pop(index)
			self.create_monster(monster, index, entity)

	def create_monster(self, monster, index, entity):
		monster.paused = False
		frames = self.monster_frames['monsters'][monster.name]
		outline_frames = self.monster_frames['outlines'][monster.name]

		if entity == 'player':
			frames = {state: [pygame.transform.flip(f, True, False) for f in state_frames] for state, state_frames in frames.items()}
			outline_frames = {state: [pygame.transform.flip(f, True, False) for f in state_frames] for state, state_frames in outline_frames.items()}
			pos = BATTLE_POSITIONS['player']
			groups = (self.battle_sprites, self.player_sprites)
		else:
			pos = BATTLE_POSITIONS['opponent']
			groups = (self.battle_sprites, self.opponent_sprites)

		monster_sprite = MonsterSprite(pos, frames, groups, monster, index, 0, entity, self.apply_attack, self.create_monster)
		MonsterOutlineSprite(monster_sprite, self.battle_sprites, outline_frames)

		name_pos = monster_sprite.rect.midleft + vector(16, -70) if entity == 'player' else monster_sprite.rect.midright + vector(-40, -70)
		name_sprite = MonsterNameSprite(name_pos, monster_sprite, self.battle_sprites, self.fonts['regular'])
		level_pos = name_sprite.rect.bottomleft if entity == 'player' else name_sprite.rect.bottomright
		MonsterLevelSprite(entity, level_pos, monster_sprite, self.battle_sprites, self.fonts['small'])
		MonsterStatsSprite(monster_sprite.rect.midbottom + vector(0, 20), monster_sprite, (150, 48), self.battle_sprites, self.fonts['small'])

	def check_active(self):
		for monster_sprite in list(self.player_sprites) + list(self.opponent_sprites):
			if monster_sprite.monster.initiative >= 100:
				self.update_all_monsters('pause')
				monster_sprite.monster.initiative = 0
				monster_sprite.monster.defending = False
				monster_sprite.set_highlight(True)
				self.current_monster = monster_sprite
				if monster_sprite.entity == 'player':
					self.selection_mode = 'general'
				else:
					self.timers['opponent delay'].activate()

	def update_all_monsters(self, option):
		for monster_sprite in list(self.player_sprites) + list(self.opponent_sprites):
			monster_sprite.monster.paused = option == 'pause'

	def get_target_group(self, attack):
		same_side = self.player_sprites if self.current_monster.entity == 'player' else self.opponent_sprites
		other_side = self.opponent_sprites if self.current_monster.entity == 'player' else self.player_sprites
		return same_side if ATTACK_DATA[attack]['target'] == 'player' else other_side

	def input(self):
		if self.selection_mode and self.current_monster:
			keys = pygame.key.get_just_pressed()

			if self.selection_mode == 'general':
				limiter = len(BATTLE_CHOICES)
			else:
				limiter = len(self.current_monster.monster.get_abilities(include_all=False)) or 1

			if keys[pygame.K_DOWN]:
				self.indexes[self.selection_mode] = (self.indexes[self.selection_mode] + 1) % limiter
			if keys[pygame.K_UP]:
				self.indexes[self.selection_mode] = (self.indexes[self.selection_mode] - 1) % limiter

			if keys[pygame.K_SPACE]:
				if self.selection_mode == 'general':
					if self.indexes['general'] == 0:
						self.selection_mode = 'attacks'
					else:
						self.current_monster.monster.defending = True
						self.update_all_monsters('resume')
						self.current_monster = None
						self.selection_mode = None
				elif self.selection_mode == 'attacks':
					abilities = self.current_monster.monster.get_abilities(include_all=False)
					if abilities:
						attack = abilities[self.indexes['attacks']]
						target_group = self.get_target_group(attack)
						target_sprite = target_group.sprites()[0] if target_group.sprites() else self.current_monster
						self.current_monster.activate_attack(target_sprite, attack)
					else:
						self.update_all_monsters('resume')
					self.current_monster = None
					self.selection_mode = None

			if keys[pygame.K_ESCAPE] and self.selection_mode == 'attacks':
				self.selection_mode = 'general'

			if keys[pygame.K_SPACE] or keys[pygame.K_ESCAPE]:
				self.indexes = {key: 0 for key in self.indexes}

	def opponent_attack(self):
		if self.current_monster and self.current_monster.entity == 'opponent':
			abilities = self.current_monster.monster.get_abilities(include_all=False)
			if abilities:
				attack = choice(abilities)
				target_group = self.get_target_group(attack)
				target_sprite = target_group.sprites()[0] if target_group.sprites() else self.current_monster
				self.current_monster.activate_attack(target_sprite, attack)
			else:
				self.update_all_monsters('resume')
			self.current_monster = None

	def update_timers(self):
		for timer in self.timers.values():
			timer.update()

	def apply_attack(self, target_sprite, attack, amount):
		AttackSprite(target_sprite.rect.center, self.monster_frames['attacks'][ATTACK_DATA[attack]['animation']], self.battle_sprites)
		self.sounds[ATTACK_DATA[attack]['animation']].play()

		attack_element = ATTACK_DATA[attack]['element']
		target_element = target_sprite.monster.element
		if (attack_element == 'fire'  and target_element == 'plant') or \
		   (attack_element == 'water' and target_element == 'fire')  or \
		   (attack_element == 'plant' and target_element == 'water'):
			amount *= 2
		if (attack_element == 'fire'  and target_element == 'water') or \
		   (attack_element == 'water' and target_element == 'plant') or \
		   (attack_element == 'plant' and target_element == 'fire'):
			amount *= 0.5

		target_defense = 1 - target_sprite.monster.get_stat('defense') / 2000
		if target_sprite.monster.defending:
			target_defense -= 0.2
		target_defense = max(0, min(1, target_defense))

		target_sprite.monster.health -= amount * target_defense
		self.check_death()
		self.update_all_monsters('resume')

	def check_death(self):
		for monster_sprite in list(self.opponent_sprites) + list(self.player_sprites):
			if monster_sprite.monster.health <= 0:
				entity = monster_sprite.entity
				if self.monster_data[entity]:
					next_index = list(self.monster_data[entity].keys())[0]
					next_monster = self.monster_data[entity].pop(next_index)
					new_monster_data = (next_monster, next_index, entity)
				else:
					new_monster_data = None
				if entity == 'opponent':
					for player_sprite in self.player_sprites:
						player_sprite.monster.update_xp(monster_sprite.monster.level * 100)
				monster_sprite.delayed_kill(new_monster_data)

	def check_end_battle(self):
		if len(self.opponent_sprites) == 0 and not self.monster_data['opponent'] and not self.battle_over:
			self.battle_over = True
			self.end_battle(self.character)
			for monster in self.monster_data['player'].values():
				monster.initiative = 0
		if len(self.player_sprites) == 0 and not self.monster_data['player']:
			pygame.quit()
			exit()

	def draw_ui(self):
		if self.current_monster:
			if self.selection_mode == 'general': self.draw_general()
			if self.selection_mode == 'attacks': self.draw_attacks()

	def draw_general(self):
		for index, (option, data_dict) in enumerate(BATTLE_CHOICES.items()):
			if index == self.indexes['general']:
				surf = self.monster_frames['ui'][f"{data_dict['icon']}_highlight"]
			else:
				surf = pygame.transform.grayscale(self.monster_frames['ui'][data_dict['icon']])
			rect = surf.get_frect(center=self.current_monster.rect.midright + data_dict['pos'])
			self.display_surface.blit(surf, rect)

	def draw_attacks(self):
		abilities = self.current_monster.monster.get_abilities(include_all=False)
		width, height = 150, 160
		item_height = height / 4
		bg_rect = pygame.FRect((0, 0), (width, height)).move_to(midleft=self.current_monster.rect.midright + vector(20, 0))
		pygame.draw.rect(self.display_surface, COLORS['white'], bg_rect, 0, 5)
		for index, ability in enumerate(abilities):
			selected = index == self.indexes['attacks']
			element = ATTACK_DATA[ability]['element']
			text_color = COLORS[element] if selected and element != 'normal' else COLORS['black'] if selected else COLORS['light']
			text_surf = self.fonts['regular'].render(ability, False, text_color)
			text_rect = text_surf.get_frect(center=bg_rect.midtop + vector(0, item_height / 2 + index * item_height))
			if selected:
				item_bg_rect = pygame.FRect((0, 0), (width, item_height)).move_to(center=text_rect.center)
				pygame.draw.rect(self.display_surface, COLORS['dark white'], item_bg_rect)
			self.display_surface.blit(text_surf, text_rect)

	def update(self, dt):
		self.check_end_battle()
		self.input()
		self.update_timers()
		self.battle_sprites.update(dt)
		self.check_active()
		self.display_surface.blit(self.bg_surf, (0, 0))
		self.battle_sprites.draw(self.current_monster, 'opponent', self.selection_mode, 0, self.player_sprites, self.opponent_sprites)
		self.draw_ui()
