# Copyright (C) 2019  Andrea Vázquez Varela

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Base Authors:
# Narciso López López
# Andrea Vázquez Varela
#Creation date: 31/01/2019
#Last update: 20/07/2019

# Modification Author:
# Martín Stockle
# Creation date: 20/07/2023
# Last update: 15/04/2025

import argparse
from time import time
import IO
from utils import *
import networkx as nx
import subprocess as sproc
from classes import *
import os
import time
import sys
import math
import matplotlib.pyplot as plt
import numpy as np

def calculate_parcel_stats(sizes):
    if not sizes:
        return 0, 0, 0, 0, 0, []

    big = max(sizes)
    small = min(sizes)
    suma_parcelas = sum(sizes)
    numero_parcelas = len(sizes)
    avg = suma_parcelas / numero_parcelas if numero_parcelas > 0 else 0
    std = np.std(sizes) if sizes else 0
    return numero_parcelas, big, small, avg, std, sizes

def plot_parcel_distribution(Lstats, Rstats, title):
    L_hist, L_bins = np.histogram(Lstats[5], bins=30)
    R_hist, R_bins = np.histogram(Rstats[5], bins=30)

    print(f"{title} - Left hemisphere parcels histogram:")
    for bin_start, bin_end, count in zip(L_bins[:-1], L_bins[1:], L_hist):
        print(f"Bin {bin_start:.2f} - {bin_end:.2f}: {count}")

    print(f"{title} - Right hemisphere parcels histogram:")
    for bin_start, bin_end, count in zip(R_bins[:-1], R_bins[1:], R_hist):
        print(f"Bin {bin_start:.2f} - {bin_end:.2f}: {count}")

def count_non_zero_processed_sub_parcels(aparcels):
    count = 0
    sizes = []
    for ap in aparcels:
        for sp in ap.sub_parcels.values():
            if len(sp.triangles) > 0:
                count += 1
                sizes.append(len(sp.triangles))
    stats = calculate_parcel_stats(sizes)
    return count, stats

def count_non_zero_hard_parcels(aparcels):
    count = 0
    sizes = []
    for ap in aparcels:
        for hp in ap.hparcels.values():
            if len(hp) > 0:
                count += 1
                sizes.append(len(hp))
    stats = calculate_parcel_stats(sizes)
    return count, stats

def count_non_zero_pcc_parcels(pcc_parcels):
    count = 0
    sizes = []
    for pcc in pcc_parcels:
        if len(pcc) > 0:
            count += 1
            sizes.append(len(pcc))
    stats = calculate_parcel_stats(sizes)
    return count, stats

def label_triangles(triangles):

    for tri in triangles:
        label0 = tri.v1.label_parcel
        label1 = tri.v2.label_parcel
        label2 = tri.v3.label_parcel

        if (label0 == label1 == label2):
            tri.label_parcel = label2
        elif (label0 == label1 and label0!=label2):
            tri.label_parcel = label0
        elif (label1 == label2 and (label1!= label0)):
            tri.label_parcel = label1
        elif (label0 == label2) and (label0!=label1):
            tri.label_parcel = label0
        else:
            tri.label_parcel = label0

    return triangles


def fusion(aparcels,anatomic_parcel,sub_parcel_list,parcel_names):
    while(len(sub_parcel_list)!=1):
        sub_parcel1 = sub_parcel_list[0]
        sub_parcel2 = sub_parcel_list[1]
        new_name = fusion_names(parcel_names[sub_parcel1.label],parcel_names[sub_parcel2.label])
        new_triangles = sub_parcel1.triangles.union(sub_parcel2.triangles)
        sub_parcel1.triangles = new_triangles
        anatomic_parcel.remove_subparcel(sub_parcel2) 
        for k,sub_parcel in anatomic_parcel.sub_parcels.items(): 
            for tri in sub_parcel.triangles:
                tri.replace_label(sub_parcel2.label,sub_parcel1.label)
                """Fuse fibers_map"""
                if sub_parcel1.label not in tri.fibers_map and sub_parcel2.label in tri.fibers_map:
                    tri.fibers_map[sub_parcel1.label] = 0
                if sub_parcel2.label in tri.fibers_map:
                    tri.fibers_map[sub_parcel1.label] += tri.fibers_map[sub_parcel2.label]
                    del tri.fibers_map[sub_parcel2.label]
        parcel_names[sub_parcel1.label] = new_name
        sub_parcel_list.remove(sub_parcel_list[1])  
    return parcel_names


