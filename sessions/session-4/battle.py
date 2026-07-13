import pygame
from sys import exit
from pygame.math import Vector2 as vector
from settings import BATTLE_POSITIONS, BATTLE_CHOICES, COLORS
from sprites import MonsterSprite, MonsterNameSprite, MonsterLevelSprite, MonsterStatsSprite, MonsterOutlineSprite, AttackSprite
from groups import BattleSprites
from game_data import ATTACK_DATA
from timer import Timer
from random import choice

# ┌─────────────────────────────────────────────────────────┐
# │ PRE-SCAFFOLD — teacher walks through this, you use it   │
# └─────────────────────────────────────────────────────────┘
# Battle manages one fight. Only one monster is ever active per side —
# when it faints, the next monster from that side's bench (monster_data)
# is sent in automatically. There's no manual switching and no catching
# wild monsters, which keeps the turn loop small:
#
# 1. setup() puts one monster on screen per side
# 2. Every frame, monster.update(dt) increases its initiative bar
# 3. When initiative hits 100, check_active() gives that monster a turn
# 4. Player's turn: input() reads the menu. Opponent's turn:
#    opponent_attack() picks randomly.
# 5. Either way, MonsterSprite.activate_attack() plays the animation,
#    which calls back into apply_attack() to do the damage math.
# 6. check_death() removes fainted monsters and sends in the next one.
# 7. check_end_battle() detects when one whole side is empty.

