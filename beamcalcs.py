
import numpy as np
import beamobjects
from beamquestions import finalbeam


E = 200* 10**9 #PA
I = 1*10**-4 #m^4 
L = 7 #m
P = -1000 #N

E = finalbeam.beam.youngs_modulus # Youngs modulus of the beam in Pascals
I = finalbeam.Moment_of_Intertia # Moment of Inertia of the beam in m^4
L = finalbeam.length # Length of the beam in meters
S = finalbeam.supports # List of supports
P = finalbeam.point_loads # List of point loads

stiffmatrix = ((E*I)/L**3) * np.array([[12, 6*L, -12, 6*L], 
                                       [6*L, 4*L**2, -6*L, 2*L**2], 
                                       [-12, -6*L, 12, -6*L], 
                                      [6*L, 2*L**2, -6*L, 4*L**2]])
stiffmatrix = stiffmatrix[2:4, 2:4]
solved = np.linalg.solve(stiffmatrix, np.array([[P],[0]]))
print(solved)