import numpy as np
import generate_delaunay as gd
import draw
import input_helper as ih
import dsm
import matplotlib.pyplot as plt

given_nodes = np.array([[0,0], [10,0], [5,5]])
given_node_supp = np.array([[1,1],[1,1],[0,0]])
given_f_ext = np.array([0,0,0, 0,0,-300000])
n_min = 4
n_max = 5

nodes, node_supp, node_disp, f_ext, beam_nodes = gd.generate_delaunay(given_nodes, given_node_supp, given_f_ext, n_min, n_max)


beam_prop = ih.get_even_beam_prop(nodes, beam_nodes)
beam_supp = np.ones((len(beam_nodes),2), dtype = int)
nodes_new, load = dsm.compute_deformation(nodes, node_supp, f_ext, beam_nodes, beam_supp, beam_prop)

#create the figure
draw.draw_structure(nodes, load, node_supp, beam_nodes, f_ext)
