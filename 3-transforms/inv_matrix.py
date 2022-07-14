import numpy as np
import sys

def readtrm(tr):
    """
    in: trmfile
    out: np.array
    """
    ar=open(tr,'r')
    t=[i.split(' ') for i in ar.read()[0:-1].split('\n')]
    ar.close()
    t=np.array(t).astype('float32')
 
    return t

matrix = readtrm(sys.argv[1])
matrix = np.matrix(matrix).I

print(matrix)