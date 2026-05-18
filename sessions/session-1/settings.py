from pygame.math import Vector2 as vector

# ┌─────────────────────────────────────────────────────────┐
# │ PRE-SCAFFOLD — teacher walks through this, you use it   │
# │                                                         │
# │ Constants are names for fixed values we use everywhere. │
# │ Instead of typing 1280 in 50 places, we write           │
# │ WINDOW_WIDTH once and use the name. Easy to change!     │
# └─────────────────────────────────────────────────────────┘

# ┌─────────────────────────────────────────────────────────┐
# │ YOUR CODE — Step 1: Define the four game constants      │
# │ Hint: Replace each ??? with the correct number.         │
# │   WINDOW_WIDTH  = 1280  (pixels wide)                   │
# │   WINDOW_HEIGHT = 720   (pixels tall)                   │
# │   TILE_SIZE     = 64    (one map tile in pixels)        │
# │   ANIMATION_SPEED = 6   (frames per second of animation)│
# └─────────────────────────────────────────────────────────┘

WINDOW_WIDTH  = ???
WINDOW_HEIGHT = ???
TILE_SIZE     = ???
ANIMATION_SPEED = ???

# ┌─────────────────────────────────────────────────────────┐
# │ PRE-SCAFFOLD — teacher walks through this, you use it   │
# │                                                         │
# │ COLORS is a dictionary of hex color codes used          │
# │ throughout the game. Instead of memorising '#f4fefa'    │
# │ we just write COLORS['white']. Pygame accepts both.     │
# └─────────────────────────────────────────────────────────┘

COLORS = {
	'white':      '#f4fefa',
	'pure white': '#ffffff',
	'dark':       '#2b292c',
	'light':      '#c8c8c8',
	'gray':       '#3a373b',
	'gold':       '#ffd700',
	'light-gray': '#4b484d',
	'fire':       '#f8a060',
	'water':      '#50b0d8',
	'plant':      '#64a990',
	'black':      '#000000',
	'red':        '#f03131',
	'blue':       '#66d7ee',
	'normal':     '#ffffff',
	'dark white': '#f0f0f0',
}

# ┌─────────────────────────────────────────────────────────┐
# │ PRE-SCAFFOLD — teacher walks through this, you use it   │
# │                                                         │
# │ WORLD_LAYERS controls drawing order — higher number =   │
# │ drawn on top. Water goes behind everything (0), while   │
# │ 'top' layer (4) goes in front of the player.            │
# └─────────────────────────────────────────────────────────┘

WORLD_LAYERS = {
	'water':  0,
	'bg':     1,
	'shadow': 2,
	'main':   3,
	'top':    4,
}

# ┌─────────────────────────────────────────────────────────┐
# │ PRE-SCAFFOLD — teacher walks through this, you use it   │
# │                                                         │
# │ Everything below is used in sessions 5-6 for battle UI. │
# │ You don't need to change anything here — just know it   │
# │ exists so the later imports don't confuse you.          │
# └─────────────────────────────────────────────────────────┘

BATTLE_POSITIONS = {
	'left': {
		'top':    (360, 260),
		'center': (190, 400),
		'bottom': (410, 520),
	},
	'right': {
		'top':    (900, 260),
		'center': (1110, 390),
		'bottom': (900, 550),
	},
}

BATTLE_LAYERS = {
	'outline': 0,
	'name':    1,
	'monster': 2,
	'effects': 3,
	'overlay': 4,
}

BATTLE_CHOICES = {
	'full': {
		'fight':  {'pos': vector(30, -60), 'icon': 'sword'},
		'defend': {'pos': vector(40, -20), 'icon': 'shield'},
		'switch': {'pos': vector(40,  20), 'icon': 'arrows'},
		'catch':  {'pos': vector(30,  60), 'icon': 'hand'},
	},
	'limited': {
		'fight':  {'pos': vector(30, -40), 'icon': 'sword'},
		'defend': {'pos': vector(40,   0), 'icon': 'shield'},
		'switch': {'pos': vector(30,  40), 'icon': 'arrows'},
	},
}

# ┌─────────────────────────────────────────────────────────┐
# │ EXTENSION — bonus challenge!                            │
# │ Ideas: Add your own color (any hex code you like),      │
# │        change ANIMATION_SPEED and see what happens,     │
# │        try WINDOW_WIDTH = 800 for a smaller window.     │
# └─────────────────────────────────────────────────────────┘
