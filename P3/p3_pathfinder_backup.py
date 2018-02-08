import Queue
from math import sqrt
from heapq import heappush, heappop

def find_path(source_point, dest_point, mesh):
	src_box = None
	dst_box = None
	
	visited_nodes = []
	path = []
		
	box_list = mesh['boxes']
	adj_list = mesh['adj']
	
	b_q = Queue.Queue()
	
	for next_box in box_list:
		
		if source_point[0] >= next_box[0] and source_point[1] >= next_box[2]:
			if source_point[0] <= next_box[1] and source_point[1] <= next_box[3]:
				src_box = next_box
		
		if dest_point[0] >= next_box[0] and dest_point[1] >= next_box[2]:
			if dest_point[0] <= next_box[1] and dest_point[1] <= next_box[3]:
				dst_box = next_box
	
	# check trivial paths or lack of paths
	if src_box == None or dst_box == None:
		print "No Path Possible!"
		return [],[]
	
	if src_box == dst_box:
		return ([(source_point, dest_point)], [src_box])
	
	path, visited_nodes = a_star_shortest_path(src_box, source_point, dst_box, dest_point, mesh, dist_point_in_box)
		
	return (path, visited_nodes)
	
def a_star_shortest_path(src_box, src_point, dst_box, dst_point, graph, adj):
	frontier = [] # the priority queue
	visited_nodes = [] # list of boxes 
	detail_points = {} # dict of points with the box containing the point as the keys
	cost_so_far = {} # dict of distances with boxes as keys
	prev = {} # dict of boxes with boxes as keys
	cost_so_far[src_box] = 0
	prev[src_box] = None
	detail_points[src_box] = src_point
	
	heappush(frontier, (0, src_box))
	visited_nodes.append(src_box)
	
	# as long as the queue is not empty
	while frontier:
		current = heappop(frontier)[1]
		
		# if the box containing the destination has been found, go calculate the path
		if current == dst_box:
			break
			
		# check if there are adjacent boxes that have not been visited or have a lower cost 
		for next in graph['adj'][current]:
			new_cost, new_priority, new_point = dist_point_in_box(detail_points[current], next, cost_so_far[current], dst_point)
			if next not in cost_so_far or new_cost < cost_so_far[next]:
				cost_so_far[next] = new_cost
				detail_points[next] = new_point
				heappush(frontier, (new_priority, next))
				visited_nodes.append(next)
				prev[next] = current
	
	# calculate the path
	if dst_box in prev: 
		point_as_box = dst_box # the box at the end of the path
		prev_point_as_box = prev[dst_box] # the previous box 
		path = []
		path.append((dst_point, detail_points[point_as_box])) # puts the actual destination point in the path as it is missed by the loop due to starting in the box not in the point
		
		# builds the path from the destination box to the source box
		while point_as_box != src_box: 
			path.append((detail_points[point_as_box], detail_points[prev_point_as_box]))
			point_as_box = prev[point_as_box]
			prev_point_as_box = prev[prev_point_as_box]
		path.reverse()
		return (path, visited_nodes)
	
	print "No Path Possible"
	return ([], [])
	
# calculates a new point in a box and its associated distance and priority for use in the priority queue
def dist_point_in_box(point, dst_box, distance_traveled, dest_point):
	point_x, point_y = point
	box_x1, box_x2, box_y1, box_y2 = dst_box
	dx, dy = (0, 0)
	
	dest_x, dest_y = dest_point
	
	if point_x < box_x1: # set x distance to minimum distance to box in x direction if point is not in box
		dx = box_x1 - point_x
	if point_x > box_x2: # set x distance to maximum distance to box in x direction if point is not in box
		dx = box_x2 - point_x
	if point_y < box_y1: # set y distance to minimum distance to box in y direction if point is not in box
		dy = box_y1 - point_y
	if point_y > box_y2: # set y distance to maximum distance to box in y direction if point is not in box
		dy = box_y2 - point_y
	
	new_pt = (point_x + dx, point_y + dy) # new point's coordinates 
	new_dst = distance_traveled + sqrt(dx * dx + dy * dy) 
	# heuristic for priority queue of distance so far + Euclidean distance from new point to destination
	priority = new_dst + sqrt((dest_x - new_pt[0])*(dest_x - new_pt[0]) + (dest_y - new_pt[1])*(dest_y - new_pt[1])) 
	
	return (new_dst, priority, new_pt)