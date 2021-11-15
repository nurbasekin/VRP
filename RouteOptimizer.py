# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 09:55:14 2021

@author: ekin.nurbas
"""



import json
import cvrp
import ga
import time

class RouteOptimizer:
    
    def __init__(self,json_file):
        self.json_file = json_file
    
    def read_json(self):
        f = open(self.json_file,)
        data = json.load(f)
        f.close()
        
        
        self.vehicles = data['vehicles']
        self.jobs = data['jobs']
        self.C = data['matrix']
        
        
        
    def run(self):
        self.read_json()
        
        t_start = time.time_ns()
        self.optimizer()
        t_end = time.time_ns()
        t_total = (t_end - t_start) 
        print("Execution Time %f milliseconds" % (t_total / 1000000) )
        self.visualize_graph()
        self.write_json()
        
    def visualize_graph(self):
        for vehicle in self.vehicles:
            print("Vehicle ID: %d " % vehicle['id'])
            print("Start Point: %d" % vehicle['start_index'])
            print("Optimum Route: " + str(vehicle['route']))
            print("Jobs: " + str(vehicle['jobs']))
            print("Total Cost: %f" % vehicle['cost'])
            print("---------------------------------------")
    
    def write_json(self):
        with open('output.json', 'w') as f:
            json.dump(self.vehicles, f)


class BruteForce(RouteOptimizer):
    
    def __init__(self,json_file):
        super().__init__(json_file)
        
        
        
    def optimizer(self):
        V = []
        for job in self.jobs:
            V.append(job['location_index'])
        
        S = []
        for vehicle in self.vehicles:  
            S.append(vehicle['start_index'])
            
        C = self.C
        
        optimum_route,minimum_total_cost,minimum_route_cost = cvrp.vrp(V,len(S),C,S)
        for i in range(len(self.vehicles)):
            optimum_route[i].reverse()
            self.vehicles[i]['route'] = optimum_route[i]
            self.vehicles[i]['jobs'] = [j['id'] for j in self.jobs for v in optimum_route[i] if j['location_index'] == v]
            self.vehicles[i]['cost'] = minimum_route_cost[i]
        
        
class GeneticAlgortihm(RouteOptimizer):

    def __init__(self,json_file,K):
        super().__init__(json_file)
        self.K = K
    
        
        
    def optimizer(self):
        
        V = []
        for job in self.jobs:
            V.append(job['location_index'])
        
        S = []
        for vehicle in self.vehicles:  
            S.append(vehicle['start_index'])
            
        C = self.C
        
        optimum_route,minimum_total_cost,minimum_route_cost = ga.ga(V,C,S,len(S),self.K)
        for i in range(len(self.vehicles)):
            optimum_route[i].reverse()
            self.vehicles[i]['route'] = optimum_route[i]
            self.vehicles[i]['jobs'] = [j['id'] for j in self.jobs for v in optimum_route[i] if j['location_index'] == v]
            self.vehicles[i]['cost'] = minimum_route_cost[i]
        

BF = BruteForce('my_test.json')
BF.run()


GA = GeneticAlgortihm('my_test.json',100)
GA.run()

