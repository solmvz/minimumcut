import random
import os
import gc
import copy
import math
from time import perf_counter_ns
import xlsxwriter


class Graph:
    def __init__(self, n_ver, n_edges, edge_list):
        self.num_vertices = n_ver
        self.num_edges = n_edges
        self.vertices = {}
        self.edges = {}
        for v in range(1, n_ver + 1):
            # new_vertex = Vertex(name=v)
            # self.vertices.append(new_vertex)
            self.vertices[str(v)] = (0, [])
        for vertex in self.vertices:
            for e in edge_list:
                edge = e.split()
                if edge[0] == str(vertex):
                    # adjVertex = self.findVertex(edge[1])
                    # vertex.AdjList.append(adjVertex)
                    self.vertices[vertex][1].append(str(edge[1]))
                elif edge[1] == str(vertex):
                    # adjVertex = self.findVertex(edge[0])
                    # vertex.AdjList.append(adjVertex)
                    self.vertices[vertex][1].append(str(edge[0]))

        for e in edge_list:
            edge = e.split()
            # edge_key1 = (self.findVertex(edge[0]), self.findVertex(edge[1]))
            edge_key1 = (edge[0], edge[1])

            edge_weight = int(edge[2])
            if edge_key1 in self.edges.keys():
                self.edges[edge_key1] += edge_weight
            else:
                self.edges[edge_key1] = edge_weight

            # edge_key2 = (self.findVertex(edge[1]), self.findVertex(edge[0]))
            edge_key2 = (edge[1], edge[0])
            edge_weight = int(edge[2])
            if edge_key2 in self.edges.keys():
                self.edges[edge_key2] += edge_weight
            else:
                self.edges[edge_key2] = edge_weight

    def contract(self, u, v):
        newVertex = str(u) + '-' + str(v)

        if (u, v) in self.edges.keys():
            del self.edges[u, v]
            self.vertices[u][1].remove(v)
            self.vertices[v][1].remove(u)

        newVertexAdjList = self.vertices[u][1] + self.vertices[v][1]
        temp_ls1 = list(self.vertices[u])
        temp_ls1[1] = list(set(self.vertices[u][1]))
        self.vertices[u] = tuple(temp_ls1)
        temp_ls2 = list(self.vertices[v])
        temp_ls1[1] = list(set(self.vertices[v][1]))
        self.vertices[v] = tuple(temp_ls2)

        for i in self.vertices[u][1]:
            self.vertices[i][1].remove(u)
            edge_key1 = (newVertex, i)
            edge_key2 = (i, newVertex)
            edge_weight = self.edges[u, i]
            if edge_key1 in self.edges.keys():
                self.edges[edge_key1] += edge_weight
                self.edges[edge_key2] += edge_weight
            else:
                self.vertices[i][1].append(newVertex)
                self.edges[edge_key1] = edge_weight
                self.edges[edge_key2] = edge_weight
            del self.edges[u, i]
            del self.edges[i, u]

        for j in self.vertices[v][1]:
            self.vertices[j][1].remove(v)
            edge_key1 = (newVertex, j)
            edge_key2 = (j, newVertex)
            edge_weight = self.edges[v, j]
            if edge_key1 in self.edges.keys():
                self.edges[edge_key1] += edge_weight
                self.edges[edge_key2] += edge_weight
            else:
                self.vertices[j][1].append(newVertex)
                self.edges[edge_key1] = edge_weight
                self.edges[edge_key2] = edge_weight
            del self.edges[v, j]
            del self.edges[j, v]
        self.num_vertices -= 1
        self.vertices[newVertex] = (0, list(set(newVertexAdjList)))
        del self.vertices[u]
        del self.vertices[v]

    def printGraph(self):
        print(self.vertices)
        print(self.edges)


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



def full_contraction(g, k):
    n = g.get_num_vertices()
    for i in range(0, n - k):
        [u, v] = edge_select(g)
        # print('edge we about to contract: ', u, '-', v)
        g.contract(u, v)
    return g


def recursive_contract(g):
    n = g.num_vertices
    if n <= 6:
        new_g = full_contraction(g, 2)
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


def karger_stein(g, k):
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


def measure_run_times(g, num_calls, num_instances, k):
    sum_times = 0.0
    for i in range(num_instances):
        gc.disable()
        start_time = perf_counter_ns()
        for i in range(num_calls):
            result = karger_stein(g, k)
        end_time = perf_counter_ns()
        gc.enable()
        sum_times += (end_time - start_time)/num_calls
    avg_time = int(round(sum_times/num_instances))
    # return average time in nanoseconds
    return [avg_time, result]


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
            k = (g.num_vertices ** 2) * round(math.log(g.num_vertices,2))

            [avg_time, result] = measure_run_times(g, num_calls, num_instances, k)

            run_times.append(avg_time)
            f_results.write(filename + '\t' + str(result) + '\n')

    f_results.close()
    with open('results/karger_stein_results.txt', 'w+') as f:
        f.write("Sizes\tTimes\n")
        for i in range(len(graph_sizes)):
            f.write("%s\t%s\n" % (graph_sizes[i], run_times[i]))
