import numpy as np
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt


import draw

"""randomly creating a truss structure of only hinges and forces (no torques)"""

#support of the structure and external forces

given_nodes = np.array([[0,0], [10,0], [5,5]])
given_node_supp = np.array([[1,1,1],[1,1,1],[0,0,0]])
given_f_ext = np.array([0,0,0, 0,0,0, 0, -1, 0])

n_given_nodes = 3

#envelope of possible node placements
x_min = np.min(given_nodes[:,0])
y_min = np.min(given_nodes[:,1])
x_max = np.max(given_nodes[:,0])
y_max = np.max(given_nodes[:,1])

n_internal_nodes = np.random.randint(1,4)
n_nodes = n_given_nodes + n_internal_nodes

nodes = np.zeros((n_nodes, 2))
for i in range(len(given_nodes[:,0])):
    nodes[i] = given_nodes[i]

node_disp = np.zeros(3*n_nodes)
f_ext = np.zeros(3*n_nodes)

for i in range(len(given_f_ext)):
    f_ext[i] = given_f_ext[i]


#generating the internal nodes
for i in range(n_internal_nodes):
    x = np.random.randint(x_min, x_max)
    y = np.random.randint(y_min, y_max)
    nodes[n_given_nodes+i] = np.array([x, y])



#creating the beams
tri = Delaunay(nodes)
#print(tri.simplices)

#creating the beams from the triangles
beam_nodes = np.zeros((len(tri.simplices)*3,2))
beam_counter = 0
for triangle in tri.simplices:
    beam0 = np.zeros(2)
    beam0[0] = triangle[0]
    beam0[1] = triangle[1]
    beam_nodes[beam_counter] = beam0
    beam_counter += 1
    beam1 = np.zeros(2)
    beam1[0] = triangle[1]
    beam1[1] = triangle[2]
    beam_nodes[beam_counter] = beam1
    beam_counter += 1
    beam2 = np.zeros(2)
    beam2[0] = triangle[0]
    beam2[1] = triangle[2]
    beam_nodes[beam_counter] = beam2
    beam_counter += 1


#removing doubles
index = np.array([],dtype = int)
length = len(beam_nodes)
for i in range(length):
    a = beam_nodes[i][0]
    b = beam_nodes[i][1]
    dublicates = 0
    for j in range(i+1, length):
        if ((a == beam_nodes[j][0] and b == beam_nodes[j][1]) or (b == beam_nodes[j][0] and a == beam_nodes[j][1])):
            if dublicates < 1:
                index = np.append(index, [j], axis=0)
            dublicates += 1

beam_nodes = np.delete(beam_nodes, index, axis = 0)




fig = plt.figure()
ax = fig.add_subplot(1,1,1)

ax.triplot(nodes[:,0], nodes[:,1], tri.simplices)
ax.plot(nodes[:,0], nodes[:,1], 'o')
plt.axis('scaled')
plt.show()
