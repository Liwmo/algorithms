// karger_mincut.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <iostream>
#include <vector>
#include <stdlib.h>
#include <fstream>
#include <sstream>
#include <string>

int find_min_cut(std::vector<int>, std::vector< std::pair<int, int> >);

int main()
{
	std::vector<int> nodes;
	std::vector< std::pair<int, int> > edges;

	std::ifstream in_file("kargerMinCut.txt");
	std::string line;

	while (std::getline(in_file, line)) {
		std::pair<int, int> data;
		std::stringstream stream(line);
		int num, vertex;
		bool is_first = true;
		while (stream >> num) {
			if (is_first) {
				vertex = num;
				nodes.push_back(vertex);
				is_first = false;
			}
			else if (vertex > num) {
				data.first = vertex;
				data.second = num;
				edges.push_back(data);
			}
		}
	}
	/*nodes.push_back(1);
	nodes.push_back(2);
	nodes.push_back(3);
	nodes.push_back(4);
	nodes.push_back(5);
	edges.push_back(std::make_pair(2, 1));
	edges.push_back(std::make_pair(3, 2));
	edges.push_back(std::make_pair(3, 1));
	edges.push_back(std::make_pair(5, 3));
	edges.push_back(std::make_pair(5, 4));*/


	int min = 1000;
	int iterations = 2000;
	for (int i = 0; i < iterations; i++) {
		srand(i);
		int min_cut = find_min_cut(nodes, edges);
		if (min_cut < min) { min = min_cut; }
		if (i % 100 == 0) { std::cout << i << std::endl; }
	}
	std::cout << min << std::endl;
    return 0;
}

int find_min_cut(std::vector<int> nodes, std::vector< std::pair<int, int> > edges) {
	//edge contraction algorithm
	while (nodes.size() != 2) {
		//choose a random edge
		int edge_idx = rand() % edges.size();
		int node_keep = edges[edge_idx].first;
		int node_toss = edges[edge_idx].second;

		//replace old node with new node, then remove self-loops
		for (int i = 0; i < edges.size(); i++) {
			if (edges[i].first == node_toss) { edges[i].first = node_keep; }
			if (edges[i].second == node_toss) { edges[i].second = node_keep; }
			if (edges[i].first == edges[i].second) { 
				edges.erase(edges.begin() + i); 
				i--;
			}
		}
		//decrement number of nodes
		nodes.erase(nodes.begin());
	}
	
	return edges.size();
}
