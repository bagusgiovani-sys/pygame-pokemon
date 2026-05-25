import pygame
from pygame.math import Vector2 as vector
from settings import WORLD_LAYERS, ANIMATION_SPEED
from support import check_connections
from timer import Timer
from random import choice

# ┌─────────────────────────────────────────────────────────┐
# │ SESSION 2 — STUDENT FILE                                │
# │ This file controls moving characters.                   │
# │ For Session 2, the important class is Player.           │
# │ Character/NPC code is pre-scaffold for later sessions.  │
# └─────────────────────────────────────────────────────────┘

class Entity(pygame.sprite.Sprite):
	def __init__(self, pos, frames, groups, facing_direction):
		super().__init__(groups)
		self.z = WORLD_LAYERS['main']
		self.frame_index = 0
		self.frames = frames
		self.facing_direction = facing_direction
		self.direction = vector()
		self.speed = 250
		self.blocked = False
		self.image = self.frames[self.get_state()][self.frame_index]
		self.rect = self.image.get_frect(center=pos)
		self.hitbox = self.rect.inflate(-self.rect.width / 2, -60)
		self.y_sort = self.rect.centery

	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 5: Entity.animate(dt)                  │
	# │ Update frame_index using ANIMATION_SPEED * dt.          │
	# │ Then choose the right frame based on get_state().        │
	# └─────────────────────────────────────────────────────────┘
	def animate(self, dt):
		# TODO: your code here
		pass  # remove this when you're done

	# ┌─────────────────────────────────────────────────────────┐
	# │ PRE-SCAFFOLD — get_state()                              │
	# │ Chooses animation name: down, left, right, up,           │
	# │ or down_idle, left_idle, right_idle, up_idle.            │
	# └─────────────────────────────────────────────────────────┘
	def get_state(self):
		moving = bool(self.direction)
		if moving:
			if self.direction.x != 0:
				self.facing_direction = 'right' if self.direction.x > 0 else 'left'
			if self.direction.y != 0:
				self.facing_direction = 'down' if self.direction.y > 0 else 'up'
		return f"{self.facing_direction}{'' if moving else '_idle'}"

	def change_facing_direction(self, target_pos):
		relation = vector(target_pos) - vector(self.rect.center)
		if abs(relation.y) < 30:
			self.facing_direction = 'right' if relation.x > 0 else 'left'
		else:
			self.facing_direction = 'down' if relation.y > 0 else 'up'

	def block(self):
		self.blocked = True
		self.direction = vector(0, 0)

	def unblock(self):
		self.blocked = False


# ┌─────────────────────────────────────────────────────────┐
# │ PRE-SCAFFOLD — Character/NPC code for later sessions     │
# │ Students do not need to edit this in Session 2.          │
# └─────────────────────────────────────────────────────────┘
class Character(Entity):
	def __init__(self, pos, frames, groups, facing_direction, character_data,
	             player, create_dialog, collision_sprites, radius, nurse, notice_sound):
		super().__init__(pos, frames, groups, facing_direction)
		self.character_data = character_data
		self.player = player
		self.create_dialog = create_dialog
		self.collision_rects = [sprite.rect for sprite in collision_sprites if sprite is not self]
		self.nurse = nurse
		self.has_moved = False
		self.can_rotate = True
		self.has_noticed = False
		self.radius = int(radius)
		self.view_directions = character_data['directions']
		self.timers = {
			'look around': Timer(1500, autostart=True, repeat=True, func=self.random_view_direction),
			'notice': Timer(500, func=self.start_move),
		}
		self.notice_sound = notice_sound

	def random_view_direction(self):
		if self.can_rotate:
			self.facing_direction = choice(self.view_directions)

	def get_dialog(self):
		key = 'defeated' if self.character_data['defeated'] else 'default'
		return self.character_data['dialog'][key]

	def raycast(self):
		if (check_connections(self.radius, self, self.player)
				and self.has_los()
				and not self.has_moved
				and not self.has_noticed):
			self.player.block()
			self.player.change_facing_direction(self.rect.center)
			self.timers['notice'].activate()
			self.can_rotate = False
			self.has_noticed = True
			self.player.noticed = True
			self.notice_sound.play()

	def has_los(self):
		if vector(self.rect.center).distance_to(self.player.rect.center) < self.radius:
			collisions = [
				bool(rect.clipline(self.rect.center, self.player.rect.center))
				for rect in self.collision_rects
			]
			return not any(collisions)

	def start_move(self):
		relation = (vector(self.player.rect.center) - vector(self.rect.center)).normalize()
		self.direction = vector(round(relation.x), round(relation.y))

	def move(self, dt):
		if not self.has_moved and self.direction:
			if not self.hitbox.inflate(10, 10).colliderect(self.player.hitbox):
				self.rect.center += self.direction * self.speed * dt
				self.hitbox.center = self.rect.center
			else:
				self.direction = vector()
				self.has_moved = True
				self.create_dialog(self)
				self.player.noticed = False

	def update(self, dt):
		for timer in self.timers.values():
			timer.update()
		self.animate(dt)
		if self.character_data['look_around']:
			self.raycast()
			self.move(dt)


class Player(Entity):
	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 6: Player.__init__                     │
	# │ Call Entity setup using super(), then store collision    │
	# │ sprites and create self.noticed.                         │
	# └─────────────────────────────────────────────────────────┘
	def __init__(self, pos, frames, groups, facing_direction, collision_sprites):
		# TODO: your code here
		pass  # remove this when you're done

	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 7: Player.input()                      │
	# │ Read arrow keys and convert them into a direction vector.│
	# │ Bonus creativity is included as commented code.          │
	# └─────────────────────────────────────────────────────────┘
	def input(self):
		# TODO: your code here
		pass  # remove this when you're done

		# ─────────────────────────────────────────────────────
		# CREATIVITY OPTION 1 — WASD controls
		# After your arrow movement works, add this inside input():
		#
		# if keys[pygame.K_w]:
		# 	input_vector.y -= 1
		# if keys[pygame.K_s]:
		# 	input_vector.y += 1
		# if keys[pygame.K_a]:
		# 	input_vector.x -= 1
		# if keys[pygame.K_d]:
		# 	input_vector.x += 1
		# ─────────────────────────────────────────────────────

		# ─────────────────────────────────────────────────────
		# CREATIVITY OPTION 2 — Sprint / sneak / dash
		# Add this before setting self.direction:
		#
		# if keys[pygame.K_SPACE]:
		# 	self.speed = 700      # dash
		# elif keys[pygame.K_LSHIFT]:
		# 	self.speed = 450      # sprint
		# elif keys[pygame.K_LCTRL]:
		# 	self.speed = 120      # sneak
		# else:
		# 	self.speed = 250      # normal walk
		# ─────────────────────────────────────────────────────

	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 8: Player.move(dt)                     │
	# │ Move horizontally first, check collision, then move      │
	# │ vertically and check collision again.                    │
	# └─────────────────────────────────────────────────────────┘
	def move(self, dt):
		# TODO: your code here
		pass  # remove this when you're done

	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 9: Player.collisions(axis)             │
	# │ If the player hitbox touches a collision sprite, push    │
	# │ the player back depending on movement direction.         │
	# └─────────────────────────────────────────────────────────┘
	def collisions(self, axis):
		# TODO: your code here
		pass  # remove this when you're done

	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 10: Player.update(dt)                  │
	# │ If not blocked: input + move. Always animate.            │
	# │ Finally update y_sort for camera draw order.             │
	# └─────────────────────────────────────────────────────────┘
	def update(self, dt):
		# TODO: your code here
		pass  # remove this when you're done
