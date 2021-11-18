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
    
    
    c_min = sys.maxsize * len(V) # Minimum cost
    opt_route = [] # Optimimum routes
    
    
    if k == 1: # If there is no vertices left (last visited vertex)
        V_n = V[0]
        c_min = C[V_p][V_n];
        
        # Returning back to depot case 
        #(if the problem is capacitated cost of the route between last visited vertex to depo added to total cost)
        if (capacitated):
            c_min = C[V_p][V_n] + C[V_n][0]
        else:
            c_min = C[V_p][V_n]
        
        # Appending last vertex to route
        route = [*V]
        
        # returning minimum cost and optimal route
        return route, c_min 
        
        
    # Iterate for each V_n in V to find the optimal route
    for V_n in V:
        
        c_n = C[V_p][V_n] # Cost between previous vertex and current vertex
        V_r = [i for idx,i in enumerate(V) if not i == V_n] # Remaining vertices
        # Re-call itself with updated vertex list and previous vertex 
        # Previous vertex <- Current vertex
        route, c_r = calculate_shortest_route(V_r,C,k-1,K,V_n,capacitated) 
        c_t = c_n + c_r # Add the cost of remaining route
        
        
        # Chech if the new cost is less than current minimum cost
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
    
    
    c_min = sys.maxsize # Minimum total cost
    opt_route = [] # Optimimum routes 
    minimum_route_cost = [] # Minimum cost list for vehicle routes
    
    if n == 1: # If there is only one vehicle left (no other options, remaining vertices must be visited by the last vehicle)
        
        # Calculate optimum route for the last vehicle
        route_n , c_min = calculate_shortest_route(V,C,len(V),len(V),S[n-1],capacitated)
        
        # if capacity for the current vehicle is not enough for the assigned jobs assign maxint() value as cost 
        if capacitated and sum([D[i] for i in route_n]) > L[n-1]:
            c_min = sys.maxsize
        
        # Appending the last vehicles route and costs
        minimum_route_cost.append(c_min)
        opt_route.append(route_n)       
        return opt_route , c_min, minimum_route_cost
    else:
        
        # Calculate Combinations of V 
        sel_comb = list(map(list, itertools.product([0, 1], repeat=len(V))))
        
        # For each combination calcuate cost
        for sel in sel_comb:
            
            # Assining vertex list for current vehicle
            V_n = [i for idx,i in enumerate(V) if sel[idx]]
            
            # Calculating optimum route for current vehicle
            route_n,c_n = calculate_shortest_route(V_n,C,len(V_n),len(V_n),S[n-1],capacitated)
            
            # Update remainin vertex list for remaining vehicles
            V_r = [i for idx,i in enumerate(V) if not sel[idx]]
            
            # Calculate optimum route for remainin vehicles by updating total number of vehicles and vertex list
            route_r , c_r, min_route_cost_r = bfsolver(V_r,n-1,C,S,D,L,capacitated)
            
            # Adding remaning routes cost to current route's cost
            c_t = c_n + c_r
            
            # if capacity for the current vehicle is not enough for the assigned jobs assign maxint() value as cost 
            if capacitated and sum([D[i] for i in route_n]) > L[n-1]:
                c_t = sys.maxsize
                     
            # Chech if the new cost is less than current minimum cost
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

      