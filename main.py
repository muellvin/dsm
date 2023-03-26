import input
import draw
import stiffness as s
import numpy as np
import matplotlib.pyplot as plt
np.set_printoptions(precision=2)
np.set_printoptions(suppress=True)



beam_k_loc = s.create_local_stiffness_matrixes(input.beam_nodes, input.beam_supp,input.beam_prop)
beam_k_glob = s.rotate_stiffness_matrices(input.beam_prop, beam_k_loc)
k_sys = s.build_k_sys(input.beam_nodes, beam_k_glob, input.node_supp)
print("k_sys")
print(k_sys)

k_ff = s.get_k_ff(k_sys, input.node_supp, input.nodes, input.beam_nodes, input.beam_supp)
k_sf = s.get_k_sf(k_sys, input.node_supp, input.nodes, input.beam_nodes, input.beam_supp)
f_ext_f = s.get_f_ext_f(input.f_ext, input.node_supp, input.nodes, input.beam_nodes, input.beam_supp)

det = np.linalg.det(k_ff)
print("determinant of k_ff")
print(det)
#the determinant should be non zero; the transformation should be reversable
if abs(det) < 1e-10:
    print("structure cannot hold")
else:
    sol = s.solve_for_u_f(k_ff, f_ext_f)
    print("solution")
    print(sol)
    reaction_forces = np.matmul(k_sf, sol)
    print("reaction forces")
    print(reaction_forces)


#create the figure
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
draw.print_supp(ax, input.nodes, input.node_supp)
draw.print_nodes(ax,input.nodes)
draw.print_beams(ax, input.beam_nodes, input.nodes)
draw.print_force_ext(ax, input.nodes, input.f_ext)

plt.axis('scaled')
plt.show()
