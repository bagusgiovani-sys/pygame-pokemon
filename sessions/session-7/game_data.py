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

MONSTER_DATA = {
	'Plumette': {
		'stats': {'element': 'plant', 'max_health': 15, 'max_energy': 17,
		          'attack': 4, 'defense': 8, 'recovery': 1, 'speed': 1},
		'abilities': {0: 'scratch', 5: 'spark'}, 'evolve': ('Ivieron', 15)},
	'Ivieron': {
		'stats': {'element': 'plant', 'max_health': 18, 'max_energy': 20,
		          'attack': 5, 'defense': 10, 'recovery': 1.2, 'speed': 1.2},
		'abilities': {0: 'scratch', 5: 'spark'}, 'evolve': ('Pluma', 32)},
	'Pluma': {
		'stats': {'element': 'plant', 'max_health': 23, 'max_energy': 26,
		          'attack': 6, 'defense': 12, 'recovery': 1.8, 'speed': 1.8},
		'abilities': {0: 'scratch', 5: 'spark'}, 'evolve': None},
	'Sparchu': {
		'stats': {'element': 'fire', 'max_health': 15, 'max_energy': 7,
		          'attack': 3, 'defense': 8, 'recovery': 1.1, 'speed': 1},
		'abilities': {0: 'scratch', 5: 'fire', 15: 'battlecry', 26: 'explosion'},
		'evolve': ('Cindrill', 15)},
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

	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 1: Add your own custom monster!        │
	# │ Hint: pick a theme — volcano creature? leaf sprite?     │
	# │       tide pool creature? Name it something memorable.  │
	# │       Stats: attack 1-6, defense 5-15, health 10-30,    │
	# │       energy 5-25, speed 1.0-3.0, recovery 1.0-2.5     │
	# └─────────────────────────────────────────────────────────┘
	# Replace 'YourMonsterName' with your monster's name.
	# Replace all ??? with real numbers.
	'YourMonsterName': {       # TODO: replace with your monster's real name!
		'stats': {
			'element': '???',      # TODO: 'fire', 'water', or 'plant'
			'max_health': ???,     # TODO: 10-30
			'max_energy': ???,     # TODO: 5-25
			'attack': ???,         # TODO: 1-6
			'defense': ???,        # TODO: 5-15
			'recovery': ???,       # TODO: 1.0-2.5 (how fast energy refills)
			'speed': ???},         # TODO: 1.0-3.0 (how fast initiative fills)
		'abilities': {0: 'scratch', 5: '???'},  # TODO: pick a second ability
		'evolve': None},           # TODO: or ('EvolvedName', level) for an evolution!

	# ┌─────────────────────────────────────────────────────────┐
	# │ EXTENSION — bonus challenge!                            │
	# │ Ideas: Add an evolved form for your monster             │
	# │        Add a second evolution stage (3-stage chain)     │
	# │        Create a water-type AND fire-type custom monster │
	# └─────────────────────────────────────────────────────────┘
	# 'YourEvolvedMonster': {
	#     'stats': {'element': '???', 'max_health': ???, ...},
	#     'abilities': {0: 'scratch', 5: '???', 15: '???'},
	#     'evolve': None},
}

ATTACK_DATA = {
	'burn':       {'target': 'opponent', 'amount': 2,    'cost': 15,  'element': 'fire',   'animation': 'fire'},
	'heal':       {'target': 'player',   'amount': -1.2, 'cost': 600, 'element': 'plant',  'animation': 'green'},
	'battlecry':  {'target': 'player',   'amount': -1.4, 'cost': 20,  'element': 'normal', 'animation': 'green'},
	'spark':      {'target': 'opponent', 'amount': 1.1,  'cost': 20,  'element': 'fire',   'animation': 'fire'},
	'scratch':    {'target': 'opponent', 'amount': 1.2,  'cost': 20,  'element': 'normal', 'animation': 'scratch'},
	'splash':     {'target': 'opponent', 'amount': 2,    'cost': 15,  'element': 'water',  'animation': 'splash'},
	'fire':       {'target': 'opponent', 'amount': 2,    'cost': 15,  'element': 'fire',   'animation': 'fire'},
	'explosion':  {'target': 'opponent', 'amount': 2,    'cost': 90,  'element': 'fire',   'animation': 'explosion'},
	'annihilate': {'target': 'opponent', 'amount': 3,    'cost': 30,  'element': 'fire',   'animation': 'explosion'},
	'ice':        {'target': 'opponent', 'amount': 2,    'cost': 15,  'element': 'water',  'animation': 'ice'},
}
