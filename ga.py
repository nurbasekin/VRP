# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 23:38:31 2021

@author: ekin.nurbas
"""
import random

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


def replace(parents,offspring,index):
    parents[index] = offspring
    return parents

def evaluate(parents,V,n):
    
    for p in parents:
        for i in range(1,n+1):
            V_i = [V[j] for j in range(len(p)) if p[j] == i]
            
def ga(V,n,k):
    print("Genetic Algorithm for VRP")
    
    K = 100
    parents = generate(V,n,K)
    
    for iteration in range(100):
        
        r_parents , c_parents = evaluate(parents, V, n)
        p1_index = random.randint(0,len(parents[0]))
        p2_index = random.randint(0,len(parents[0]))
        while p1_index == p2_index:
            p2_index = random.randint(0,len(parents[0]))
        
        offsprings = crossover([parents[p1_index],parents[p1_index]])
        
        

                                    
        
            
    