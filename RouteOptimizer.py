# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 09:55:14 2021

@author: ekin.nurbas
"""



import json
import bf
import ga
import time
import numpy as np

class RouteOptimizer:
    
    def __init__(self,input_json_file,output_json_file,capacitated):
        self.input_json_file = input_json_file
        self.output_json_file = output_json_file
        self.capacitated = capacitated
    
    def read_json(self):
        f = open(self.input_json_file,)
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
        self.print_results()
        self.write_json()
        
    def print_results(self):
        print("*****************************************")
        for vehicle in self.vehicles:
            print("Vehicle ID: %d " % vehicle['id'])
            print("Capacity: %d" % vehicle['capacity'][0])
            print("Start Point: %d" % vehicle['start_index'])
            print("Optimum Route: " + str(vehicle['route']))
            print("Jobs: " + str(vehicle['jobs']))
            print("Route Cost: %f" % vehicle['cost'])
            print("---------------------------------------")
    
    def write_json(self):
        with open(self.output_json_file, 'w') as f:
            json.dump(self.result, f,indent = 4, sort_keys=True)
        f.close()


class BruteForce(RouteOptimizer):
    
    def __init__(self,input_json_file,output_json_file,capacitated):
        super().__init__(input_json_file,output_json_file,capacitated)
        
        
        
    def optimizer(self):
        V = []
        D = list(np.zeros([len(self.C)]))
        for job in self.jobs:
            V.append(job['location_index'])
            D[job['location_index']] = job['delivery'][0]
        
        S = []
        L = []
        for vehicle in self.vehicles:
            S.append(vehicle['start_index'])
            L.append(vehicle['capacity'][0])
            
        C = self.C
        
        
        optimum_route,minimum_total_cost,minimum_route_cost = bf.bfsolver(V,len(S),C,S,D,L,self.capacitated)
        
        routes = {}
        total_delivery_duration = 0
        
        for i in range(len(self.vehicles)):
            optimum_route[i].reverse()

            route = {}
            route['jobs'] = [str(j['id'])  for v in optimum_route[i] for j in self.jobs if v == j['location_index']]
            route['delivery_duration'] = minimum_route_cost[i]
            routes[str(self.vehicles[i]['id'])] = route
            total_delivery_duration += minimum_route_cost[i]
            self.vehicles[i]['route'] = optimum_route[i]
            self.vehicles[i]['jobs'] = [j['id']  for v in optimum_route[i] for j in self.jobs if v == j['location_index']]
            self.vehicles[i]['cost'] = minimum_route_cost[i]
        
        self.result = {}
        self.result['total_delivery_duration'] = total_delivery_duration
        self.result['routes'] = routes
        
class GeneticAlgortihm(RouteOptimizer):

    def __init__(self,input_json_file,output_json_file,K,capacitated):
        super().__init__(input_json_file,output_json_file,capacitated)
        self.K = K
    
        
        
    def optimizer(self):
        
        V = []
        D = list(np.zeros([len(self.C)]))
        for job in self.jobs:
            V.append(job['location_index'])
            D[job['location_index']] = job['delivery'][0]
        
        S = []
        L = []
        for vehicle in self.vehicles:  
            S.append(vehicle['start_index'])
            L.append(vehicle['capacity'][0])
            
        C = self.C
        
        optimum_route,minimum_total_cost,minimum_route_cost = ga.gasolver(V,C,S,D,L,len(S),self.K,self.capacitated)
        
        routes = {}
        total_delivery_duration = 0

        for i in range(len(self.vehicles)):
            optimum_route[i].reverse()

            route = {}
            route['jobs'] = [str(j['id'])  for v in optimum_route[i] for j in self.jobs if v == j['location_index']]
            route['delivery_duration'] = minimum_route_cost[i]
            routes[str(self.vehicles[i]['id'])] = route
            total_delivery_duration += minimum_route_cost[i]            
            self.vehicles[i]['route'] = optimum_route[i]
            self.vehicles[i]['jobs'] = [j['id']  for v in optimum_route[i] for j in self.jobs if v == j['location_index']]
            self.vehicles[i]['cost'] = minimum_route_cost[i]
        
        self.result = {}
        self.result['total_delivery_duration'] = total_delivery_duration
        self.result['routes'] = routes
        


