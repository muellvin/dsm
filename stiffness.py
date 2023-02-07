import numpy as np

def create_local_stiffness_matrixes(beam_nodes, beam_supp,beam_prop):
    beam_k_loc = np.zeros((len(beam_nodes), 6, 6), dtype=float)

    for i in range(len(beam_nodes)):
        A = beam_prop[i][0]
        E = beam_prop[i][1]
        I = beam_prop[i][2]
        L = beam_prop[i][3]

        #beam clamped on both sides
        if (beam_supp[i].all() == [1, 1, 1, 1, 1, 1]).all():
            a = E*I/(L**3)*np.array([[A*L**2/I, 0, 0, -A*L**2/I, 0, 0], \
                                                [0, 12, 6*L, 0, -12, 6*L], \
                                                [0, 6*L,4*L**2, 0, -6*L, 2*L**2], \
                                                [-A*L**2/I, 0, 0, A*L**2/I, 0, 0], \
                                                [0, -12, -6*L, 0, 12, -6*L], \
                                                [0, 6*L, 2*L**2, 0, -6*L, 4*L**2]], dtype=float)
        #beam pinned on both sides
        elif (beam_supp[i] == [1, 1, 0, 1, 1, 0]).all():
            a = E*I/(L**3)*np.array([[A*L**2/I, 0, 0, -A*L**2/I, 0, 0], \
                                                [0, 0, 0, 0, 0, 0], \
                                                [0, 0, 0, 0, 0, 0], \
                                                [-A*L**2/I, 0, 0, A*L**2/I, 0, 0], \
                                                [0, 0, 0, 0, 0, 0], \
                                                [0, 0, 0, 0, 0, 0]], dtype=float)
        #beam pinned on the left and clamped on the right
        elif (beam_supp[i] == [1, 1, 0, 1, 1, 1]).all():
            a = E*I/(L**3)*np.array([[A*L**2/I, 0, 0, -A*L**2/I, 0, 0], \
                                                [0, 3, 0, 0, -3, 3*L], \
                                                [0, 0, 0, 0, 0, 0], \
                                                [-A*L**2/I, 0, 0, A*L**2/I, 0, 0], \
                                                [0, -3, 0, 0, 3, -3*L], \
                                                [0, 3*L, 0, 0, -3*L, 3*L**2]], dtype=float)
        #beam clamped on the left and pinned on the right
        elif (beam_supp[i] == [1, 1, 1, 1, 1, 0]).all():
            a = E*I/(L**3)*np.array([[A*L**2/I, 0, 0, -A*L**2/I, 0, 0], \
                                                [0, 3, 3*L, 0, -3, 0], \
                                                [0, 3*L, 3*L**2, 0, -3*L, 0], \
                                                [-A*L**2/I, 0, 0, A*L**2/I, 0, 0], \
                                                [0, -3, -3*L, 0, 3, 0], \
                                                [0, 0, 0, 0, 0, 0]], dtype=float)

        else:
            assert false, f"beam {i} false support"
        beam_k_loc[i] = np.array(a, dtype = float)
    print(beam_k_loc)
    return beam_k_loc

def rotate_stiffness_matrices(beam_prop, beam_k_loc):
    beam_k_glob = np.zeros((len(beam_prop), 6, 6))
    for i in range(len(beam_prop)):
        phi = beam_prop[i][4]
        R = np.array([[np.cos(phi), -np.sin(phi), 0, 0, 0, 0], \
                      [np.sin(phi), np.cos(phi), 0, 0, 0, 0], \
                      [0, 0, 1, 0, 0, 0],\
                      [0, 0, 0, np.cos(phi), -np.sin(phi), 0], \
                      [0, 0, 0, np.sin(phi), np.cos(phi), 0], \
                      [0, 0, 0, 0, 0, 1]])
        beam_k_glob[i] = np.matmul(np.transpose(R), np.matmul(beam_k_loc[i], R))
    print("beam_k_glob")
    print(beam_k_glob)
    return beam_k_glob

def build_k_sys(beam_nodes, beam_k_glob, node_supp):
    k_sys = np.zeros((3*len(node_supp),3*len(node_supp)))
    for beam in range(len(beam_nodes)):
        node_a = beam_nodes[beam][0]
        node_b = beam_nodes[beam][1]
        #building the 4 3x3 blocks in the matrix
        #beam_k_glob[beam] = [[aa, ab],
        #                     [ba, bb]]
        #block aa
        for i in range(0, 3):
            for j in range(0,3):
                k_sys[3*node_a+i][3*node_a+j] += beam_k_glob[beam][i][j]
        #block ab
        for i in range(0, 3):
            for j in range(0,3):
                k_sys[3*node_a+i][3*node_b+j] += beam_k_glob[beam][i][3+j]
        #block ba
        for i in range(0, 3):
            for j in range(0,3):
                k_sys[3*node_b+i][3*node_a+j] += beam_k_glob[beam][3+i][j]
        #block bb
        for i in range(0, 3):
            for j in range(0,3):
                k_sys[3*node_b+i][3*node_b+j] += beam_k_glob[beam][3+i][3+j]
    print("k_sys")
    print(k_sys)
    return k_sys

def get_free_nodes(node_supp):
    frees = np.array([], dtype=int)
    for i in range(len(node_supp)):
        for j in range(0,3):
            if node_supp[i][j] == 0:
                frees = np.append(frees, [int(3*i+j)], axis=0)
    print("free degrees")
    print(frees)
    return frees

def get_fixed_nodes(node_supp):
    fixed = np.array([])
    for i in range(len(node_supp)):
        for j in range(0,3):
            if node_supp[i][j] == 1:
                fixed = np.append(fixed, [int(3*i+j)], axis=0)
    print("fixed degrees")
    print(fixed)
    return fixed

def get_k_ff(k_sys, node_supp):

    frees = get_free_nodes(node_supp)
    k_ff = np.zeros((len(frees), len(frees)))

    counter_d = 0
    for d in np.nditer(frees):
        counter_o = 0
        for o in np.nditer(frees):
            k_ff[counter_d][counter_o] = k_sys[d][o]
            counter_o +=1
        counter_d += 1

    print("k_ff")
    print(k_ff)
    return k_ff


def get_k_sf(k_sys, node_supp):
    frees = get_free_nodes(node_supp)
    fixed = get_fixed_nodes(node_supp)

    k_sf = np.zeros((len(fixeds), len(frees)))

    counter_d = 0
    for d in np.nditer(fixeds):
        counter_o = 0
        for o in np.nditer(frees):
            k_sf[counter_d][counter_o] = k_sys[d][o]
            counter_o +=1
        counter_d += 1

    print("k_sf")
    print(k_sf)
    return k_sf

def get_f_ext_f(f_ext, node_supp):
    frees = get_free_nodes(node_supp)
    f_ext_f = np.zeros((len(frees)))

    counter = 0
    for i in np.nditer(frees):
        f_ext_f[counter] = f_ext[i]
        counter += 1

    print("f_ext_f")
    print(f_ext_f)
    return f_ext_f

def solve_for_u_f(k_ff, f_ext_f):
    return np.matmul(np.linalg.inv(k_ff), f_ext_f)
