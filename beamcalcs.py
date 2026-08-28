
import numpy as np
import beamobjects
import math
from beamquestions import finalbeam

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
 
def solve_beam(finalbeam):


    E = finalbeam.beam.youngs_modulus # Youngs modulus of the beam in Pascals
    I = finalbeam.Moment_of_Intertia # Moment of Inertia of the beam in m^4
    L = finalbeam.length # Length of the beam in meters
    S = finalbeam.supports # List of supports
    P = finalbeam.point_loads # List of point loads
    D = finalbeam.distributed_loads # List of distributed loads
    EF = finalbeam.extreme_fiber

    #Nodes will come from supports, point loads, and distributed loads. The nodes will be sorted in ascending order and duplicates will be removed.

    #Iterate through each list of supports ands loads and add the distances associated with each load 2, 2, 3 - 4

    #Initiate 2 lists, one for the x values and the other for the node type so when it comes to applying the boundary conditions, it is easier for the program to know


    x = []
    S_distance = []
    P_distance = []
    D_distance = []
    P_Force = []
    D_Force = []
    for i in range(len(S)):
        x.append(S[i].distance) #ex: [0, 4, 1]
        S_distance.append(S[i].distance)

    for i in range (len(P)):
        x.append(P[i].distance)
        P_distance.append(P[i].distance)
        P_Force.append(P[i].force)

    for i in range (len(D)):
        x.append(D[i].x_initial)
        x.append(D[i].x_final)
        D_distance.append([D[i].x_initial, D[i].x_final])
        D_Force.append(D[i].load_value)

    x = sorted(list(set(x))) #ex: [0, 1, 3, 4, 6]

    #Now match the support distances to the actual list of x distances
    constrained = []
    for i in range(len(S)): #len 3
        ind = x.index(S_distance[i])
        if S[i].support_type == "FIXED":
            constrained.extend([2*ind,2*ind+1]) #(v, theta)
        else:
            constrained.append(2*ind)

    free = []
    for i in range(len(x)*2):
        if i in constrained:
            pass
        else:
            free.append(i)

    #Construct the force vector

    globalvector = [0] * (2*len(x))
    for i in range(len(P)): #len 3
        ind = x.index(P_distance[i])
        globalvector[2*ind] = P_Force[i]

    for j in range(len(D)): #must be even number
        sub_list = [pos for pos in x if D_distance[j][0] <= pos <= D_distance[j][1]]
        w = D_Force[j]
        if len(sub_list) > 2 and D[j].load_type in ["triangular bottom to top", "triangular top to bottom"]:
            raise ValueError("If you are using triangular loads, it must span equal to or less than 2 elements")
        else:
            for i in range(len(sub_list)-1):
                ind = [x.index(sub_list[i]), x.index(sub_list[i+1])]
                L = sub_list[i+1] - sub_list[i]
                if D[j].load_type == "rectangular":
                    globalvector[2*ind[0]] += w*(L/2)
                    globalvector[2*ind[0] + 1] += w*(L**2/12)
                    globalvector[2*ind[1]] += w*(L/2)
                    globalvector[2*ind[1] + 1] -= w*(L**2/12)
                elif D[j].load_type == "triangular bottom to top":
                    theta = math.atan(w/(D_distance[j][1] - D_distance[j][0] ))
                    w_new = (sub_list[i+1] - sub_list[0]) * math.tan(theta)
                    globalvector[2*ind[0]] += (3*w_new*L) / 20
                    globalvector[2*ind[0] + 1] += (w_new*L**2) / 30
                    globalvector[2*ind[1]] += (7*w_new*L) / 20
                    globalvector[2*ind[1] + 1] -= (w_new*L**2) / 20
                elif D[j].load_type == "triangular top to bottom":
                    theta = math.atan(w/(D_distance[j][1] - D_distance[j][0] ))
                    w_new = L * math.tan(theta)
                    globalvector[2*ind[0]] += (7*w_new*L) / 20
                    globalvector[2*ind[0] + 1] += (w_new*L**2) / 20
                    globalvector[2*ind[1]] += (3*w_new*L) / 20
                    globalvector[2*ind[1] + 1] -= (w_new*L**2) / 30



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
    
    cut = np.ix_(free, free)
    Cut_Matrix = Global_matrix[cut]

    globalvector = np.array(globalvector)
    Cut_Vector = globalvector[free]

    solved = np.linalg.solve(Cut_Matrix, Cut_Vector)

    full_displacement = [0] * (len(x)*2)
    for i in range(len(free)):
        full_displacement[free[i]] = solved[i]

    reaction_and_forces = Global_matrix @ full_displacement



    def hermite(s, L, v1, theta1, v2, theta2 ):
        ξ = s/L
        N1 = 1 - 3*(ξ**2) + 2*(ξ**3)
        N2 = L*(ξ - 2*ξ**2 + ξ**3)
        N3 = 3*ξ**2 - 2*ξ**3
        N4 = L*(-(ξ**2) + ξ**3)

        v = N1*v1 + N2*theta1 + N3*v2 + N4*theta2
        return v

    def hermiteM(s, L, v1, theta1, v2, theta2 ):
        ξ = s/L
        N1 = -6 + 12*(ξ)
        N2 = L*(- 4 + 6*ξ)
        N3 = 6 - 12*ξ
        N4 = L*(-2 + 6*ξ)
        Mom = (E*I)/(L**2)* (N1*v1 + N2*theta1 + N3*v2 + N4*theta2)
        return Mom
    def hermiteV(L, v1, theta1, v2, theta2):
        N1 = 12
        N2 = L*6
        N3 = -12
        N4 = L*6
        Shear = (E*I)/(L**3)* (N1*v1 + N2*theta1 + N3*v2 + N4*theta2)
        return Shear

    x_vals = []
    v_points = []
    m_vals = []
    shear_vals = []
    for i in range(len(x)-1):
        L = x[i+1]-x[i]
        Shear = hermiteV(L, full_displacement[2*i], full_displacement[2*i+1], full_displacement[2*i+2], full_displacement[2*i+3])
        for j in range(0,L*2+1):
            s = j/2
            v = hermite(s, L, full_displacement[2*i], full_displacement[2*i+1], full_displacement[2*i+2], full_displacement[2*i+3])
            Mom = hermiteM(s, L, full_displacement[2*i], full_displacement[2*i+1], full_displacement[2*i+2], full_displacement[2*i+3])
            x_vals.append(x[i]+s)
            v_points.append(v)
            m_vals.append(Mom)
            shear_vals.append(Shear)

    m_vals = np.array(m_vals)
    stress = (m_vals * EF)/ I
    strain = stress / E

    #Max Displacement
    MaxDisplace = np.max(np.abs(v_points))
    MaxDisplacePosition = x_vals[np.argmax(np.abs(v_points))]

    #Max Moment
    MaxMoment = np.max(np.abs(m_vals))
    MaxMomentPosition = x_vals[np.argmax(np.abs(m_vals))]

    #Max Stress
    MaxStress = np.max(np.abs(stress))
    MaxStressPosition = x_vals[np.argmax(np.abs(stress))]

    #Max Strain
    MaxStrain = np.max(np.abs(strain))
    MaxStrainPosition = x_vals[np.argmax(np.abs(strain))]

    finalfinalbeam = beamobjects.BeamFinalValues(Md = MaxDisplace, Mdp = MaxDisplacePosition, Mm = MaxMoment, Mmp = MaxMomentPosition, Mstress = MaxStress, Mstressp = MaxStressPosition, Mstrain = MaxStrain, Mstrainp = MaxStrainPosition, x_vals = x_vals, v_points = v_points, m_vals = m_vals, stress = stress, strain = strain, shear = shear_vals, reactforces = reaction_and_forces, fulldisplacement= full_displacement, globalmatrix = Global_matrix )
    return finalfinalbeam

finalfinalbeam = solve_beam(finalbeam)