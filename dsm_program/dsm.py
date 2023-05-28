import numpy as np


#PRE:   listed arguments
#POST:  creates a stiffness matrix for each beam and returns them in an array
def create_local_stiffness_matrixes(beam_nodes, beam_supp, beam_prop):
    beam_k_loc = np.zeros((len(beam_nodes), 4, 4), dtype=float)
    for i in range(len(beam_nodes)):
        A = beam_prop[i][0]
        E = beam_prop[i][1]
        L = beam_prop[i][3]
        # 1'000 N/mm^2 * mm² / 1'000 mm = N/mm
        v = E*A/L

        #beam pinned on both sides
        assert((beam_supp[i].all() == [1, 1, 1, 1]).all(), "at least one beam is not supported through hinges")
        a = np.array([[v, 0, -v, 0], \
                      [0, 0, 0, 0], \
                      [-v, 0, v, 0], \
                      [0, 0, 0, 0]], dtype=float)

        beam_k_loc[i] = np.array(a, dtype = float)
    return beam_k_loc


#PRE:
#POST:  rotates the stiffness matrix of each beam and returns the rotated stiffness matrices as an array
def rotate_stiffness_matrices(beam_prop, beam_k_loc):
    beam_k_glob = np.zeros((len(beam_prop), 4, 4))

    for i in range(len(beam_prop)):
        phi = beam_prop[i][4]
        #print(f"bream {i} has angle {phi}")
        R = np.array([[np.cos(phi), np.sin(phi), 0, 0], \
                      [-np.sin(phi), np.cos(phi), 0, 0], \
                      [0, 0, np.cos(phi), np.sin(phi)], \
                      [0, 0, -np.sin(phi), np.cos(phi)]])
        beam_k_glob[i] = np.matmul(np.transpose(R), np.matmul(beam_k_loc[i], R))

    return beam_k_glob


#PRE:
#POST:  creates the system stiffness matrix, all degrees of freedom are included
def build_k_sys(beam_nodes, beam_k_glob, node_supp):
    k_sys = np.zeros((2*len(node_supp),2*len(node_supp)))

    for beam in range(len(beam_nodes)):
        node_a = beam_nodes[beam][0]
        node_b = beam_nodes[beam][1]
        #building the 4 2x2 blocks in the matrix
        #beam_k_glob[beam] = [[aa, ab],
        #                     [ba, bb]]
        #block aa
        for i in range(0, 2):
            for j in range(0,2):
                k_sys[2*node_a+i][2*node_a+j] += beam_k_glob[beam][i][j]
        #block ab
        for i in range(0, 2):
            for j in range(0,2):
                k_sys[2*node_a+i][2*node_b+j] += beam_k_glob[beam][i][2+j]
        #block ba
        for i in range(0, 2):
            for j in range(0,2):
                k_sys[2*node_b+i][2*node_a+j] += beam_k_glob[beam][2+i][j]
        #block bb
        for i in range(0, 2):
            for j in range(0,2):
                k_sys[2*node_b+i][2*node_b+j] += beam_k_glob[beam][2+i][2+j]

    return k_sys



#PRE:
#POST:  returns a list of the degrees of freedoms which have no external support (not supported externally)
#       the number corresponds to the place in the system stiffness matrix (the number of the degree of freedom)
"""free degrees are all the degrees of freedom not held externally"""
def get_free_degs(node_supp):
    frees = np.array([], dtype=int)
    for i in range(len(node_supp)):
        for j in range(0,2):
            if node_supp[i][j] == 0:
                frees = np.append(frees, [int(2*i+j)], axis=0)
    print("free degrees")
    print(frees)
    return frees

#PRE:
#POST:  returns a list of the degrees of freedoms which have an external support (supported externally)
#       the number corresponds to the place in the system stiffness matrix (the number of the degree of freedom)
"""fixed degrees are all the degrees of freedom held externally"""
def get_fixed_degs(node_supp):
    fixed = np.array([], dtype = int)
    for i in range(len(node_supp)):
        for j in range(0,2):
            if node_supp[i][j] == 1:
                fixed = np.append(fixed, [int(2*i+j)], axis=0)
    print("fixed degrees")
    print(fixed)
    return fixed

