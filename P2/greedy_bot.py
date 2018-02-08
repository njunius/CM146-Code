def think(state, quip):
	max_score = -1
	max_move = None
	for move in state.get_moves():
		new_state = state.copy()
		new_state.apply_move(move)
		new_score = new_state.get_score()[state.get_whos_turn()]
		if new_score >= max_score:
			max_move = move
			max_score = new_score
	return max_move