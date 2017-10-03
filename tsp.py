import math
NUM_VERT = 0

def read_file(filename):
	"""
	Reads in a list of x,y coordinates from a given file.
	These represent points for the traveling salesman problem.
	Return: a list of 2-tuples [(2.35, 1.59), ...]
	"""
	vertices = []
	with open('data/' + filename, 'r') as f:
		for line in f:
			data = line.split()
			if len(data) == 1:
				global NUM_VERT
				NUM_VERT = int(data[0])
				continue
			vertices.append((float(data[0]), float(data[1])))
	return vertices

def get_dist(a, b):
	return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def flip_bit(num, index):
	flip = 2 ** (index - 1)
	return num & ~flip

def get(lengths, smaller_set, k):
	if k == 1 and smaller_set == 1:
		return 0
	elif k == 1:
		return float('inf')
	else:
		return lengths[(smaller_set, k)]

def get_traveling_salesman(data):
	lengths = {}
	for size in range(2, NUM_VERT + 1):
		for subprob in range(2 ** size):
			if subprob & 1 == 1:
				indices = [i for i in range(1, NUM_VERT + 1) if format(subprob, '0' + str(NUM_VERT) + 'b')[-i] == '1']
				for j in indices:
					if j != 1:
						lengths[(subprob, j)] = min((get(lengths, flip_bit(subprob, j), k) + get_dist(data[k-1], data[j-1])
															for k in indices if k != j), default=float('inf'))
		for i in range(2 ** (size-1)):
			for k in range(2, size):
				lengths.pop((i, k), None)
	return lengths

if __name__=='__main__':
	"""
	For the particular data set given in tsp.txt, there appears to be two clusters
	when plotted. Thus, the data set has been split into two text files, for which
	the shortest cost cycle is computed for each cluster respectively. Both clusters 
	share one common edge which is subsequently subtracted off.
	(i.e. edge between vertex 12 and 13 with indices starting at 1).
	"""
	data_left = read_file("tsp_left.txt")
	subprob_left = get_traveling_salesman(data_left)
	full_set = 2 ** NUM_VERT - 1
	dist_left = min(subprob_left[(full_set, j)] + get_dist(data_left[0], data_left[j-1]) 
					for j in range(2, NUM_VERT + 1))

	data_right = read_file("tsp_right.txt")
	subprob_right = get_traveling_salesman(data_right)
	full_set = 2 ** NUM_VERT - 1
	dist_right = min(subprob_right[(full_set, j)] + get_dist(data_right[0], data_right[j-1]) 
					for j in range(2, NUM_VERT + 1))

	print(dist_left + dist_right - 2 * get_dist(data_left[11], data_left[12]))
