# ┌─────────────────────────────────────────────────────────┐
# │ PRE-SCAFFOLD — teacher walks through this, you use it   │
# │                                                         │
# │ Read this file carefully — you'll BUILD this yourself   │
# │ in session 2!                                           │
# │                                                         │
# │ A Timer lets us do something after a delay.             │
# │ Examples in this game:                                  │
# │   - NPC looks around every 1.5 seconds                  │
# │   - Battle actions have a short pause between them      │
# │   - Encounter cooldown so fights don't start instantly  │
# │                                                         │
# │ How it works:                                           │
# │   1. Call activate() to start the clock                 │
# │   2. Call update() every frame                          │
# │   3. When enough time passes, it calls func() for you   │
# │      and deactivates itself                             │
# └─────────────────────────────────────────────────────────┘

from pygame.time import get_ticks

class Timer:
	def __init__(self, duration, repeat=False, autostart=False, func=None):
		self.duration = duration    # how many milliseconds to wait
		self.start_time = 0         # when did the timer start?
		self.active = False         # is the timer currently running?
		self.repeat = repeat        # should it restart after finishing?
		self.func = func            # function to call when time is up
		if autostart:
			self.activate()

	def activate(self):
		self.active = True
		self.start_time = get_ticks()  # record the current time in ms

	def deactivate(self):
		self.active = False
		self.start_time = 0
		if self.repeat:
			self.activate()  # immediately restart if repeat=True

	def update(self):
		if self.active:
			current_time = get_ticks()
			if current_time - self.start_time >= self.duration:
				if self.func:
					self.func()    # trigger the callback
				self.deactivate()
