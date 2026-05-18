import pygame
from pygame.math import Vector2 as vector
from settings import WORLD_LAYERS, COLORS
from timer import Timer

# ┌─────────────────────────────────────────────────────────┐
# │ PRE-SCAFFOLD — teacher walks through this, you use it   │
# │                                                         │
# │ DialogSprite draws a single speech bubble above an NPC. │
# │ DialogTree manages stepping through all lines of dialog │
# │ when the player presses SPACE.                          │
# │                                                         │
# │ Key design note: we use a Timer(250) after each line    │
# │ so the player can't accidentally skip dialog by         │
# │ holding SPACE. You'll learn to build timer-gated input  │
# │ yourself in session 7.                                  │
# └─────────────────────────────────────────────────────────┘

class DialogSprite(pygame.sprite.Sprite):
	def __init__(self, message, character, groups, font):
		super().__init__(groups)
		self.z = WORLD_LAYERS['top']

		text_surf = font.render(message, False, COLORS['dark'])
		padding   = 10
		width     = max(text_surf.get_width() + padding * 2, 60)
		height    = text_surf.get_height() + padding * 2

		self.image = pygame.Surface((width, height), pygame.SRCALPHA)
		pygame.draw.rect(self.image, COLORS['pure white'], self.image.get_frect(), 0, 5)
		self.image.blit(text_surf, (padding, padding))
		self.rect = self.image.get_frect(midbottom=character.rect.midtop + vector(0, -10))


class DialogTree:
	def __init__(self, character, player, all_sprites, font, end_dialog):
		self.character   = character
		self.player      = player
		self.all_sprites = all_sprites
		self.font        = font
		self.end_dialog  = end_dialog
		self.dialog      = character.get_dialog()
		self.dialog_index = 0
		self.dialog_sprite = DialogSprite(
			self.dialog[self.dialog_index],
			self.character,
			self.all_sprites,
			self.font
		)
		self.timer = Timer(250, autostart=True)

	def input(self):
		keys = pygame.key.get_just_pressed()
		if keys[pygame.K_SPACE] and not self.timer.active:
			self.dialog_sprite.kill()
			self.dialog_index += 1
			if self.dialog_index < len(self.dialog):
				self.dialog_sprite = DialogSprite(
					self.dialog[self.dialog_index],
					self.character,
					self.all_sprites,
					self.font
				)
				self.timer.activate()
			else:
				self.end_dialog(self.character)

	def update(self):
		self.timer.update()
		self.input()
