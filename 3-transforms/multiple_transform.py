import subprocess as sp
import sys
import os

subjs_dir = sys.argv[1]
input_matrix = sys.argv[2] # e.g: T2_to_Tal_trm.trm
subs = 5#len(os.listdir(subjs_dir))
sub = '001'
sp.call(['g++', '-std=c++14', '-O3', 'transform.cpp', '-o', 'transform', '-fopenmp', '-ffast-math'])
for i in range(1,subs+1):
    if i < 10:
        sub = '00' + str(i)
    else:
        sub = '0' + str(i)
    print("Transforming subject "+sub+": T2 to Tal")
    subj_bundle = subjs_dir+"/"+sub+"/resampled/"
    output = subjs_dir+"/"+sub+"/transformed_Tal"
    trm_matrix = subjs_dir+"/"+sub+"/TransformMatrices/"+input_matrix
    sp.call(['./transform', subj_bundle, output+'/', trm_matrix]);
    