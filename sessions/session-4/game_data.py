# ┌─────────────────────────────────────────────────────────┐
# │ PRE-SCAFFOLD — teacher walks through this, you use it   │
# └─────────────────────────────────────────────────────────┘
# TRAINER_DATA defines all the NPC trainers in the world:
# their dialog, the monsters they carry, and how they behave.
# This is pre-written because there is a LOT of it — study the
# format so you understand how the game connects data to characters!

TRAINER_DATA = {
	'o1': {
		'monsters': {0: ('Jacana', 14), 1: ('Cleaf', 15)},
		'dialog': {'default': ['Hey, how are you?', 'Oh, so you want to fight?', 'FIGHT!'], 'defeated': ['You are very strong!', "Let's fight again sometime?"]},
		'directions': ['down'], 'look_around': True, 'defeated': False, 'biome': 'forest'},
	'o2': {
		'monsters': {0: ('Atrox', 14), 1: ('Pouch', 15), 2: ('Draem', 13), 3: ('Cindrill', 13)},
		'dialog': {'default': ["I don't like sand", "It's coarse and rough", 'oh god, fight'], 'defeated': ['May the force be with you']},
		'directions': ['left', 'down'], 'look_around': False, 'defeated': False, 'biome': 'sand'},
	'o3': {
		'monsters': {0: ('Atrox', 14), 1: ('Pouch', 15), 2: ('Draem', 13), 3: ('Cindrill', 13)},
		'dialog': {'default': ['I love skating!', 'FIGHT!'], 'defeated': ['Good luck with the boss', "It's so cold in here"]},
		'directions': ['left', 'right', 'up', 'down'], 'look_around': True, 'defeated': False, 'biome': 'sand'},
	'Nurse': {
		'direction': 'down', 'radius': 0, 'look_around': False,
		'dialog': {'default': ['Welcome to the hospital', 'Your monsters have been healed'], 'defeated': None},
		'directions': ['down'], 'defeated': False, 'biome': None}
}

# ============================================================
# ┌─────────────────────────────────────────────────────────┐
# │ YOUR CODE — Step 1: Design your own monsters!           │
# │ Hint: stats scale with level — keep numbers small!      │
# │       attack 1-6, defense 5-15, health 10-30 is good.  │
# └─────────────────────────────────────────────────────────┘

# Here are two monsters already filled in — study their structure.
# Then add TWO more of your own below (find the ??? placeholders).

