import numpy as np
import input_helper as ih

#run this script in the begining of the programm
#afterwards the arrays nodes, node_supp, node_disp, f_ext, beam_nodes, beam_supp, beam_prop
#will have been intiialisend and filled with values
#eighter by and hard coded example or by a user input


example_choice = int(input("Choose: 0 example, 1 randomly generated, 2 user input"))


#the first 4 are hard coded examples
if(example_choice==0):
    nodes = np.array([[0,0], [1,0], [2,0], [2,1]])
    node_supp = np.array([[1,1], [0,0], [0,1], [0,0]])

    # 1000 N
    f_ext = np.array([0,0, 0,0, 0,0, 300000,0])


    beam_nodes = np.array([[0,1], [1,2], [0,3], [1,3], [2,3]])
    beam_supp = np.ones((beam_nodes.shape[0],4))
    beam_prop = ih.get_even_beam_prop(nodes, beam_nodes)


if (example_choice==1):
    print("to be connected, just run generate_structure.py")

    #this is the user interface
elif(example_choice==2):

    #make a declaration of the later used things, it should all be overwritten and appended to
    nodes = np.array([[0,0]])
    node_supp = np.array([[0,0,0]])

    node_disp = np.array([0,0,0, 0,0,0])
    f_ext = np.array([0,0,0, 0,0,0])


    beam_nodes = np.array([[0,0]])
    beam_supp = np.array([[0, 0, 0, 0, 0, 0]])
    beam_prop = np.array([[1, 1, 1, 1,0]])


    number_of_nodes = int(input("how many nodes do you need?"))
    for i in range(number_of_nodes):
        print("node number: ", i)
        nodes = np.append(nodes, [[0,0]], axis=0)#this should be one too many
        print(nodes)
        nodes[i][0] = int(input("X Position"))
        nodes[i][1] = int(input("Y Position"))

        print("Please enter how this node is externally supported")
        node_supp = np.append(node_supp,[[1,1,1]], axis=0)
        node_supp[i][0] = bool(input("X direction fixed? 0 if not"))
        node_supp[i][1] = bool(input("Y direction fixed? 0 if not"))
        node_supp[i][2] = bool(input("torque fixed? 0 if not"))

    node_disp = np.zeros(number_of_nodes)#this will be later used, and filled by the computer

    number_of_forces = int(input("how many forces do you really need?"))
    for i in range(number_of_nodes):#create an empty force array
        f_ext =np.append(f_ext, [0,0,0], axis=0)#the unused third 0 is the moment

    for i in range(number_of_forces):
        print("force numer :", i)
        force_node_number = int(input("on wich node does the force act?"))
        force_x_direction = float(input("X direction, put 0 if not"))
        force_y_direction = float(input("Y direction"))


        f_ext[force_node_number*3 ]= force_x_direction
        f_ext[force_node_number*3 +1]= force_y_direction#this should be the correct position in the long array

    number_of_beams = int(input("how many beams are there? Count twise, programme once!"))
    for i in range(number_of_beams):
        print("beam number: ", i)
        begin_of_beam = int(input("number of begining node"))
        end_of_beam = int(input("number of end node"))

        beam_supp_1_X = bool(input("support of begining node in X direction"))
        beam_supp_1_Y = bool(input("support of begining node in Y direction"))
        beam_supp_1_T = bool(input("support of begining node in Torsion direction"))
        beam_supp_2_X = bool(input("support of end node in X direction"))
        beam_supp_2_Y = bool(input("support of end node in Y direction"))
        beam_supp_2_T = bool(input("support of end node in Torsion direction"))


        beam_nodes = np.append(beam_nodes, [[0,0]], axis=0)
        beam_nodes[i][0] = begin_of_beam
        beam_nodes[i][1] = end_of_beam

        beam_supp = np.append(beam_supp, [[0,0,0,0,0,0]], axis=0)
        beam_supp[i][0]= beam_supp_1_X
        beam_supp[i][1]= beam_supp_1_Y
        beam_supp[i][2]= beam_supp_1_T
        beam_supp[i][3]= beam_supp_2_X
        beam_supp[i][4]= beam_supp_2_Y
        beam_supp[i][5]= beam_supp_2_T

        #let's give this monster a try
        beam_angle_Diff_X = nodes[beam_nodes[i][1]][0]-nodes[beam_nodes[i][0]][0]
        beam_angle_Diff_Y = nodes[beam_nodes[i][1]][1]-nodes[beam_nodes[i][0]][1]
        beam_angle = np.arctan(beam_angle_Diff_Y/ beam_angle_Diff_X)

        np.append(beam_prop, [[1,1,1,1,0]])
        beam_prop[i]=[1,1,1,1, beam_angle]


else:
    print("Wronge choice, go home")
