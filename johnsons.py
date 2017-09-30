from heapq import heapify, heappop, heappush
NUM_VERT = 0
NUM_EDGE = 0
COUNT = 0

def read_file():
	"""
	Returns a dict (adjacency list) for a directed, weighted graph.
	Example: {'1': {'in':[('2', -3), ...], 'out':[('25', 8), ...]}, ...}
	Each vertex maintains a list of adjacent verticies and their 
	corresponding edge weights for inbound and outbound edge separately.
	Note that costs may be negative; the graph may contain negative cycles.
	"""
	print('READING FILE...')
	with open('data/g3.txt', 'r') as f:
		line = f.readline()
		data = line.split()
		global NUM_VERT, NUM_EDGE
		NUM_VERT, NUM_EDGE = int(data[0]), int(data[1])
		graph = {str(i): {'in': [], 'out': []} for i in range(1, NUM_VERT + 1)}
		for line in f:
			data = line.split()
			tail, head, cost = data[0], data[1], int(data[2])
			graph[tail]['out'].append((head, cost))
			graph[head]['in'].append((tail, cost))
	return graph

def get_augmented_graph(g):
	print('AUGMENTING GRAPH...')
	"""
	Given a graph with N vertices, create a vertex N+1 with an outgoing
	edge with weight 0 to each existing vertex. 
	"""
	graph = g.copy()
	num_vert = len(graph)
	for v in graph:
		graph[v]['in'].append((str(num_vert + 1), 0))
	graph[str(num_vert + 1)] = {'in': [], 'out': [(v,0) for v in graph]}
	return graph

def get_bellman_ford_lengths(graph, source):
	"""
	Finds the shortest path to all vertices given a single source vertex.
	Returns none if a negative-cost cycle is present.
	Asymptotic runtime: O(mn).
	"""
	print('RUNNING BELLMAN-FORD...')
	num_vert = len(graph)
	min_lengths = [[0 if str(v) == source else float('inf') for v in range(num_vert + 1)] 
					for i in range(num_vert + 1)]

	for i in range(1, num_vert + 1):
		for v in graph:
			min_incoming = min((min_lengths[i-1][int(w[0])] + w[1] for w in graph[v]['in']), default=float('inf'))
			min_lengths[i][int(v)] = min(min_lengths[i-1][int(v)], min_incoming)
		if min_lengths[i-1] == min_lengths[i]: return min_lengths[i-1]
	return None

def reweigh_edges(graph, weights):
	"""
	For a given edge (s,v) with cost C, reweigh the cost to be 
	non-negative by computing C + W_s - W_v. Weights W_s and W_v
	are determined by using the Bellman-Ford algorithm on the 
	augmented graph (specified above). 
	"""
	print('REWEIGHING EDGES...')
	for s in graph:
		for i in range(len(graph[s]['out'])):
			v = graph[s]['out'][i]
			new_weight = v[1] + weights[int(s)] - weights[int(v[0])]
			graph[s]['out'][i] = (v[0], new_weight)
	return graph
	
def get_dijkstra_lengths(graph, start):
	"""
	Finds the length of the shortest path given a starting and 
	ending vertex. If a path does not exist, +infinity is returned.
	Heap-based implementation runtime: O(n log n)
	"""
	global COUNT
	COUNT += 1
	if COUNT % 100 == 0: print(COUNT)

	lengths = {start: 0}
	frontier = [(adj[1], adj[0]) for adj in graph[start]['out']]
	heapify(frontier)
	explored = set()
	explored.add(start)

	while len(frontier) != 0:
		min_cost, min_head = heappop(frontier)
		if min_head not in explored:
			explored.add(min_head)
			lengths[min_head] = min_cost
			for i in [(adj[1] + lengths[min_head], adj[0]) for adj in graph[min_head]['out'] if adj[0] not in explored]:
				heappush(frontier, i)
	return [(v, start, k) for k,v in lengths.items() if k != start]

if __name__=='__main__':
	graph = read_file()
	g_aug = get_augmented_graph(graph)
	weights = get_bellman_ford_lengths(g_aug, str(NUM_VERT + 1))
	if weights:
		graph = reweigh_edges(graph, weights)
	else:
		raise ValueError("NEGATIVE-COST CYCLE DETECTED")
	print('RUNNING DIJKSTRAS ALGORITHM...')
	min_candidates = []
	for s in range(1, len(graph) + 1):
		min_candidates.extend(get_dijkstra_lengths(graph, str(s)))
	min_adjusted_length = min([c - weights[int(s)] + weights[int(v)] for c,s,v in min_candidates])
	print('MIN PAIR PATH LENGTH:', min_adjusted_length)