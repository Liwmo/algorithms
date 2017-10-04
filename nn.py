import math
NUM_VERT = 0

def read_file():
	"""
	Reads in a list of x,y coordinates from a given file.
	These represent points for the traveling salesman problem.
	Return: a list of 2-tuples [(2.35, 1.59), ...]
	"""
	vertices = []
	with open('data/nn.txt', 'r') as f:
		for line in f:
			data = line.split()
			if len(data) == 1:
				global NUM_VERT
				NUM_VERT = int(data[0])
				continue
			vertices.append((float(data[1]), float(data[2])))
	return vertices

def get_squared_dist(a, b):
	return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

def min_dist_heuristic(data):
	count = total = 0
	begin = start = data[0]
	data.pop(0)
	while data:
		count += 1
		if count % 1000 == 0: print(count)
		min_dist, min_idx = min((get_squared_dist(start, data[i]), i) for i in range(len(data)))
		total += math.sqrt(min_dist)
		start = data[min_idx]
		data.pop(min_idx)
	total += math.sqrt(get_squared_dist(start, begin))
	return total

if __name__=='__main__':
	data = read_file()
	dist = min_dist_heuristic(data)
	print(dist)
