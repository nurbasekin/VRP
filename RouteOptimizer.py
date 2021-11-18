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
    #Base class for Route Optimization Algorithms
    
    def __init__(self,input_json_file,output_json_file,capacitated):
        self.input_json_file = input_json_file
        self.output_json_file = output_json_file
        self.capacitated = capacitated
    
    def read_json(self):
        #Reading input json file
        f = open(self.input_json_file,)
        data = json.load(f)
        f.close()
        
        # Assigning values to variables
        self.vehicles = data['vehicles']
        self.jobs = data['jobs']
        self.C = data['matrix']
        
               
    def run(self):
        # Main methos whic reads the input file, run the optimization algoritmhs, print results and write result to output file
        
        self.read_json() # Reading input json file
        
        t_start = time.time_ns()
        self.optimizer() # Caling route optimizer algorithms
        t_end = time.time_ns()
        t_total = (t_end - t_start) 
        print("Execution Time %f milliseconds" % (t_total / 1000000) )
        
        self.print_results() #printing results
        self.write_json() #writing results to output json file
        
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
        # Writing results to output json file
        f = open(self.output_json_file, 'w')
        json.dump(self.result, f,indent = 4, sort_keys=True)
        f.close()


class BruteForce(RouteOptimizer):
    
    #BruteForce Algorithm Class 
    def __init__(self,input_json_file,output_json_file,capacitated):
        super().__init__(input_json_file,output_json_file,capacitated)
        
        
        
    def optimizer(self):
        
        # Assining necessery variables
        
        V = [] # List of vertices
        D = list(np.zeros([len(self.C)])) # Amount of delveries
        for job in self.jobs:
            V.append(job['location_index'])
            D[job['location_index']] = job['delivery'][0]
        
        S = [] # Start index of the vehicles
        L = [] # Capacity limits of the vehicles
        for vehicle in self.vehicles:
            S.append(vehicle['start_index'])
            L.append(vehicle['capacity'][0])
            
        C = self.C # Cost Matrix
        
        # Calling bfsolver() 
        optimum_route,minimum_total_cost,minimum_route_cost = bf.bfsolver(V,len(S),C,S,D,L,self.capacitated)
        
        # Assining optimum routes to vehicles
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
    #Genetic Algorithm Class
    
    def __init__(self,input_json_file,output_json_file,K,T,prob,capacitated):
        super().__init__(input_json_file,output_json_file,capacitated)
        self.K = K
        self.T = T
        self.prob = prob
    
        
        
    def optimizer(self):
        
       # Assining necessery variables
        
        V = [] # List of vertices
        D = list(np.zeros([len(self.C)])) # Amount of delveries
        for job in self.jobs:
            V.append(job['location_index'])
            D[job['location_index']] = job['delivery'][0]
        
        S = [] # Start index of the vehicles
        L = [] # Capacity limits of the vehicles
        for vehicle in self.vehicles:
            S.append(vehicle['start_index'])
            L.append(vehicle['capacity'][0])
            
        C = self.C # Cost Matrix
        
        # Calling gasolver() 
        optimum_route,minimum_total_cost,minimum_route_cost = ga.gasolver(V,C,S,D,L,len(S),self.K,self.T,self.prob,self.capacitated)
        
        routes = {}
        total_delivery_duration = 0

        # Assining optimum routes to vehicles
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
        