#reduces the stiffness matrix k_sys to the part with only the terms
def get_k_ff(k_sys, node_supp, nodes, beam_nodes, beam_supp):

    frees = get_free_degs(node_supp)

    k_ff = np.zeros((len(frees), len(frees)))


    #iterate over all free degrees of freedom
    counter_i = 0
    counter_j = 0
    for i in frees:
        for j in frees:
            k_ff[counter_i][counter_j] = k_sys[i][j]
            counter_j +=1
        counter_j = 0
        counter_i += 1

    print("k_ff")
    print(k_ff)
    return k_ff

#PRE:
#POST:  returns a part of the system stiffness matrix
#       it is the matrix that calculates the forces at the externally fixed degrees of freedom
#       they only depend on the free degrees of freedom, as the others are
#       fixed (no deflection)
def get_k_sf(k_sys, node_supp, nodes, beam_nodes, beam_supp):
    frees = get_free_degs(node_supp)
    fixed = get_fixed_degs(node_supp)

    k_sf = np.zeros((len(fixed), len(frees)))

    counter_i = 0
    counter_j = 0
    for i in fixed:
        for j in frees:
            k_sf[counter_i][counter_j] = k_sys[i][j]
            counter_j +=1
        counter_j = 0
        counter_i += 1

    print("k_sf")
    print(k_sf)
    return k_sf


def get_f_ext_f(f_ext, node_supp, nodes, beam_nodes, beam_supp):
    frees = get_free_degs(node_supp)

    f_ext_f = np.zeros(len(frees))

    counter = 0
    for i in frees:
            f_ext_f[counter] = f_ext[i]
            counter += 1

    print("f_ext_f")
    print(f_ext_f)
    return f_ext_f


def solve_for_u_f(k_ff, f_ext_f):
    #mm/N * 1000 N = m
    return np.matmul(np.linalg.inv(k_ff), f_ext_f)


def get_u_glob(nodes, sol, node_supp):
    frees = get_free_degs(node_supp)
    node_disp = np.zeros(len(nodes)*2)

    count = 0
    for i in frees:
        node_disp[i] = sol[count]
        count += 1
    return node_disp

def inner_forces(nodes_new, beam_nodes, beam_prop):
    load = np.zeros(len(beam_nodes),dtype=float)
    for i in range(len(beam_nodes)):
        node_a = beam_nodes[i][0]
        node_b = beam_nodes[i][1]

        A = beam_prop[i][0]
        E = beam_prop[i][1]
        f_y = beam_prop[i][2]
        L = beam_prop[i][3]

        l_new = np.linalg.norm(nodes_new[node_b]-nodes_new[node_a])
        e = (l_new/L-1)

        #mm² * 1000 N/mm² = N
        force = A*E*e

        # N /(mm² * N/mm²)
        q = force/(A*f_y)

        load[i] = abs(q)

    return load


def compute_deformation(nodes, node_supp, f_ext, beam_nodes, beam_supp, beam_prop):
    beam_k_loc = create_local_stiffness_matrixes(beam_nodes, beam_supp, beam_prop)
    beam_k_glob = rotate_stiffness_matrices(beam_prop, beam_k_loc)
    k_sys = build_k_sys(beam_nodes, beam_k_glob, node_supp)
    print("k_sys")
    print(k_sys)

    k_ff = get_k_ff(k_sys, node_supp, nodes, beam_nodes, beam_supp)
    k_sf = get_k_sf(k_sys, node_supp, nodes, beam_nodes, beam_supp)
    f_ext_f = get_f_ext_f(f_ext, node_supp, nodes, beam_nodes, beam_supp)

    det = np.linalg.det(k_ff)
    print("determinant of k_ff")
    print(det)
    #the determinant should be non zero; the transformation should be reversable
    if abs(det) < 1e-10:
        print("structure cannot hold")
        return False
    else:
        sol = solve_for_u_f(k_ff, f_ext_f)
        print("solution")
        print(sol)
        reaction_forces = np.matmul(k_sf, sol)
        print("reaction forces")
        print(reaction_forces)

        #displacements of each node
        u_glob = get_u_glob(nodes, sol, node_supp)
        print("u_glob")
        print(u_glob)

        #deformed nodes
        nodes_new = np.zeros((len(nodes),2), dtype = float)
        for i in range(len(nodes)):
            for j in range(2):
                nodes_new[i][j] = nodes[i][j]+ u_glob[2*i+j]

        load = inner_forces(nodes_new, beam_nodes, beam_prop)
        return nodes_new, load
