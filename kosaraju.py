NUM_VERT = 875714
import sys
import threading
import collections

def read_file():
	"""
	Returns a graph (dict) with an adjacency list representation.
	For example, {1: {'adj': [1, 2, 3, 4], 'is_explored': False},...}
	In this case, the graph is directed (edge from node 10 to 8).
	The boolean is used to indicate whether a node has been traversed.
	"""
	graph = {}
	with open('data/SCC.txt', 'r') as f:
		old_index = '1'
		adjacency_list = []
		for line in f:
			data = line.split()
			new_index = data[0]
			if old_index != new_index:
				graph[old_index] = {'adj_nodes': adjacency_list, 'is_explored': False}
				old_index = new_index
				adjacency_list = []
			adjacency_list.append(data[1])
		graph[old_index] = {'adj_nodes': adjacency_list, 'is_explored': False}

	for i in range(1, NUM_VERT + 1):
		if graph.get(str(i), False) is False:
			graph[str(i)] = {'adj_nodes': [], 'is_explored': False}
	return graph

def reverse_graph(graph):
	g_rev = {}
	for vertex in graph.keys():
		for edge in graph[vertex]['adj_nodes']:
			is_key = g_rev.get(edge, False)
			if is_key:
				g_rev[edge]['adj_nodes'].append(vertex)
			else:
				g_rev[edge] = {'adj_nodes': [vertex], 'is_explored': False}

	for i in range(1, NUM_VERT + 1):
		if g_rev.get(str(i), False) is False:
			g_rev[str(i)] = {'adj_nodes': [], 'is_explored': False}
	return g_rev

finishing_time = 0
starting_node = None
leader = {}
times = {}

def dfs_loop(graph):
	for i in range(NUM_VERT, 0, -1):
		if graph[str(i)]['is_explored'] is False:
			global starting_node
			starting_node = str(i)
			dfs(graph, str(i))

def dfs(graph, tail):
	graph[tail]['is_explored'] = True
	leader[tail] = starting_node
	for head in graph[tail]['adj_nodes']:
		if graph[head]['is_explored'] is False:
			dfs(graph, head)
	global finishing_time
	finishing_time += 1
	times[tail] = finishing_time

def relabel(graph):
	new_graph = {}
	for key in graph.keys():
		new_graph[str(times[key])] = graph[key]
	for tail in new_graph.keys():
		for i in range(len(new_graph[tail]['adj_nodes'])):
			head = new_graph[tail]['adj_nodes'][i]
			new_graph[tail]['adj_nodes'][i] = str(times[head])
	return new_graph

def scc():
	print(len(leader))
	counts = {}
	for key in leader.keys():
		if leader[key] in counts:
			counts[leader[key]] += 1
		else:
			counts[leader[key]] = 1
	c = collections.Counter(counts)
	for node, count in c.most_common(5):
		print('%s: %5d' % (node, count))

def main():
	graph = read_file()
	g_rev = reverse_graph(graph)
	dfs_loop(g_rev)
	ordered_graph = relabel(graph)
	dfs_loop(ordered_graph)
	scc()
	
threading.stack_size(67108864) # 64MB stack
sys.setrecursionlimit(2 ** 20) # something real big
                               # you actually hit the 64MB limit first
                               # going by other answers, could just use 2**32-1

# only new threads get the redefined stack size
thread = threading.Thread(target=main)
thread.start()
