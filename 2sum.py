import math
import bisect

def get_next():
	with open('data/2sum.txt', 'r') as f:
		for line in f:
			yield int(line)

class Node:
	def __init__(self, key, value):
		self.next = None
		self.key = key
		self.value = value

class LinkedList:
	def __init__(self):
		self.head = None
		self.length = 0

	def insert(self, key, value):
		node = Node(key, value)
		node.next = self.head
		self.head = node
		self.length += 1

	def search(self, key):
		current = self.head
		while current.key is not key:
			if current.next is None:
				return None
			current = current.next
		return current.value

class HashTable:
	NUM_BUCKETS = 12888803

	def __init__(self):
		self._list = [None] * self.NUM_BUCKETS
		self._keys = []

	def insert(self, key, value):
		index = self._hash(key)
		self._keys.append(key)
		if self._list[index] == None:
			link = LinkedList()
			link.insert(key, value)
			self._list[index] = link
		else:
			self._list[index].insert(key, value)

	def get(self, key):
		index = self._hash(key)
		if self._list[index] == None:
			return None
		value = self._list[index].search(key)
		return value

	def keys(self):
		return self._keys

	def _hash(self, value):
		return value % self.NUM_BUCKETS

if __name__=='__main__':
	iterator = get_next()
	# table = HashTable()
	values = []
	for key in iterator:
		# table.insert(int(key), 1)
		bisect.insort_left(values, key)

	all_sums = []
	for x in values:
		lower = bisect.bisect_left(values, -10000 - x)
		upper = bisect.bisect(values, 10000 - x)
		valid_sums = [ x + i for i in values[lower:upper] ]
		all_sums.extend(valid_sums)

	print(len(set(all_sums)))

# max_collision = 0
# index = 0
# for i in range(HashTable.NUM_BUCKETS):
# 	if table._list[i] is not None:
# 		if table._list[i].length > max_collision:
# 			max_collision = table._list[i].length
# 			index = i
# print(max_collision, index)

# tally = 0
# for target in range(-10000,10000):
# 	if target % 100 == 0:
# 		print(target)
# 	# for key in table.keys():
# 	for key in values:
# 		search = target - key
# 		# result = table.get(search)
# 		result = index(values, search)
# 		if result and search is not key:
# 			tally += 1 
# 			break
# print(tally)