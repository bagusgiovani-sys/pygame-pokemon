import pygame
from os.path import join

# ┌─────────────────────────────────────────────────────────┐
# │ PRE-SCAFFOLD — teacher walks through this, you use it   │
# │                                                         │
# │ This file will grow each session as we need more        │
# │ helpers. For now you just need import_image.            │
# │                                                         │
# │ import_image loads a PNG file from disk and returns a   │
# │ pygame Surface (an image you can draw to the screen).   │
# │                                                         │
# │ Usage example:                                          │
# │   surf = import_image('..', '..', 'graphics',           │
# │                        'other', 'shadow')               │
# │ The *path trick lets you pass as many folder pieces     │
# │ as you need — join() stitches them together.            │
# └─────────────────────────────────────────────────────────┘

def import_image(*path, alpha=True, format='png'):
	full_path = join(*path) + f'.{format}'
	if alpha:
		surf = pygame.image.load(full_path).convert_alpha()
	else:
		surf = pygame.image.load(full_path).convert()
	return surf
