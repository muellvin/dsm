#imports
import matplotlib.pyplot as plt
import numpy as np

#function that prints the gross cross section
def print_beams(beam_nodes, nodes):
    for beam in beam_nodes:
        x = []
        y = []
        x.append(nodes[beam[0]][0])
        y.append(nodes[beam[0]][1])
        x.append(nodes[beam[1]][0])
        y.append(nodes[beam[1]][1])

        plt.plot(x, y, 'k')

    plt.axis('scaled')
    plt.show()


def print_support(node_supp, nodes):
    for i in range(len(nodes)):
        if node_supp[i][0]==1 and node_supp[i][1]==1 and node_supp[i][2]==1:
            print(nodes[i][0])
            plt.scatter(nodes[i][0], nodes[i][1],s=None, c='blue', marker='s')
        if node_supp[i][0]==1 and node_supp[i][1]==1 and node_supp[i][2]==0:
            print(nodes[i][0])
            plt.scatter(nodes[i][0], nodes[i][1],s=None, c='blue', marker='o')
