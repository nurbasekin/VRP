# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 13:00:19 2021

@author: ekin.nurbas
"""

import numpy as np
import math as math
import matplotlib.pyplot as plt
import itertools

# Generating Vertices
V  = [1,2,3,4]

def calculate_shortest_route(V):
    return(1/(sum(V)+1))
#random cost function
    

def vrp(V,n):
    
    c_min = 100
    opt_route = []
    
    if n == 1:
        c_min = calculate_shortest_route(V)
        print("Numer of Vehicles: %d | Cost :%f | Current Route: "  % (n,c_min) +  str(V) )

        opt_route.append(V)        
        return opt_route , c_min
    else:
        
        # Calculate Combinations of V
        sel_comb = list(map(list, itertools.product([0, 1], repeat=len(V))))
        
        # For each combination calcuate cost
        for sel in sel_comb:
            V_n = [i for idx,i in enumerate(V) if sel[idx]]
            c_n = calculate_shortest_route(V_n)
            print("Numer of Vehicles: %d | Cost :%f | Current Route: "  % (n,c_n) +  str(V_n) )

            
            V_r = [i for idx,i in enumerate(V) if not sel[idx]]
            route , c_r = vrp(V_r,n-1)

            c_t = c_n + c_r
                    
            if(c_t < c_min):
                c_min = c_t
                opt_route = []
                opt_route.append(route)
                opt_route.append(V_n)
                #print("Minimum Distance is updated!! -> %f n = :%d" % (c_min, n))
                #print(routes)
            
            if(n == 3):
                print("----------------------------------------------------")
                print("Optimum Routes:")
                print(opt_route)
                print("Cost: %f" % c_min)
                print("----------------------------------------------------")

                
    
    return opt_route , c_min

       

r, c = vrp(V,3)
print(c)
            