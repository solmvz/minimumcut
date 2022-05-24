import random
import os
import gc
import copy
import math
from time import perf_counter_ns
import xlsxwriter


class Graph:
	def __init__(self, n_ver, n_edges):
		self.num_vertices = n_ver
		self.num_edges = n_edges
		rows = self.num_vertices+1
		self.edges = {}
		self.adjList = [[] for _ in range(self.num_vertex+1)]

	def add_edges(self, list_edges):
		for i in list_edges:
			keys = []
            weights = []
            for i in list_edges:

                edge = i.split()
                if edge[0] != edge[1]:
                    keys.append(str(edge[0]) + ' ' + str(edge[1]))
                    weights.append(int(edge[2]))

            for k in range(len(keys)):
                self.edges[keys[k]] = weights[k] uguale

    def find_adj(self, v):
        adj_ls = []
        # find the adjacency list for a given vertex
        for i in self.edges:
            edge_key = i.split(' ')
            if int(edge_key[0]) == v:
                adj_ls.append(int(edge_key[1]))
            elif int(edge_key[1]) == v:
                adj_ls.append(int(edge_key[0]))
        return adj_ls

	def diminish_nodes(self):
		self.num_vertices = self.num_vertices - 1

	def get_graph(self):
		print(self.edges)


def stMinCut(g):
	Q = maxHeap(g)
	for v in range(len(g.num_vertices)):
		v.key = 0
		insert(Q, v, v.key)

	s = None
	t = None
	while not Q.isEmpty():
		u = Q.extractMax()
		s = t
		t = u
		for v in u.adjList:
			if v in Q:
				v.key = v.key + weight(u,v)
				IncreaseKey(Q, v, v.key)

	return 'ciao'
	#return (V - {t}, {t}), s, t


if __name__ == '__main__':

	dir_name = 'dataset'
	num_calls = 1
	num_instances = 1
	graph_sizes = []
	run_times = []

	f_results = open('results/karger_cuts.txt', 'w+')
	f_results.write('File\tSize of Cut\n')

	directory = os.fsencode(dir_name)
	for file in sorted(os.listdir(directory)):
		filename = os.fsdecode(file)

		if(filename.endswith('.txt')):
			print('processing ', filename)
			f = open(dir_name + '/' + filename)

			line = f.readline().split()
			g = Graph(int(line[0]), int(line[1]))

			edges = f.read().splitlines()
			g.add_edges(edges)

			f.close()

			graph_sizes.append(g.num_vertices)

			# stMinCut(g)
