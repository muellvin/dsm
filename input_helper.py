import numpy as np

def get_even_beam_prop(nodes, beam_nodes):
    beam_prop = np.zeros((len(beam_nodes), 5))
    for i in range(len(beam_prop)):
        node_a = nodes[beam_nodes[i][0]]
        node_b = nodes[beam_nodes[i][1]]
        print(node_a)
        print(node_b)
        if node_a[0] == node_b[0]:
            if node_a[1] < node_b[1]:
                angle = np.pi/2
            else:
                angle = -np.pi/2
        else:
            angle = np.arctan((node_b[1]-node_a[1])/(node_b[0]-node_a[0]))
        length = np.linalg.norm(node_b-node_a)
        #beam prop: A mm², E GPa 1'000 N/mm², f_y N/mm², L m, angle rad
        beam_prop[i] = [2000, 210, 250, length, angle]
    return beam_prop


    