def joinable_sparcels(clique, visited):
    subparcels = []
    for node in clique:
        if node.label < len(visited):
            if not visited[node.label]:
                subparcels.append(node)
                visited[node.label] = True
    return subparcels


def delete_reps(us,idc_matrix):
    cliques = []
    for clique in us:
        cliques.append(sorted(clique, key = lambda kv: kv.label))

    cliques = sorted(cliques, key = lambda kv: sum([sp.label for sp in kv]))

    rep_map = {}
    selected_cliques = {}
    for i,clique in enumerate(cliques):
        for sparcel in clique:
            if sparcel not in rep_map:
                rep_map[sparcel] = [i]
            else:
                rep_map[sparcel].append(i)
    for sparcel1,clique_list in rep_map.items():
        if len(clique_list) > 1:
            max_idc = 1
            selected_cliques[sparcel1] = -1
            for i in clique_list:
                clique = cliques[i]
                sum_idc = 0
                for sparcel2 in clique:
                    sum_idc+=idc_matrix[sparcel1.label][sparcel2.label]
                if sum_idc > max_idc:
                    max_idc = sum_idc
                    selected_cliques[sparcel1] = i

    for sparcel,index_clique in selected_cliques.items():
        for i in range(len(cliques)):
            if i !=index_clique and sparcel in cliques[i]:
                cliques[i].remove(sparcel)


    return (sorted(cliques, key = len, reverse = True))

def remove_less_representative_triangles(subparcel):
    triangles_to_remove = []
    thr = 1
    for triangle in subparcel.triangles:
        if subparcel.label in triangle.subjects_map and triangle.subjects_map[subparcel.label]< thr:
            triangles_to_remove.append(triangle.index)
            del triangle.fibers_map[subparcel.label]
            triangle.labels_subparcel.remove(subparcel.label)
    for triangle in triangles_to_remove:
        subparcel.remove_triangle(triangle)
        

def create_fusion_list_nuevo_thr(anatomic_parcel,dc_thr,thr_idc,names,hemi):
    fusion_list = []
    nsparcels = len(names)
    idc_matrix = np.zeros((nsparcels,nsparcels))
    connect_graph = nx.Graph()
    for k,sparcel in anatomic_parcel.sub_parcels.items():
        connect_graph.add_node(sparcel)
    for k,sparcel1 in anatomic_parcel.sub_parcels.items():
        for k,sparcel2  in anatomic_parcel.sub_parcels.items():
            if sparcel1!=sparcel2:
                triangles1 = [tri for tri in sparcel1.triangles if tri.prob_map[sparcel1.label]>0.1725*math.exp(-0.07*len(tri.prob_map))]
                triangles2 = [tri for tri in sparcel2.triangles if tri.prob_map[sparcel2.label]>0.1725*math.exp(-0.07*len(tri.prob_map))]
                inter = intersection(triangles1, triangles2)
                min_inter = min(len(sparcel1.triangles),len(sparcel2.triangles))
                idc = len(inter) / min_inter
                if idc >= thr_idc: #Si se solapan mucho las subparcelas...
                    connect_graph.add_edge(sparcel1,sparcel2)
                    idc_matrix[sparcel1.label][sparcel2.label] = idc
                    idc_matrix[sparcel2.label][sparcel1.label] = idc

    cliques = sorted(nx.find_cliques(connect_graph), key=len, reverse=True)
    cliques = delete_reps(cliques,idc_matrix)
    
    visited = np.zeros(len(names), bool)
    for clique in cliques:
        parcel_list = joinable_sparcels(clique,visited)
        fusion_list.append(parcel_list)
    return fusion_list

