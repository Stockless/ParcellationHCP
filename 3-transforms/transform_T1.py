import subprocess as sp
import sys
import os

subjs_dir = sys.argv[1]
subs = len(os.listdir(subjs_dir))
sub = '001'
sp.call(['g++', '-std=c++14', '-O3', 'transform.cpp', '-o', 'transform', '-fopenmp', '-ffast-math'])
for i in range(1,subs+1):
    if i < 10:
        sub = '00' + str(i)
    else:
        sub = '0' + str(i)
    print("Transforming subject "+sub+": Tal to T1")
    subj_bundle = subjs_dir+"/"+sub+"/segmented_Tal/"
    output = subjs_dir+"/"+sub+"/segmented_T1"
    trm_matrix = subjs_dir+"/"+sub+"/TransformMatrices/Tal_to_T1.trm"
    sp.call(['./transform', subj_bundle, output+'/', trm_matrix]);