import subprocess as sp
import sys
import os

subjs_dir = sys.argv[1]
subs = len(os.listdir(subjs_dir))
sub = '001'
for i in range(1,subs+1):
    if i < 10:
        sub = '00' + str(i)
    else:
        sub = '0' + str(i)
    print("Aligning subject "+sub)
    sub_dir = subjs_dir+"/"+sub+"/segmented_T1/"
    aligned_out = subjs_dir+"/"+sub+"/aligned_T1"
    sp.call(['python', 'align_bundles.py', sub_dir, aligned_out])
    # sp.call(['rm','-rf',sub_dir])