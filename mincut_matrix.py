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
        rows = self.num_vertices + 1
        self.w_adjacency_matrix = [[0] * rows for _ in range(rows)]
        self.weighted_degree = [0] * rows

    def add_edges(self, list_edges):
        for i in list_edges:
            edge = i.split()
            self.w_adjacency_matrix[int(edge[0])][int(edge[1])] = int(edge[2])
            self.w_adjacency_matrix[int(edge[1])][int(edge[0])] = int(edge[2])

    def build_weighted_degree(self):
        for vertex in range(self.num_vertices + 1):
            weight_sum = 0
            for v in range(self.num_vertices + 1):
                weight_sum = weight_sum + self.w_adjacency_matrix[vertex][v]
            self.weighted_degree[vertex] = weight_sum

    def get_num_vertices(self):
        verticies = []
        for vertex in range(self.num_vertices + 1):
            for v in range(self.num_vertices + 1):
                if self.w_adjacency_matrix[vertex][v] != 0:
                    if vertex not in verticies:
                        verticies.append(vertex)
                    if v not in verticies:
                        verticies.append(v)

        return len(verticies)

    def get_graph(self):
        for i in range(self.num_vertices + 1):
            for j in range(self.num_vertices + 1):
                if self.w_adjacency_matrix[i][j] != 0:
                    print(i, ' ', j, ' -> ', self.w_adjacency_matrix[i][j])

    def get_weighted_degree(self):
        print(self.weighted_degree)


def upper_bound(arr, N, X):
    # Initialize starting and ending index
    mid = 0
    low = 0
    high = N

    # Till low is less than high
    while low < high:
        # Find the middle index
        mid = low + (high - low) // 2
        # If X is greater than or equal to arr[mid] then find in right subarray
        if X >= arr[mid]:
            low = mid + 1
        # If X is less than arr[mid] then find in left subarray
        else:
            high = mid

    # if X is greater than arr[n-1]
    if low < N and arr[low] <= X:
        low = low + 1

    # Return the upper_bound index
    return low


def binary_search(search_list, low, high, x):
    i = upper_bound(search_list, len(search_list), x)
    if search_list[i - 1] <= x < search_list[i]:
        return i


# function used to pick an edge proportionally to its weight
def random_select(cumulative_weights):
    r = random.choice(range(0, cumulative_weights[-1]))
    bound = binary_search(cumulative_weights, 0, len(cumulative_weights), r)
    return bound


# function that selects the starting edge (u,v) for the contraption procedure
def edge_select(g):
    # choose the vertex u proportional to the weighted degree with a call to random_select
    # build the weighted degree of the graph
    g.build_weighted_degree()
    # g.get_weighted_degree()
    cumulative_weights_D = []
    weight_sum = 0
    # create the cumulative weights we will use in random select
    for i in range(len(g.weighted_degree)):
        weight_sum = weight_sum + g.weighted_degree[i]
        cumulative_weights_D.append(weight_sum)

    u = random_select(cumulative_weights_D)
    # choose vertex v proportional to the weighted matrix with a call to random_select
    cumulative_weights_W = []
    weight_sum = 0
    # create the cumulative weights for the matrix we will use in random select
    for vertex in range(g.num_vertices + 1):
        weight_sum = weight_sum + g.w_adjacency_matrix[u][vertex]
        cumulative_weights_W.append(weight_sum)

    v = random_select(cumulative_weights_W)
    return [u, v]


def contract_edge(g, u, v):
    g.weighted_degree[u] = g.weighted_degree[u] + g.weighted_degree[v] - (2 * g.w_adjacency_matrix[u][v])
    g.weighted_degree[v] = 0
    g.w_adjacency_matrix[v][u] = 0
    g.w_adjacency_matrix[u][v] = 0
    for w in range(g.num_vertices + 1):
        if w != u and w != v:
            g.w_adjacency_matrix[u][w] = g.w_adjacency_matrix[u][w] + g.w_adjacency_matrix[v][w]
            g.w_adjacency_matrix[w][u] = g.w_adjacency_matrix[w][u] + g.w_adjacency_matrix[w][v]
            g.w_adjacency_matrix[v][w] = 0
            g.w_adjacency_matrix[w][v] = 0


def contract(g, k):
    n = g.get_num_vertices()
    for i in range(0, n - k):
        [u, v] = edge_select(g)
        # print('edge we about to contract: ', u, '-', v)
        contract_edge(g, u, v)

    return g


def recursive_contract(g):
    n = g.get_num_vertices()
    if n <= 6:
        new_g = contract(g, 2)
        # new_g.get_graph()
        for i in range(g.num_vertices + 1):
            for j in range(g.num_vertices + 1):
                if new_g.w_adjacency_matrix[i][j] != 0:
                    return new_g.w_adjacency_matrix[i][j]

    t = math.ceil((n / math.sqrt(2)) + 1)

    compare_graphs = []
    compare_weights = []

    for i in range(1, 2):
        compare_graphs.append(contract(g, t))
        compare_weights.append(recursive_contract(compare_graphs[i - 1]))

    return min(compare_weights)


def karger(g, k):
    a = g.num_edges + 1
    step = 1
    c = 0
    minimum = 999999999
    while a != 0:
        #print("step: ", step)
        k_instance = (step*(step**2) * round(math.log(step, 2)))//2
        #print("k: ", k_instance)
        for i in range(1, k_instance):
            t = recursive_contract(g)
            if t < minimum:
                minimum = t
        step += 1
        a -= 1
    return minimum


if __name__ == '__main__':

    dir_name = 'dataset'
    graph_sizes = []

    directory = os.fsencode(dir_name)
    for file in sorted(os.listdir(directory)):
        filename = os.fsdecode(file)

        if filename.endswith('.txt'):
            print('processing ', filename)
            f = open(dir_name + '/' + filename)
            line = f.readline().split()
            g = Graph(int(line[0]), int(line[1]))
            edges = f.read().splitlines()
            g.add_edges(edges)
            f.close()
            graph_sizes.append(g.num_vertices)
            k = 10 * (g.num_vertices**4) * round(math.log(g.num_vertices, 2))
            result = karger(g, k)
            print(result)
