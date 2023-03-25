import numpy as np

#PRE:   listed arguments
#POST:  creates a stiffness matrix for each beam and returns them in an array
def create_local_stiffness_matrixes(beam_nodes, beam_supp, beam_prop):
    beam_k_loc = np.zeros((len(beam_nodes), 4, 4), dtype=float)

    for i in range(len(beam_nodes)):
        A = beam_prop[i][0]
        E = beam_prop[i][1]
        I = beam_prop[i][2]
        L = beam_prop[i][3]
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
        R = np.array([[np.cos(phi), -np.sin(phi), 0, 0], \
                      [np.sin(phi), np.cos(phi), 0, 0], \
                      [0, 0, np.cos(phi), -np.sin(phi)], \
                      [0, 0, np.sin(phi), np.cos(phi)]])
        beam_k_glob[i] = np.matmul(np.transpose(R), np.matmul(beam_k_loc[i], R))

    return beam_k_glob


#PRE:
#POST:  creates the system stiffness matrix, all degrees of freedom are included
#       it is two dimensional, symmetrical
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
#POST:  returns a list of the degrees of freedoms which have no stiffness from any beam (not supported internally)
#       the number corresponds to the place in the system stiffness matrix (the number of the degree of freedom)
"""in case of a truss structure (only hinges) the only possibility for this to happen is, if a node is only connected through one beam"""
def get_zero_degs(nodes, beam_nodes, beam_supp):
    non_zeros = np.array([],dtype=int)
    zeros = np.array([],dtype=int)
    node_number = 0
    #iterate over all node numbers
    for i in range(len(nodes)):
        #iterate over all degrees of freedom of this node
        for deg in range(0,2):
            zero = True
            beam_number = 0
            #iterate over all beams, check whether it is connected to that node
            #and whether this degree of freedom is connected
            for beam in beam_nodes:
                if beam[0] == i:
                    if beam_supp[beam_number][deg] == 1:
                        zero = False
                if beam[1] == i:
                    if beam_supp[beam_number][2+deg] == 1:
                        zero = False
                beam_number+=1
            #if at leas one beam is connected to this degree of freedom then it is non zero
            if zero == False:
                non_zeros = np.append(non_zeros, [int(2*node_number+deg)], axis=0)
        node_number += 1
    #iterate over all 2*nodes degrees of freedom, if it is a zero meaning if it is not
    #in non_zeros then we add it the the list
    for i in range(2*len(nodes)):
        zero = True
        for j in non_zeros:
            if i == j:
                zero = False
        if zero:
            zeros = np.append(zeros, [i], axis=0)

    return zeros


#PRE:
#POST:  returns a list of the degrees of freedoms which have no external support (not supported externally)
#       the number corresponds to the place in the system stiffness matrix (the number of the degree of freedom)
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
    zeros = get_zero_degs(nodes, beam_nodes, beam_supp)

    size = 0
    for i in frees:
        non_zero_free = True
        for j in zeros:
            if i == j:
                non_zero_free = False
        if non_zero_free == True:
            size+= 1
    k_ff = np.zeros((size, size))

    #iterate over all free degrees of freedom
    counter_d = 0
    for d in frees:
        #check whether d is a zero degree of freedom
        d_zero = False
        for i in zeros:
            if d == i:
                d_zero = True
        #if it is also a non zero
        if d_zero == False:
            counter_o = 0
            for o in frees:
                o_zero = False
                for i in zeros:
                    if o == i:
                        o_zero = True
                if o_zero == False:
                    k_ff[counter_d][counter_o] = k_sys[d][o]
                    counter_o +=1
            counter_d += 1

    print("k_ff")
    print(k_ff)
    return k_ff

#PRE:
#POST:  returns a part of the system stiffness matrix
#       it is the matrix that calculates the forces at the externally fixed degrees of freedom
#       they only depend on the free and non zero degrees of freedom, as the others are
#       fixed (no deflection) of zero stiffness (no reaction)
def get_k_sf(k_sys, node_supp, nodes, beam_nodes, beam_supp):
    frees = get_free_degs(node_supp)
    zeros = get_zero_degs(nodes, beam_nodes, beam_supp)

    size = 0
    for i in frees:
        non_zero_free = True
        for j in zeros:
            if i == j:
                non_zero_free = False
        if non_zero_free == True:
            size+= 1

    fixed = get_fixed_degs(node_supp)

    k_sf = np.zeros((len(fixed), size))

    counter_d = 0
    for d in fixed:
        counter_o = 0
        for o in frees:
            #check whether o is a zero degree of freedom
            o_zero = False
            for i in zeros:
                if o == i:
                    o_zero = True
            #if it is also a non zero
            if o_zero == False:
                k_sf[counter_d][counter_o] = k_sys[d][o]
                counter_o +=1
        counter_d += 1

    print("k_sf")
    print(k_sf)
    return k_sf

def get_f_ext_f(f_ext, node_supp, nodes, beam_nodes, beam_supp):
    frees = get_free_degs(node_supp)
    zeros = get_zero_degs(nodes, beam_nodes, beam_supp)
    size = 0
    for i in frees:
        non_zero_free = True
        for j in zeros:
            if i == j:
                non_zero_free = False
        if non_zero_free == True:
            size+= 1
    f_ext_f = np.zeros((size))

    counter = 0
    for i in frees:
        #check whether o is a zero degree of freedom
        i_zero = False
        for j in zeros:
            if i == j:
                i_zero = True
        #if it is also a non zero
        if i_zero == False:
            f_ext_f[counter] = f_ext[i]
            counter += 1

    print("f_ext_f")
    print(f_ext_f)
    return f_ext_f

def solve_for_u_f(k_ff, f_ext_f):
    return np.matmul(np.linalg.inv(k_ff), f_ext_f)
