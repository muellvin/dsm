import numpy as np
import generate_delaunay as gd
import draw
import matplotlib.pyplot as plt

given_nodes = np.array([[0,0], [10,0], [5,5]])
given_node_supp = np.array([[1,1],[1,1],[0,0]])
given_f_ext = np.array([0,0,0, 0,0,0, 0, 1, 0])
n_min = 4
n_max = 5

nodes, node_supp, node_disp, f_ext, beam_nodes = gd.generate_delaunay(given_nodes, given_node_supp, given_f_ext, n_min, n_max)



#create the figure
draw.draw_structure(nodes, node_supp, beam_nodes, f_ext)
