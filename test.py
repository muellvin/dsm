import numpy as np

nodes = np.array([[0,0], [1,0], [2,0]])

node_dis = np.array([[0,0,0],[0,0,0],[0,0,0]])
f_ext = np.array([[0,0,0],[0,-1,0],[0,0,0]])
p_int = np.array([[0,0,0],[0,0,0],[0,0,0]])

beam_nodes = np.array([[0,1],[1,2]])
beam_supp = np.array([[1, 1, 1, 1, 1, 0],[1, 1, 0, 1, 1, 0]])

#building the stiffness matrixes of each beam
beam_k_loc = np.array((len(beam_nodes), 6, 6))

for i in range(len(beam_nodes)):
    k_loc = np.array([[1,0,0,-1,0,0],[0,1,1,0,-1,1],[0,1,1,0,-1,1],[-1,0,0,1,0,0],[0,-1,-1,0,1,-1],[0,1,1,0,-1,1]])
    for j in range(0,3):
        k_loc = k_loc[j]*beam_supp
    #then also rotating
    #then adding
    beam_k_loc[i] = k_loc


k_sys = np.zeros((3*len(nodes),3*len(nodes)))

#iterating through beams and their nodes
for i in range(0, len(beam_nodes)):
    nodei = beam_nodes[i][0]
    nodej = beam_nodes[i][1]
