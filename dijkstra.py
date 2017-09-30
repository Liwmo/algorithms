NUM_VERT = 200

def read_file():
	"""
	Returns a dict (adjacency list) for a directed, weighted graph.
	Example: {'1': [{'head': 1, 'weight': 36},...], ...}
	"""
	graph = {}
	with open('data/dijkstraData.txt', 'r') as f:
		adjacency_list = []
		for line in f:
			data = line.split()
			for entry in data[1:]:
				head, weight = entry.split(',')
				adjacency_list.append( {'head': head, 'weight': int(weight)} )
			graph[data[0]] = adjacency_list
			adjacency_list = []
	return graph

def shortest_path_length(graph, start, end):
	"""
	Finds the length of the shortest path given a starting and 
	ending vertex. If a path does not exist, 1000000 is returned.
	"""
	lengths = {start: 0}
	all_nodes = set(str(i) for i in range(1, NUM_VERT + 1))
	all_explored = set(start)
	while all_nodes != all_explored and end not in all_explored:
		min_criterion, min_head = min( (adj['weight'] + lengths[node], adj['head']) 
			for node in all_explored for adj in graph[node] if adj['head'] not in all_explored)
		all_explored.add(min_head)
		lengths[min_head] = min_criterion
	dist = lengths.get(end, 1000000)
	return dist

if __name__=='__main__':
	graph = read_file()
	answer_string = ''
	for i in ['7','37','59','82','99','115','133','165','188','197']:
		dist = shortest_path_length(graph, '1', i)	
		answer_string += str(dist) + ','
	print(answer_string)
	
