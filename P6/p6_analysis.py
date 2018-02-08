# Chaiz Tuimoloau
# Nick Junius
# 
# Uses BFS to collect all possible player states within the level.
# Draws all possible paths to a destination highlighted by the cursor
#
from p6_game import Simulator
global PREV
PREV = {}

def analyze(design):
	PREV.clear()

	sim = Simulator(design)
	init = sim.get_initial_state()
	moves = sim.get_moves()
	
	queue = []
	queue.append(init)
	PREV[init] = None
	
	while queue:
		current_state = queue.pop(0)
		for move in moves:
			next_state = sim.get_next_state(current_state, move)
			if next_state != None and next_state not in PREV:
				queue.append(next_state)
				PREV[next_state] = current_state
	

def inspect((i,j), draw_line):
	current_state = None

	for state in PREV:
		coords = state[0]
		if coords == (i, j):
			current_state = state
			prev_state = PREV[current_state]
			while prev_state != None:
				draw_line(current_state[0], prev_state[0], state, prev_state[1])
				current_state = prev_state
				prev_state = PREV[current_state]
