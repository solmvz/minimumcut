import os


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

        #for k in self.vertices:
            #self.vertices[k] = (self.vertex_tightness(k), self.vertices[k][1])

    def contract(self, u, v):
        newVertex = str(u) + '-' + str(v)
        newVertexValue = self.vertices[u][0] + self.vertices[v][0]
        if (u, v) in self.edges.keys():
            newVertexValue -= self.edges[u, v]
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

    def reset(self):
        for v in self.vertices:
            self.vertices[v] = (0, self.vertices[v][1])
        return


class maxHeap:
    # Constructor to initialize a heap
    def __init__(self):
        self.Heap = {}
        self.keyToIndex = {}

    def extractHeapify(self, index):
        # Update Heap to keep maximum at root
        largest = index
        left = 2 * index + 1
        right = 2 * index + 2
        # if the child is lareger than parent, change indexes
        if left < len(self.Heap) and self.Heap[left][1] > self.Heap[largest][1]:
            largest = left
        if right < len(self.Heap) and self.Heap[right][1] > self.Heap[largest][1]:
            largest = right
        # if the  index has chnaged swap nodes and heapify again
        if largest != index:
            self.Heap[index], self.Heap[largest] = self.Heap[largest], self.Heap[index]
            self.keyToIndex[self.Heap[largest][0]] = largest
            self.keyToIndex[self.Heap[index][0]] = index
            self.extractHeapify(largest)

    def extractMax(self):
        # Extract the maximum value (in root)
        if self.isEmpty():
            return
        root_key = self.Heap[0][0]
        root_value = self.Heap[0][1]
        # Substitite the root with last element
        self.Heap[0] = self.Heap[len(self.Heap) - 1]
        self.keyToIndex[self.Heap[0][0]] = 0
        # del self.Heap[len(self.Heap) - 1]
        #print(self.keyToIndex)
        del self.keyToIndex[root_key]
        del self.Heap[len(self.Heap) - 1]
        # Update heap
        self.extractHeapify(0)

        return root_key

    def insertHeapify(self, index):
        # update heap after insert
        parent = int(((index - 1) / 2))
        # check if the inserted element is larger than its parent
        if self.Heap[index][1] > self.Heap[parent][1]:
            self.Heap[index], self.Heap[parent] = self.Heap[parent], self.Heap[index]
            self.keyToIndex[self.Heap[parent][0]] = parent
            self.keyToIndex[self.Heap[index][0]] = index
            self.insertHeapify(parent)

    def insert(self, key, value):
        # insert node at the end of heap
        # self.Heap.append(v)
        # print(key, value)
        index = len(self.Heap)
        self.Heap[index] = (str(key), int(value))
        self.keyToIndex[str(key)] = str(index)
        self.insertHeapify(index)
        return

    def increaseKey(self, key, newValue):

        index = int(self.keyToIndex[key])
        self.Heap[index] = tuple([key, newValue])
        parent = int(((index - 1) / 2))
        #print("parent: ", parent, "value: ", self.Heap)

        if self.Heap[index][1] > self.Heap[parent][1]:
            self.Heap[index], self.Heap[parent] = self.Heap[parent], self.Heap[index]
            self.keyToIndex[self.Heap[parent][0]] = parent
            self.keyToIndex[self.Heap[index][0]] = index
            self.insertHeapify(parent)

    def isEmpty(self):
        return len(self.Heap) == 0

    def isInMaxHeap(self, k):
        if k in self.keyToIndex.keys():
            return True
        return False

    def print_Heap(self):
        print("HEAP: ")
        print(self.Heap)
        # print(self.keyToIndex)


def stMinCut(G):
    G.reset()
    Q = maxHeap()
    for key in G.vertices:
        Q.insert(key, 0)
    s = 'null'
    t = 'null'
    while not Q.isEmpty():
        u = Q.extractMax()
        s = t
        t = u
        for v in G.vertices[u][1]:
            if Q.isInMaxHeap(v):
                new_value = G.vertices[v][0] + G.edges[u, v]
                G.vertices[v] = (new_value, G.vertices[v][1])
                Q.increaseKey(v, new_value)

    cutOfthePhase = 0
    for n in G.vertices[t][1]:
        cutOfthePhase += G.edges[t, n]
    return cutOfthePhase, s, t


def GlobalMinCut(G):
    if G.num_vertices == 2:
        solution = []
        for i in G.vertices:
            solution.append(i)
        cutOfthePhase = G.edges[solution[0], solution[1]]
        return cutOfthePhase
    else:
        C1, s, t = stMinCut(G)
        G.contract(s, t)
        C2 = GlobalMinCut(G)
        if C1 <= C2:
            return C1
        else:
            return C2


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

        if filename.endswith('.txt'):
            print('processing ', filename)
            f = open(dir_name + '/' + filename)

            line = f.readline().split()
            edges = f.read().splitlines()
            g = Graph(int(line[0]), int(line[1]), edges)

            minCutWeight = GlobalMinCut(g)

            print("MIN CUT IS: ", minCutWeight)

            f.close()

