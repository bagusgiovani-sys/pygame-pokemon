# ┌─────────────────────────────────────────────────────────┐
# │ PRE-SCAFFOLD — teacher walks through this, you use it   │
# │                                                         │
# │ Timer lets us trigger actions after a delay.            │
# │ Used for:                                               │
# │   - NPC patrol pauses (look around every 1.5 s)         │
# │   - Battle action delays                                │
# │   - Encounter cooldowns (so fights don't start twice)   │
# │                                                         │
# │ You're building the whole class yourself today.         │
# │ Read each YOUR CODE block carefully before you type!    │
# └─────────────────────────────────────────────────────────┘

from pygame.time import get_ticks

class Timer:

	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 1: __init__                            │
	# │ Store these four parameters as instance attributes:     │
	# │   self.duration   = duration                            │
	# │   self.start_time = 0      (not started yet)            │
	# │   self.active     = False  (not running yet)            │
	# │   self.repeat     = repeat                              │
	# │   self.func       = func                                │
	# │ Then, if autostart is True, call self.activate().       │
	# │ Hint: use an if statement at the END of __init__.       │
	# └─────────────────────────────────────────────────────────┘
	def __init__(self, duration, repeat=False, autostart=False, func=None):
		# TODO: your code here
		pass  # remove this when you're done

	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 2: activate()                          │
	# │ Set self.active to True and record when it started.     │
	# │ Hint: get_ticks() returns the current time in ms.       │
	# │       Store it in self.start_time.                      │
	# └─────────────────────────────────────────────────────────┘
	def activate(self):
		# TODO: your code here
		pass  # remove this when you're done

	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 3: deactivate()                        │
	# │ Set self.active = False and self.start_time = 0.        │
	# │ Then, if self.repeat is True, call self.activate()      │
	# │ again so it restarts automatically.                     │
	# └─────────────────────────────────────────────────────────┘
	def deactivate(self):
		# TODO: your code here
		pass  # remove this when you're done

	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 4: update()                            │
	# │ This is called every frame. Only do work if active.     │
	# │   1. Get the current time with get_ticks().             │
	# │   2. If (current_time - self.start_time) >= duration:   │
	# │        a. Call self.func() — but only if self.func      │
	# │           is not None! Use: if self.func: self.func()   │
	# │        b. Call self.deactivate()                        │
	# └─────────────────────────────────────────────────────────┘
	def update(self):
		# TODO: your code here
		pass  # remove this when you're done

# ┌─────────────────────────────────────────────────────────┐
# │ EXTENSION — bonus challenge!                            │
# │ Ideas: Add a pause() method that saves the remaining    │
# │        time, and a resume() method that restores it.    │
# │        (Hint: store remaining = duration -              │
# │         (get_ticks() - start_time) in pause(),          │
# │         then in resume() set start_time =               │
# │         get_ticks() - (duration - remaining).)          │
# └─────────────────────────────────────────────────────────┘
