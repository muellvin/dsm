import numpy as np

nodes = np.array([[0,0], [1,0], [2,0]])

node_disp = np.array([0,0,0, 0,0,0, 0,0,0])
f_ext = np.array([0,0,0, 0,-1,0, 0,0,0])
#p_int = np.array([[0,0,0],[0,0,0],[0,0,0]])

beam_nodes = np.array([[0,1],[1,2]])
beam_supp = np.array([[1, 1, 1, 1, 1, 0],[1, 1, 0, 1, 1, 1]])
beam_prop = np.array([[A, E , I, L],[]])

#building the stiffness matrixes of each beam
beam_k_loc = np.array((len(beam_nodes), 6, 6))
beam_k_glob = beam_k_loc

for i in range(len(beam_nodes)):
    if (beam_supp[i] == [1, 1, 1, 1, 1, 0]):
        beam_k_loc[i] = a
    else if (beam_supp[i] == [1, 1, 0, 1, 1, 1]):
        abs
    else if (beam_supp[i] == [1, 1, 1, 1, 1, 1]):
        abs
    else
        falsefalsefalse



k_sys = np.zeros((3*len(nodes),3*len(nodes)))

#iterating through beams and their nodes
for i in range(0, len(beam_nodes)):
    nodei = beam_nodes[i][0]
    nodej = beam_nodes[i][1]
