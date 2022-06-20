import bundleTools as BT
import os
import sys
import visual_tools as vt
from collections import defaultdict
import vtk

#For loading more than one bundle
def load_bundles(path):
    dir = os.listdir(path);
    bundles = []
    for bundle in dir:
        if bundle.endswith('.bundles'):
            bundles.append(BT.read_bundle("bundles/"+bundle))
    return bundles

#Loads the mesh
Lhemi_path = 'lh.obj' ;
Lvertex, Lpolygons = BT.read_mesh_obj(Lhemi_path)
Lhemi = vt.Polygon(Lvertex, Lpolygons);
Lhemi.setOpacity(0.6)

# bundles = load_bundles('bundles/')

bun = BT.read_bundle("bundles/aligned_lh_CG.bundles") #loads one bundle
vt.visual_allpoints(bun,Lhemi)
