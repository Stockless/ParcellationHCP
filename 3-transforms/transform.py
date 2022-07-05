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
    print("Transforming subject "+sub+": T2 to Tal")
    subj_bundle = subjs_dir+"/"+sub+"/resampled/"
    output = subjs_dir+"/"+sub+"/transformed"
    sp.call(['./transform', subj_bundle, output+'/', 'T2_to_Tal_tr_tmp.trm']);
    print("Transforming subject "+sub+": Tal to MNI")
    output_mni = output+"_MNI/"
    print(output)
    print(output_mni)
    sp.call(['./transform', output+'/', output_mni, 'Tal_to_MNI.trm']);
    sp.call(['rm','-rf',output])
    