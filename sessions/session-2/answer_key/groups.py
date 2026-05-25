import pygame
from pygame.math import Vector2 as vector
from settings import WORLD_LAYERS, BATTLE_LAYERS, WINDOW_WIDTH, WINDOW_HEIGHT
from support import import_image
from entities import Entity

# ┌─────────────────────────────────────────────────────────┐
# │ PRE-SCAFFOLD — teacher walks through this, you use it   │
# │                                                         │
# │ AllSprites is a custom sprite group with a camera.      │
# │ A normal pygame group just draws sprites at their rect  │
# │ positions. AllSprites shifts every sprite by an offset  │
# │ so the player always appears at the centre of the screen│
# │ — this is how the scrolling world camera works.         │
# │                                                         │
# │ draw() also handles:                                    │
# │   - shadow under every Entity                           │
# │   - the '!' notice bubble when an NPC spots the player  │
# │   - z-sorting so nearer sprites draw on top of far ones │
# └─────────────────────────────────────────────────────────┘

class AllSprites(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.offset          = vector()
		self.shadow_surf     = import_image('..', '..', '..', 'graphics', 'other', 'shadow')
		self.notice_surf     = import_image('..', '..', '..', 'graphics', 'ui', 'notice')

	def draw(self, player):
		self.offset.x = -(player.rect.centerx - WINDOW_WIDTH  / 2)
		self.offset.y = -(player.rect.centery - WINDOW_HEIGHT / 2)

		bg_sprites   = [s for s in self if s.z < WORLD_LAYERS['main']]
		main_sprites = sorted(
			[s for s in self if s.z == WORLD_LAYERS['main']],
			key=lambda s: s.y_sort
		)
		fg_sprites   = [s for s in self if s.z > WORLD_LAYERS['main']]

		for layer in (bg_sprites, main_sprites, fg_sprites):
			for sprite in layer:
				if isinstance(sprite, Entity):
					self.display_surface.blit(
						self.shadow_surf,
						sprite.rect.topleft + self.offset + vector(40, 110)
					)
				self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)
				if sprite == player and player.noticed:
					rect = self.notice_surf.get_frect(midbottom=sprite.rect.midtop)
					self.display_surface.blit(self.notice_surf, rect.topleft + self.offset)


# ┌─────────────────────────────────────────────────────────┐
# │ PRE-SCAFFOLD — BattleSprites comes in session 5         │
# │ Stubbed here so imports don't break.                    │
# └─────────────────────────────────────────────────────────┘
class BattleSprites(pygame.sprite.Group):
	pass
