import input
import draw
import numpy as np
import dsm
import matplotlib.pyplot as plt


print(input.beam_prop)
nodes_new, load = dsm.compute_deformation(input.nodes, input.node_supp, input.f_ext, input.beam_nodes, input.beam_supp, input.beam_prop)

#create the figure
draw.draw_structure(input.nodes, load, input.node_supp, input.beam_nodes, input.f_ext)