def create_fusion_list(anatomic_parcel,dc_thr,thr_idc,names,hemi):
    fusion_list = []
    nsparcels = len(names)
    idc_matrix = np.zeros((nsparcels,nsparcels))
    connect_graph = nx.Graph()
    for k,sparcel in anatomic_parcel.sub_parcels.items():
        connect_graph.add_node(sparcel)
    for k,sparcel1 in anatomic_parcel.sub_parcels.items():
        for k,sparcel2  in anatomic_parcel.sub_parcels.items():
            if sparcel1!=sparcel2:
                triangles1 = sparcel1.get_triangles_prob(dc_thr, sparcel1.label)
                triangles2 = sparcel2.get_triangles_prob(dc_thr, sparcel2.label)
                inter = intersection(triangles1, triangles2)
                min_inter = min(len(sparcel1.triangles),len(sparcel2.triangles))
                idc = len(inter) / min_inter
                if idc >= thr_idc: #Si se solapan mucho las subparcelas...
                    connect_graph.add_edge(sparcel1,sparcel2)
                    idc_matrix[sparcel1.label][sparcel2.label] = idc
                    idc_matrix[sparcel2.label][sparcel1.label] = idc

    cliques = sorted(nx.find_cliques(connect_graph), key=len, reverse=True)
    cliques = delete_reps(cliques,idc_matrix)
    
    visited = np.zeros(len(names), bool)
    for clique in cliques:
        parcel_list = joinable_sparcels(clique,visited)
        if len(parcel_list) > 1:
            fusion_list.append(parcel_list)
    return fusion_list


def recalc_probability(anatomic_parcel):
    for k,sub_parcel in anatomic_parcel.sub_parcels.items():
        for tri in sub_parcel.triangles:
            tri.set_prob_map()


def remove_subparcel(aparcels,anatomic_parcel,subparcel):
    for k,sparcel in anatomic_parcel.sub_parcels.items():
        for tri in sparcel.triangles:
            tri.remove_labels([subparcel.label])
            if subparcel.label in tri.fibers_map:
                del tri.fibers_map[subparcel.label]
    anatomic_parcel.remove_subparcel(subparcel)


def remove_small_parcels(aparcels,anatomic_parcel,parcel_names,size_thr,trac,trac_path,hemi):
    avg_inter = 0
    parcel_sizes = [len(sparcel.triangles) for k,sparcel in anatomic_parcel.sub_parcels.items()]
    avg_size = sum(parcel_sizes) / (len(anatomic_parcel.sub_parcels))
    ed_parcels = np.std(parcel_sizes)
    thr = max(0,avg_size - size_thr*ed_parcels)
    if trac == "y":
        remove_file = open(trac_path+"/"+hemi+"remove.txt","a+")
    inter_sizes = []
    for k,sparcel in anatomic_parcel.sub_parcels.items():
        inter_sizes += [len(tri.labels_subparcel) for tri in sparcel.triangles]
        avg_inter +=sum([len(tri.labels_subparcel) for tri in sparcel.triangles])
    avg_inter = avg_inter / (len(anatomic_parcel.sub_parcels))
    ed_inter = np.std(inter_sizes)
    thr_inter = max(0,avg_inter - size_thr*ed_inter)
    n = 0
    nap_flag = 0
    sp_to_remove = []
    for k,sparcel in anatomic_parcel.sub_parcels.items():
        num_inters = sum([len(tri.labels_subparcel) for tri in sparcel.triangles])
        if (len(sparcel.triangles) < thr) or (num_inters < thr_inter):
            n+=1
            if trac == "y":
                if nap_flag == 0:
                    remove_file.write("ap "+str(anatomic_parcel.label)+"\n")
                    nap_flag = 1
                remove_file.write(str(sparcel.label)+"\n")
            sp_to_remove.append(sparcel)
    for sparcel in sp_to_remove:        
        remove_subparcel(aparcels,anatomic_parcel,sparcel)
    return n

