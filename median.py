import math

def get_next():
	with open('data/Median.txt', 'r') as f:
		for line in f:
			yield int(line)

class Heap:
	def __init__(self):
		self._list = [0]

	def _get_parent(self, index):
		if index == 1:
			return None, None
		else:
			return math.floor(index / 2), self._list[math.floor(index / 2)]

	def _get_left_child(self, index):
		if 2 * index < len(self._list):
			return 2 * index, self._list[2 * index]
		return None, 100000

	def _get_right_child(self, index):
		if 2 * index + 1 < len(self._list):
			return 2 * index + 1, self._list[2 * index + 1]
		return None, 100000

	def insert(self, value):
		self._list.append(value)
		self._bubble_up(len(self._list) - 1)

	def extract(self):
		 self._list[1], self._list[len(self._list) - 1] = self._list[len(self._list) - 1], self._list[1]
		 minmax = self._list.pop()
		 if len(self._list) > 2:
		 	self._bubble_down(1)
		 return minmax

	def size(self):
		return len(self._list) - 1

class MinHeap(Heap):
	def _bubble_up(self, index):
		parent_idx, parent_val = self._get_parent(index)
		if parent_idx and parent_val > self._list[index]:
			self._list[index], self._list[parent_idx] = self._list[parent_idx], self._list[index]
			self._bubble_up(parent_idx)
		return

	def _bubble_down(self, index):
		current = self._list[index]
		left_idx, left_val = self._get_left_child(index)
		right_idx, right_val = self._get_right_child(index)
		if left_val == 100000 and right_val == 100000:
			return
		if current > left_val or current > right_val:
			if left_val <= right_val:
				self._list[left_idx], self._list[index] = self._list[index], self._list[left_idx]
				self._bubble_down(left_idx)
			else:
			 	self._list[right_idx], self._list[index] = self._list[index], self._list[right_idx]
			 	self._bubble_down(right_idx)

class MaxHeap(Heap):
	def _bubble_up(self, index):
		parent_idx, parent_val = self._get_parent(index)
		if parent_idx and parent_val < self._list[index]:
			self._list[index], self._list[parent_idx] = self._list[parent_idx], self._list[index]
			self._bubble_up(parent_idx)
		return

	def _bubble_down(self, index):
		current = self._list[index]
		left_idx, left_val = self._get_left_child(index)
		right_idx, right_val = self._get_right_child(index)
		if left_val == 100000: left_val = 0
		if right_val == 100000: right_val = 0
		if left_val == 0 and right_val == 0:
			return
		if current < left_val or current < right_val:
			if left_val >= right_val:
				self._list[left_idx], self._list[index] = self._list[index], self._list[left_idx]
				self._bubble_down(left_idx)
			else:
			 	self._list[right_idx], self._list[index] = self._list[index], self._list[right_idx]
			 	self._bubble_down(right_idx)

if __name__=='__main__':
	medians = []
	stream = get_next()
	max_heap = MaxHeap()
	min_heap = MinHeap()

	init = next(stream)
	min_heap.insert(init)
	medians.append(init)
	after = next(stream)
	if after < init:
		max_heap.insert(after)
		medians.append(after)
	else:
		val = min_heap.extract()
		min_heap.insert(after)
		max_heap.insert(val)
		medians.append(init)

	for val in stream:
		maximum = min_heap.extract()
		minimum = max_heap.extract()
		if min_heap.size() - max_heap.size() == 1:
			if val <= minimum:
				max_heap.insert(val)
				max_heap.insert(minimum)
				min_heap.insert(maximum)
				medians.append(minimum)
			elif val > minimum and val < maximum:
				max_heap.insert(minimum)
				max_heap.insert(val)
				min_heap.insert(maximum)
				medians.append(val)
			else:
				max_heap.insert(minimum)
				max_heap.insert(maximum)
				min_heap.insert(val)
				medians.append(maximum)
		else:
			if val <= minimum:
				max_heap.insert(val)
				min_heap.insert(maximum)
				min_heap.insert(minimum)
				medians.append(minimum)
			elif val > minimum and val < maximum:
				max_heap.insert(minimum)
				min_heap.insert(val)
				min_heap.insert(maximum)
				medians.append(val)
			else:
				max_heap.insert(minimum)
				min_heap.insert(maximum)
				min_heap.insert(val)
				medians.append(maximum)

	print(sum(medians))