import pygame
from sys import exit
from pygame.math import Vector2 as vector
from settings import BATTLE_POSITIONS, BATTLE_CHOICES, COLORS
from sprites import MonsterSprite, MonsterNameSprite, MonsterLevelSprite, MonsterStatsSprite, MonsterOutlineSprite, AttackSprite, TimedSprite
from groups import BattleSprites
from game_data import ATTACK_DATA
from support import draw_bar
from timer import Timer
from random import choice

# ┌─────────────────────────────────────────────────────────┐
# │ PRE-SCAFFOLD — teacher walks through this, you use it   │
# └─────────────────────────────────────────────────────────┘
# Battle manages the whole fight: setup, turn order, attack selection,
# and win/lose logic. The UI sprites (health bars, names) are
# pre-scaffolded in sprites.py — your job is to wire them together here.
#
# How a battle works:
# 1. setup() puts monsters on screen from both sides
# 2. Every frame, monster.update(dt) increases their initiative bar
# 3. When initiative hits 100, check_active() gives that monster a turn
# 4. The player picks an action from the menu (input())
# 5. The attack plays out via activate_attack() on the MonsterSprite
# 6. apply_attack() calculates damage, check_death() removes fainted monsters
# 7. check_end_battle() detects win/loss

class Battle:
	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 1: Build __init__                      │
	# │ Hint: You need these groups: battle_sprites (BattleSprites),│
	# │       player_sprites, opponent_sprites (pygame.sprite.Group)│
	# │       Control vars: current_monster=None,               │
	# │       selection_mode=None, selected_attack=None,        │
	# │       selection_side='player', battle_over=False        │
	# │       indexes dict needs keys: general, monster,        │
	# │       attacks, switch, target (all start at 0)          │
	# │       timers needs 'opponent delay': Timer(600, func=self.opponent_attack)│
	# └─────────────────────────────────────────────────────────┘
	def __init__(self, player_monsters, opponent_monsters, monster_frames, bg_surf, fonts, end_battle, character, sounds):
		self.display_surface = pygame.display.get_surface()
		self.bg_surf = bg_surf
		self.monster_frames = monster_frames
		self.fonts = fonts
		self.monster_data = {'player': player_monsters, 'opponent': opponent_monsters}
		self.end_battle = end_battle
		self.character = character
		self.sounds = sounds

		# TODO: Create the sprite groups
		# self.battle_sprites = BattleSprites()
		# self.player_sprites = pygame.sprite.Group()
		# self.opponent_sprites = pygame.sprite.Group()

		# TODO: Create battle control variables
		# self.battle_over = False
		# self.current_monster = None
		# self.selection_mode = None
		# self.selected_attack = None
		# self.selection_side = 'player'

		# TODO: Create indexes dict (all start at 0)
		# self.indexes = {'general': 0, 'monster': 0, 'attacks': 0, 'switch': 0, 'target': 0}

		# TODO: Create timers dict with 'opponent delay'
		# self.timers = {'opponent delay': Timer(600, func=self.opponent_attack)}

		# TODO: Call self.setup() to create the initial monster sprites
		pass  # remove this when you're done

	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 2: Build setup()                       │
	# │ Hint: loop self.monster_data for 'player' and 'opponent'│
	# │       Use {k: v for k, v in monsters.items() if k <= 2} │
	# │       to get only the first 3 monsters per side.        │
	# │       After creating opponent sprites, delete their     │
	# │       entries from monster_data['opponent'].            │
	# └─────────────────────────────────────────────────────────┘
	def setup(self):
		# Create the first 3 monsters on each side using create_monster().
		# Then remove the placed opponents from monster_data (they're on screen now).
		# TODO: your code here
		pass  # remove this when you're done

	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 3: Build create_monster()              │
	# │ Hint: set monster.paused = False first.                 │
	# │       For 'player' entity: flip frames horizontally.    │
	# │       Use BATTLE_POSITIONS['left'] for player,          │
	# │       BATTLE_POSITIONS['right'] for opponent.           │
	# │       Create MonsterSprite, then MonsterOutlineSprite,  │
	# │       MonsterNameSprite, MonsterLevelSprite,            │
	# │       MonsterStatsSprite in that order.                 │
	# └─────────────────────────────────────────────────────────┘
	def create_monster(self, monster, index, pos_index, entity):
		monster.paused = False
		frames = self.monster_frames['monsters'][monster.name]
		outline_frames = self.monster_frames['outlines'][monster.name]

		# TODO: Flip frames if entity == 'player'
		# frames = {state: [pygame.transform.flip(f, True, False) for f in state_frames]
		#           for state, state_frames in frames.items()}
		# (same for outline_frames)

		# TODO: Pick position from BATTLE_POSITIONS
		# if entity == 'player': pos = list(BATTLE_POSITIONS['left'].values())[pos_index]
		# else: pos = list(BATTLE_POSITIONS['right'].values())[pos_index]

		# TODO: Pick sprite groups
		# if entity == 'player': groups = (self.battle_sprites, self.player_sprites)
		# else: groups = (self.battle_sprites, self.opponent_sprites)

		# TODO: Create the sprites
		# monster_sprite = MonsterSprite(pos, frames, groups, monster, index, pos_index, entity,
		#                                self.apply_attack, self.create_monster)
		# MonsterOutlineSprite(monster_sprite, self.battle_sprites, outline_frames)
		# name_pos = monster_sprite.rect.midleft + vector(16, -70) if entity == 'player'
		#            else monster_sprite.rect.midright + vector(-40, -70)
		# name_sprite = MonsterNameSprite(name_pos, monster_sprite, self.battle_sprites, self.fonts['regular'])
		# level_pos = name_sprite.rect.bottomleft if entity == 'player' else name_sprite.rect.bottomright
		# MonsterLevelSprite(entity, level_pos, monster_sprite, self.battle_sprites, self.fonts['small'])
		# MonsterStatsSprite(monster_sprite.rect.midbottom + vector(0, 20), monster_sprite,
		#                    (150, 48), self.battle_sprites, self.fonts['small'])
		pass  # remove this when you're done

	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 4: Build check_active()                │
	# │ Hint: loop player_sprites + opponent_sprites.           │
	# │       If initiative >= 100: pause all, reset initiative │
	# │       to 0, set highlight, store as current_monster.    │
	# │       Check which group the sprite is in:               │
	# │       if self.player_sprites in sprite.groups():        │
	# │           set selection_mode = 'general'                │
	# │       else: activate timers['opponent delay']           │
	# └─────────────────────────────────────────────────────────┘
	def check_active(self):
		# Check if any monster's initiative bar is full.
		# If so: pause everyone, give that monster their turn.
		# TODO: your code here
		pass  # remove this when you're done

	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 5: Build update_all_monsters(option)   │
	# │ Hint: loop sprites in both groups.                      │
	# │       option == 'pause'  -> monster.paused = True       │
	# │       option == 'resume' -> monster.paused = False      │
	# └─────────────────────────────────────────────────────────┘
	def update_all_monsters(self, option):
		# Pause or resume all monsters.
		# TODO: your code here
		pass  # remove this when you're done

	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 6: Build input()                       │
	# │ Hint: Use match/case on self.selection_mode.            │
	# │       For 'general': index 0 = 'attacks', index 1 = defend,│
	# │       index 2 = 'switch', index 3 = 'target' (catch).  │
	# │       For 'attacks': move selection up/down, SPACE to   │
	# │       confirm and switch to 'target' mode.              │
	# │       For 'target': SPACE calls activate_attack.        │
	# │       ESC goes back to 'general' from any sub-mode.     │
	# └─────────────────────────────────────────────────────────┘
	def input(self):
		if self.selection_mode and self.current_monster:
			keys = pygame.key.get_just_pressed()
			# Calculate how many items are in the current list
			match self.selection_mode:
				case 'general': limiter = len(BATTLE_CHOICES['full'])
				case 'attacks': limiter = len(self.current_monster.monster.get_abilities(include_all=False))
				case 'switch':  limiter = len(self.available_monsters) if hasattr(self, 'available_monsters') else 1
				case 'target':  limiter = len(self.opponent_sprites) if self.selection_side == 'opponent' else len(self.player_sprites)
				case _: limiter = 1

			# TODO: Handle K_DOWN — increment index with wrap
			# self.indexes[self.selection_mode] = (self.indexes[self.selection_mode] + 1) % limiter

			# TODO: Handle K_UP — decrement index with wrap

			# TODO: Handle K_SPACE to confirm selection
			# match self.selection_mode:
			#   case 'general':
			#     if index == 0: selection_mode = 'attacks'
			#     if index == 1: defend + resume + clear current_monster
			#     if index == 2: selection_mode = 'switch'
			#     if index == 3: selection_mode = 'target', side = 'opponent'
			#   case 'attacks':
			#     selection_mode = 'target'
			#     selected_attack = abilities[index]
			#     selection_side = ATTACK_DATA[attack]['target']
			#   case 'target':
			#     get the target sprite, call current_monster.activate_attack(target, selected_attack)
			#     then clear: selected_attack, current_monster, selection_mode = None
			#   --- EXTENSION ---
			#   case 'switch':
			#     swap the monster out

			# TODO: Handle K_ESCAPE to go back
			# if mode in ('attacks', 'switch', 'target'): go back to 'general'

			# TODO: Reset all indexes to 0 after any SPACE/ESC press
			pass  # remove this when you're done

	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 7: Build opponent_attack()             │
	# │ Hint: pick a random ability from the monster.           │
	# │       Check ATTACK_DATA[ability]['target'] to know      │
	# │       which side to pick the target from.               │
	# │       'player' target = attack player_sprites.          │
	# │       'opponent' target = attack opponent_sprites.      │
	# └─────────────────────────────────────────────────────────┘
	def opponent_attack(self):
		# The AI picks a random ability and a random valid target.
		# TODO: your code here
		pass  # remove this when you're done

	def update_timers(self):
		for timer in self.timers.values():
			timer.update()

	# ┌─────────────────────────────────────────────────────────┐
	# │ PRE-SCAFFOLD — teacher walks through this, you use it   │
	# └─────────────────────────────────────────────────────────┘
	# apply_attack, check_death, check_end_battle are the damage
	# and win/lose logic — you will build these in Session 6!
	# For now they are pre-scaffolded as stubs so the game runs.

	def apply_attack(self, target_sprite, attack, amount):
		# Session 6 task — for now just play the animation
		AttackSprite(target_sprite.rect.center, self.monster_frames['attacks'][ATTACK_DATA[attack]['animation']], self.battle_sprites)
		if attack in self.sounds:
			self.sounds[ATTACK_DATA[attack]['animation']].play()
		target_sprite.monster.health -= amount * 0.5
		self.check_death()
		self.update_all_monsters('resume')

	def check_death(self):
		for monster_sprite in self.opponent_sprites.sprites() + self.player_sprites.sprites():
			if monster_sprite.monster.health <= 0:
				if self.player_sprites in monster_sprite.groups():
					active_monsters = [(monster_sprite.index, monster_sprite.monster) for monster_sprite in self.player_sprites.sprites()]
					available_monsters = [(index, monster) for index, monster in self.monster_data['player'].items() if monster.health > 0 and (index, monster) not in active_monsters]
					new_monster_data = [(monster, index, monster_sprite.pos_index, 'player') for index, monster in available_monsters][0] if available_monsters else None
				else:
					new_monster_data = (list(self.monster_data['opponent'].values())[0], monster_sprite.index, monster_sprite.pos_index, 'opponent') if self.monster_data['opponent'] else None
					if self.monster_data['opponent']:
						del self.monster_data['opponent'][min(self.monster_data['opponent'])]
					xp_amount = monster_sprite.monster.level * 100 / len(self.player_sprites)
					for player_sprite in self.player_sprites:
						player_sprite.monster.update_xp(xp_amount)
				monster_sprite.delayed_kill(new_monster_data)

	def check_end_battle(self):
		if len(self.opponent_sprites) == 0 and not self.battle_over:
			self.battle_over = True
			self.end_battle(self.character)
			for monster in self.monster_data['player'].values():
				monster.initiative = 0
		if len(self.player_sprites) == 0:
			pygame.quit()
			exit()

	def draw_ui(self):
		if self.current_monster:
			if self.selection_mode == 'general': self.draw_general()
			if self.selection_mode == 'attacks': self.draw_attacks()
			if self.selection_mode == 'switch':  self.draw_switch()

	def draw_general(self):
		for index, (option, data_dict) in enumerate(BATTLE_CHOICES['full'].items()):
			if index == self.indexes['general']:
				surf = self.monster_frames['ui'][f"{data_dict['icon']}_highlight"]
			else:
				surf = pygame.transform.grayscale(self.monster_frames['ui'][data_dict['icon']])
			rect = surf.get_frect(center=self.current_monster.rect.midright + data_dict['pos'])
			self.display_surface.blit(surf, rect)

	def draw_attacks(self):
		abilities = self.current_monster.monster.get_abilities(include_all=False)
		width, height = 150, 200
		visible_attacks = 4
		item_height = height / visible_attacks
		v_offset = 0 if self.indexes['attacks'] < visible_attacks else -(self.indexes['attacks'] - visible_attacks + 1) * item_height
		bg_rect = pygame.FRect((0,0), (width,height)).move_to(midleft=self.current_monster.rect.midright + vector(20,0))
		pygame.draw.rect(self.display_surface, COLORS['white'], bg_rect, 0, 5)
		for index, ability in enumerate(abilities):
			selected = index == self.indexes['attacks']
			if selected:
				element = ATTACK_DATA[ability]['element']
				text_color = COLORS[element] if element != 'normal' else COLORS['black']
			else:
				text_color = COLORS['light']
			text_surf = self.fonts['regular'].render(ability, False, text_color)
			text_rect = text_surf.get_frect(center=bg_rect.midtop + vector(0, item_height / 2 + index * item_height + v_offset))
			text_bg_rect = pygame.FRect((0,0), (width, item_height)).move_to(center=text_rect.center)
			if bg_rect.collidepoint(text_rect.center):
				if selected:
					if text_bg_rect.collidepoint(bg_rect.topleft):
						pygame.draw.rect(self.display_surface, COLORS['dark white'], text_bg_rect, 0, 0, 5, 5)
					elif text_bg_rect.collidepoint(bg_rect.midbottom + vector(0,-1)):
						pygame.draw.rect(self.display_surface, COLORS['dark white'], text_bg_rect, 0, 0, 0, 0, 5, 5)
					else:
						pygame.draw.rect(self.display_surface, COLORS['dark white'], text_bg_rect)
				self.display_surface.blit(text_surf, text_rect)

	def draw_switch(self):
		width, height = 300, 320
		visible_monsters = 4
		item_height = height / visible_monsters
		v_offset = 0 if self.indexes['switch'] < visible_monsters else -(self.indexes['switch'] - visible_monsters + 1) * item_height
		bg_rect = pygame.FRect((0,0), (width, height)).move_to(midleft=self.current_monster.rect.midright + vector(20,0))
		pygame.draw.rect(self.display_surface, COLORS['white'], bg_rect, 0, 5)
		active_monsters = [(monster_sprite.index, monster_sprite.monster) for monster_sprite in self.player_sprites]
		self.available_monsters = {index: monster for index, monster in self.monster_data['player'].items() if (index, monster) not in active_monsters and monster.health > 0}
		for index, monster in enumerate(self.available_monsters.values()):
			selected = index == self.indexes['switch']
			item_bg_rect = pygame.FRect((0,0), (width, item_height)).move_to(midleft=(bg_rect.left, bg_rect.top + item_height / 2 + index * item_height + v_offset))
			icon_surf = self.monster_frames['icons'][monster.name]
			icon_rect = icon_surf.get_frect(midleft=bg_rect.topleft + vector(10, item_height / 2 + index * item_height + v_offset))
			text_surf = self.fonts['regular'].render(f'{monster.name} ({monster.level})', False, COLORS['red'] if selected else COLORS['black'])
			text_rect = text_surf.get_frect(topleft=(bg_rect.left + 90, icon_rect.top))
			if selected:
				if item_bg_rect.collidepoint(bg_rect.topleft):
					pygame.draw.rect(self.display_surface, COLORS['dark white'], item_bg_rect, 0, 0, 5, 5)
				elif item_bg_rect.collidepoint(bg_rect.midbottom + vector(0,-1)):
					pygame.draw.rect(self.display_surface, COLORS['dark white'], item_bg_rect, 0, 0, 0, 0, 5, 5)
				else:
					pygame.draw.rect(self.display_surface, COLORS['dark white'], item_bg_rect)
			if bg_rect.collidepoint(item_bg_rect.center):
				for surf, rect in ((icon_surf, icon_rect), (text_surf, text_rect)):
					self.display_surface.blit(surf, rect)
				health_rect = pygame.FRect((text_rect.bottomleft + vector(0,4)), (100,4))
				energy_rect = pygame.FRect((health_rect.bottomleft + vector(0,2)), (80,4))
				draw_bar(self.display_surface, health_rect, monster.health, monster.get_stat('max_health'), COLORS['red'], COLORS['black'])
				draw_bar(self.display_surface, energy_rect, monster.energy, monster.get_stat('max_energy'), COLORS['blue'], COLORS['black'])

	def update(self, dt):
		self.check_end_battle()
		self.input()
		self.update_timers()
		self.battle_sprites.update(dt)
		self.check_active()
		self.display_surface.blit(self.bg_surf, (0,0))
		self.battle_sprites.draw(self.current_monster, self.selection_side, self.selection_mode, self.indexes['target'], self.player_sprites, self.opponent_sprites)
		self.draw_ui()
