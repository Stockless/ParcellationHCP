import os
import sys
import numpy as np

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
 
def writetrm(m,tr):
    """
    in: np.array
    out: trmfile
    """
    ar=open(tr,'w')
    t=''
    for i in range(4):
        t=t+str(m[i][0])+' '+str(m[i][1])+' '+str(m[i][2])+'\n'
    ar.write(t);ar.close()
    return


def inv_trm(trmfile,trmfileout):
    """
    in: trmfilein
    out: trmfileout
    """
    m=readtrm(trmfile)

    m3=np.zeros((4,4))
    m3[-1,-1]=1
    m3[0:3,0:3]=np.linalg.inv(m[1::,:])
    m3[0:3,3]=  - np.dot(np.linalg.inv(m[1::,:]),  m[0].T)
    
    m4=np.zeros((4,3))
    m4[1::,:]=m3[0:3,0:3]
    m4[0]=m3[0:3,3]
    
    writetrm(m4,trmfileout)


subs_path = sys.argv[1]
trm_matrix = sys.argv[2]
out_trm_name = sys.argv[3]
for sub in os.listdir(subs_path):
    input_matrix = subs_path + sub + '/TransformMatrices/'+trm_matrix
    output_matrix = subs_path + sub + '/TransformMatrices/'+out_trm_name
    inv_trm(input_matrix,output_matrix)
