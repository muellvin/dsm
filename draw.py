#imports
import matplotlib.pyplot as plt
import numpy as np

#adds all the nodes to the ax object as scatter points
def print_nodes(ax, nodes):
        ax.scatter(nodes[:,0], nodes[:,1],s=None, c='blue', marker='o')


#function that prints the gross cross section
def print_beams(ax, beam_nodes, nodes, load):
    colors = plt.cm.jet(np.linspace(0,1,30))
    index = 0
    for beam in beam_nodes:
        x = []
        y = []
        x.append(nodes[beam[0]][0])
        y.append(nodes[beam[0]][1])
        x.append(nodes[beam[1]][0])
        y.append(nodes[beam[1]][1])

        c = int(load[index]*30)
        ax.plot(x, y, color = colors[c])
        index += 1

def print_supp(ax, nodes, node_supp):
    for i in range(len(nodes)):
        x = nodes[i][0]
        y = nodes[i][1]
        if node_supp[i][0] == 1:
            ax.scatter(x, y, c='magenta', marker='>', s=250)
        if node_supp[i][1] == 1:
            ax.scatter(x, y, c='red', marker='^', s=250)


#function that prints the gross cross section
def print_force_ext(ax, nodes, f_ext):#number_of_nodes not necesary, as it is a third of the size of f_ext
    for i in range(len(nodes)):
        fx = f_ext[i*2]
        fy = f_ext[i*2 + 1]

        #if there is any force then act
        if ((fx != 0) or (fy !=0)):
            x = []
            y = []
            x.append(nodes[i][0])
            y.append(nodes[i][1])

            x.append(nodes[i][0]-0.2*fx)
            y.append(nodes[i][1]-0.2*fy)

            ax.plot(x, y, c='red')

def draw_structure(nodes, load, node_supp, beam_nodes, f_ext):
    print(load)
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    print_supp(ax, nodes, node_supp)
    print_nodes(ax,nodes)
    print_beams(ax, beam_nodes, nodes, load)
    print_force_ext(ax, nodes, f_ext)

    plt.axis('scaled')
    plt.show()
