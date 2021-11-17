# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 13:00:19 2021

@author: ekin.nurbas
"""

import itertools
import sys

def calculate_shortest_route(V,C,k,K,V_p,capacitated):
    
    # V : Set of vertices
    # C : Cost Dictionary i.e. C[i,j] is the cost for V[i] -> V[j]
    # k : Number of remaining vertices
    # K : Total number of vertices
    # V_p: Previous vertex

    c_min = sys.maxsize * len(V)
    opt_route = []
    
    if k == 1:
        V_n = V[0]
        c_min = C[V_p][V_n];
        
        # Returning back to depot case
        if (capacitated):
            c_min = C[V_p][V_n] + C[V_n][0]
        else:
            c_min = C[V_p][V_n]
            
        route = [*V]
        return route, c_min 
        
        
    
    for V_n in V:
        
        c_n = C[V_p][V_n]
        V_r = [i for idx,i in enumerate(V) if not i == V_n]
        route, c_r = calculate_shortest_route(V_r,C,k-1,K,V_n,capacitated)
        c_t = c_n + c_r
        
        if c_t < c_min:
            c_min = c_t
            opt_route = [*route]
            opt_route.append(V_n)
            
    
    return opt_route,c_min
        

def bfsolver(V,n,C,S,D,L,capacitated):
    
    # V: Set of Vertices
    # n: Number of remaning vehicles
    # C: Cost matrix
    # S: Start vertices for each vehicle
    
    
    c_min = sys.maxsize
    opt_route = []
    minimum_route_cost = []
    
    if n == 1:
        route_n , c_min = calculate_shortest_route(V,C,len(V),len(V),S[n-1],capacitated)
        # print("Vehicle: %d | Cost :%f | Set: "  % (n,c_min) +  str(V) + " | Optimal Route: " + str(route_n))
        if capacitated and sum([D[i] for i in route_n]) > L[n-1]:
            c_min = sys.maxsize
                
        minimum_route_cost.append(c_min)
        opt_route.append(route_n)       
        return opt_route , c_min, minimum_route_cost
    else:
        
        # Calculate Combinations of V
        sel_comb = list(map(list, itertools.product([0, 1], repeat=len(V))))
        
        # For each combination calcuate cost
        for sel in sel_comb:
            V_n = [i for idx,i in enumerate(V) if sel[idx]]
            route_n,c_n = calculate_shortest_route(V_n,C,len(V_n),len(V_n),S[n-1],capacitated)
            
            V_r = [i for idx,i in enumerate(V) if not sel[idx]]
            route_r , c_r, min_route_cost_r = bfsolver(V_r,n-1,C,S,D,L,capacitated)

            c_t = c_n + c_r
            
            if capacitated and sum([D[i] for i in route_n]) > L[n-1]:
                c_t = sys.maxsize
                                
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

    
    return opt_route , c_min , minimum_route_cost

      