def remove_small_parcels_original(aparcels,anatomic_parcel,parcel_names,size_thr,trac,trac_path,hemi):
    avg_inter = 0
    avg_size = sum([len(sparcel.triangles) for k,sparcel in anatomic_parcel.sub_parcels.items()]) / (len(anatomic_parcel.sub_parcels))
    if trac == "y":
        remove_file = open(trac_path+"/"+hemi+"remove.txt","a+")
    for k,sparcel in anatomic_parcel.sub_parcels.items():
        avg_inter +=sum([len(tri.labels_subparcel) for tri in sparcel.triangles])
    avg_inter = avg_inter / (len(anatomic_parcel.sub_parcels))
    thr = (avg_size*size_thr)
    thr_inter = (avg_inter*size_thr)
    n = 0
    nap_flag = 0
    sp_to_remove = []
    for k,sparcel in anatomic_parcel.sub_parcels.items():
        num_inters = sum([len(tri.labels_subparcel) for tri in sparcel.triangles])
        if (len(sparcel.triangles) < thr) or (num_inters < thr_inter):
            n+=1
            if trac == "y":
                if nap_flag == 0:
                    remove_file.write("ap "+str(anatomic_parcel.label)+"\n")
                    nap_flag = 1
                remove_file.write(str(sparcel.label)+"\n")
            sp_to_remove.append(sparcel)
    for sparcel in sp_to_remove:        
        remove_subparcel(aparcels,anatomic_parcel,sparcel)
    return n


def processing_parcels(aparcels,idc,dc_thr,size_thr,parcel_names,trac,trac_path,hemi):
    n_remove = 0
    for i,anatomic_parcel in enumerate(aparcels):
        if len(anatomic_parcel.sub_parcels) > 0:
            if trac == "y":
                fusion_file = open(trac_path+"/"+hemi+"fusion.txt","a+")
            """Remove less representative triangle from subparcels"""
            for j, subparcel in anatomic_parcel.sub_parcels.items():
                remove_less_representative_triangles(subparcel)
                if len(subparcel.triangles) == 0:
                    anatomic_parcel.remove_subparcel(subparcel) #debo eliminarlas después
            """Density center calculation"""
            recalc_probability(anatomic_parcel)
            n_remove += remove_small_parcels(aparcels,anatomic_parcel,parcel_names,size_thr,trac,trac_path,hemi)
            """Parcel overlapping"""
            fusion_list = create_fusion_list(anatomic_parcel,dc_thr,idc,parcel_names,hemi)
            for list in fusion_list:
                if len(list)>0:
                    if trac == "y":
                        fusion_file.write("ap "+str(anatomic_parcel.label)+"\n")
                        fusion_file.write(" ".join([str(parcel.label) for parcel in list])+"\n")
                if (len(list)>1):
                    parcel_names = fusion(aparcels,anatomic_parcel,list,parcel_names)
    print("Removed subparcels: ",n_remove)
    return aparcels, parcel_names

