import os


class Vertex:
    def __init__(self, name):
        self.Name = str(name)
        self.Value = 0
        self.AdjList = []


class Graph:
    def __init__(self, n_ver, n_edges, edge_list):
        self.num_vertices = n_ver
        self.num_edges = n_edges
        self.vertices = []
        self.edges = {}
        for v in range(1, n_ver + 1):
            new_vertex = Vertex(name=v)
            self.vertices.append(new_vertex)
        for vertex in self.vertices:
            for e in edge_list:
                edge = e.split()
                if edge[0] == str(vertex.Name):
                    adjVertex = self.findVertex(edge[1])
                    vertex.AdjList.append(adjVertex)
                if edge[1] == str(vertex.Name):
                    adjVertex = self.findVertex(edge[0])
                    vertex.AdjList.append(adjVertex)

        for e in edge_list:
            edge = e.split()
            edge_key = (self.findVertex(edge[0]), self.findVertex(edge[1]))
            edge_weight = int(edge[2])
            if edge_key in self.edges.keys():
                self.edges[edge_key] += edge_weight
            else:
                self.edges[edge_key] = edge_weight

    def findVertex(self, Name):
        for i in self.vertices:
            if str(i.Name) == str(Name):
                return i
        return

    def contract(self, u, v):
        newVertex = Vertex(name=str(u) + '-' + str(v))
        newVertexAdj = u.AdjList + v.AdjList
        newVertex.AdjList.append(newVertexAdj)

        for i in u.AdjList:
            edge_key = (newVertex, i)
            edge_weight = self.edges[(u, i)]
            if edge_key in self.edges.keys():
                self.edges[edge_key] += edge_weight
            else:
                self.edges[edge_key] = edge_weight
            del self.edges[edge_key]

        for j in v.AdjList:
            edge_key = (newVertex, j)
            edge_weight = self.edges[(v, j)]
            if edge_key in self.edges.keys():
                self.edges[edge_key] += edge_weight
            else:
                self.edges[edge_key] = edge_weight
            del self.edges[edge_key]

        self.vertices.remove(u)
        self.vertices.remove(v)

    def printGraph(self):
        print("================ VERTICES ==================")
        for v in self.vertices:
            print("Vertex: ", v.Name)
            print("Adj list")
            for a in set(v.AdjList):
                print(a.Name)
            print("------------------------------------------")

        for e in self.edges:
            print("EDGE: ")
            for i in e:
                print(i.Name)
            print("WEIGHT: ", self.edges[e])


class maxHeap:

    # Constructor to initialize a heap
    def __init__(self):
        self.Heap = []
        self.Size = 0
        self.valueToIndex = {}

    def extractHeapify(self, idx):
        # Update Heap to keep maximum at root
        largest = idx
        left = 2 * idx + 1
        right = 2 * idx + 2
        # if the child is lareger than parent, change indexes
        if left < len(self.Heap) and self.Heap[left].Value > self.Heap[largest].Value:
            largest = left
        if right < len(self.Heap) and self.Heap[right].Value < self.Heap[largest].Value:
            largest = right
        # if the  index has chnaged swap nodes and heapify again
        if largest != idx:
            self.Heap[idx], self.Heap[largest] = self.Heap[largest], self.Heap[idx]
            self.valueToIndex[self.Heap[largest]] = largest
            self.valueToIndex[self.Heap[idx]] = idx
            self.extractHeapify(largest)

    def extractMax(self):
        # Extract the maximum value (in root)
        if self.isEmpty():
            return
        root = self.Heap[0]
        # Substitite the root with last element
        self.Heap[0] = self.Heap[len(self.Heap) - 1]
        self.valueToIndex[self.Heap[0]] = 0
        self.Heap.pop()
        self.valueToIndex[root] = None
        # Update heap
        self.extractHeapify(0)

        return root

    def insertHeapify(self, idx):
        # update heap after insert
        parent = int(((idx - 1) / 2))
        # check if the inserted element is larger than its parent
        if self.Heap[idx].Value > self.Heap[parent].Value:
            self.Heap[idx], self.Heap[parent] = self.Heap[parent], self.Heap[idx]
            self.valueToIndex[self.Heap[parent]] = parent
            self.valueToIndex[self.Heap[idx]] = idx
            self.insertHeapify(parent)

    def insert(self, v):
        # insert node at the end of heap
        self.Heap.append(v)
        self.valueToIndex[v] = len(self.Heap) - 1
        self.insertHeapify(self.valueToIndex[v])
        return

    def increaseKey(self, v):
        idx = self.valueToIndex[v]
        parent = int(((idx - 1) / 2))
        if self.Heap[idx].Value > self.Heap[parent].Value:
            self.Heap[idx], self.Heap[parent] = self.Heap[parent], self.Heap[idx]
            self.valueToIndex[self.Heap[parent]] = parent
            self.valueToIndex[self.Heap[idx]] = idx
            self.insertHeapify(parent)

    def isEmpty(self):
        return len(self.Heap) == 0

    def isInMaxHeap(self, v):
        return self.valueToIndex[v] is not None

    def print_Heap(self):
        print("HEAP: ")
        for i in self.Heap:
            print("Name: ", i.Name, ", Value: ", i.Value)


def stMinCut(G):
    Q = maxHeap()
    for ver in G.vertices:
        Q.insert(ver)
    V = G.vertices
    s = None
    t = None
    while not Q.isEmpty():
        u = Q.extractMax()
        s = t
        t = u
        for v in u.AdjList:
            if Q.isInMaxHeap(v):
                v.Value += G.edges[(v, u)]
                Q.increaseKey(v)
    V.remove(t)
    minCut = [[], []]
    minCut_weight = 0
    for i in V:
        current_edge = i.Name + ' ' + t.Name
        if current_edge in G.edges.keys():
            minCut[0].append(current_edge)
            minCut_weight += G.get_weight(i, t)
    minCut[1].append(minCut_weight)
    return minCut, s, t


def GlobalMinCut(G):
    if len(G.vertices) == 2:
        return G.vertices
    else:
        C1, s, t = stMinCut(G)
        G.contract(s, t)
        C2 = GlobalMinCut(G)
        if C1[1][0] <= C2[1][0]:
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

        if (filename.endswith('.txt')):
            print('processing ', filename)
            f = open(dir_name + '/' + filename)

            line = f.readline().split()
            edges = f.read().splitlines()
            g = Graph(int(line[0]), int(line[1]), edges)
            # g.printGraph()
            # g.add_edges(edges)
            minCut = GlobalMinCut(g)
            print(minCut)
            f.close()

            # graph_sizes.append(g.num_vertices)

            # stMinCut(g)
