# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 21:14:23 2021

@author: Cristobal
"""

#VER SOLO UN FASCÍCULO: CC

import bundleTools as BT
import bundleTools3 as BT3
import numpy as np
import os
import sys
import math
import statistics
import visualizationTools as vt
#import visual_tools as vs
from dipy.segment.metric import EuclideanMetric
from dipy.segment.metric import mdf
from dipy.segment.metric import dist
from subprocess import call
from os import path
from collections import defaultdict
import vtk
from dipy.segment.metric import CosineMetric


def read_intersection( infile ):

    f = open(infile, 'r');

    total_triangles = np.uint32(f.readline());
    InTri = list(map(np.uint32,f.readline().split()));
    print(total_triangles,len(InTri))
    FnTri = list(map(np.uint32,f.readline().split()));

    InPoints = list(map(np.float32,f.readline().split()))
    FnPoints = list(map(np.float32,f.readline().split()))

    fib_index = list(map(np.uint32,f.readline().split()))

    f.close();
    return InTri, FnTri, InPoints, FnPoints, fib_index;


def triangles_per_fascicle(hemi_dict, sp_dict):
    #Para cada triángulo...
    for tri in hemi_dict.keys():
        for k, v in hemi_dict[tri].items():

            #Si es el contador general del triángulo, no hacer nada.
            if k == 'n':
                continue

            #Si es el contador de una subparcela, agregarlo al diccionario de subparcelas
            else:
                sp_dict[k][tri] = v


#Lhemi_path =r'\\wsl$\Ubuntu-18.04\home\joaquin\joaquin\pmt_mt\pruebas\prueba_079\Archi\079\079\079\lh.obj'.replace('\\','/') ;
Lhemi_path = 'rh.obj' ;
Lvertex, Lpolygons = BT.read_mesh_obj(Lhemi_path)
Lhemi = vt.Polygon(Lvertex, Lpolygons);
Lhemi.setOpacity(1.0)
render = vt.Render();
render.AddActor(Lhemi);

Lneighbors = BT.mesh_neighbors(Lpolygons)
#Rneighbors = bt.mesh_neighbors(Rpolygons)
#Left_bundles_intersec = os.listdir(r'\\wsl$\Ubuntu-18.04\home\joaquin\joaquin\pmt_mt\pruebas\prueba_079\Archi\079\079\Mesh_Intersection\Left'.replace('\\','/'));
Left_bundles_intersec = os.listdir('intersection');

Atlas_L_fasc_dict = defaultdict(lambda: defaultdict(float))
Atlas_Lhemi_dict = defaultdict(lambda: defaultdict(int))

#Left_bundles_intersec = [Left_bundles_intersec[3]]  #9 Ver solo uno
for bundle in Left_bundles_intersec:
    #print(bundle)
    #ix_path_lh = r'\\wsl$\Ubuntu-18.04\home\joaquin\joaquin\pmt_mt\pruebas\prueba_079\Archi\079\079\Mesh_Intersection\Left'+'/'+bundle
    #ix_path_lh = ix_path_lh.replace('\\','/')

    ix_path_lh = 'intersection'+'/'+bundle
    ix_path_lh = ix_path_lh.replace('\\','/')
    #ix_path_rh = r'\\wsl$\Ubuntu-18.04\home\cris\Memoria2021\Archi\002\002\Mesh_Intersection\Right\align_cluster_subject_to_rh_PoC-PrC_0.intersectiondata'.replace('\\','/')
    #print(ix_path_lh)
    #fibers = r'\\wsl$\Ubuntu-18.04\home\joaquin\joaquin\pmt_mt\pruebas\prueba_079\Archi\079\079\Fasciculos_T1\LEFT' + '/'+bundle[:len(bundle)-16]+'bundles'
    #fibers = fibers.replace('\\','/')
    print(bundle)
    #fibers_lh = BT.read_bundle(fibers)

    #fibers_rh = BT.read_bundle(r'\\wsl$\Ubuntu-18.04\home\cris\Memoria2021\Archi\002\002\Fasciculos_T1\Right\align_cluster_subject_to_rh_PoC-PrC_0.bundles'.replace('\\','/'))

    #Lhemi_path =r'\\wsl$\Ubuntu-18.04\home\joaquin\joaquin\pmt_mt\pruebas\prueba_079\Archi\079\079\079\lh.obj'.replace('\\','/') ; # left hemisphere path
    #Rhemi_path = r'\\wsl$\Ubuntu-18.04\home\cris\MemoriaARCHI\Archi\002\002\002\rh.obj'.replace('\\','/') ; # right hemisphere path

    InTri, FnTri, InPoints, FnPoints, fib_index = read_intersection(ix_path_lh);
    #print(InTri, FnTri)

    tri = vt.Polygon(Lvertex, Lpolygons[InTri])
    tri.setColor((1.0,1.0/4,1.0/4))
    render.AddActor(tri)

    tri = vt.Polygon(Lvertex, Lpolygons[FnTri])
    tri.setColor((0.0,0.0,1.0))
    render.AddActor(tri)

    if bundle[:len(bundle)-17] + '_A' not in Atlas_L_fasc_dict:
        Atlas_L_fasc_dict[bundle[:len(bundle)-17] + '_A'] = {}

    if bundle[:len(bundle)-17]+ '_B' not in Atlas_L_fasc_dict:
        Atlas_L_fasc_dict[bundle[:len(bundle)-17] + '_B'] = {}

    for i,tri in enumerate(InTri):
        print(i)
        Atlas_Lhemi_dict[tri]['n'] += 1
        Atlas_Lhemi_dict[tri][bundle[:len(bundle)-17] + '_A'] += 1

        nbors = Lneighbors[tri]
        for nbor in nbors:
            if nbor in InTri:
                Atlas_Lhemi_dict[tri]['n'] += 1
                Atlas_Lhemi_dict[tri][bundle[:len(bundle)-17] + '_A'] += 1

    for i,tri in enumerate(FnTri):
        print(i)
        Atlas_Lhemi_dict[tri]['n'] += 1
        Atlas_Lhemi_dict[tri][bundle[:len(bundle)-17] + '_B'] += 1

        nbors = Lneighbors[tri]
        for nbor in nbors:
            if nbor in InTri:
                Atlas_Lhemi_dict[tri]['n'] += 1
                Atlas_Lhemi_dict[tri][bundle[:len(bundle)-17] + '_B'] += 1


triangles_per_fascicle(Atlas_Lhemi_dict, Atlas_L_fasc_dict)

dir = os.listdir('bundles/');
bundles = []
for bundle in dir:
    print()
    bundles.append(BT.read_bundle(dir+bundle))
for bundle in bundles:
    for fiber in bundle:
        fib = vt.Line(fiber)
        fib.setJetColormap()
        render.AddActor(fib)
render.Start();

del render