def get_hard_parcels(anatomic_parcels, parcel_names, trac, trac_path, hemi):
    if trac == "y":
        probmap_file = open(trac_path + "/" + hemi + "probmap.txt", "a+")
    
    # Step 1: Group triangles by their most probable subparcel and count the amount of different triangles in the subparcels
    triangle_groups = {}
    subparcel_triangles = set()
    subparcel_count = 0
    for anatomic_parcel in anatomic_parcels:
        recalc_probability(anatomic_parcel)
        for sub_parcel in anatomic_parcel.sub_parcels.values():
            subparcel_count += 1
            for triangle in sub_parcel.triangles:
                subparcel_triangles.add(triangle)
                if triangle.prob_map:
                    most_probable_label = max(triangle.prob_map, key=triangle.prob_map.get)
                    if most_probable_label not in triangle_groups:
                        triangle_groups[most_probable_label] = set()
                    triangle_groups[most_probable_label].add(triangle)
                    if trac == "y":
                        probmap_file.write(str(triangle.index) + " " + str(most_probable_label) + "\n")
    
    # Compare the number of different triangles in the subparcels with the number of triangles in the triangle_groups
    num_subparcel_triangles = len(subparcel_triangles)
    num_triangle_groups_triangles = sum(len(triangles) for triangles in triangle_groups.values())
    if num_subparcel_triangles != num_triangle_groups_triangles:
        print(f"Warning: Mismatch in triangle counts. Subparcels: {num_subparcel_triangles}, Triangle groups: {num_triangle_groups_triangles}")
    
    # Compare the number of subparcels with the number of triangle_groups
    num_triangle_groups = len(triangle_groups)
    if subparcel_count != num_triangle_groups:
        print(f"Warning: Mismatch in subparcel counts. Subparcels: {subparcel_count}, Triangle groups: {num_triangle_groups}")
    
    # Step 2: Create hard parcels and add triangles to them
    for anatomic_parcel in anatomic_parcels:
        anatomic_parcel.hard_parcels = set()  # Ensure hard_parcels is initialized as an empty set
        for sub_parcel in anatomic_parcel.sub_parcels.values():
            label = sub_parcel.label
            if label in triangle_groups:
                hard_parcel = SubParcel(label, anatomic_parcel.label, triangle_groups[label], [])
                anatomic_parcel.hard_parcels.add(hard_parcel)
                anatomic_parcel.add_hparcel_triangles(parcel_names[int(label)], triangle_groups[label])
    if trac == "y":
        probmap_file.close()
    
    return anatomic_parcels

def get_hard_parcels_original(aparcels,parcel_names,trac,trac_path,hemi):
    if trac == "y":
        probmap_file = open(trac_path+"/"+hemi+"probmap.txt","a+")
    for ap in aparcels:
        recalc_probability(ap)
        hparcels_map = {}
        for k,sp in ap.sub_parcels.items():
            for tri in sp.triangles:
                selected_parcel = most_probable(tri.prob_map)
                if trac == "y":
                    probmap_file.write(str(tri.index)+" "+str(selected_parcel)+"\n")
                if selected_parcel != -1:
                    selected_parcel = ap.find_subparcel(selected_parcel)
                    if selected_parcel != None:
                        if not selected_parcel.label in hparcels_map:
                            hparcels_map[selected_parcel.label] = set()
                        hparcels_map[selected_parcel.label].add(tri)
        for label, triangles in hparcels_map.items():
            sp = ap.find_subparcel(label)
            hparcel = SubParcel(label, ap.label, triangles, [])
            ap.add_hparcel_triangles(parcel_names[int(label)],triangles)
            ap.hard_parcels.add(hparcel)
    return aparcels

def get_PCC(aparcels,triangles):
    parcel_cc = {}
    triangles_arr = np.asarray([[tri.v1.index,tri.v2.index,tri.v3.index] for tri in triangles])
    t1 = time.time()
    n = 0
    for ap in aparcels:
        n += len(ap.hard_parcels)
        for k,tris in ap.hparcels.items():
            #parcel_cc[k] = PCC(tris,triangles_arr)
            tris = np.array(list(tris))
            if len(tris) == 0:
                parcel_cc[k] = tris
            else:
                edges_poly = []
                for ind in tris:
                    edges_poly.append([triangles_arr[ind,0],triangles_arr[ind,1]])
                    edges_poly.append([triangles_arr[ind,0],triangles_arr[ind,2]])
                    edges_poly.append([triangles_arr[ind,1],triangles_arr[ind,2]])

                edges_poly = np.unique(edges_poly,axis=0)

                G = nx.Graph();
                G.add_edges_from(edges_poly);
                
                cc = list(nx.connected_components(G));
                len_cc = [len(comp) for comp in cc];
                len_cc_thr = int(np.max(len_cc))
                regions_cc = list(cc[np.argmax(len_cc)]);
                regions_cc_2 = [list(cc[i]) for i, comp in enumerate(cc) if len_cc[i] >= len_cc_thr]
                #print(len(regions_cc_2))
                #if len(regions_cc_2) > 1:
                #    for n_cc, region_cc in enumerate(regions_cc_2):
                #        ind = [np.where(triangles_arr[tris] == vertex)[0] for vertex in region_cc]
                #        ind = np.unique(np.concatenate(ind))
                #        parcel_cc[k + "_" + str(n_cc)] = tris[ind]
                #else:
                ind = []
                for region_cc in regions_cc:
                    ind.extend(np.where((triangles_arr[tris] == region_cc).any(axis=1))[0])
                ind = np.unique(ind)
                parcel_cc[k] = tris[ind]

    t2 = time.time()
    # print("PCC time: ",t2-t1)
    print("Total hard parcels:",n)
    return parcel_cc

