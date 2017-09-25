import random
NUM_VERT = 0
NUM_BITS = 0

class UnionFind:
	def __init__(self, vertices):
		"""
		self.nodes: a dict of (node, parent) pairs.
		self.sizes: a dict with parents as keys and its corresponding
		            set length as the values
		self.sets: a dict with parents as keys and the corresponding
				   set (list of nodes) as the value
		"""
		self.nodes = {vertex: vertex for vertex in vertices}
		self.sizes = {parent: 1 for parent in vertices}
		self.sets = {vertex: [vertex] for vertex in vertices}

	def find(self, node):
		"""
		Returns the parent of a given node.
		"""
		return self.nodes[node]

	def join(self, node1, node2):
		"""
		Given two nodes, u and v where u is in set A and v is in set B, join(u, v) 
		is equivalent to the union of sets A and B. If u and v are in the same set 
		(i.e. have the same parents), no action is performed.
		"""
		parent1, parent2 = self.find(node1), self.find(node2)
		if parent1 == parent2:
			return
		if self.sizes[parent1] > self.sizes[parent2]:
			for node in [v for v in self.nodes if self.nodes[v] == parent2]:
				self.nodes[node] = parent1
				self.sets[parent1].append(node)
				self.sizes[parent1] += 1
			del self.sizes[parent2]
			del self.sets[parent2]
		else:
			for node in [v for v in self.nodes if self.nodes[v] == parent1]:
				self.nodes[node] = parent2
				self.sets[parent2].append(node)
				self.sizes[parent2] += 1
			del self.sizes[parent1]
			del self.sets[parent1]


def read_file():
	graph = {}
	with open('data/clustering1.txt', 'r') as f:
		for line in f:
			data = line.split()
			if len(data) == 1:
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

def read_bin_file():
	graph = {}
	with open('data/clustering_big.txt', 'r') as f:
		for line in f:
			data = line.split()
			if len(data) == 2:
				global NUM_BITS
				NUM_BITS = int(data[1])
				continue
			key = ''.join(data)
			if key not in graph:
				graph[key] = {}
			else:
				new_key = key + str(random.randint(0, 1000))
				graph[new_key] = {'dist0': key, 'dist1': [], 'dist2': []}
	return populate(graph)

def populate(graph):
	for key in graph:
		if len(key) > NUM_BITS: continue
		dist1_precheck = get_neighbors(list(key))
		dist1 = [x for x in dist1_precheck if x in graph]
		dist2 = []
		for i in dist1_precheck:
			dist2.extend([x for x in get_neighbors(list(i), key) 
							if x in graph and x not in dist1])
		graph[key] = {'dist0': [],'dist1': dist1, 'dist2': dist2}
	return graph

def get_neighbors(bits, old_key=None):
	neighbors = []
	for i in range(NUM_BITS):
		if bits[i] == '0':
			bits[i] = '1'
			new = ''.join(bits)
			if old_key == new: continue
			neighbors.append(new)
			bits[i] = '0'
		elif bits[i] == '1':
			bits[i] = '0'
			new = ''.join(bits)
			if old_key == new: continue
			neighbors.append(new)
			bits[i] = '1'
	return neighbors

def single_link_clustering(graph, num_clusters):
	edges = iter(sorted([(int(graph[start][end]), start, end) for start in graph 
							for end in graph[start] if start < end]))
	uf = UnionFind([str(i) for i in range(1, NUM_VERT + 1)])
	while num_clusters != len(uf.sets):
		weight, start, end = next(edges)
		uf.join(start, end)
	return uf

def implicit_weights_clustering(graph):
	uf = UnionFind(graph.keys())
	edges = []
	for key in graph:
		if graph[key]['dist0']: edges.append((key, graph[key]['dist0']))
		if graph[key]['dist1']: edges.extend([(key, v) for v in graph[key]['dist1'] if key > v])
		if graph[key]['dist2']: edges.extend([(key, v) for v in graph[key]['dist2'] if key > v])
	print(len(edges))
	count = 0
	for edge in edges:
		count += 1
		if count % 100 == 0: print(count)
		start, end = edge
		uf.join(start, end)
	return uf

if __name__=='__main__':
	#graph = read_file()
	graph = read_bin_file()
	uf = implicit_weights_clustering(graph)
	print(len(uf.sets))
	# test = list(graph.keys())
	# for i in test[:50]:
	# 	print(i, graph[i]['dist1'], graph[i]['dist2'])

	# uf = single_link_clustering(graph, 4)
	# spacing = min([int(graph[start][end]) for start in graph for end in graph[start] 
	# 				if uf.find(start) != uf.find(end)])
	# print(spacing)