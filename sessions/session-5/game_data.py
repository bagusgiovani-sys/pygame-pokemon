# TRAINER_DATA defines all the NPC trainers in the world:
# their dialog, the monsters they carry, and how they behave.

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

# Stats scale with level, so keep the base numbers small — a level 10
# monster with attack 3 hits at 30, not 3.

MONSTER_DATA = {
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

	# Fast and fierce fire type — low defense, high speed and attack.
	'Vulpyre': {
		'stats': {'element': 'fire', 'max_health': 14, 'max_energy': 10,
		          'attack': 5, 'defense': 6, 'recovery': 1.0, 'speed': 2.2},
		'abilities': {0: 'scratch', 5: 'fire'},
		'evolve': None},

	# Magic-user plant type — high energy pool built around healing.
	'Verdil': {
		'stats': {'element': 'plant', 'max_health': 16, 'max_energy': 22,
		          'attack': 2, 'defense': 9, 'recovery': 1.6, 'speed': 1.1},
		'abilities': {0: 'scratch', 5: 'spark', 10: 'heal'},
		'evolve': None},

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

# 'target' is 'opponent' to hurt them, or 'player' to help yourself
# (like heal). 'amount' > 1 means more damage, < 0 means healing.

ATTACK_DATA = {
	'scratch': {'target': 'opponent', 'amount': 1.2,  'cost': 20,  'element': 'normal', 'animation': 'scratch'},
	'fire':    {'target': 'opponent', 'amount': 2,    'cost': 15,  'element': 'fire',   'animation': 'fire'},
	'spark':   {'target': 'opponent', 'amount': 1.1,  'cost': 20,  'element': 'fire',   'animation': 'fire'},
	'heal':    {'target': 'player',   'amount': -1.2, 'cost': 600, 'element': 'plant',  'animation': 'green'},
	'burn':       {'target': 'opponent', 'amount': 2,    'cost': 15,  'element': 'fire',   'animation': 'fire'},
	'battlecry':  {'target': 'player',   'amount': -1.4, 'cost': 20,  'element': 'normal', 'animation': 'green'},
	'splash':     {'target': 'opponent', 'amount': 2,    'cost': 15,  'element': 'water',  'animation': 'splash'},
	'explosion':  {'target': 'opponent', 'amount': 2,    'cost': 90,  'element': 'fire',   'animation': 'explosion'},
	'annihilate': {'target': 'opponent', 'amount': 3,    'cost': 30,  'element': 'fire',   'animation': 'explosion'},
	'ice':        {'target': 'opponent', 'amount': 2,    'cost': 15,  'element': 'water',  'animation': 'ice'},
}
