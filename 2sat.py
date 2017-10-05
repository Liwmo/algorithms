NUM_VERT = 0
import sys
import threading
import collections

def read_file(f):
	"""
	Returns a graph (dict) with an adjacency list representation.
	For example, {1: {'adj': [1, 2, 3, 4], 'is_explored': False},...}
	For the 2-SAT problem, there are two vertices for each variable.
	For instance, X and -X, the latter of which denotes NOT X. 
	Given a constraint X OR Y, there are two directed edges: NOT X -> Y and NOT Y -> X.
	"""
	graph = {}
	with open('data/' + f + '.txt', 'r') as f:
		for line in f:
			data = line.split()
			if len(data) == 1:
				global NUM_VERT
				NUM_VERT = int(data[0])
				continue
			x, y = int(data[0]), int(data[1])
			if graph.get(str(-x), None) == None:
				graph[str(-x)] = {'adj_nodes': [str(y)], 'is_explored': False}
			elif str(y) not in graph[str(-x)]['adj_nodes']:
				graph[str(-x)]['adj_nodes'].append(str(y))
			if graph.get(str(-y), None) == None:
				graph[str(-y)] = {'adj_nodes': [str(x)], 'is_explored': False}
			elif str(x) not in graph[str(-y)]['adj_nodes']:
				graph[str(-y)]['adj_nodes'].append(str(x))

	for i in range(-NUM_VERT, NUM_VERT + 1):
		if graph.get(str(i), False) is False:
			graph[str(i)] = {'adj_nodes': [], 'is_explored': False}
	return graph

def reverse_graph(graph):
	g_rev = {}
	for vertex in graph:
		for edge in graph[vertex]['adj_nodes']:
			is_key = g_rev.get(edge, False)
			if is_key:
				g_rev[edge]['adj_nodes'].append(vertex)
			else:
				g_rev[edge] = {'adj_nodes': [vertex], 'is_explored': False}

	for i in range(-NUM_VERT, NUM_VERT + 1):
		if g_rev.get(str(i), False) is False:
			g_rev[str(i)] = {'adj_nodes': [], 'is_explored': False}
	return g_rev

finishing_time = 0
starting_node = None
leader = {}
times = {}

def dfs_loop(graph):
	for i in range(NUM_VERT, -NUM_VERT - 1, -1):
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

def scc(graph, times):
	for key in graph:
		node_a = str(times[key])
		node_b = str(times[str(-int(key))])
		if leader[node_a] == leader[node_b] and node_a != node_b: 
			return False
	return True

def main():
	graph = read_file('2sat6')
	global finishing_time
	finishing_time = -NUM_VERT - 1
	g_rev = reverse_graph(graph)
	dfs_loop(g_rev)
	time_copy = times.copy()
	ordered_graph = relabel(graph)
	dfs_loop(ordered_graph)
	result = scc(graph, time_copy)
	print(result)
		
threading.stack_size(67108864) # 64MB stack
sys.setrecursionlimit(2 ** 20) # something real big
                               # you actually hit the 64MB limit first
                               # going by other answers, could just use 2**32-1

# only new threads get the redefined stack size
thread = threading.Thread(target=main)
thread.start()