MONSTER_DATA = {
	# --- Pre-filled examples: study these! ---
	'Sparchu': {
		'stats': {'element': 'fire', 'max_health': 15, 'max_energy': 7,
		          'attack': 3, 'defense': 8, 'recovery': 1.1, 'speed': 1},
		'abilities': {0: 'scratch', 5: 'fire', 15: 'battlecry', 26: 'explosion'},
		'evolve': ('Cindrill', 15)},
	'Ivieron': {
		'stats': {'element': 'plant', 'max_health': 18, 'max_energy': 20,
		          'attack': 5, 'defense': 10, 'recovery': 1.2, 'speed': 1.2},
		'abilities': {0: 'scratch', 5: 'spark'},
		'evolve': ('Pluma', 32)},
	'Finsta': {
		'stats': {'element': 'water', 'max_health': 13, 'max_energy': 17,
		          'attack': 2, 'defense': 8, 'recovery': 1.5, 'speed': 1.8},
		'abilities': {0: 'scratch', 5: 'spark', 15: 'splash', 20: 'ice', 25: 'heal'},
		'evolve': ('Gulfin', 34)},
	'Gulfin': {
		'stats': {'element': 'water', 'max_health': 18, 'max_energy': 20,
		          'attack': 3, 'defense': 10, 'recovery': 1.8, 'speed': 2},
		'abilities': {0: 'scratch', 5: 'spark', 15: 'splash', 20: 'ice', 25: 'heal'},
		'evolve': ('Finiette', 45)},

	# --- YOUR TWO CUSTOM MONSTERS: fill in the ??? values! ---
	# Monster 1: a fire-type creature.
	# Think about its personality — is it fast and fierce, or slow and tough?
	'MyFireMonster': {           # TODO: replace 'MyFireMonster' with a cool name!
		'stats': {
			'element': 'fire',
			'max_health': 10,     # TODO: pick a number, 10-30 (this is just a placeholder)
			'max_energy': 5,      # TODO: pick a number, 5-25
			'attack': 1,          # TODO: pick a number, 1-6
			'defense': 5,         # TODO: pick a number, 5-15
			'recovery': 1.0,      # TODO: pick a float like 1.0 or 1.5
			'speed': 1.0},        # TODO: pick a float like 1.0 or 2.0
		'abilities': {0: 'scratch', 5: 'fire'},  # unlocks 'fire' at level 5
		'evolve': None},          # TODO: change to ('EvolvedName', level) if you want an evolution!

	# Monster 2: a plant-type creature.
	'MyPlantMonster': {          # TODO: replace 'MyPlantMonster' with a cool name!
		'stats': {
			'element': 'plant',
			'max_health': 10,     # TODO: pick a number (this is just a placeholder)
			'max_energy': 5,      # TODO: pick a number
			'attack': 1,          # TODO: pick a number
			'defense': 5,         # TODO: pick a number
			'recovery': 1.0,      # TODO: pick a float
			'speed': 1.0},        # TODO: pick a float
		'abilities': {0: 'scratch', 5: 'spark', 10: 'heal'},
		'evolve': None},          # TODO: or add ('EvolvedName', level)

	# ┌─────────────────────────────────────────────────────────┐
	# │ PRE-SCAFFOLD — the rest of the monsters are pre-added   │
	# │ so the full game world works. Study the format!         │
	# └─────────────────────────────────────────────────────────┘
	'Plumette': {
		'stats': {'element': 'plant', 'max_health': 15, 'max_energy': 17,
		          'attack': 4, 'defense': 8, 'recovery': 1, 'speed': 1},
		'abilities': {0: 'scratch', 5: 'spark'}, 'evolve': ('Ivieron', 15)},
	'Pluma': {
		'stats': {'element': 'plant', 'max_health': 23, 'max_energy': 26,
		          'attack': 6, 'defense': 12, 'recovery': 1.8, 'speed': 1.8},
		'abilities': {0: 'scratch', 5: 'spark'}, 'evolve': None},
	'Cindrill': {
		'stats': {'element': 'fire', 'max_health': 18, 'max_energy': 10,
		          'attack': 3.5, 'defense': 10, 'recovery': 1.2, 'speed': 1.1},
		'abilities': {0: 'scratch', 5: 'fire', 15: 'battlecry', 26: 'explosion'},
		'evolve': ('Charmadillo', 33)},
	'Charmadillo': {
		'stats': {'element': 'fire', 'max_health': 29, 'max_energy': 12,
		          'attack': 4, 'defense': 17, 'recovery': 1.35, 'speed': 1.1},
		'abilities': {0: 'scratch', 5: 'fire', 15: 'battlecry', 26: 'explosion', 45: 'annihilate'},
		'evolve': None},
	'Finiette': {
		'stats': {'element': 'water', 'max_health': 27, 'max_energy': 23,
		          'attack': 4, 'defense': 17, 'recovery': 2, 'speed': 2.5},
		'abilities': {0: 'scratch', 5: 'spark', 15: 'splash', 20: 'ice', 25: 'heal'},
		'evolve': None},
	'Atrox': {
		'stats': {'element': 'fire', 'max_health': 18, 'max_energy': 20,
		          'attack': 3, 'defense': 10, 'recovery': 1.3, 'speed': 1.9},
		'abilities': {0: 'scratch', 5: 'spark', 30: 'fire'}, 'evolve': None},
	'Pouch': {
		'stats': {'element': 'plant', 'max_health': 23, 'max_energy': 25,
		          'attack': 4, 'defense': 12, 'recovery': 1, 'speed': 1.5},
		'abilities': {0: 'scratch', 5: 'spark', 25: 'heal'}, 'evolve': None},
	'Draem': {
		'stats': {'element': 'plant', 'max_health': 23, 'max_energy': 25,
		          'attack': 4, 'defense': 12, 'recovery': 1.2, 'speed': 1.4},
		'abilities': {0: 'scratch', 5: 'heal', 20: 'explosion', 25: 'splash'},
		'evolve': None},
	'Larvea': {
		'stats': {'element': 'plant', 'max_health': 15, 'max_energy': 17,
		          'attack': 1, 'defense': 8, 'recovery': 1, 'speed': 1},
		'abilities': {0: 'scratch', 5: 'spark'}, 'evolve': ('Cleaf', 4)},
	'Cleaf': {
		'stats': {'element': 'plant', 'max_health': 18, 'max_energy': 20,
		          'attack': 3, 'defense': 10, 'recovery': 1.7, 'speed': 1.6},
		'abilities': {0: 'scratch', 5: 'heal'}, 'evolve': None},
	'Jacana': {
		'stats': {'element': 'fire', 'max_health': 12, 'max_energy': 19,
		          'attack': 3, 'defense': 10, 'recovery': 2.1, 'speed': 2.6},
		'abilities': {0: 'scratch', 5: 'spark', 15: 'burn', 20: 'explosion', 25: 'heal'},
		'evolve': None},
	'Friolera': {
		'stats': {'element': 'water', 'max_health': 13, 'max_energy': 20,
		          'attack': 4, 'defense': 6, 'recovery': 1.3, 'speed': 2},
		'abilities': {0: 'scratch', 5: 'spark', 15: 'splash', 20: 'ice', 25: 'heal'},
		'evolve': None},
}

