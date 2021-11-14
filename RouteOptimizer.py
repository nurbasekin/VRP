# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 09:55:14 2021

@author: ekin.nurbas
"""



import json
import cvrp

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
        
        
    def optimizer(self):
        
        V = []
        for job in self.jobs:
            V.append(job['location_index'])
        
        S = []
        for vehicle in self.vehicles:  
            S.append(vehicle['start_index'])
            
        C = self.C
        
        optimum_route,minimum_total_cost,minimum_route_cost = cvrp.vrp(V,len(S),C,S)
        # optimum_route.reverse()
        for i in range(len(self.vehicles)):
            optimum_route[i].reverse()
            self.vehicles[i]['route'] = optimum_route[i]
            self.vehicles[i]['jobs'] = [j['id'] for j in self.jobs for v in optimum_route[i] if j['location_index'] == v]
            self.vehicles[i]['cost'] = minimum_route_cost[i]
        
        
    def run(self):
        self.read_json()
        self.optimizer()
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
            
        
    

RO = RouteOptimizer('my_test.json')
RO.run()