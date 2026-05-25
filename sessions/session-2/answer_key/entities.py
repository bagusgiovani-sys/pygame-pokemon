import pygame
from pygame.math import Vector2 as vector
from settings import WORLD_LAYERS, ANIMATION_SPEED
from support import check_connections
from timer import Timer
from random import choice

# ┌─────────────────────────────────────────────────────────┐
# │ PRE-SCAFFOLD — teacher walks through this, you use it   │
# │                                                         │
# │ Entity is the base class for both Player and Character  │
# │ (NPCs). It handles the sprite image, rect, hitbox, and  │
# │ the shared animate() / get_state() logic.               │
# │                                                         │
# │ Sprite setup is tricky so it's given to you here.       │
# │ You'll write animate() and the full Player class below. │
# └─────────────────────────────────────────────────────────┘

class Entity(pygame.sprite.Sprite):
	def __init__(self, pos, frames, groups, facing_direction):
		super().__init__(groups)
		self.z                 = WORLD_LAYERS['main']
		self.frame_index       = 0
		self.frames            = frames
		self.facing_direction  = facing_direction
		self.direction         = vector()
		self.speed             = 250 # tweak this for diff speed
		self.blocked           = False
		self.image             = self.frames[self.get_state()][self.frame_index]
		self.rect              = self.image.get_frect(center=pos)
		self.hitbox            = self.rect.inflate(-self.rect.width / 2, -60)
		self.y_sort            = self.rect.centery

	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 5: Entity.animate(dt)                  │
	# │ Two lines:                                               │
	# │   1. Add ANIMATION_SPEED * dt to self.frame_index.      │
	# │   2. Set self.image to the correct frame:               │
	# │        self.frames[self.get_state()][int(...)]          │
	# │      Use % (modulo) to wrap around when you reach the   │
	# │      end of the list.                                    │
	# │ Hint: int(self.frame_index % len(self.frames[state]))   │
	# └─────────────────────────────────────────────────────────┘
	def animate(self, dt):
		state = self.get_state()
		self.frame_index += ANIMATION_SPEED * dt
		self.image = self.frames[state][int(self.frame_index % len(self.frames[state]))]

	# ┌─────────────────────────────────────────────────────────┐
	# │ PRE-SCAFFOLD — teacher walks through this, you use it   │
	# │                                                         │
	# │ get_state() figures out which animation to play based   │
	# │ on the direction the entity is moving.                  │
	# │ It returns strings like 'down', 'right_idle', etc.      │
	# │ The frames dict has these strings as keys.              │
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
# │ PRE-SCAFFOLD — teacher walks through this, you use it   │
# │                                                         │
# │ Character handles all NPC behaviour: patrol, raycast,   │
# │ line-of-sight, walking toward the player, and dialog.   │
# │ This is complex so it's given to you — study it to see  │
# │ how Timer is used in practice.                          │
# └─────────────────────────────────────────────────────────┘

