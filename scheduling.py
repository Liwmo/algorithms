def read_file():
	weights = []
	lengths = []
	with open('data/jobs.txt', 'r') as f:
		for line in f:
			data = line.split()
			if len(data) == 1: 
				continue
			weights.append(int(data[0]))
			lengths.append(int(data[1]))
	return weights, lengths

#Key function for sorting tasks by (weight - length)
#In case of ties, prioritize tasks with the highest weight
def unoptimal_schedule_fn(task):
	return task[0] - task[1], task[0]

#Key function for sorting tasks optimally (weight/length)
def optimal_schedule_fn(task):
	return task[0] / task[1]

def calc_weighted_sum(tasks):
	completion_time = 0
	weighted_sum = 0
	for task in tasks:
		weight, length = task[0], task[1]
		completion_time += length
		weighted_sum += weight * completion_time
	return weighted_sum

if __name__=='__main__':
	weights, lengths = read_file()
	tasks = list(zip(weights, lengths))
	tasks.sort(key=optimal_schedule_fn, reverse=True)
	score = calc_weighted_sum(tasks)
	print(score)