import numpy as np
import os
import sys
import math
import statistics
#import matplotlib.pyplot as plt
#import visualizationTools as vt
#import visual_tools as vs
from dipy.segment.metric import EuclideanMetric
from dipy.segment.metric import mdf
from dipy.segment.metric import dist
from subprocess import call

#Import bundleTools from parent directory
sys.path.append('../bundleTools')
import bundleTools as BT
import bundleTools3 as BT3

subjects_path = sys.argv[1]
subjects_list = os.listdir(subjects_path);

for subject in subjects_list:
    print(subject)
    if(subject != 'meshes_obj'):
        #Juntar 3 tractografias en un solo archivo .bundles
        all_points=[]
        fiber_bun_1_3 = subjects_path+subject+'/OverSampledFibers/tractography-streamline-regularized-deterministic_1_3.bundles'
        fiber_points_1_3 = BT.read_bundle(fiber_bun_1_3)
        for fiber in fiber_points_1_3:
            all_points.append(fiber)

        fiber_bun_2_3 = subjects_path+subject+'/OverSampledFibers/tractography-streamline-regularized-deterministic_2_3.bundles'
        fiber_points_2_3 = BT.read_bundle(fiber_bun_2_3)
        for fiber in fiber_points_2_3:
            all_points.append(fiber)

        fiber_bun_3_3 = subjects_path+subject+'/OverSampledFibers/tractography-streamline-regularized-deterministic_3_3.bundles'
        fiber_points_3_3 = BT.read_bundle(fiber_bun_3_3)
        for fiber in fiber_points_3_3:
            all_points.append(fiber)

        BT3.write_bundle(subjects_path+subject+'/tractography-streamline-regularized-deterministic_'+subject+'.bundles', all_points)
