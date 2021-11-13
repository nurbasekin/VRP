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
        
        self.V = []
        for job in data['jobs']:
            self.V.append(job['location_index'])
        
        self.S = []
        for vehicle in data['vehicles']:
            self.S.append(vehicle['start_index'])
            
        self.C = data['matrix']
        
    def optimize(self):
        optimum_route,minimum_cost = cvrp.vrp(self.V,len(self.S),self.C)
        print(optimum_route )
        
    def run(self):
        self.read_json()
        self.optimize()
        
    

RO = RouteOptimizer('my_test.json')
RO.run()