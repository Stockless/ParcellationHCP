import bundleTools as BT
import bundleTools3 as BT3
import numpy as np
import os
import sys
import math
import statistics
import visual_tools as vt
#import visual_tools as vs
from subprocess import call
from os import path
from collections import defaultdict
import vtk

Lhemi_path = 'lh.obj' ;
Lvertex, Lpolygons = BT.read_mesh_obj(Lhemi_path)
Lhemi = vt.Polygon(Lvertex, Lpolygons);
Lhemi.setOpacity(0.6)
# render = vt.Render();
# render.AddActor(Lhemi);

dir = os.listdir('bundles/');
bundles = []
for bundle in dir:
    if bundle.endswith('.bundles'):
        bundles.append(BT.read_bundle("bundles/"+bundle))

bun = BT.read_bundle("bundles/aligned_lh_CG.bundles")
fibra1 = bun[0]
vt.visual_allpoints(bun,Lhemi)

# vt.visual_allpoints([bun])