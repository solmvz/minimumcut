import matplotlib.pyplot as plt
import math


#--------------------------------------------PLOTS FOR STOER WAGNER ALGORITHM--------------------------------------------
sizes_stoer = []
edges_stoer = []
times_stoer = []
with open('results/stoer_wagner_results.txt', 'r') as f:
    f.readline()
    data = f.readlines()
    for line in data:
        info = line.split()
        sizes_stoer.append(info[0])
        edges_stoer.append(info[1])
        times_stoer.append(info[2])

constant_stoer = [round(int(times_stoer[i])/int(sizes_stoer[i]),3) for i in range(len(sizes_stoer))]

reference_stoer = []
for i in range(len(sizes_stoer)):
    reference_stoer.append(constant_stoer[len(constant_stoer) - 1] * int(sizes_stoer[i]) * int(edges_stoer[i]) * math.log(int(sizes_stoer[i])))

plt.plot(sizes_stoer, times_stoer, label='Measured times')
plt.plot(sizes_stoer, reference_stoer, label='Reference')
plt.legend()
plt.xlabel('Size of the graph')
plt.ylabel('Run times (ns)')
plt.show()

#--------------------------------------------PLOTS FOR STOER WAGNER ALGORITHM--------------------------------------------

