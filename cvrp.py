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

    c_min = 10e6 * len(V)
    opt_route = []
    
    if k == 1:
        V_n = V[0]
        c_min = C[V_p][V_n];
        
        # Returning back to depot case
        # c_min = C[V_p,V_n] + C[V_n,0]; 
        route = [*V]
        return route, c_min 
        
        
    
    for V_n in V:
        
        # if(len(V) == K):
        #     V_p = 
            
        c_n = C[V_p][V_n]
        V_r = [i for idx,i in enumerate(V) if not i == V_n]
        route, c_r = calculate_shortest_route(V_r,C,k-1,K,V_n)
        c_t = c_n + c_r
        
        if c_t < c_min:
            c_min = c_t
            opt_route = [*route]
            opt_route.append(V_n)
            
        
        # if k == K:
        #     print("------------------------------------------")
        #     print("Cost: %f" % c_min)
        #     print(opt_route)
        #     print("------------------------------------------")
        
    return opt_route,c_min
        

def vrp(V,n,C,S):
    
    # V: Set of Vertices
    # n: Number of remaning vehicles
    # C: Cost matrix
    # S: Start vertices for each vehicle
    
    
    c_min = 10e6
    opt_route = []
    minimum_route_cost = []
    
    if n == 1:
        route_n , c_min = calculate_shortest_route(V,C,len(V),len(V),S[n-1])
        print("Vehicle: %d | Cost :%f | Set: "  % (n,c_min) +  str(V) + " | Optimal Route: " + str(route_n))
        minimum_route_cost.append(c_min)
        opt_route.append(route_n)       
        return opt_route , c_min, minimum_route_cost
    else:
        
        # Calculate Combinations of V
        sel_comb = list(map(list, itertools.product([0, 1], repeat=len(V))))
        
        # For each combination calcuate cost
        for sel in sel_comb:
            V_n = [i for idx,i in enumerate(V) if sel[idx]]
            route_n,c_n = calculate_shortest_route(V_n,C,len(V_n),len(V_n),S[n-1])
            print("Vehicle: %d | Cost :%f | Previous Vertex: %d |Set: "  % (n,c_n,S[n-1]) +  str(V_n) + " | Optimal Route: " + str(route_n))

            
            V_r = [i for idx,i in enumerate(V) if not sel[idx]]
            route_r , c_r, min_route_cost_r = vrp(V_r,n-1,C,S)

            c_t = c_n + c_r
                    
            if(c_t < c_min):
                c_min = c_t
                
                opt_route = []
                for route in route_r:
                    opt_route.append(route)   
                opt_route.append(route_n)
                
                minimum_route_cost = []
                for min_cost in min_route_cost_r:
                    minimum_route_cost.append(min_cost) 
                minimum_route_cost.append(c_n)

            
            if(n == 3):
                print("----------------------------------------------------")
                print("Optimum Routes:")
                print(opt_route)
                print("Cost: %f" % c_min)
                print("----------------------------------------------------")

                
    
    return opt_route , c_min , minimum_route_cost

      