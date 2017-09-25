from heapq import heappop, heappush
NUM_VERT = 0

class Node:
	def __init__(self, symbol, left=None, right=None, parent=None):
		self.symbol = symbol
		self.left = left
		self.right = right
		self.parent = parent

def read_file():
	h = []
	i = 0
	with open('data/huffman.txt', 'r') as f:
		for line in f:
			if i == 0:
				i += 1
				global NUM_VERT
				NUM_VERT = int(line)
				continue
			heappush(h, (int(line), Node(str(i))))
			i += 1
	return h

def huffman_encoding(h):
	while len(h) != 2:
		freq_a, node_a = heappop(h)
		freq_b, node_b = heappop(h)
		freq_ab = freq_a + freq_b
		symbol_ab = node_a.symbol + node_b.symbol
		node_ab = Node(symbol_ab, node_a, node_b)
		node_a.parent = node_b.parent = node_ab
		heappush(h, (freq_ab, node_ab))
	return h

def tree_traversal(node, depth, lengths):
	if node == None:
		lengths.append(depth - 1)
		return
	tree_inorder_traversal(node.left, depth + 1, lengths)
	tree_inorder_traversal(node.right, depth + 1, lengths)

if __name__=='__main__':
	heap = read_file()
	h = huffman_encoding(heap)
	freq_a, node_a = heappop(h)
	freq_b, node_b = heappop(h)
	root = Node("root", node_a, node_b)
	node_a.parent = node_b.parent = root
	lengths = []
	tree_traversal(root, 0, lengths)
	print("max codeword length:", max(lengths), "min cw len:", min(lengths))
