import sys, threading
CAPACITY = 0
NUM_ITEMS = 0

def read_file():
	x, i = [], 0
	with open('data/knapsack_big.txt', 'r') as f:
		for line in f:
			data = line.split()
			if i == 0:
				x.append({'value': 0, 'weight': 0})
				global CAPACITY, NUM_ITEMS
				CAPACITY, NUM_ITEMS = int(data[0]), int(data[1])
				i += 1
				continue
			value, weight = int(data[0]), int(data[1])
			x.append({'value': value, 'weight': weight})
	return x

def get_optimal(i, w, data, cache):
	if i == 1:
		return data[i]['value'] if data[i]['weight'] < w else 0
	if (i,w) in cache:
		return cache[(i,w)]
	if data[i]['weight'] > w:
		cache[(i,w)] = get_optimal(i-1, w, data, cache)
	else:
		cache[(i,w)] = max(get_optimal(i-1, w, data, cache), 
			get_optimal(i-1, w-data[i]['weight'], data, cache) + data[i]['value'])
	return cache[(i,w)]

def main():
	data_set = read_file()
	cache = {}
	optimal_value = get_optimal(NUM_ITEMS, CAPACITY, data_set, cache)
	print(optimal_value)

threading.stack_size(67108864) # 64MB stack
sys.setrecursionlimit(2 ** 20) # something real big
                               # you actually hit the 64MB limit first

# only new threads get the redefined stack size
thread = threading.Thread(target=main)
thread.start()