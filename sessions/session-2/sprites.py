import pygame
from settings import WORLD_LAYERS, ANIMATION_SPEED

# ┌─────────────────────────────────────────────────────────┐
# │ SESSION 2 — STUDENT FILE                                │
# │ This file defines normal world sprites.                  │
# │ For Session 2, focus on:                                │
# │   Sprite = visible thing                                │
# │   CollidableSprite = visible thing that blocks player   │
# │ We keep other classes as pre-scaffold for later sessions│
# │ so imports do not break when the project grows.         │
# └─────────────────────────────────────────────────────────┘


class Sprite(pygame.sprite.Sprite):
	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 10: Sprite.__init__                    │
	# │ A basic visible sprite needs:                           │
	# │   image, rect, hitbox, z, y_sort                         │
	# │ z controls layer. y_sort controls draw order.            │
	# └─────────────────────────────────────────────────────────┘
	def __init__(self, pos, surf, groups, z=WORLD_LAYERS['bg']):
		# TODO: your code here
		pass  # remove this when you're done


class CollidableSprite(pygame.sprite.Sprite):
	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 11: CollidableSprite.__init__           │
	# │ Same as Sprite, but it also goes into collision_sprites.│
	# │ The hitbox is slightly smaller so collision feels better│
	# │ when the player touches rocks/walls. z is always 'main'.│
	# └─────────────────────────────────────────────────────────┘
	def __init__(self, pos, surf, groups):
		# TODO: your code here
		pass  # remove this when you're done


# ┌─────────────────────────────────────────────────────────┐
# │ PRE-SCAFFOLD — AnimatedSprite is for later sessions      │
# │ It is already complete so Session 3/4 imports stay safe. │
# └─────────────────────────────────────────────────────────┘
class AnimatedSprite(Sprite):
	def __init__(self, pos, frames, groups, z=WORLD_LAYERS['main']):
		self.frames = frames
		self.frame_index = 0
		super().__init__(pos, self.frames[self.frame_index], groups, z)

	def animate(self, dt):
		self.frame_index += ANIMATION_SPEED * dt
		self.image = self.frames[int(self.frame_index % len(self.frames))]

	def update(self, dt):
		self.animate(dt)


# ┌─────────────────────────────────────────────────────────┐
# │ PRE-SCAFFOLD — BorderSprite kept for compatibility       │
# │ In this updated Session 2, we use visible CollidableSprite│
# │ walls instead of invisible BorderSprite walls.           │
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
# │ PRE-SCAFFOLD — Used in later sessions                    │
# └─────────────────────────────────────────────────────────┘
class MonsterPatchSprite(AnimatedSprite):
	def __init__(self, pos, frames, groups, biome, monsters, level):
		z = WORLD_LAYERS['main'] if biome != 'sand' else WORLD_LAYERS['bg']
		super().__init__(pos, frames, groups, z)
		self.y_sort -= 40
		self.biome = biome
		self.monsters = monsters.split(',') if isinstance(monsters, str) else monsters
		self.level = level


class TransitionSprite(pygame.sprite.Sprite):
	def __init__(self, pos, size, target, groups):
		super().__init__(groups)
		surf = pygame.Surface(size)
		self.image = surf
		self.rect = self.image.get_frect(topleft=pos)
		self.target = target
		self.hitbox = self.rect.copy()
		self.z = WORLD_LAYERS['bg']
		self.y_sort = self.rect.centery


# ┌─────────────────────────────────────────────────────────┐
# │ PRE-SCAFFOLD — Battle sprites come in Session 5          │
# └─────────────────────────────────────────────────────────┘