# ============================================================
# ┌─────────────────────────────────────────────────────────┐
# │ YOUR CODE — Step 2: Design your attacks!                │
# │ Hint: 'target' is 'opponent' to hurt them,              │
# │       or 'player' to help yourself (like heal).         │
# │       amount > 1 means more damage, < 0 means healing. │
# └─────────────────────────────────────────────────────────┘

# Two attacks are pre-filled. Fill in 'spark' and 'heal'.
# Then the full list is pre-added below so the game works.

ATTACK_DATA = {
	# --- Pre-filled examples ---
	'scratch': {'target': 'opponent', 'amount': 1.2,  'cost': 20,  'element': 'normal', 'animation': 'scratch'},
	'fire':    {'target': 'opponent', 'amount': 2,    'cost': 15,  'element': 'fire',   'animation': 'fire'},

	# --- YOUR ATTACKS: fill in the ??? values! ---
	# 'spark' is a fire attack that does moderate damage.
	'spark': {
		'target': 'opponent', # TODO: 'opponent' or 'player'? (this is just a placeholder)
		'amount': 1.0,        # TODO: how much damage? (1.0 to 3.0)
		'cost': 10,           # TODO: energy cost (10 to 100)
		'element': 'normal',  # TODO: 'fire', 'water', 'plant', or 'normal'
		'animation': 'fire'  # this stays as 'fire' — uses fire animation
	},

	# 'heal' restores health to your own monster.
	# Tip: use a negative amount (like -1.2) to restore health!
	'heal': {
		'target': 'opponent', # TODO: healing goes to 'player', not 'opponent'! (this is just a placeholder)
		'amount': 1.0,        # TODO: use a negative float like -1.2 to restore health
		'cost': 10,           # TODO: healing costs a lot of energy — try 600
		'element': 'plant',  # healing is plant-type
		'animation': 'green'
	},

	# ┌─────────────────────────────────────────────────────────┐
	# │ PRE-SCAFFOLD — remaining attacks pre-added for the game │
	# └─────────────────────────────────────────────────────────┘
	'burn':       {'target': 'opponent', 'amount': 2,    'cost': 15,  'element': 'fire',   'animation': 'fire'},
	'battlecry':  {'target': 'player',   'amount': -1.4, 'cost': 20,  'element': 'normal', 'animation': 'green'},
	'splash':     {'target': 'opponent', 'amount': 2,    'cost': 15,  'element': 'water',  'animation': 'splash'},
	'explosion':  {'target': 'opponent', 'amount': 2,    'cost': 90,  'element': 'fire',   'animation': 'explosion'},
	'annihilate': {'target': 'opponent', 'amount': 3,    'cost': 30,  'element': 'fire',   'animation': 'explosion'},
	'ice':        {'target': 'opponent', 'amount': 2,    'cost': 15,  'element': 'water',  'animation': 'ice'},
}
