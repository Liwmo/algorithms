NUM_VERT = 0

def read_file():
	x, i = [], 0
	with open('data/mwis.txt', 'r') as f:
		for line in f:
			if i == 0:
				i += 1
				global NUM_VERT
				NUM_VERT = int(line)
				continue
			x.append(int(line))
	return x

def get_ind_set_max_weights(data_set):
	max_weights = [None] * (NUM_VERT + 1)
	max_weights[0], max_weights[1] = 0, data_set[0]
	for i in range(2, NUM_VERT + 1):
		max_weights[i] = max(max_weights[i-1], max_weights[i-2] + data_set[i-1])
	return max_weights

def reconstruct_ind_set_vertices(max_weights, data_set):
	vertices = []
	i = NUM_VERT
	while i >= 1:
		if max_weights[i-1] >= max_weights[i-2] + data_set[i-1]:
			i -= 1
		else:
			vertices.append(i)
			i -= 2
	return vertices

if __name__=='__main__':
	data_set = read_file()
	max_weights = get_ind_set_max_weights(data_set)
	ind_set_vertices = reconstruct_ind_set_vertices(max_weights, data_set)
	problem_test_set = [1, 2, 3, 4, 17, 117, 517, 997]
	print(''.join(['1' if i in ind_set_vertices else '0' for i in problem_test_set]))