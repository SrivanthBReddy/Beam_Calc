
import numpy as np
import beamobjects
from beamquestions import finalbeam
from beamquestions import supports_list

"""
How does the stifness matrix work?
Each element in the stifness matrix is a representative of the reactions that occur to applied forces/moments
The process proceeds by having all the local stifness matrix's identified based on the meshes created
Lets say you have N nodes [1, .., N]. Your system size is going to be 2 x (N+1) w 2 DOFs (v, theta) per node
The elemnts in your calculation is going to be N-1 with 
"""

#Fixed support constrains both force and moment (0,0)
#A roller contrains only the force in the direction of the roller vertical movement (0, 1)
#A pin contrains force in both directions but allows rotation (0,1)

E = 200* 10**9 #PA
I = 1*10**-4 #m^4 
L = 7 #m
P = -1000 #N

E = finalbeam.beam.youngs_modulus # Youngs modulus of the beam in Pascals
I = finalbeam.Moment_of_Intertia # Moment of Inertia of the beam in m^4
L = finalbeam.length # Length of the beam in meters
S = finalbeam.supports # List of supports
P = finalbeam.point_loads # List of point loads
D = finalbeam.distributed_loads # List of distributed loads

x = [0, 3, 7] # Example of the node positions used for calculations
#Nodes will come from supports, point loads, and distributed loads. The nodes will be sorted in ascending order and duplicates will be removed.

#Iterate through each list of supports ands loads and add the distances associated with each load 2, 2, 3 - 4

#Initiate 2 lists, one for the x values and the other for the node type so when it comes to applying the boundary conditions, it is easier for the program to know


x = []
S_distance = []
for i in range(len(S)):
    x.append(S[i].distance) #ex: [0, 4, 1]
    S_distance.append(S[i].distance)
for i in range (len(P)):
    x.append(P[i].distance)

for i in range (len(D)):
    x.append(D[i].x_initial)
    x.append(D[i].x_final)

x = sorted(list(set(x))) #ex: [0, 1, 3, 4, 6]

#Now match the support distances to the actual list of x distances
constrained = []
for i in range(len(S)): #len 3
    ind = x.index(S_distance[i])
    if S[i].support_type == "fixed":
        constrained.extend([2*ind,2*ind+1]) #(v, theta)
    else:
        constrained.extend([2*ind])
        
free = []
for i in range(len(x)*2):
    if i in constrained:
        pass
    else:
        free.append(i)


#Once that is finished you have to identify which supports they are to identify their constrains (fixed: (0,0), Roller: (0,1), Pin: (0,1))




node_elements = len(x) - 1 # reads as 2
matrix_list = [None] * node_elements
for i in range(node_elements): # reads as 0, 1
    L = x[i+1] - x[i]
    matrix_list[i] = ((E*I)/L**3) * np.array([[12, 6*L, -12, 6*L], 
                                       [6*L, 4*L**2, -6*L, 2*L**2], 
                                       [-12, -6*L, 12, -6*L], 
                                      [6*L, 2*L**2, -6*L, 4*L**2]])

# construct global stiffness matrix

Global_matrix = np.zeros((2*(len(x)), 2*(len(x))))

for i in range(node_elements):
    Global_matrix[2*i:2*i+ 4, 2*i:2*i + 4] += matrix_list[i]
