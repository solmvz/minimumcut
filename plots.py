import matplotlib.pyplot as plt
import math

##--------------------------------------------------PREPARATION DATA--------------------------------------------
sizes_nodes = []
sizes_edges = []
times_stoer = []
with open('results/stoer_wagner_results.txt', 'r') as f:
    f.readline()
    data = f.readlines()
    for line in data:
        info = line.split()
        sizes_nodes.append(info[0])
        sizes_edges.append(info[1])
        times_stoer.append(info[2])

times_karger = []
with open('results/karger_stein_results.txt', 'r') as f:
    f.readline()
    data = f.readlines()
    for line in data:
        info = line.split()
        times_karger.append(info[1])

#--------------------------------------------PLOTS FOR STOER WAGNER ALGORITHM--------------------------------------------
constant_stoer = []
for i in range(len(sizes_nodes)):
    constant_stoer.append(round(int(times_stoer[i])/(int(sizes_nodes[i]) * int(sizes_edges[i])),3))

reference_stoer = []
theoretical_reference_stoer = []
for i in range(len(sizes_nodes)):
    theoretical_reference_stoer.append(int(constant_stoer[len(constant_stoer) // 2] * (int(sizes_nodes[i]) * int(sizes_edges[i])) * math.log(int(sizes_nodes[i]),2)))
    reference_stoer.append(int(constant_stoer[len(constant_stoer) // 2] * (int(sizes_nodes[i]) * int(sizes_edges[i]))))

times_stoer = [int(i) for i in times_stoer]
"""
plt.plot(sizes_nodes, times_stoer, label='Measured times')
plt.plot(sizes_nodes, theoretical_reference_stoer, label='O(mn*log(n))')
plt.plot(sizes_nodes, reference_stoer, label='O(mn)')
plt.xlabel('Size of the graph')
plt.ylabel('Run times (ns)')
plt.legend()
plt.savefig('confront_stoer.png',dpi=1200)
"""
#--------------------------------------------PLOTS FOR KARGER STEIN ALGORITHM--------------------------------------------
plt.figure()
constant_karger = []
for i in range(len(sizes_nodes)):
    constant_karger.append(round(int(times_karger[i])/(int(sizes_nodes[i])),3))

reference_karger = []
theoretical_reference_karger = []
for i in range(len(sizes_nodes)):
    reference_karger.append(int(constant_karger[len(constant_karger) // 2] * (int(sizes_nodes[i])**2)))# * (math.log(int(sizes_nodes[i]),2)**2)))
    theoretical_reference_karger.append(int(constant_karger[len(constant_karger) // 2] * (int(sizes_nodes[i])**2) * (math.log(int(sizes_nodes[i]),2)**3)))

times_karger = [int(i) for i in times_karger]
plt.plot(sizes_nodes, times_karger, label='Measured times')
plt.plot(sizes_nodes, reference_karger, label='O(n^2)')
#plt.plot(sizes_nodes, theoretical_reference_karger, label='O(n^2*log^3(n))')
plt.xlabel('Size of the graph')
plt.ylabel('Run times (ns)')
plt.legend()
plt.savefig('confront_karger.png',dpi=1200)

plt.show()
