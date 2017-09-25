#include "stdafx.h"
#include <iostream>
#include <vector>
#include <fstream>

struct Pair {
	long long inversions;
	std::vector<int> sorted;
};
Pair make_pair(int x, std::vector<int> y) {
	Pair p = { x, y };
	return p;
}
Pair sort_and_count(std::vector<int>);
Pair merge_and_count(std::vector<int>, std::vector<int>);

int main()
{
	std::vector<int> vals;
	int val = 0;
	std::ifstream input_file{ "IntegerArray.txt" };
	while (input_file >> val) {
		vals.push_back(val);
	}
	if (vals.size() > 0) {
		Pair result = sort_and_count(vals);
		std::cout << result.inversions << std::endl;
	}
	/*for (int i = 0; i < result.sorted.size(); i++) {
		std::cout << result.sorted[i];
	}
	std::cout << std::endl;*/
}

//merge sort algorithm O(n log n)
Pair sort_and_count(std::vector<int> vals) {
	if (vals.size() == 1) {
		return Pair{ 0, vals };
	}

	int half_idx = vals.size() / 2;
	std::vector<int> a(vals.begin(), vals.begin() + half_idx);
	std::vector<int> b(vals.begin() + half_idx, vals.end());

	Pair left = sort_and_count(a);
	Pair right = sort_and_count(b);
	Pair split = merge_and_count(left.sorted, right.sorted);
	return Pair{ left.inversions + right.inversions + split.inversions, split.sorted };
}

Pair merge_and_count(std::vector<int> left, std::vector<int> right) {
	int i = 0, j = 0;
	std::vector<int> sorted;
	long long inversions = 0;
	while (i < left.size() && j < right.size()) {
		if (left[i] > right[j]) {
			inversions += (left.size() - i);
			sorted.push_back(right[j]);
			j++;
		}
		else {
			sorted.push_back(left[i]);
			i++;
		}
	}
	if (i < left.size()) { sorted.insert(sorted.end(), left.begin() + i, left.end()); }
	else { sorted.insert(sorted.end(), right.begin() + j, right.end()); }
	return Pair{ inversions, sorted };
}