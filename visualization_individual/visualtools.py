#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Agosto 10 20:09:15 2020

@author: fondecyt-1190701
"""
import numpy as np
import os
from collections import defaultdict

import bundleTools as bt
import visualizationTools as vt

import pickle

import hashlib

def deterministic_random_float_list(input_value, size=3):
    # Convert input_value to a hash (you can use any string/number as input)
    input_str = str(input_value).encode('utf-8')
    hashed = hashlib.sha256(input_str).hexdigest()

    # Convert hash into an integer and use modulo to get a reasonable seed
    random_seed = int(hashed, 16) % (2**32)
    np.random.seed(random_seed)

    # Generate a list of random floats between 0 and 1
    return np.random.random(size).tolist()

def load_restricted_triangles():
    #Existen ciertos triángulos que, por definición, no pueden representar parcelas. Estos corresponden a regiones posterior-inferior de la línea media...
    #...donde ambos hemisferios se unen, ya que en estricto rigor no corresponden a corteza, si no que a materia blanca/gris interna.
    
    #La parcelación obtenida por Lefranc indica cuales triángulos están "restringidos", los cuales están guardados en el archivo .pkl:
    #Lrestricted.pkl para el hemisferio izquierdo.
    #Rrestricted.pkl para el hemisferio derecho.
    
    with open('pickles/Lnope.pkl', 'rb') as f:
        Lrestricted = set(pickle.load(f))
    
    with open('pickles/Rnope.pkl', 'rb') as f:
        Rrestricted = set(pickle.load(f))
    
    return Lrestricted, Rrestricted

#Carga parcelas ('hard','cc','final')    
def load_parcels (parcels, parcels_path): #hard cc final
    Lparcels_path =  parcels_path + '/'+ parcels +'_parcels/left/'
    Rparcels_path = parcels_path + '/'+ parcels +'_parcels/right/'

    Lparcels = dict()
    Rparcels = dict()
    set_triangles = set()
    for Dir in os.listdir(Lparcels_path):
        Lparcels[Dir.split('.')[0]] = bt.read_parcels(Lparcels_path + Dir)
        set_triangles = set_triangles.union(set(Lparcels[Dir.split('.')[0]]))
    for Dir in os.listdir(Rparcels_path):
        Rparcels[Dir.split('.')[0]] = bt.read_parcels(Rparcels_path + Dir)
            
    return Lparcels, Rparcels

#Formula del coeficiente DICE
def DSC(A,B):
    set_A = set(A)
    set_B = set(B)
    
    interx = set_A.intersection(set_B)
    
    return (2*len(interx))/((len(set_A)+len(set_B)))

#Calculo de coeficiente DICE para comparar parcelas con atlas
def dise_comparision (atlas_comparision, parcels_path, dice_thr):
    # Lectura de parcelas propias.    
    lh_mine_dict, rh_mine_dict = load_parcels('final', parcels_path)
        
    # Cargar parcelación del atlas seleccionado.
    with open(atlas_comparision + '_Lparcels.pkl', 'rb') as f:   
        lh_atlas_dict = pickle.load(f)
    
    with open(atlas_comparision + '_Rparcels.pkl', 'rb') as f:   
        rh_atlas_dict = pickle.load(f)    
        
    # Cálculo de DSC entre parcelas.
    # Diccionario parcela_propia:parcela_atlas, para aquellos casos que superan el umbral de DSC.
    lh_dice_dict = defaultdict(int)
    rh_dice_dict = defaultdict(int)

    # Lista que almacena las parcelas ya utilizadas.
    used = []
    nl_parcels = len(lh_mine_dict.keys())
    nr_parcels = len(rh_mine_dict.keys())
    print('n° de parcelas izquierdo: %d' % nl_parcels)
    print('n° de parcelas derecho: %d' % nr_parcels)
    # Iteración sobre todas las parcelas propias obtenidas.
    for parcel, tris in lh_mine_dict.items():
        #Se registra el mayor DSC obtenido entre todas las comparaciones, y el nombre de la parcela asociada.
        dice_max = 0 
        winner = ''
      
        #Se itera sobre las parcelas del atlas.
        for ref, rtris in lh_atlas_dict.items():
            
            #Si la parcela ya fue utilizada, ignorar.
            if ref in used:
                continue
            
            #Cálculo de DSC entre parcela propia y parcela del atlas.
            dice = DSC(tris,rtris)
            
            #Si es mayor al máximo obtenido, actualizar.
            if dice > dice_max:
                dice_max = dice
                winner = ref
        
        #Si el mayor valor obtenido supera el umbral de similitud, se agrega al diccionario de parcelas similares, y a la lista de parcelas ya utilizadas.
        if dice_max >= dice_thr:
            lh_dice_dict[parcel] = winner
            used.append(winner)
            
        # Si no supera el umbral, continuar con la siguiente parcela.
        else:
            continue
    
    #Se repite lo mismo para el hemisferio derecho.
    used = []
    
    for parcel, tris in rh_mine_dict.items():
        dice_max = 0
        winner = ''
      
        for ref, rtris in rh_atlas_dict.items():
            if ref in used:
                continue
            dice = DSC(tris,rtris)
            if dice > dice_max:
                dice_max = dice
                winner = ref
            
        if dice_max >= dice_thr:
            rh_dice_dict[parcel] = winner
            used.append(winner)
            
        else:
            continue  
    
    #Diccionario de parcelas similares, considerando los triángulos asociados en el caso de la parcelación propia.
    lh_mine_common = {k:lh_mine_dict[k] for k in list(lh_dice_dict.keys()) if k in lh_mine_dict}
    rh_mine_common = {k:rh_mine_dict[k] for k in list(rh_dice_dict.keys()) if k in rh_mine_dict}
    
    #Diccionario de parcelas similares, considerando los triángulos asociados en el caso de la parcelación del atlas.
    lh_atlas_common = {k:lh_atlas_dict[k] for k in list(lh_dice_dict.values()) if k in lh_atlas_dict}
    rh_atlas_common = {k:rh_atlas_dict[k] for k in list(rh_dice_dict.values()) if k in rh_atlas_dict}
    
    if not os.path.exists('Dise/'+atlas_comparision.replace('atlas/',"")):
        os.makedirs('Dise/'+atlas_comparision.replace('atlas/',""))
        
    save_txt('Dise/'+atlas_comparision.replace('atlas/',"")+parcels_path.replace("Registro_salidas","")+'_lh_list_'+atlas_comparision.replace("/",""),lh_mine_common, dice_thr)
    save_txt('Dise/'+atlas_comparision.replace('atlas/',"")+parcels_path.replace("Registro_salidas","")+'_rh_list_'+atlas_comparision.replace("/",""), rh_mine_common, dice_thr)
    
    return lh_mine_common, rh_mine_common, lh_atlas_common, rh_atlas_common

def save_txt (name, diccionary, dice_thr):
    count=0
    with open(name+'_'+str(int(dice_thr*100))+'.txt', 'w') as f:
        for line in diccionary.keys():
            f.write(line)
            f.write('\n')
            count+=1
        f.write('\nTotal=%d' % count)
   #%%     

def visualize_parcellation(meshes_path, L_sp, R_sp, sub, seed = False):
    #Cargar trianguos restringidos
    Lrestricted, Rrestricted= load_restricted_triangles()
    
    #Semilla para colores aleatorios
    if seed != False:
        np.random.seed(seed)
    
    #Parcelas finales a graficar
    final_parcels = set()

    for k in L_sp.keys():
        final_parcels.add(k)
        
    for k in R_sp.keys():
        final_parcels.add(k)

    fp = list(final_parcels)    

    #Paleta de colores según cantidad de parcelas
    paleta = [(np.random.random(), np.random.random(), np.random.random()) for i in range(len(fp))]

    #Directorios de los mallados corticales
    Lhemi_path = meshes_path + '/lh.obj'; # left hemisphere path
    Rhemi_path = meshes_path + '/rh.obj'; # right hemisphere path

    #Lectura de mallados
    Lvertex, Lpolygons = bt.read_mesh_obj(Lhemi_path)
    Rvertex, Rpolygons = bt.read_mesh_obj(Rhemi_path)
    
    Lhemi = vt.Polygon(Lvertex, Lpolygons);
    Rhemi = vt.Polygon(Rvertex, Rpolygons);
    
    Lhemi.setOpacity(1);
    Rhemi.setOpacity(1);
    
    #Creación del render a visualizar
    render = vt.Render();
    
    #Se renderizan los mallados
    render.AddActor(Lhemi);
    render.AddActor(Rhemi);
    
    # Variables to track triangles
    L_total_triangles = len(Lpolygons)
    R_total_triangles = len(Rpolygons)
    L_unique_triangles = set()
    R_unique_triangles = set()
    L_repeated_triangles = set()  # To track already counted repeated triangles
    R_repeated_triangles = set()

    total_restricted = len(Lrestricted) + len(Rrestricted)
    usable_triangles = L_total_triangles + R_total_triangles - total_restricted  # Adjusted total
    
    #Para cada parcela del hemisferio izquierdo...
    for k, v in L_sp.items():
        #Se selecciona un color de la paleta
        color = deterministic_random_float_list(k)
        
        if len(v) == 0:
            continue

        #De todos los triángulos con parcelas, se eliminan aquellos que pertenecen al conjunto de triángulos restringidos.
        v_restricted = list(set(v).difference(Lrestricted))
      
        # Collect all triangles for overlap calculation
        for tri in v_restricted:
            if tri in L_unique_triangles:
                L_repeated_triangles.add(tri)
            else:
                L_unique_triangles.add(tri)
        #Se renderizan los triángulos y polígonos.
        sp_tri = vt.Polygon(Lvertex, Lpolygons[v_restricted]);
        sp_tri.setColor((color[0], color[1], color[2]));
        render.AddActor(sp_tri);

    #Ídem para el derecho
    for k, v in R_sp.items():
        color = deterministic_random_float_list(k)
    
        if len(v) == 0:
            continue
    
        v_restricted = list(set(v).difference(Rrestricted))
        # Collect all triangles for overlap calculation
        for tri in v_restricted:
            if tri in R_unique_triangles:
                R_repeated_triangles.add(tri)
            else:
                R_unique_triangles.add(tri)

    
        sp_tri = vt.Polygon(Rvertex, Rpolygons[v_restricted]);
        sp_tri.setColor((color[0], color[1], color[2]));
        render.AddActor(sp_tri);
    
    # Calculate percentages
    percentage_included = (len(L_unique_triangles) + len(R_unique_triangles)) / usable_triangles * 100
    percentage_repeated = (len(L_repeated_triangles) + len(R_repeated_triangles)) / usable_triangles * 100

    # Print results
    print(f"Percentage of triangles included in regions (excluding restricted): {percentage_included:.2f}%")
    print(f"Percentage of repeated triangles (overlap): {percentage_repeated:.2f}%")
    
    render.Start();
    del render


def multiple_DSC_comp():

    #Comparacion Dice
    atlas_info = {}
    for atlas in atlases:
        print(''.join(atlas[6:]))
        atlas_info[''.join(atlas[6:])] = []
        for folder in os.listdir('Parcellation/'):
            params = folder.split('_')
            dc = ''.join(params[1][2:])
            idc = ''.join(params[2][3:])
            output_parcellation = 'Parcellation/'+folder+'/'
            lh_mine_common, rh_mine_common, lh_atlas_common, rh_atlas_common = dise_comparision(atlas, output_parcellation, dice_thr)
            atlas_info[''.join(atlas[6:])].append([dc, idc, 0.1, len(lh_mine_common.keys()), len(rh_mine_common.keys()), len(lh_mine_common.keys()) + len(rh_mine_common.keys())])
    
    """Para guardar los resultados en una tabla de latex"""
    file = open("comparisons.txt", "w")
    for k,v in atlas_info.items():
        file.write('\\multirow{'+k+'}')
        for info in v:
            i = 0
            file.write(' & '+info[i]+' & '+str(info[i+1])+' & '+str(info[i+2])+' & '+str(info[i+3])+' & '+str(info[i+4])+' & '+str(info[i+5])+' \\\\ \n')
        file.write('\\hline\n')
    file.close()

#Sujeto base. Puede ser cualquiera, ya que todos los mallados tienen triángulos correspondientes.
sub = '111312'
meshes_path= '../9-individualization/inputs/subject_mesh/'
dice_thr=0.6

# Selección de atlas a comparar.
atlases = ['atlas/Lefranc','atlas/Brainnetome','atlas/Narciso','atlas/Richards']
semilla_visualizacion = 48

# Comparación Dice
salidas = "D:/documentos/universidad/TESIS/parcellation/parcellation-master/visualization_individual/outputHCP5"
lh_atlas_dict, rh_atlas_dict = load_parcels('final', 'ParcellationHARDI/')
with open('atlas/Richards_Lparcels.pkl','wb') as handle:
    pickle.dump(lh_atlas_dict,handle)
with open('atlas/Richards_Rparcels.pkl','wb') as handle:
    pickle.dump(rh_atlas_dict,handle)
#for Dir in os.listdir(salidas):
 #   final_parcels = 'Registro_salidas/'+Dir
    #lh_mine_common, rh_mine_common, lh_atlas_common, rh_atlas_common = dise_comparision(atlases[0], final_parcels, dice_thr)
    #lh_mine_common, rh_mine_common, lh_atlas_common, rh_atlas_common = dise_comparision(atlases[1], final_parcels, dice_thr)
    #lh_mine_common, rh_mine_common, lh_atlas_common, rh_atlas_common = dise_comparision(atlases[2], final_parcels, dice_thr)
  #  lh_mine_common, rh_mine_common, lh_atlas_common, rh_atlas_common = dise_comparision(atlases[3], final_parcels, dice_thr)

    # Visualizacion para Dice
    # visualize_parcellation(meshes_path, lh_atlas_common, rh_atlas_common, '001', seed = 47)
    # visualize_parcellation(meshes_path, lh_mine_common, rh_mine_common, '001', seed = 47)
final_parcels = "Parcellation"
#
Lparcels_ps, Rparcels_ps= load_parcels('ps', final_parcels)
Lparcels_fp, Rparcels_fp= load_parcels('fp', final_parcels)
Lparcels_hard, Rparcels_hard= load_parcels('hard', final_parcels)
Lparcels_cc, Rparcels_cc= load_parcels('cc', final_parcels)
Lparcels_final, Rparcels_final= load_parcels('final', final_parcels)
#
visualize_parcellation(meshes_path, Lparcels_ps, Rparcels_ps, sub, seed = semilla_visualizacion)
visualize_parcellation(meshes_path, Lparcels_fp, Rparcels_fp, sub, seed = semilla_visualizacion)
visualize_parcellation(meshes_path, Lparcels_hard, Rparcels_hard, sub, seed = semilla_visualizacion)
visualize_parcellation(meshes_path, Lparcels_cc, Rparcels_cc, sub, seed = semilla_visualizacion)
visualize_parcellation(meshes_path, Lparcels_final, Rparcels_final, sub, seed = semilla_visualizacion)