def get_PCC_first(aparcels,triangles):
    parcel_cc = {}
    triangles_arr = np.asarray([[tri.v1.index,tri.v2.index,tri.v3.index] for tri in triangles])
    t1 = time.time()
    n = 0
    for ap in aparcels:
        n += len(ap.sub_parcels)
        for ii, sp in ap.sub_parcels.items():
            tris = []
            for tri in sp.triangles:
                tris.append(tri.index)
            #parcel_cc[k] = PCC(tris,triangles_arr)
            #tris = np.array(list(tris))
            k = sp.label
            if len(tris) == 0:
                parcel_cc[k] = tris
            else:
                edges_poly = []
                for ind in tris:
                    edges_poly.append([triangles_arr[ind,0],triangles_arr[ind,1]])
                    edges_poly.append([triangles_arr[ind,0],triangles_arr[ind,2]])
                    edges_poly.append([triangles_arr[ind,1],triangles_arr[ind,2]])

                edges_poly = np.unique(edges_poly,axis=0)

                G = nx.Graph();
                G.add_edges_from(edges_poly);
                
                cc = list(nx.connected_components(G));
                len_cc = [len(comp) for comp in cc];
                len_cc_thr = int(np.max(len_cc))
                regions_cc = list(cc[np.argmax(len_cc)]);
                regions_cc_2 = [list(cc[i]) for i, comp in enumerate(cc) if len_cc[i] >= len_cc_thr]
                #print(len(regions_cc_2))
                #if len(regions_cc_2) > 1:
                #    for n_cc, region_cc in enumerate(regions_cc_2):
                #        ind = [np.where(triangles_arr[tris] == vertex)[0] for vertex in region_cc]
                #        ind = np.unique(np.concatenate(ind))
                #        parcel_cc[k + "_" + str(n_cc)] = tris[ind]
                #else:
                ind = []
                for region_cc in regions_cc:
                    ind.extend(np.where((triangles_arr[tris] == region_cc).any(axis=1))[0])
                #ind = np.unique(ind)
                parcel_cc[k] = tris[ind]

    t2 = time.time()
    # print("PCC time: ",t2-t1)
    print("Total hard parcels:",n)
    return parcel_cc

def PCC(Tri,triangles):
    Tri = np.array(list(Tri))
    if len(Tri) == 0:
        return Tri
    edges_poly = []
    for ind in Tri:
        edges_poly.append([triangles[ind,0],triangles[ind,1]])
        edges_poly.append([triangles[ind,0],triangles[ind,2]])
        edges_poly.append([triangles[ind,1],triangles[ind,2]])

    edges_poly = np.unique(edges_poly,axis=0)

    G = nx.Graph();
    G.add_edges_from(edges_poly);
    
    cc = list(nx.connected_components(G));
    len_cc = [len(comp) for comp in cc];
    regions_cc = list(cc[np.argmax(len_cc)]);
    
    ind = [np.where(triangles[Tri]==region_cc)[0] for region_cc in regions_cc];
    print(regions_cc)
    ind = np.unique(np.concatenate(ind));
    return Tri[ind]

