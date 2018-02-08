from p1_support import load_level, show_level
from math import sqrt
from heapq import heappush, heappop

def dijkstras_shortest_path(src, dst, graph, adj):
	frontier = []
	heappush(frontier, (0, src))
	cost_so_far = {}
	prev = {}
	cost_so_far[src] = 0
	prev[src] = None
	
	while frontier:
		current = heappop(frontier)[1]
		
		if current == dst:
			path = []
			print cost_so_far[current]
			while current:
				path.append(current)
				current = prev[current]
			path.reverse()
			return path
			
		for next in adj(graph, current):
			#next_dist, next_pos = next
			new_cost = cost_so_far[current] + next[0]
			if next[1] not in cost_so_far or new_cost < cost_so_far[next[1]]:
				cost_so_far[next[1]] = new_cost
				heappush(frontier, (new_cost, next[1]))	
				#print (next[1][0], next[1][1]), new_cost
				prev[next[1]] = current
				
	return []

def navigation_edges(level, cell):
	steps = []
	x, y = cell
	for dx in [-1,0,1]:
		for dy in [-1,0,1]:
			next_cell = (x + dx, y + dy)
			dist = sqrt(dx*dx+dy*dy)
			if dist > 0 and next_cell in level['spaces']:
				steps.append((dist, next_cell))

	return steps

def test_route(filename, src_waypoint, dst_waypoint):
	level = load_level(filename)

	show_level(level)

	src = level['waypoints'][src_waypoint]
	dst = level['waypoints'][dst_waypoint]

	path = dijkstras_shortest_path(src, dst, level, navigation_edges)

	if path:
		show_level(level, path)
	else:
		print "No path possible!"

if __name__ ==  '__main__':
	import sys
	_, filename, src_waypoint, dst_waypoint = sys.argv
	test_route(filename, src_waypoint, dst_waypoint)
