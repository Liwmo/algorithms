// quicksort.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <vector>
#include <iostream>
#include <fstream>

long quicksort(std::vector<int>&, int, int);
int partition(std::vector<int>&, int, int, int);
int get_pivot_index(std::vector<int>, int, int);

int main()
{
	//std::vector<int> list = { 5, 2, 6, 3, 7, 0, 1, 8, 4, 9 };
	std::vector<int> list;
	std::ifstream input_file("QuickSort.txt");
	int val = 0;
	while (input_file >> val) {
		list.push_back(val);
	}
	long comparisons = quicksort(list, 0, list.size());
	/*for (int i = 0; i < list.size(); i++) {
		std::cout << list[i];
	}*/
	std::cout << std::endl;
	std::cout << comparisons << std::endl;
    return 0;
}

long quicksort(std::vector<int>& list, int left, int right) {
	long comparisons = 0;
	if (right - left <= 1) {
		return 0;
	}
	else {
		comparisons += (right - left - 1);
	}
	
	int p_idx = get_pivot_index(list, left, right);
	int new_idx = partition(list, p_idx, left, right);

	comparisons += quicksort(list, left, new_idx);
	comparisons += quicksort(list, new_idx + 1, right);
	return comparisons;
}

int partition(std::vector<int>& list, int p_idx, int left, int right) {
	//swap pivot to first position
	int temp = list[left];
	int pivot = list[p_idx];
	list[left] = pivot;
	list[p_idx] = temp;

	//partition the list (<pivot on left, >pivot on right)
	int i = left + 1;
	for (int j = left + 1; j < right; j++) {
		if (list[j] < pivot) {
			temp = list[i];
			list[i] = list[j];
			list[j] = temp;
			i++;
		}
	}

	//reswap pivot to final position
	temp = list[i-1];
	list[i-1] = pivot;
	list[left] = temp;
	return i-1;
}

//find median index from 1st, middle, and last element of list
int get_pivot_index(std::vector<int> list, int left, int right) {
	int arr[3];
	arr[0] = left;
	arr[1] = left + (right - left - 1) / 2;
	arr[2] = right - 1;

	//find max and min
	int max = 0, min = INT_MAX;
	int max_idx, min_idx, pivot_idx;
	for (int i = 0; i < 3; i++) {
		if (list[arr[i]] > max) { 
			max = list[arr[i]];
			max_idx = i;
		}
		if (list[arr[i]] < min) {
			min = list[arr[i]];
			min_idx = i;
		}
	}

	//return NOT max or min (median)
	for (int i = 0; i < 3; i++) {
		if (i != max_idx && i != min_idx) {
			pivot_idx = arr[i];
		}
	}
	return pivot_idx;
}