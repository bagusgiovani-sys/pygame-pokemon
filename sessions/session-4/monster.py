# ┌─────────────────────────────────────────────────────────┐
# │ PRE-SCAFFOLD — teacher walks through this, you use it   │
# └─────────────────────────────────────────────────────────┘
# Monster stores all the data about one creature:
# its name, level, stats, health, energy, XP, and abilities.
# One Monster object = one creature in your team or the opponent's team.

from game_data import MONSTER_DATA, ATTACK_DATA
from random import randint

class Monster:
	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 3: Build __init__                      │
	# │ Hint: MONSTER_DATA[name]['stats'] gives you the stats   │
	# │       dict. Use it to set element, base_stats, health,  │
	# │       energy, and abilities.                            │
	# └─────────────────────────────────────────────────────────┘
	def __init__(self, name, level):
		# Store name and level
		# TODO: your code here
		pass  # remove this when you're done

		# This monster can be paused (frozen) during battle
		# TODO: self.paused = False

		# Load stats from MONSTER_DATA
		# TODO: self.element = MONSTER_DATA[name]['stats']['element']
		# TODO: self.base_stats = MONSTER_DATA[name]['stats']

		# Current health = max_health * level  (stats scale with level!)
		# TODO: self.health = ...
		# TODO: self.energy = ...

		# Initiative tracks whose turn it is (0 to 100)
		# TODO: self.initiative = 0

		# Abilities dict: {min_level: 'attack_name'}
		# TODO: self.abilities = MONSTER_DATA[name]['abilities']

		# Defending flag (set when the monster uses Defend action)
		# TODO: self.defending = False

		# XP tracking
		# TODO: self.xp = 0
		# TODO: self.level_up = level * 150   (XP needed to reach next level)

		# Evolution data: None or ('EvolvedName', level_needed)
		# TODO: self.evolution = MONSTER_DATA[self.name]['evolve']

	# ┌─────────────────────────────────────────────────────────┐
	# │ PRE-SCAFFOLD — teacher walks through this, you use it   │
	# └─────────────────────────────────────────────────────────┘
	# __repr__ is what Python prints when you do print(my_monster)
	def __repr__(self):
		return f'monster: {self.name}, lvl: {self.level}'

	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 4: get_stat(stat)                      │
	# │ Hint: multiply base_stats[stat] by level to scale it!  │
	# └─────────────────────────────────────────────────────────┘
	def get_stat(self, stat):
		# Return the stat value scaled by level.
		# Example: base attack of 3 at level 10 = 30
		# TODO: your code here
		pass  # remove this when you're done

	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 5: get_stats()                         │
	# │ Hint: call self.get_stat() for each key. The keys are:  │
	# │       'health', 'energy', 'attack', 'defense',          │
	# │       'speed', 'recovery'                               │
	# └─────────────────────────────────────────────────────────┘
	def get_stats(self):
		# Return a dict with all 6 scaled stats.
		# Used by the monster index screen to draw stat bars.
		# TODO: your code here
		pass  # remove this when you're done

	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 6: get_abilities(include_all=True)     │
	# │ Hint: loop through self.abilities.items() — each item   │
	# │       is (required_level, ability_name).                │
	# │       If include_all=False, also check energy:          │
	# │       ATTACK_DATA[ability]['cost'] < self.energy        │
	# └─────────────────────────────────────────────────────────┘
	def get_abilities(self, include_all=True):
		# Return a list of ability names this monster can currently use.
		# include_all=True  -> all abilities unlocked by level
		# include_all=False -> only abilities the monster has energy for
		# TODO: your code here
		pass  # remove this when you're done

	# ┌─────────────────────────────────────────────────────────┐
	# │ PRE-SCAFFOLD — teacher walks through this, you use it   │
	# └─────────────────────────────────────────────────────────┘
	# get_info returns (current, max) tuples for health, energy, initiative.
	# The battle UI uses this to draw the health bars.
	def get_info(self):
		return (
			(self.health, self.get_stat('max_health')),
			(self.energy, self.get_stat('max_energy')),
			(self.initiative, 100)
		)

	# ┌─────────────────────────────────────────────────────────┐
	# │ PRE-SCAFFOLD — teacher walks through this, you use it   │
	# └─────────────────────────────────────────────────────────┘
	# reduce_energy subtracts the cost of an attack from energy.
	def reduce_energy(self, attack):
		self.energy -= ATTACK_DATA[attack]['cost']

	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 7: get_base_damage(attack)             │
	# │ Hint: use self.get_stat('attack') * ATTACK_DATA amount  │
	# └─────────────────────────────────────────────────────────┘
	def get_base_damage(self, attack):
		# Calculate how much damage this monster deals with an attack.
		# base damage = attack stat * attack's amount multiplier
		# TODO: your code here
		pass  # remove this when you're done

	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 8: update_xp(amount)                   │
	# │ Hint: self.level_up - self.xp is how much XP is left    │
	# │       before the next level. If amount fits, just add   │
	# │       it. If not, level up and carry over the leftover! │
	# └─────────────────────────────────────────────────────────┘
	def update_xp(self, amount):
		# Add XP. Level up if we hit the threshold.
		# Carry over any leftover XP past the level-up point.
		# After levelling up, recalculate self.level_up.
		# TODO: your code here
		pass  # remove this when you're done

	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 9: stat_limiter()                      │
	# │ Hint: use max(0, min(value, max_value)) to clamp.       │
	# │       You need to clamp both health and energy.         │
	# └─────────────────────────────────────────────────────────┘
	def stat_limiter(self):
		# Make sure health and energy never go below 0 or above max.
		# health should stay between 0 and get_stat('max_health')
		# energy should stay between 0 and get_stat('max_energy')
		# TODO: your code here
		pass  # remove this when you're done

	# ┌─────────────────────────────────────────────────────────┐
	# │ PRE-SCAFFOLD — teacher walks through this, you use it   │
	# └─────────────────────────────────────────────────────────┘
	# update is called every frame. It keeps stats in bounds and
	# advances the initiative bar (so faster monsters get turns sooner).
	def update(self, dt):
		self.stat_limiter()
		if not self.paused:
			self.initiative += self.get_stat('speed') * dt

	# ┌─────────────────────────────────────────────────────────┐
	# │ EXTENSION — bonus challenge!                            │
	# │ Ideas: Add is_fainted() -> returns True if health <= 0  │
	# │        Add is_low_energy() -> True if energy < 20%      │
	# │        Add describe() that prints a nice stat summary   │
	# └─────────────────────────────────────────────────────────┘
