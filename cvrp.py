# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 13:00:19 2021

@author: ekin.nurbas
"""

import numpy as np
import math as math
import matplotlib.pyplot as plt
import itertools



def calculate_shortest_route(V,C,k,K,V_p):
    
    # V : Set of vertices
    # C : Cost Dictionary i.e. C[i,j] is the cost for V[i] -> V[j]
    # k : Number of remaining vertices
    # K : Total number of vertices
    # V_p: Previous vertex

    c_min = 10e20
    opt_route = []
    
    if k == 1:
        V_n = V[0]
        c_min = C[V_p,V_n];
        route = [*V]
        # print("%d Current Node: %d | Cost :%f | Previous Node: %d"  % (k,V_n,c_min,V_p) )        
        return route, c_min 
        
        
    
    for V_n in V:
        
        if(len(V) == K):
            V_p = 0
            
        c_n = C[V_p,V_n]
        V_r = [i for idx,i in enumerate(V) if not i == V_n]
        route, c_r = calculate_shortest_route(V_r,C,k-1,K,V_n)
        c_t = c_n + c_r
        
        if c_t < c_min:
            c_min = c_t
            opt_route = [*route]
            # opt_route.append(route)
            opt_route.append(V_n)
            
        
        if k == K:
            print("------------------------------------------")
            print("Cost: %f" % c_min)
            print(opt_route)
            print("------------------------------------------")
    return opt_route,c_min
        

def vrp(V,n):
    
    c_min = 100
    opt_route = []
    
    if n == 1:
        c_min = calculate_shortest_route(V)
        print("Number of Vehicles: %d | Cost :%f | Current Route: "  % (n,c_min) +  str(V) )

        opt_route.append(V)        
        return opt_route , c_min
    else:
        
        # Calculate Combinations of V
        sel_comb = list(map(list, itertools.product([0, 1], repeat=len(V))))
        
        # For each combination calcuate cost
        for sel in sel_comb:
            V_n = [i for idx,i in enumerate(V) if sel[idx]]
            c_n = calculate_shortest_route(V_n)
            print("Number of Vehicles: %d | Cost :%f | Current Route: "  % (n,c_n) +  str(V_n) )

            
            V_r = [i for idx,i in enumerate(V) if not sel[idx]]
            route , c_r = vrp(V_r,n-1)

            c_t = c_n + c_r
                    
            if(c_t < c_min):
                c_min = c_t
                opt_route = []
                opt_route.append(route)
                opt_route.append(V_n)

            
            if(n == 3):
                print("----------------------------------------------------")
                print("Optimum Routes:")
                print(opt_route)
                print("Cost: %f" % c_min)
                print("----------------------------------------------------")

                
    
    return opt_route , c_min

       




# Generating Vertices
V  = [0,1,2,3,4]
P =  [(0,0),(3,8),(7,4),(17,45), (9,30)]
E =  [(i,j) for i in V for j in V]
C = {(i,j): math.sqrt(pow(P[i][0] - P[j][0],2) + pow(P[i][1] - P[j][1],2)) for i in V for j in V}
V  = [1,2,3,4]
r, c = vrp(V,3)
print(c)
            