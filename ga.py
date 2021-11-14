# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 23:38:31 2021

@author: ekin.nurbas
"""
import random
import math
import numpy as np

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
        


def generate(V,n,K):
    # V : Set of vertices
    # n : number of vehicles
    # K : population size
    
    population = []
    for i in range(K):
        p = [random.randint(1, n) for i in range(len(V))]
        population.append(p)
        
    
    return population


def crossover(parents):    
    offspring = []
    for i in range(2):
        o = []
        for j in range(len(parents[0])):
            o.append(parents[(j+i)%2][j])
        offspring.append(o)
        
    return offspring


def replace(parents,route_parent,cost_parent,cost_total_parent , offspring, route_offspring,cost_offspring, cost_total_offspring, index):
    parents[index] = offspring
    route_parent[index]  = route_offspring
    cost_parent[index]  = cost_offspring
    cost_total_parent[index]  = cost_total_offspring
    return parents

def evaluate(parents,V,C,n):
    
    r = []
    c = []
    c_total = []
    for p in parents:
        r_p = []
        c_p = []
        c_total_p = 0;
        for i in range(1,n+1):
            V_i = [V[j] for j in range(len(p)) if p[j] == i]
            r_i,c_i = calculate_shortest_route(V_i,C,len(V_i),len(V_i),0)
            r_p.append(r_i)
            c_p.append(c_i)
            c_total_p += c_i
        r.append(r_p)
        c.append(c_p)
        c_total.append(c_total_p)
        
    return r,c,c_total
            
def ga(V,C,n,K):
    print("Genetic Algorithm for VRP")
    
    parents = generate(V,n,K)
    
    r_parents , c_parents, c_total_parents = evaluate(parents, V, C, n)

    for iteration in range(3):
        
        sorted_parent_index = np.argsort(c_total_parents)
        eliminated_parent_index = sorted_parent_index[V[len(V)-2:len(V)]]
        
        print(parents)
        print(c_total_parents)
        p1_index = random.randint(0,len(parents[0]))
        p2_index = random.randint(0,len(parents[0]))
        while p1_index == p2_index:
            p2_index = random.randint(0,len(parents[0]))
        
        offsprings = crossover([parents[p1_index],parents[p2_index]])
        r_offsprings, c_offsprings,c_total_offsprings = evaluate(offsprings,V,C,n)
        # sorted_offspring_index = np.argsort(c_total_offsprings)
        # offsprings = offsprings[sorted_offspring_index]
        # r_offsprings = r_offsprings[sorted_offspring_index]
        # c_offsprings = c_offsprings[sorted_offspring_index]
        # c_total_offsprings = c_total_offsprings[sorted_offspring_index]

        print(offsprings)
        print(c_total_offsprings)
        
        for i in range(2):
            if(c_total_offsprings[i] < c_total_parents[i]):
                parents = replace(parents,r_parents,c_parents,c_total_parents, offsprings[i],r_offsprings[i], c_offsprings[i],c_total_offsprings[i],eliminated_parent_index[i])
            
        
        
        
V = [0,1,2,3,4]
P = [(0,0),(5,10),(24,78),(44,56),(57,14)]
C = [math.sqrt(pow(P[i][0] - P[j][0],2) + pow(P[i][1] - P[j][1],2)) for i in V for j in V]
C = np.reshape(C,(5,5))       
V = [1,2,3,4]    
ga(V,C,3,5)
    