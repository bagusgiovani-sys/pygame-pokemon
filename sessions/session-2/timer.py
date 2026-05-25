from pygame.time import get_ticks

# ┌─────────────────────────────────────────────────────────┐
# │ SESSION 2 — STUDENT FILE                                │
# │ Build this first. The Timer will be useful in later     │
# │ sessions for NPCs, dialog, attacks, transitions, etc.   │
# └─────────────────────────────────────────────────────────┘

class Timer:
	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 1: Timer.__init__                      │
	# │ Store the timer settings:                               │
	# │   duration, start_time, active, repeat, func             │
	# │ If autostart is True, call self.activate().              │
	# └─────────────────────────────────────────────────────────┘
	def __init__(self, duration, repeat=False, autostart=False, func=None):
		# TODO: your code here
		pass  # remove this when you're done

	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 2: activate()                          │
	# │ Turn the timer on and save the current time.             │
	# └─────────────────────────────────────────────────────────┘
	def activate(self):
		# TODO: your code here
		pass  # remove this when you're done

	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 3: deactivate()                        │
	# │ Turn the timer off. If repeat is True, activate again.   │
	# └─────────────────────────────────────────────────────────┘
	def deactivate(self):
		# TODO: your code here
		pass  # remove this when you're done

	# ┌─────────────────────────────────────────────────────────┐
	# │ YOUR CODE — Step 4: update()                            │
	# │ Check if the timer duration has passed.                  │
	# │ If yes, run func if it exists, then deactivate.          │
	# └─────────────────────────────────────────────────────────┘
	def update(self):
		# TODO: your code here
		pass  # remove this when you're done