def main():
    sys.setrecursionlimit(1750)
    parser = argparse.ArgumentParser(description='Create parcel of multiple subjects')
    parser.add_argument('--Intersection-dir',type= str,help='Input intersection directory')
    parser.add_argument('--LVtk-file', type=str, help='Input file with the vtk')
    parser.add_argument('--RVtk-file', type=str, help='Input file with the vtk')
    parser.add_argument('--Lvlabels-file',type= str,help='Input file with the vertex labels')
    parser.add_argument('--Rvlabels-file',type= str,help='Input file with the vertex labels')
    parser.add_argument('--parcel-names',type= str, help='Input file with the names of the parcels')
    parser.add_argument('--output-dir', type=str, help='Output directory')
    parser.add_argument('--traceability',type= str, default='y', help='Write y, to obtain the traceability of the parcels')
    parser.add_argument('--size-thr', type=float, default='0.1',help='Size to delete small parcels')
    parser.add_argument('--dc-thr', type=float, default='0.2',help='Less probable triangles in a parcel (probability)')
    parser.add_argument('--idc', type=float, default='0.3',help='Percent of common triangles in the intersection of two density centers')
    parser.add_argument('--ero', type=int, default='1',help='Erosion threshold')
    parser.add_argument('--dil', type=int, default='4',help='Dilation threshold')
    args = parser.parse_args()
    start = time.time()
    atlas_path,trac_path,cc_path,hp_path,fp_path,ps_path = IO.create_atlas_dirs(args.output_dir,args.traceability)

    trac = args.traceability.lower()
    t1 = time.time()
    Lparcel_names, Lanatomic_parcels = IO.read_parcel_names(args.parcel_names)
    Rparcel_names, Ranatomic_parcels = IO.read_parcel_names(args.parcel_names)
    Lvertex_labels = IO.read_vertex_labels(args.Lvlabels_file) 
    Rvertex_labels = IO.read_vertex_labels(args.Rvlabels_file)

    Ltriangles = IO.read_mesh_obj(args.LVtk_file,Lvertex_labels)
    Ltriangles =  label_triangles(Ltriangles)  
    Rtriangles = IO.read_mesh_obj(args.RVtk_file, Rvertex_labels)
    Rtriangles = label_triangles(Rtriangles)

    print("Obtaining preliminary subparcels")
    Lanatomic_parcels, Lparcel_names = IO.preliminary_subparcels(args.Intersection_dir, Lparcel_names,Ltriangles,Lanatomic_parcels,'l') 
    Ranatomic_parcels, Rparcel_names = IO.preliminary_subparcels(args.Intersection_dir, Rparcel_names, Rtriangles,Ranatomic_parcels, 'r')
    t2 = time.time()
    print("Time for IO operations: ",t2-t1)
    idc = args.idc 
    dc_thr = args.dc_thr 
    size_thr = args.size_thr 
    if trac == "y":
        for aparcel in Lanatomic_parcels:
            recalc_probability(aparcel)
        for aparcel in Ranatomic_parcels:
            recalc_probability(aparcel)
        IO.write_atlas(Lanatomic_parcels, Lparcel_names,Ltriangles, trac_path,True,"L")
        IO.write_atlas(Ranatomic_parcels, Rparcel_names,Rtriangles, trac_path,True,"R")
    IO.write_preliminary_subparcels(Lanatomic_parcels,ps_path,"left",trac_path,Lparcel_names)
    IO.write_preliminary_subparcels(Ranatomic_parcels,ps_path,"right",trac_path,Rparcel_names)
    
    t1 = time.time()

    print("Processing parcels")
    Lanatomic_parcels, Lparcel_names = processing_parcels(Lanatomic_parcels,idc,dc_thr,size_thr,Lparcel_names,trac,trac_path,"L")
    Ranatomic_parcels, Rparcel_names = processing_parcels(Ranatomic_parcels,idc,dc_thr,size_thr,Rparcel_names,trac,trac_path,"R")
    IO.write_parcels_fussed(Lanatomic_parcels,fp_path,"left")
    IO.write_parcels_fussed(Ranatomic_parcels,fp_path,"right")
    
    # Count and print the number of non-zero processed sub-parcels
    #L_non_zero_processed_sub_parcels, L_processed_stats = count_non_zero_processed_sub_parcels(Lanatomic_parcels)
    #R_non_zero_processed_sub_parcels, R_processed_stats = count_non_zero_processed_sub_parcels(Ranatomic_parcels)
    #print(f"Non-zero processed sub-parcels (left hemisphere): {L_non_zero_processed_sub_parcels}")
    #print(f"Non-zero processed sub-parcels (right hemisphere): {R_non_zero_processed_sub_parcels}")
    #plot_parcel_distribution(L_processed_stats, R_processed_stats, 'Distribución de tamaños de sub-parcelas procesadas')

    print("Obtaining hard parcels")
    Lhard_parcels = get_hard_parcels(Lanatomic_parcels,Lparcel_names,trac,trac_path,"L")
    Rhard_parcels = get_hard_parcels(Ranatomic_parcels,Rparcel_names,trac,trac_path,"R")
    IO.write_hparcels_triangles(Lhard_parcels,hp_path,"left")
    IO.write_hparcels_triangles(Rhard_parcels,hp_path,"right")

    # Count and print the number of non-zero hard parcels
    #L_non_zero_hard_parcels, L_hard_stats = count_non_zero_hard_parcels(Lhard_parcels)
    #R_non_zero_hard_parcels, R_hard_stats = count_non_zero_hard_parcels(Rhard_parcels)
    #print(f"Non-zero hard parcels (left hemisphere): {L_non_zero_hard_parcels}")
    #print(f"Non-zero hard parcels (right hemisphere): {R_non_zero_hard_parcels}")
    #plot_parcel_distribution(L_hard_stats, R_hard_stats, 'Distribución de tamaños de parcelas duras')

    print("Obtaining principal connected components")
    Lparcel_cc = get_PCC(Lhard_parcels,Ltriangles)
    Rparcel_cc = get_PCC(Rhard_parcels,Rtriangles)
    IO.write_parcels_cc(Lparcel_cc,cc_path,"left")
    IO.write_parcels_cc(Rparcel_cc,cc_path,"right")

