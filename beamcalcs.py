
import numpy as np
import beamobjects
from beamquestions import finalbeam


E = 200* 10**9 #PA
I = 1*10**-4 #m^4 
L = 7 #m
P = -1000 #N

E = finalbeam.beam.youngs_modulus
I = finalbeam.Moment_of_Intertia
L = finalbeam.length
S = finalbeam.supports
P = finalbeam.point_loads

stiffmatrix = ((E*I)/L**3) * np.array([[12, 6*L, -12, 6*L], 
                                       [6*L, 4*L**2, -6*L, 2*L**2], 
                                       [-12, -6*L, 12, -6*L], 
                                      [6*L, 2*L**2, -6*L, 4*L**2]])
stiffmatrix = stiffmatrix[2:4, 2:4]
solved = np.linalg.solve(stiffmatrix, np.array([[P],[0]]))
print(solved)