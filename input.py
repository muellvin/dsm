import numpy as np

example_choise = int(input("Woud you like to use a standart example?: 0-2 are basic, 3-4 are usefull, 5 is free user input"))
if(example_choise==0):
    print("This is the basic example, one beam fixed on both ends")
    nodes = np.array([[0,0], [1,0]])
    node_supp = np.array([[1,1,1],[1,1,1]])

    node_disp = np.array([0,0,0, 0,0,0])
    f_ext = np.array([0,0,0, 0,-1,0])


    beam_nodes = np.array([[0,1]])
    beam_supp = np.array([[1, 1, 1, 1, 1, 1]])
    beam_prop = np.array([[1, 1, 1, 1,0]])

elif(example_choise==1):
    print("This basic example is fixed on the first side and free on the second")
    nodes = np.array([[0,0], [1,0]])
    node_supp = np.array([[1,1,1],[1,1,0]])

    node_disp = np.array([0,0,0, 0,0,0])
    f_ext = np.array([0,0,0, 0,-1,0])


    beam_nodes = np.array([[0,1]])
    beam_supp = np.array([[1, 1, 1, 1, 1, 0]])
    beam_prop = np.array([[1, 1, 1, 1,0]])

elif(example_choise==2):
    print("This basic example is fixed on the second side and free on the first")
    nodes = np.array([[0,0], [1,0]])
    node_supp = np.array([[1,1,0],[1,1,1]])

    node_disp = np.array([0,0,0, 0,0,0])
    f_ext = np.array([0,0,0, 0,-1,0])


    beam_nodes = np.array([[0,1]])
    beam_supp = np.array([[1, 1, 0, 1, 1, 1]])
    beam_prop = np.array([[1, 1, 1, 1,0]])

elif(example_choise==3):
    print("This examle consists of tow beams, both are fixed on one side and are connected by a swillinging thingy")
    nodes = np.array([[0,0], [1,0], [2,0]])
    node_supp = np.array([[1,1,1],[0,0,0],[1,1,1]])

    node_disp = np.array([0,0,0, 0,0,0, 0,0,0])
    f_ext = np.array([0,0,0, 0,-1,0, 0,0,0])


    beam_nodes = np.array([[0,1],[1,2]])
    beam_supp = np.array([[1, 1, 1, 1, 1, 0],[1, 1, 0, 1, 1, 1]])
    beam_prop = np.array([[1, 1, 1, 1,0],[1, 1, 1, 1,0]])

elif(example_choise==4):
    print("This is one node suspended by 4 fixed beams")
    nodes = np.array([[0,0], [1,0], [-1,0],[0,1],[0,-1]])
    node_supp = np.array([[0,0,0],[1,1,1],[1,1,1],[1,1,1],[1,1,1]])

    node_disp = np.array([0,0,0, 0,0,0, 0,0,0, 0,0,0, 0,0,0])
    f_ext = np.array([0,0,1, 0,0,0, 0,0,0, 0,0,0, 0,0,0])


    beam_nodes = np.array([[0,1],[0,2],[0,3],[0,4]])
    beam_supp = np.array([[1, 1, 0, 1, 1, 1],[1, 1, 0, 1, 1, 1],[1, 1, 0, 1, 1, 1],[1, 1, 0, 1, 1, 1]])
    beam_prop = np.array([[1, 1, 1, 1,0],[1, 1, 1, 1,0],[1, 1, 1, 1, np.pi()*-0.5],[1, 1, 1, 1, np.pi()*-0.5]])

elif(example_choise==5):
    number_of_nodes = int(input("how many nodes do you need?"))
    for i in range(number_of_nodes):
        print("node number: ", i)
        nodes[i][0] = int(input("X Position"))
        nodes[i][1] = int(input("Y Position"))

        node_supp[i][0] = bool(input("X direction fixed? 0 if not"))
        node_supp[i][1] = bool(input("Y direction fixed? 0 if not"))
        node_supp[i][2] = bool(input("torque fixed? 0 if not"))

    node_disp = np.zeros(number_of_nodes)

    number_of_forces = int(input("how many forces do you realy need?")
    for i in range(number_of_forces):
        print("force numer :", i)
        force_node_number = int(input("on wich node does the force act?"))
        force_x_direction = float(input("X direction, put 0 if not"))
        force_y_direction = float(input("Y direction"))

        f_ext[force_node_number*3]= force_x_direction
        f_ext[force_node_number*3 + 1]= force_y_direction
                           
    
else:
    print("Wronge choice, go home")
