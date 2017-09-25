NUM_VERT = 0

def read_file():
	graph = {}
	with open('data/prim_edges.txt', 'r') as f:
		adjacency_list = []
		for line in f:
			data = line.split()
			if len(data) == 2:
				global NUM_VERT
				NUM_VERT = int(data[0])
			else:
				start, end, length = data[0], data[1], data[2]
				if graph.get(start, False) is False: 
					graph[start] = {data[1]: data[2]}
				else:
					graph[start].update({data[1]: data[2]})
				if graph.get(end, False) is False:
					graph[end] = {data[0]: data[2]}
				else:
					graph[end].update({data[0]: data[2]})
	return graph

def minimum_spanning_tree(graph):
	tree_edges = []
	all_nodes = set(str(i) for i in range(1, NUM_VERT + 1))
	all_explored = set('1')
	while all_nodes != all_explored:
		min_weight, min_head, min_tail = min( (int(v), node, k) 
			for node in all_explored for k,v in graph[node].items() if k not in all_explored)
		all_explored.add(min_tail)
		tree_edges.append((min_head, min_tail))
	return tree_edges

if __name__=='__main__':
	graph = read_file()
	mst = minimum_spanning_tree(graph)
	total_cost = 0
	for edge in mst:
		start, end = edge
		total_cost += int(graph[start][end])
	print(total_cost)
