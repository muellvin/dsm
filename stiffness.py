import numpy



def create_local_stiffness_matrixes(beam_nodes, beam_supp,beam_prop):
    beam_k_loc = np.array((len(beam_nodes), 6, 6))

    for i in range(beam_nodes):
        if (beam_supp[i] == [1, 1, 1, 1, 1, 0]):
            beam_k_loc[i] =
        else if (beam_supp[i] == [1, 1, 0, 1, 1, 1]):
            beam_k_loc[i] =
        else if (beam_supp[i] == [1, 1, 1, 1, 1, 1]):
            beam_k_loc[i] =
        else
            falsefalsefalse
    return beam_k_loc

def rotate_stiffness_matrices(beam_k_loc):

k_sys = np.zeros((3*len(nodes),3*len(nodes)))
