import numpy as np



def expand(A) : 
    line , row = A.shape
    B = np.zeros((line+2 , row+2))
    B[1:line+1 , 1 : row+1] = A
    for j in range(line) : 
        B[j+1][0] = A[j][1]
        B[j+1][row+1] = A[j][2]
    B[0] = B[2]
    B[line+1] = B[line-1]
    B[0][0] = A[1][1]
    B[0][row+1] = A[1][row-2]
    B[line+1][0] = A[line-2][1]  
    B[line+1][row+1] = A[line-2][row-2]

    return B
def produit(A) :

    B = np.ones(A.shape) 
    return A*B

A = np.random.rand(4,4)

print(expand(A))

print('***********************')

print(produit(A))