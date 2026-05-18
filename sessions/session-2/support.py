import pygame
from os.path import join
from os import walk

# ┌─────────────────────────────────────────────────────────┐
# │ PRE-SCAFFOLD — teacher walks through this, you use it   │
# │                                                         │
# │ support.py is a toolbox of helper functions used all    │
# │ across the game. You don't write these — just use them. │
# │                                                         │
# │ Functions added this session:                           │
# │   import_image       — load one PNG file                │
# │   import_folder      — load all PNGs in a folder        │
# │   import_folder_dict — same but keyed by filename       │
# │   import_tilemap     — slice a spritesheet into tiles   │
# │   character_importer — build directional walk frames    │
# │   all_character_import — import all characters at once  │
# │   coast_importer     — animated coast tiles             │
# │   draw_bar           — draw an HP/energy bar            │
# │   check_connections  — NPC line-of-sight range check    │
# └─────────────────────────────────────────────────────────┘

def import_image(*path, alpha=True, format='png'):
	full_path = join(*path) + f'.{format}'
	if alpha:
		surf = pygame.image.load(full_path).convert_alpha()
	else:
		surf = pygame.image.load(full_path).convert()
	return surf

def import_folder(*path):
	frames = []
	for folder_path, sub_folders, image_names in walk(join(*path)):
		for image_name in sorted(image_names, key=lambda name: int(name.split('.')[0])):
			full_path = join(folder_path, image_name)
			surf = pygame.image.load(full_path).convert_alpha()
			frames.append(surf)
	return frames

def import_folder_dict(*path):
	frames = {}
	for folder_path, sub_folders, image_names in walk(join(*path)):
		for image_name in image_names:
			full_path = join(folder_path, image_name)
			surf = pygame.image.load(full_path).convert_alpha()
			frames[image_name.split('.')[0]] = surf
	return frames

def import_tilemap(cols, rows, *path):
	frames = {}
	surf = import_image(*path)
	cell_width  = surf.get_width()  / cols
	cell_height = surf.get_height() / rows
	for col in range(cols):
		for row in range(rows):
			cutout_rect = pygame.Rect(col * cell_width, row * cell_height, cell_width, cell_height)
			cutout_surf = pygame.Surface((cell_width, cell_height))
			cutout_surf.fill('green')
			cutout_surf.set_colorkey('green')
			cutout_surf.blit(surf, (0, 0), cutout_rect)
			frames[(col, row)] = cutout_surf
	return frames

def character_importer(cols, rows, *path):
	frame_dict = import_tilemap(cols, rows, *path)
	new_dict = {}
	for row, direction in enumerate(('down', 'left', 'right', 'up')):
		new_dict[direction]              = [frame_dict[(col, row)] for col in range(cols)]
		new_dict[f'{direction}_idle']    = [frame_dict[(0, row)]]
	return new_dict

def all_character_import(*path):
	new_dict = {}
	for _, __, image_names in walk(join(*path)):
		for image in image_names:
			image_name = image.split('.')[0]
			new_dict[image_name] = character_importer(4, 4, *path, image_name)
	return new_dict

def coast_importer(cols, rows, *path):
	frame_dict = import_tilemap(cols, rows, *path)
	new_dict = {}
	terrains = ['grass', 'grass_i', 'sand_i', 'sand', 'rock', 'rock_i', 'ice', 'ice_i']
	sides = {
		'topleft':     (0, 0), 'top':    (1, 0), 'topright':    (2, 0),
		'left':        (0, 1),                    'right':       (2, 1),
		'bottomleft':  (0, 2), 'bottom': (1, 2), 'bottomright': (2, 2),
	}
	for index, terrain in enumerate(terrains):
		new_dict[terrain] = {}
		for key, pos in sides.items():
			new_dict[terrain][key] = [
				frame_dict[(pos[0] + index * 3, pos[1] + row)]
				for row in range(0, rows, 3)
			]
	return new_dict

def draw_bar(surface, rect, value, max_value, color, bg_color, radius=1):
	ratio = rect.width / max_value
	bg_rect = rect.copy()
	progress = max(0, min(rect.width, value * ratio))
	progress_rect = pygame.FRect(rect.topleft, (progress, rect.height))
	pygame.draw.rect(surface, bg_color, bg_rect, 0, radius)
	pygame.draw.rect(surface, color, progress_rect, 0, radius)

def check_connections(radius, entity, target, tolerance=30):
	from pygame.math import Vector2 as vector
	relation = vector(target.rect.center) - vector(entity.rect.center)
	if relation.length() < radius:
		if (entity.facing_direction == 'left'  and relation.x < 0 and abs(relation.y) < tolerance) or \
		   (entity.facing_direction == 'right' and relation.x > 0 and abs(relation.y) < tolerance) or \
		   (entity.facing_direction == 'up'    and relation.y < 0 and abs(relation.x) < tolerance) or \
		   (entity.facing_direction == 'down'  and relation.y > 0 and abs(relation.x) < tolerance):
			return True
	return False