class Battle:
	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 11a: Build __init__                    │
	# │ Hint: You need three sprite groups: battle_sprites       │
	# │       (BattleSprites), player_sprites, opponent_sprites  │
	# │       (both pygame.sprite.Group).                        │
	# │       Control vars: battle_over=False,                   │
	# │       current_monster=None, selection_mode=None.         │
	# │       indexes dict needs keys 'general' and 'attacks',   │
	# │       both starting at 0.                                │
	# │       timers needs 'opponent delay':                     │
	# │       Timer(600, func=self.opponent_attack)              │
	# │       Finish by calling self.setup().                    │
	# └─────────────────────────────────────────────────────────┘
	def __init__(self, player_monsters, opponent_monsters, monster_frames, bg_surf, fonts, end_battle, character, sounds):
		self.display_surface = pygame.display.get_surface()
		self.bg_surf = bg_surf
		self.monster_frames = monster_frames
		self.fonts = fonts
		self.monster_data = {'player': dict(player_monsters), 'opponent': dict(opponent_monsters)}
		self.end_battle = end_battle
		self.character = character
		self.sounds = sounds

		# TODO: your code here
		pass  # remove this when you're done

	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 11b: Build setup()                      │
	# │ Hint: for entity in ('player', 'opponent'):              │
	# │         pop the first (index, monster) pair out of       │
	# │         self.monster_data[entity] and pass it to          │
	# │         create_monster(monster, index, entity).           │
	# │       Popping removes it from the bench — it's on         │
	# │       screen now, not waiting anymore.                    │
	# └─────────────────────────────────────────────────────────┘
	def setup(self):
		# TODO: your code here
		pass  # remove this when you're done

	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 11c: Build create_monster()             │
	# │ Hint: monster.paused = False first.                       │
	# │       Look up frames = monster_frames['monsters'][name]   │
	# │       and outline_frames the same way from 'outlines'.    │
	# │       If entity == 'player': flip every frame horizontally│
	# │       with pygame.transform.flip(f, True, False) — the    │
	# │       player's monster faces right, the opponent's        │
	# │       faces left, using the same source art.              │
	# │       Position: BATTLE_POSITIONS['player'] or ['opponent']│
	# │       Groups: (battle_sprites, player_sprites) or          │
	# │       (battle_sprites, opponent_sprites).                  │
	# │       Then create, in order: MonsterSprite(pos, frames,    │
	# │       groups, monster, index, 0, entity, self.apply_attack,│
	# │       self.create_monster), MonsterOutlineSprite,          │
	# │       MonsterNameSprite, MonsterLevelSprite,               │
	# │       MonsterStatsSprite — see finished/session-4 for the  │
	# │       exact positioning math if you want to match it.      │
	# └─────────────────────────────────────────────────────────┘
	def create_monster(self, monster, index, entity):
		# TODO: your code here
		pass  # remove this when you're done

	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 12a: Build check_active()               │
	# │ Hint: loop player_sprites + opponent_sprites.             │
	# │       If a monster's initiative >= 100:                   │
	# │         pause everyone (update_all_monsters('pause')),    │
	# │         reset that monster's initiative to 0,             │
	# │         reset its defending flag to False (a fresh turn   │
	# │         means the old defend bonus no longer applies),    │
	# │         set_highlight(True) so it's visually obvious,     │
	# │         store it as self.current_monster.                 │
	# │       Then: if it's a 'player' monster, set                │
	# │       selection_mode = 'general' so input() takes over.    │
	# │       Otherwise activate timers['opponent delay'] so      │
	# │       opponent_attack() fires after a short pause.         │
	# └─────────────────────────────────────────────────────────┘
	def check_active(self):
		# TODO: your code here
		pass  # remove this when you're done

	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 12b: Build update_all_monsters(option)  │
	# │ Hint: loop sprites in both groups.                        │
	# │       option == 'pause'  -> monster.paused = True         │
	# │       option == anything else -> monster.paused = False   │
	# └─────────────────────────────────────────────────────────┘
	def update_all_monsters(self, option):
		# TODO: your code here
		pass  # remove this when you're done

	# ┌─────────────────────────────────────────────────────────┐
	# │ PRE-SCAFFOLD — teacher walks through this, you use it   │
	# └─────────────────────────────────────────────────────────┘
	# ATTACK_DATA['target'] is always relative to whoever is attacking:
	# 'player' means "my own side" (used by heal), 'opponent' means
	# "the other side". This works the same whether the attacker is
	# the human or the AI.
	def get_target_group(self, attack):
		same_side = self.player_sprites if self.current_monster.entity == 'player' else self.opponent_sprites
		other_side = self.opponent_sprites if self.current_monster.entity == 'player' else self.player_sprites
		return same_side if ATTACK_DATA[attack]['target'] == 'player' else other_side

	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 13: Build input()                       │
	# │ Hint: only run if self.selection_mode and self.current_monster.│
	# │       limiter = len(BATTLE_CHOICES) in 'general' mode,    │
	# │       or len(current_monster.monster.get_abilities(       │
	# │       include_all=False)) (or 1 if that's empty) in       │
	# │       'attacks' mode.                                     │
	# │       K_DOWN / K_UP: move indexes[selection_mode] by      │
	# │       ±1 with wraparound: % limiter.                      │
	# │       K_SPACE in 'general': index 0 -> selection_mode =   │
	# │       'attacks'. index 1 (defend) -> set                  │
	# │       current_monster.monster.defending = True, resume    │
	# │       everyone, clear current_monster and selection_mode. │
	# │       K_SPACE in 'attacks': look up the chosen ability,    │
	# │       find its target with self.get_target_group(attack), │
	# │       call current_monster.activate_attack(target, attack)│
	# │       then clear current_monster and selection_mode.      │
	# │       K_ESCAPE from 'attacks' goes back to 'general'.      │
	# │       After SPACE or ESCAPE, reset every index to 0.       │
	# └─────────────────────────────────────────────────────────┘
	def input(self):
		# TODO: your code here
		pass  # remove this when you're done

	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 14: Build opponent_attack()             │
	# │ Hint: only run if current_monster exists and its entity   │
	# │       is 'opponent'. Pick a random usable ability with     │
	# │       choice(current_monster.monster.get_abilities(        │
	# │       include_all=False)) — guard against an empty list!  │
	# │       Find the target the same way input() does, with     │
	# │       self.get_target_group(attack), then call             │
	# │       current_monster.activate_attack(target, attack).     │
	# │       Clear self.current_monster either way.               │
	# └─────────────────────────────────────────────────────────┘
	def opponent_attack(self):
		# TODO: your code here
		pass  # remove this when you're done

	# ┌─────────────────────────────────────────────────────────┐
	# │ PRE-SCAFFOLD — teacher walks through this, you use it   │
	# └─────────────────────────────────────────────────────────┘
	def update_timers(self):
		for timer in self.timers.values():
			timer.update()

	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 15: Build apply_attack()                │
	# │ Hint: this runs when the attack animation finishes — see  │
	# │       MonsterSprite.animate() in sprites.py.               │
	# │       1. Play the animation + sound (already written       │
	# │          below — study it, don't rewrite it).              │
	# │       2. attack_element = ATTACK_DATA[attack]['element'],  │
	# │          target_element = target_sprite.monster.element.   │
	# │       3. Type effectiveness: fire beats plant, water beats │
	# │          fire, plant beats water -> amount *= 2. The       │
	# │          reverse three matchups -> amount *= 0.5.          │
	# │       4. target_defense = 1 - target's defense stat / 2000 │
	# │          (higher defense = smaller target_defense).        │
	# │          If target_sprite.monster.defending: subtract 0.2. │
	# │          Clamp target_defense between 0 and 1.             │
	# │       5. target_sprite.monster.health -= amount * target_defense│
	# │       6. Call self.check_death() then                      │
	# │          self.update_all_monsters('resume').                │
	# └─────────────────────────────────────────────────────────┘
	def apply_attack(self, target_sprite, attack, amount):
		AttackSprite(target_sprite.rect.center, self.monster_frames['attacks'][ATTACK_DATA[attack]['animation']], self.battle_sprites)
		self.sounds[ATTACK_DATA[attack]['animation']].play()

		# TODO: your code here
		pass  # remove this when you're done

	# ┌─────────────────────────────────────────────────────────┐
	# │ PRE-SCAFFOLD — teacher walks through this, you use it   │
	# │ check_death, check_end_battle and the draw_* methods are │
	# │ UI/bookkeeping code, not new concepts — study them, but   │
	# │ they're given so this session stays focused on Steps      │
	# │ 11-15 above.                                              │
	# └─────────────────────────────────────────────────────────┘
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