class Character(Entity):
	def __init__(self, pos, frames, groups, facing_direction, character_data,
	             player, create_dialog, collision_sprites, radius, nurse, notice_sound):
		super().__init__(pos, frames, groups, facing_direction)
		self.character_data   = character_data
		self.player           = player
		self.create_dialog    = create_dialog
		self.collision_rects  = [sprite.rect for sprite in collision_sprites if sprite is not self]
		self.nurse            = nurse
		self.has_moved        = False
		self.can_rotate       = True
		self.has_noticed      = False
		self.radius           = int(radius)
		self.view_directions  = character_data['directions']
		self.timers = {
			'look around': Timer(1500, autostart=True, repeat=True, func=self.random_view_direction),
			'notice':      Timer(500,  func=self.start_move),
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
			self.can_rotate    = False
			self.has_noticed   = True
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
				self.rect.center    += self.direction * self.speed * dt
				self.hitbox.center   = self.rect.center
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
	# │ Three things to do:                                     │
	# │   1. Call super().__init__(pos, frames, groups,         │
	# │                             facing_direction)           │
	# │   2. Store: self.collision_sprites = collision_sprites  │
	# │   3. Set:   self.noticed = False                        │
	# │      (True when an NPC has spotted you)                 │
	# └─────────────────────────────────────────────────────────┘
	def __init__(self, pos, frames, groups, facing_direction, collision_sprites):
		super().__init__(pos, frames, groups, facing_direction)
		self.collision_sprites = collision_sprites
		self.noticed = False

	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 7: Player.input()                      │
	# │ Read the keyboard and set self.direction.               │
	# │   1. keys = pygame.key.get_pressed()                    │
	# │   2. Create input_vector = vector()  (starts at 0, 0)  │
	# │   3. Check each arrow key:                              │
	# │        K_UP    → input_vector.y -= 1                    │
	# │        K_DOWN  → input_vector.y += 1                    │
	# │        K_LEFT  → input_vector.x -= 1                    │
	# │        K_RIGHT → input_vector.x += 1                    │
	# │   4. If input_vector is non-zero, normalize it so       │
	# │      diagonal movement isn't faster than straight.      │
	# │      self.direction = input_vector.normalize() if       │
	# │                        input_vector else input_vector   │
	# └─────────────────────────────────────────────────────────┘
	def input(self):
		keys = pygame.key.get_pressed()
		input_vector = vector()

		# Basic arrow-key movement
		if keys[pygame.K_s]:  #if keys[pygame.K_W] to make W to go up
			input_vector.y -= 1 #this makes the player goes down
		if keys[pygame.K_w]: 
			input_vector.y += 1 #this to go up
		if keys[pygame.K_a]:
			input_vector.x -= 1 #this to go left
		if keys[pygame.K_d]: 
			input_vector.x += 1 #this to go right

		if keys[pygame.K_SPACE]:
			self.speed = 700      # dash
		elif keys[pygame.K_LSHIFT]:
		 	self.speed = 450      # sprint
			 
		elif keys[pygame.K_LCTRL]:
			self.speed = 120  	# sneak
		else:
			self.speed = 250      # normal walk

		# ─────────────────────────────────────────────────────
		# CREATIVITY OPTION 1 — WASD controls
		# To activate: remove the # symbols below.
		# This allows students to move using both arrows and WASD.
		# ─────────────────────────────────────────────────────

		# if keys[pygame.K_w]:
		# 	input_vector.y -= 1
		# if keys[pygame.K_s]:
		# 	input_vector.y += 1
		# if keys[pygame.K_a]:
		# 	input_vector.x -= 1
		# if keys[pygame.K_d]:
		# 	input_vector.x += 1

		# ─────────────────────────────────────────────────────
		# CREATIVITY OPTION 2 — Sprint / sneak / dash
		# To activate: remove the # symbols below.
		# IMPORTANT: if you activate this block, comment out
		# the default self.speed = 250 line below it.
		# ─────────────────────────────────────────────────────

		# if keys[pygame.K_SPACE]:
		# 	self.speed = 700      # dash
		# elif keys[pygame.K_LSHIFT]:
		# 	self.speed = 450      # sprint
		# elif keys[pygame.K_LCTRL]:
		# 	self.speed = 120      # sneak
		# else:
		# 	self.speed = 250      # normal walk

		# Default movement speed. Comment this line out if you activate
		# the sprint/sneak/dash creativity option above.
		self.speed = 250

		self.direction = input_vector.normalize() if input_vector else input_vector

	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 8: Player.move(dt)                     │
	# │ Move the player in two passes (x then y) so corner      │
	# │ collisions resolve correctly.                           │
	# │   1. self.rect.centerx += self.direction.x * self.speed * dt
	# │   2. self.hitbox.centerx = self.rect.centerx            │
	# │   3. self.collisions('horizontal')                      │
	# │   4. self.rect.centery += self.direction.y * self.speed * dt
	# │   5. self.hitbox.centery = self.rect.centery            │
	# │   6. self.collisions('vertical')                        │
	# └─────────────────────────────────────────────────────────┘
	def move(self, dt):
		self.rect.centerx += self.direction.x * self.speed * dt
		self.hitbox.centerx = self.rect.centerx
		self.collisions('horizontal')

		self.rect.centery += self.direction.y * self.speed * dt
		self.hitbox.centery = self.rect.centery
		self.collisions('vertical')

	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 9: Player.collisions(axis)             │
	# │ Push the player back when they touch a wall.            │
	# │ Loop through self.collision_sprites:                    │
	# │   if sprite.hitbox collides with self.hitbox:           │
	# │     if axis == 'horizontal':                            │
	# │       moving right → set self.hitbox.right =           │
	# │                           sprite.hitbox.left           │
	# │       moving left  → set self.hitbox.left  =           │
	# │                           sprite.hitbox.right          │
	# │       then sync: self.rect.centerx = self.hitbox.centerx│
	# │     else (vertical):                                    │
	# │       moving down  → self.hitbox.bottom = sprite.hitbox.top
	# │       moving up    → self.hitbox.top    = sprite.hitbox.bottom
	# │       self.rect.centery = self.hitbox.centery           │
	# │ Hint: use self.direction.x > 0 to mean "moving right". │
	# └─────────────────────────────────────────────────────────┘
	def collisions(self, axis):
		for sprite in self.collision_sprites:
			if sprite.hitbox.colliderect(self.hitbox):

				if axis == 'horizontal':
					if self.direction.x > 0:
						self.hitbox.right = sprite.hitbox.left
					if self.direction.x < 0:
						self.hitbox.left = sprite.hitbox.right
					self.rect.centerx = self.hitbox.centerx

				else:
					if self.direction.y > 0:
						self.hitbox.bottom = sprite.hitbox.top
					if self.direction.y < 0:
						self.hitbox.top = sprite.hitbox.bottom
					self.rect.centery = self.hitbox.centery

	# ┌─────────────────────────────────────────────────────────┐
	# │ PRE-SCAFFOLD — teacher walks through this, you use it   │
	# │                                                         │
	# │ update() ties everything together each frame:           │
	# │   y_sort ensures the player is drawn at the right depth │
	# │   blocked stops movement during dialog / battle         │
	# └─────────────────────────────────────────────────────────┘
	def update(self, dt):
		self.y_sort = self.rect.centery
		if not self.blocked:
			self.input()
			self.move(dt)
		self.animate(dt)

# ┌─────────────────────────────────────────────────────────┐
# │ EXTENSION — bonus challenge!                            │
# │ Ideas: The normalize() call in input() already caps     │
# │        diagonal speed — explain why to your teacher.    │
# │        Try removing normalize() and see what happens.   │
# │        Add a SPRINT mode: if pygame.K_LSHIFT is held    │
# │        set self.speed = 400 else 250.                   │
# └─────────────────────────────────────────────────────────┘
