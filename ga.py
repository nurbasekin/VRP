# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 23:38:31 2021

@author: ekin.nurbas
"""
import random
import math
import numpy as np
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
        


def generate(V,n,K):
    # V : Set of vertices
    # n : number of vehicles
    # K : population size
    
    # Generating random pupulation with size K
    population = []
    for i in range(K):
        p = [random.randint(1, n) for i in range(len(V))]
        population.append(p)
        
    
    return population


def crossover(parents):
    
    # Randomly select two parents
    selected_parents = []
    p1_index = random.randint(0,len(parents[0]))
    selected_parents.append(parents[p1_index])
    p2_index = random.randint(0,len(parents[0]))
    while p1_index == p2_index:
        p2_index = random.randint(0,len(parents[0]))
    selected_parents.append(parents[p2_index])

    # Crossover parents to generate two offsprings
    # Offspring 1 = [P1(1),P2(2),P1(3),...]
    # Offspring 2 = [P2(1),P1(2),P2(3),...]
    offspring = []
    for i in range(2):
        o = []
        for j in range(len(parents[0])):
            o.append(selected_parents[(j+i)%2][j])
        offspring.append(o)
        
    return offspring


def replace(parents,route_parent,cost_parent,cost_total_parent , offspring, route_offspring,cost_offspring, cost_total_offspring, index):
    # Replacing selected parent with offspring
    parents[index] = offspring
    route_parent[index]  = route_offspring
    cost_parent[index]  = cost_offspring
    cost_total_parent[index]  = cost_total_offspring
    return parents,route_parent,cost_parent,cost_total_parent

def mutation(offsprings,n,prob):
    offsprings_ = []
    for o in offsprings:
        if(random.uniform(0,1) < prob):
            random_index = random.randint(0, len(o)-1)
            random_value = random.randint(0, n)
            o[random_index] = random_value
        offsprings_.append(o)
    return offsprings_


def evaluate(parents,V,C,S,D,L,n,capacitated):
    # Evaluating parents costs
    r = []
    c = []
    c_total = []
    for p in parents:
        r_p = []
        c_p = []
        c_total_p = 0;
        for i in range(1,n+1):
            V_i = [V[j] for j in range(len(p)) if p[j] == i]
            r_i,c_i = calculate_shortest_route(V_i,C,len(V_i),len(V_i),S[i-1],capacitated)
            r_p.append(r_i)
            c_p.append(c_i)
            c_total_p += c_i
            
            # if capacity for the current vehicle is not enough for the assigned jobs assign maxint() value as cost 
            if capacitated and sum([D[i] for i in V_i]) > L[i-1]:
                c_total_p = sys.maxsize
                
        r.append(r_p)
        c.append(c_p)
        c_total.append(c_total_p)
        
    return r,c,c_total
            
def gasolver(V,C,S,D,L,n,K,T,prob,capacitated):
    
    # Generating parents
    parents = generate(V,n,K)
    
    # Evaluating parents
    r_parents , c_parents, c_total_parents = evaluate(parents, V, C,S,D,L, n,capacitated)

    # Iterations
    for iteration in range(T):
        
        #Sort parents costs
        sorted_parent_index = np.argsort(c_total_parents)
        
        #Select two parents with highest costs
        eliminated_parent_index = sorted_parent_index[V[len(V)-2:len(V)]]
        
        # Generate offsprings
        offsprings = crossover(parents)
        
        # Apply Mutation
        offsprings = mutation(offsprings, n, prob)
        
        # Evaluating offsprings 
        r_offsprings, c_offsprings,c_total_offsprings = evaluate(offsprings,V,C,S,D,L,n,capacitated)

        # Sort offsprings
        sorted_offspring_index = np.argsort(c_total_offsprings)

        # If offsprings cost < selected parents to be eliminated replace offspring with parent
        for i in range(2):
            offspring_index = sorted_offspring_index[i]
            parent_index = eliminated_parent_index[1-i]
            
            if(c_total_offsprings[offspring_index] < c_total_parents[parent_index]):
                parents,r_parents,c_parents,c_total_parents = replace(parents,r_parents,c_parents,c_total_parents, offsprings[offspring_index],r_offsprings[offspring_index], c_offsprings[offspring_index],c_total_offsprings[offspring_index],parent_index)
        
    
    #Select Minimum 
    sorted_parent_index = np.argsort(c_total_parents)
    min_parent_index = sorted_parent_index[0]
    optimum_route = r_parents[min_parent_index]
    c_min_total = c_total_parents[min_parent_index]
    c_min = c_parents[min_parent_index]
    
    
    return optimum_route , c_min_total, c_min
    

    