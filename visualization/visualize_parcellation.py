import visualizationTools as vt
import numpy as np
import bundleTools as bt
import pickle
import os

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
    Lrestricted, Rrestricted = {},{}
    return Lrestricted, Rrestricted

def load_parcels (parcels, parcels_path): #hard cc final
    Lparcels_path =  parcels +'Lparcels.txt'
    Rparcels_path = parcels +'Rparcels.txt'

    Lparcels = read_parcel(Lparcels_path,'L')
    Rparcels = read_parcel(Rparcels_path,'R')
    print(Lparcels.keys())
    print(Rparcels.keys())
    return Lparcels, Rparcels

def load_parcels_2(parcels_path):
    Lparcels_path = parcels_path + '/left/'
    Rparcels_path = parcels_path + '/right/'

    Lparcels = dict()
    Rparcels = dict()

    for Dir in os.listdir(Lparcels_path):
        Lparcels[Dir.split('.')[0]] = bt.read_parcels(Lparcels_path + Dir)
        
    for Dir in os.listdir(Rparcels_path):
        Rparcels[Dir.split('.')[0]] = bt.read_parcels(Rparcels_path + Dir)
            
    return Lparcels, Rparcels


def read_parcel(parcel_path, hemi):
    parcel = dict()
    with open(parcel_path,"r") as fp:
        for line in fp.readlines():
            line = line.split()
            if line[0] == "sp":
                label = line[1]
            if line[0] == "t":
                parcel[label+"_"+hemi] = list(map(int,line[1:]))
                label = ""
    return parcel

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
    print(len(fp))
    #Paleta de colores según cantidad de parcelas
    paleta = [(np.random.random(), np.random.random(), np.random.random()) for i in range(len(fp))]

    #Directorios de los mallados corticales
    Lhemi_path = meshes_path + sub + '/lh.obj'; # left hemisphere path
    Rhemi_path = meshes_path + sub + '/rh.obj'; # right hemisphere path

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
    
    #Para cada parcela del hemisferio izquierdo...
    # for k, v in L_sp.items():
    #     #Se selecciona un color de la paleta
    #     color = paleta[fp.index(k)]
        
    #     if len(v) == 0:
    #         continue
      
    #     #De todos los triángulos con parcelas, se eliminan aquellos que pertenecen al conjunto de triángulos restringidos.
    #     v_restricted = list(set(v)) #list(set(v).difference(Lrestricted))

    #     #Se renderizan los triángulos y polígonos.
    #     sp_tri = vt.Polygon(Lvertex, Lpolygons[v_restricted]);
    #     sp_tri.setColor((color[0], color[1], color[2]));
    #     render.AddActor(sp_tri);

    add_parcels_to_render(render, Lvertex, Lpolygons, L_sp, paleta, fp, Lrestricted)
    add_parcels_to_render(render, Rvertex, Rpolygons, R_sp, paleta, fp, Rrestricted)
    
    render.Start();
    del render

def add_parcels_to_render(render, Hvertex, Hpolygons, H_sp, paleta, fp, restricted = {},seed = False):
    for k, v in H_sp.items():
        #Se selecciona un color de la paleta
        color = paleta[fp.index(k)]
        
        if len(v) == 0:
            continue
      
        #De todos los triángulos con parcelas, se eliminan aquellos que pertenecen al conjunto de triángulos restringidos.
        v_restricted = list(set(v).difference(restricted))

        #Se renderizan los triángulos y polígonos.
        sp_tri = vt.Polygon(Hvertex, Hpolygons[v_restricted]);
        sp_tri.setColor((color[0], color[1], color[2]));
        render.AddActor(sp_tri);
    return render

output = "output"
# Lparcels_final, Rparcels_final = load_parcels('final_atlas/',     output)
Lparcels_final, Rparcels_final = load_parcels_2('final_parcels/')
print(len(Lparcels_final.keys()),len(Rparcels_final.keys()))
meshes_path = "meshes/"
visualize_parcellation(meshes_path,Lparcels_final,Rparcels_final,"001")

