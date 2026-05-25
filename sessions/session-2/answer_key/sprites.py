import pygame
from pygame.math import Vector2 as vector
from random import uniform
from settings import WORLD_LAYERS, ANIMATION_SPEED

# ┌─────────────────────────────────────────────────────────┐
# │ PRE-SCAFFOLD — teacher walks through this, you use it   │
# │                                                         │
# │ sprites.py has two sections:                            │
# │   OVERWORLD SPRITES — you build today (steps 10-12)     │
# │   BATTLE SPRITES    — pre-scaffolded in session 5       │
# │                                                         │
# │ Every overworld sprite inherits from pygame.sprite.Sprite│
# │ (via our Sprite base class). The key attributes are:    │
# │   self.image  — the Surface pygame draws                │
# │   self.rect   — where to draw it (position + size)      │
# │   self.hitbox — the collision area (often smaller)      │
# │   self.z      — drawing layer (see WORLD_LAYERS)        │
# │   self.y_sort — used to sort which entity draws on top  │
# └─────────────────────────────────────────────────────────┘

# --------------- OVERWORLD SPRITES ---------------

# ┌─────────────────────────────────────────────────────────┐
# │ YOUR CODE — Step 10: Sprite (base overworld sprite)     │
# │ Write the __init__ method:                              │
# │   def __init__(self, pos, surf, groups,                 │
# │                z=WORLD_LAYERS['bg']):                   │
# │     super().__init__(groups)                            │
# │     self.image  = surf                                  │
# │     self.rect   = self.image.get_frect(topleft=pos)     │
# │     self.hitbox = self.rect.copy()                      │
# │     self.y_sort = self.rect.centery                     │
# │     self.z      = z                                     │
# └─────────────────────────────────────────────────────────┘
class Sprite(pygame.sprite.Sprite):
	def __init__(self, pos, surf, groups, z=WORLD_LAYERS['bg']):
		super().__init__(groups)
		self.image = surf
		self.rect = self.image.get_frect(topleft=pos)
		self.hitbox = self.rect.copy()
		self.y_sort = self.rect.centery
		self.z = z


# ┌─────────────────────────────────────────────────────────┐
# │ YOUR CODE — Step 11: BorderSprite                       │
# │ Borders are invisible walls that block movement.        │
# │ They use the FULL rect as the hitbox (unlike regular    │
# │ sprites which might shrink the hitbox).                 │
# │                                                         │
# │ def __init__(self, pos, surf, groups):                  │
# │     super().__init__(groups)                            │
# │     self.image  = surf                                  │
# │     self.rect   = self.image.get_frect(topleft=pos)     │
# │     self.hitbox = self.rect.copy()                      │
# └─────────────────────────────────────────────────────────┘
class BorderSprite(pygame.sprite.Sprite):
	def __init__(self, pos, surf, groups):
		super().__init__(groups)
		self.image = surf
		self.rect = self.image.get_frect(topleft=pos)
		self.hitbox = self.rect.copy()
		self.z = WORLD_LAYERS['bg']
		self.y_sort = self.rect.centery


# ┌─────────────────────────────────────────────────────────┐
# │ YOUR CODE — Step 12: CollidableSprite                   │
# │ These are solid objects (trees, fences, buildings).     │
# │ The hitbox is SMALLER than the image so the player can  │
# │ walk right up to the base of an object realistically.   │
# │                                                         │
# │ def __init__(self, pos, surf, groups):                  │
# │     super().__init__(groups)                            │
# │     self.image  = surf                                  │
# │     self.rect   = self.image.get_frect(topLeft=pos)     │
# │     self.hitbox = self.rect.inflate(-10, -10)           │
# │ Hint: inflate(-10, -10) shrinks by 10 px on each side.  │
# └─────────────────────────────────────────────────────────┘
class CollidableSprite(pygame.sprite.Sprite):
	def __init__(self, pos, surf, groups):
		super().__init__(groups)
		self.image = surf
		self.rect = self.image.get_frect(topleft=pos)
		self.hitbox = self.rect.inflate(-10, -10)
		self.z = WORLD_LAYERS['main']
		self.y_sort = self.rect.centery


# ┌─────────────────────────────────────────────────────────┐
# │ PRE-SCAFFOLD — teacher walks through this, you use it   │
# │                                                         │
# │ AnimatedSprite loops through a list of frames each      │
# │ frame, giving the illusion of movement (water ripples,  │
# │ flickering fire, etc.).                                  │
# │ You will write this yourself in session 3!              │
# └─────────────────────────────────────────────────────────┘
class AnimatedSprite(pygame.sprite.Sprite):
	def __init__(self, pos, frames, groups, z=WORLD_LAYERS['main']):
		self.frame_index = 0
		self.frames      = frames
		super().__init__(groups)
		self.image  = self.frames[0]
		self.rect   = self.image.get_frect(topleft=pos)
		self.z      = z
		self.hitbox = self.rect.copy()
		self.y_sort = self.rect.centery

	def animate(self, dt):
		self.frame_index += ANIMATION_SPEED * dt
		self.image = self.frames[int(self.frame_index % len(self.frames))]

	def update(self, dt):
		self.animate(dt)


# ┌─────────────────────────────────────────────────────────┐
# │ PRE-SCAFFOLD — teacher walks through this, you use it   │
# │                                                         │
# │ MonsterPatchSprite marks grass patches where monsters   │
# │ can appear. It stores biome (grass, sand, etc.) and     │
# │ which monsters can appear here.                         │
# └─────────────────────────────────────────────────────────┘
class MonsterPatchSprite(AnimatedSprite):
	def __init__(self, pos, frames, groups, biome, monsters, level):
		z = WORLD_LAYERS['main'] if biome != 'sand' else WORLD_LAYERS['bg']
		super().__init__(pos, frames, groups, z)
		self.y_sort -= 40
		self.biome    = biome
		self.monsters = monsters.split(',') if isinstance(monsters, str) else monsters
		self.level    = level


# ┌─────────────────────────────────────────────────────────┐
# │ PRE-SCAFFOLD — teacher walks through this, you use it   │
# │                                                         │
# │ TransitionSprite is an invisible trigger zone.          │
# │ When the player steps on it, the game loads a new map.  │
# │ self.target stores (map_name, spawn_point) as a tuple.  │
# └─────────────────────────────────────────────────────────┘
class TransitionSprite(pygame.sprite.Sprite):
	def __init__(self, pos, size, target, groups):
		super().__init__(groups)
		surf         = pygame.Surface(size)
		self.image   = surf
		self.rect    = self.image.get_frect(topleft=pos)
		self.target  = target
		self.hitbox  = self.rect.copy()
		self.z       = WORLD_LAYERS['bg']
		self.y_sort  = self.rect.centery


# ┌─────────────────────────────────────────────────────────┐
# │ PRE-SCAFFOLD — battle sprites come in session 5         │
# │ (MonsterSprite, MonsterOutlineSprite, etc.)             │
# └─────────────────────────────────────────────────────────┘

# ┌─────────────────────────────────────────────────────────┐
# │ EXTENSION — bonus challenge!                            │
# │ Ideas: Add a second coloured square as an obstacle      │
# │        in main.py using CollidableSprite, then walk     │
# │        into it. Does the collision feel right?          │
# │        Try changing the inflate values in               │
# │        CollidableSprite and see how it affects gameplay.│
# └─────────────────────────────────────────────────────────┘
