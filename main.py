import input
import draw
import stiffness as s
import numpy as np
import matplotlib.pyplot as plt
print(input.beam_nodes)
#draw.print_support(input.node_supp, input.nodes)
#draw.print_beams(input.beam_nodes, input.nodes)

beam_k_loc = s.create_local_stiffness_matrixes(input.beam_nodes, input.beam_supp,input.beam_prop)
beam_k_glob = s.rotate_stiffness_matrices(input.beam_prop, beam_k_loc)
k_sys = s.build_k_sys(input.beam_nodes, beam_k_glob, input.node_supp)
k_ff = s.get_k_ff(k_sys, input.node_supp, input.nodes, input.beam_nodes, input.beam_supp)
k_sf = s.get_k_sf(k_sys, input.node_supp, input.nodes, input.beam_nodes, input.beam_supp)
f_ext_f = s.get_f_ext_f(input.f_ext, input.node_supp, input.nodes, input.beam_nodes, input.beam_supp)

if np.linalg.det(k_ff) == 0:
    print("structure cannot hold")
else:
    sol = s.solve_for_u_f(k_ff, f_ext_f)
    print("solution")
    print(s)


reaction_forces = np.matmul(k_sf, sol)
print("reaction forces")
print(reaction_forces)

#create the figure
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
#draw.print_support_beams(input.beam_supp, input.beam_nodes, input.number_of_beams, input.nodes)
#draw.print_force_ext(ax, input.f_ext, input.number_of_nodes, input.nodes)
draw.print_support_nodes(ax, input.node_supp, input.nodes)
draw.print_beams(ax, input.beam_nodes, input.nodes)

plt.axis('scaled')
plt.show()
