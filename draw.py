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



#function that prints the gross cross section
def print_force_ext(f_ext, number_of_nodes, nodes):#number_of_nodes not necesary, as it is a third of the size of f_ext
    for i in range(number_of_nodes):
        #if there is any force then act
        if ((f_ext[i*3] != 0) or (f_ext[i*3 + 1] != 0)):

            x = []
            y = []
            #this is the node on wich the force acts
            x.append(nodes[i][0])
            y.append(nodes[i][1])

            #this is the force
            x.append(f_ext[i*3 ])
            y.append(f_ext[i*3 +1])

            #maybe add an other color?
            plt.plot(x, y, 'k')

def print_nodes(nodes):
    for i in range(len(nodes)):
            plt.scatter(nodes[i][0], nodes[i][1],s=None, c='blue', marker='s')
            plt.scatter(nodes[i][0], nodes[i][1],s=None, c='blue', marker='o')


def print_support_nodes(node_supp, nodes):
    for i in range(len(nodes)):
        if node_supp[i][0]==1 and node_supp[i][1]==1 and node_supp[i][2]==1:
            print(nodes[i][0])
            plt.scatter(nodes[i][0], nodes[i][1],s=None, c='blue', marker='s')
        if node_supp[i][0]==1 and node_supp[i][1]==1 and node_supp[i][2]==0:
            print(nodes[i][0])
            plt.scatter(nodes[i][0], nodes[i][1],s=None, c='blue', marker='o')

def print_support_beams(beam_supp, beam_nodes, number_of_beams, nodes):
    #cycle throuth all beams
    for i in range(number_of_beams):
#begining node
        #completly fixed
        if beam_supp[i][0]==1 and node_supp[i][1]==1 and node_supp[i][2]==1:
            #print(nodes[i][0])#this looks like a debug thing
            plt.scattern(nodes[beam_nodes[i][0]][0], nodes[beam_nodes[i][1]][1],s=None, c='blue', marker='s')
        #torsion allowed
        if beam_supp[i][0]==1 and beam_supp[i][1]==1 and beam_supp[i][2]==0:
            print(nodes[i][0])
            plt.scatter(nodes[beam_nodes[i][0]][0], nodes[beam_nodes[i][1]][1],s=None, c='blue', marker='o')
        #free
        if beam_supp[i][0]==0 and beam_supp[i][1]==0 and beam_supp[i][2]==0:
            print(nodes[i][0])
            plt.scatter(nodes[beam_nodes[i][0]][0], nodes[beam_nodes[i][1]][1],s=None, c='blue', marker='o')#use a different marker for free node
#endinging node
        #completly fixed
        if beam_supp[i][3]==1 and node_supp[i][4]==1 and node_supp[i][5]==1:
            #print(nodes[i][0])#this looks like a debug thing
            plt.scattern(nodes[beam_nodes[i][0]][0], nodes[beam_nodes[i][1]][1],s=None, c='blue', marker='s')
        #torsion allowed
        if beam_supp[i][3]==1 and beam_supp[i][4]==1 and beam_supp[i][5]==0:
            print(nodes[i][0])
            plt.scatter(nodes[beam_nodes[i][0]][0], nodes[beam_nodes[i][1]][1],s=None, c='blue', marker='o')
        #free
        if beam_supp[i][3]==0 and beam_supp[i][4]==0 and beam_supp[i][5]==0:
            print(nodes[i][0])
            plt.scatter(nodes[beam_nodes[i][0]][0], nodes[beam_nodes[i][1]][1],s=None, c='blue', marker='o')#use a different marker for free node
