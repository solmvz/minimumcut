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
		self.w_adjacency_matrix = [[0]*rows for _ in range(rows)]
		self.weighted_degree = [0] * (rows)

	def add_edges(self, list_edges):
		for i in list_edges:
			edge = i.split()
			self.w_adjacency_matrix[int(edge[0])][int(edge[1])] = int(edge[2])
			self.w_adjacency_matrix[int(edge[1])][int(edge[0])] = int(edge[2])

	def build_weighted_degree(self):
		for vertex in range(self.num_vertices+1):
			sum = 0
			for v in range(self.num_vertices+1):
				sum = sum + self.w_adjacency_matrix[vertex][v]

			self.weighted_degree[vertex] = sum

	def cumulative_weights(self):
		

	def get_graph(self):
		for i in range(self.num_vertices+1):
			for j in range(self.num_vertices+1):
				print(i, ' ', j, ' -> ', self.w_adjacency_matrix[i][j])

	def get_weighted_degree(self):
		print(self.weighted_degree)


# function used to pick the random edge that we will contract
def random_select(g):
	print('stuff')
	#cumulative_weights = 
#	r = random.choice(range(0, cumulative_weights[-1]))


def edge_select(matrix, weighted_degree):
	print('foo')


def contract_edge(u, v):
	print('foo')


def contract(g, k):
	print('foo')


def recursive_contract(g):
	print('foo')


if __name__ == '__main__':

	dir_name = 'dataset'
	graph_sizes = []

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
			#g.get_graph()
			#g.get_weighted_degree()
			random_select(g)


