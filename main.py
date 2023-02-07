import input
import draw
import stiffness as s

print(input.beam_nodes)
#draw.print_support(input.node_supp, input.nodes)
#draw.print_beams(input.beam_nodes, input.nodes)

beam_k_loc = s.create_local_stiffness_matrixes(input.beam_nodes, input.beam_supp,input.beam_prop)
