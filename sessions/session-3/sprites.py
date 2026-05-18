import pygame
from pygame.math import Vector2 as vector
from random import uniform
from settings import WORLD_LAYERS, ANIMATION_SPEED

# ┌─────────────────────────────────────────────────────────┐
# │ PRE-SCAFFOLD — teacher walks through this, you use it   │
# │                                                         │
# │ Session 2 sprites (Sprite, BorderSprite, CollidableSprite│
# │ are complete below — you wrote those last time.         │
# │                                                         │
# │ New this session (steps 14-16):                         │
# │   AnimatedSprite    — water, coast effects              │
# │   MonsterPatchSprite — grass/sand encounter zones       │
# │   TransitionSprite  — doorways between maps             │
# └─────────────────────────────────────────────────────────┘

# --------------- OVERWORLD SPRITES (session 2 — complete) ---------------

class Sprite(pygame.sprite.Sprite):
	def __init__(self, pos, surf, groups, z=WORLD_LAYERS['bg']):
		super().__init__(groups)
		self.image  = surf
		self.rect   = self.image.get_frect(topleft=pos)
		self.hitbox = self.rect.copy()
		self.y_sort = self.rect.centery
		self.z      = z


class BorderSprite(pygame.sprite.Sprite):
	def __init__(self, pos, surf, groups):
		super().__init__(groups)
		self.image  = surf
		self.rect   = self.image.get_frect(topleft=pos)
		self.hitbox = self.rect.copy()


class CollidableSprite(pygame.sprite.Sprite):
	def __init__(self, pos, surf, groups):
		super().__init__(groups)
		self.image  = surf
		self.rect   = self.image.get_frect(topleft=pos)
		self.hitbox = self.rect.inflate(-10, -10)


# --------------- NEW SESSION 3 SPRITES ---------------

# ┌─────────────────────────────────────────────────────────┐
# │ YOUR CODE — Step 14: AnimatedSprite                     │
# │ This sprite cycles through a list of frames to create   │
# │ animation (water ripples, coast foam, etc.).            │
# │                                                         │
# │ __init__(self, pos, frames, groups,                     │
# │           z=WORLD_LAYERS['main']):                      │
# │   Store frames list and set frame_index = 0.            │
# │   Call super().__init__(groups).                        │
# │   self.image  = self.frames[0]                          │
# │   self.rect   = self.image.get_frect(topleft=pos)       │
# │   self.z      = z                                       │
# │   self.hitbox = self.rect.copy()                        │
# │   self.y_sort = self.rect.centery                       │
# │                                                         │
# │ animate(self, dt):                                      │
# │   self.frame_index += ANIMATION_SPEED * dt              │
# │   self.image = self.frames[                             │
# │       int(self.frame_index % len(self.frames))]         │
# │                                                         │
# │ update(self, dt):                                       │
# │   self.animate(dt)                                      │
# └─────────────────────────────────────────────────────────┘
class AnimatedSprite(pygame.sprite.Sprite):
	def __init__(self, pos, frames, groups, z=WORLD_LAYERS['main']):
		# TODO: your code here
		pass  # remove this when you're done

	def animate(self, dt):
		# TODO: your code here
		pass  # remove this when you're done

	def update(self, dt):
		# TODO: your code here
		pass  # remove this when you're done


# ┌─────────────────────────────────────────────────────────┐
# │ YOUR CODE — Step 15: MonsterPatchSprite                 │
# │ Inherits from AnimatedSprite. This is the tall grass    │
# │ or sand patch where wild monsters appear.               │
# │                                                         │
# │ __init__(self, pos, frames, groups, biome,              │
# │           monsters, level):                             │
# │   1. Choose z layer:                                    │
# │        z = WORLD_LAYERS['main'] if biome != 'sand'      │
# │            else WORLD_LAYERS['bg']                      │
# │   2. Call super().__init__(pos, frames, groups, z)      │
# │   3. self.y_sort -= 40  (push back in draw order)       │
# │   4. self.biome    = biome                              │
# │   5. self.monsters = monsters.split(',')                │
# │        (monsters is a comma-separated string like       │
# │         'Sparchu,Cindrill')                             │
# │   6. self.level = level                                 │
# └─────────────────────────────────────────────────────────┘
class MonsterPatchSprite(AnimatedSprite):
	def __init__(self, pos, frames, groups, biome, monsters, level):
		# TODO: your code here
		pass  # remove this when you're done


# ┌─────────────────────────────────────────────────────────┐
# │ YOUR CODE — Step 16: TransitionSprite                   │
# │ An invisible zone that teleports the player to a new    │
# │ area when they walk over it.                            │
# │                                                         │
# │ __init__(self, pos, size, target, groups):              │
# │   super().__init__(groups)                              │
# │   surf          = pygame.Surface(size)                  │
# │   self.image    = surf                                  │
# │   self.rect     = self.image.get_frect(topleft=pos)     │
# │   self.target   = target   ← stores the destination!   │
# │   self.hitbox   = self.rect.copy()                      │
# │   self.z        = WORLD_LAYERS['bg']                    │
# │   self.y_sort   = self.rect.centery                     │
# │ Hint: target is a tuple (map_name, spawn_point) passed  │
# │ in from the TMX file. main.py reads it during setup.    │
# └─────────────────────────────────────────────────────────┘
class TransitionSprite(pygame.sprite.Sprite):
	def __init__(self, pos, size, target, groups):
		# TODO: your code here
		pass  # remove this when you're done


# ┌─────────────────────────────────────────────────────────┐
# │ PRE-SCAFFOLD — battle sprites section (session 5)       │
# │ MonsterSprite, MonsterOutlineSprite, MonsterNameSprite, │
# │ MonsterLevelSprite, MonsterStatsSprite, AttackSprite,   │
# │ TimedSprite all come in session 5.                      │
# └─────────────────────────────────────────────────────────┘

# ┌─────────────────────────────────────────────────────────┐
# │ EXTENSION — bonus challenge!                            │
# │ Ideas: Give AnimatedSprite a random starting frame_index│
# │        so all water tiles don't ripple in sync:         │
# │          from random import uniform                     │
# │          self.frame_index = uniform(0, len(frames))     │
# │        Try changing ANIMATION_SPEED in settings.py and  │
# │        watch the water speed up or slow down.           │
# └─────────────────────────────────────────────────────────┘