# REVERSE ORDER
    
    print("Obtaining principal connected components")
    Lparcel_cc_1 = get_PCC_first(Lanatomic_parcels, Ltriangles)
    Rparcel_cc_1 = get_PCC_first(Ranatomic_parcels, Rtriangles)
    IO.write_parcels_cc(Lparcel_cc_1,cc_path,"left")
    IO.write_parcels_cc(Rparcel_cc_1,cc_path,"right")

    print("Obtaining hard parcels")
    Lhard_parcels_1 = get_hard_parcels(Lparcel_cc_1, Lparcel_names, trac,trac_path, "L")
    Rhard_parcels_1 = get_hard_parcels(Rparcel_cc_1, Rparcel_names, trac,trac_path, "R")
    IO.write_hparcels_triangles(Lhard_parcels_1,hp_path,"left")
    IO.write_hparcels_triangles(Rhard_parcels_1,hp_path,"right")

    t2 = time.time()
    print("Time to process the atlas: ", t2-t1)

    IO.write_atlas(Lhard_parcels,Lparcel_names,Ltriangles,atlas_path,False,"L")
    IO.write_atlas(Rhard_parcels,Rparcel_names,Rtriangles,atlas_path,False,"R")

    Lparcelcc_path = cc_path + "/left/"
    Rparcelcc_path = cc_path + "/right/"
    Lhemi_path = args.LVtk_file
    Rhemi_path = args.RVtk_file

    Lfinal_path = args.output_dir + '/final_parcels/left/'
    Rfinal_path = args.output_dir + '/final_parcels/right/'
    
    if not os.path.exists(Lfinal_path):
        os.makedirs(Lfinal_path)
    
    if not os.path.exists(Rfinal_path):
        os.makedirs(Rfinal_path)
    print("Morphologic opening")
    sproc.call(['make']);
    sproc.call(['./main', Lhemi_path, Rhemi_path, str(args.ero), str(args.dil),  Lparcelcc_path, Rparcelcc_path, Lfinal_path, Rfinal_path]);

    finish = time.time()
    print("Parcellation finished")
    print("Total time: ", finish-start)

if __name__ == '__main__':
    main()