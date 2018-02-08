import random
from math import sqrt
from math import log
import time

THINK_DURATION = 1

class Node:
    def __init__(self, move = None, parent = None, state = None, last_move = None):
        self.move = move
        self.parent = parent
        self.child_nodes = []
        self.reward = 0.0
        self.times_visited = 0.0
        self.untried_moves = state.get_moves()
        self.who = last_move
        #self.player_moved = state.player_moved

    def uct_select_child(self):
        s = sorted(self.child_nodes, key = lambda c: c.reward/c.times_visited + sqrt(2*log(self.times_visited)/c.times_visited))[-1]
        return s

    def add_child(self, m, s, last_move = None):
        n = Node(move = m, parent = self, state = s, last_move = last_move)
        self.untried_moves.remove(m)
        self.child_nodes.append(n)
        return n

def think(state, quip):

	t_start = time.time()
	t_deadline = t_start + THINK_DURATION
	
	iterations = 0
	
	if state.get_whos_turn() == 'red':
		rootnode = Node(state = state, last_move = 'blue')
	else:
		rootnode = Node(state = state, last_move = 'red')
		
	rootnode.times_visited = 1.0
	while True:
		iterations += 1
		node = rootnode
		next_state = state.copy()
		#Selection
		#While node still has children to explore and all moves have been tried
		while not node.untried_moves and node.child_nodes:
			node = node.uct_select_child()
			next_state.apply_move(node.move)
		#Expansion
		if node.untried_moves:
			m = random.choice(node.untried_moves)
			turn = next_state.get_whos_turn()
			next_state.apply_move(m)
			node = node.add_child(m, next_state, last_move = turn)
		#Rollout
		while not (next_state.is_terminal()):
			rollout_move = random.choice( next_state.get_moves() )
			next_state.apply_move( rollout_move )
		#Backpropogation
		score = next_state.get_score()
		while node != None:
			result = score[node.who]
			node.times_visited += 1
			node.reward += result
			node = node.parent

		t_now = time.time()
		if t_now > t_deadline:
			break
	sample_rate = float(iterations)/(t_now - t_start)
	quip(sample_rate)
	return sorted(rootnode.child_nodes, key = lambda c: c.reward/c.times_visited)[-1].move
	#return sorted(rootnode.child_nodes, key = lambda c: c.reward)[-1].move