# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 01:02:24 2021

@author: ekin.nurbas
"""

import random
import math
import numpy as np
import json
import matplotlib.pyplot as plt
%matplotlib inline
from itertools import cycle
    


def visualize_results(input_json_file,output_json_file,capacitated):
    
    plt.figure()
    
    f = open(input_json_file,)
    input_data = json.load(f)
    f.close()
    
    vehicles = input_data['vehicles']
    jobs = input_data['jobs']
    positions = input_data['positions']
    
    for v in vehicles:
        p = positions[v['start_index']]
        plt.scatter(p[0],p[1],c = 'r',marker = 'o')
        plt.annotate("Vehicle " + str(v['id']), xy = (p[0]+2,p[1] + 6),color = 'r')
        plt.annotate("Capacity: " + str(v['capacity']), xy = (p[0]+2,p[1]),color = 'r')
        plt.grid()
        
        
    
    for j in jobs:
        p = positions[j['location_index']]
        plt.scatter(p[0],p[1],c = 'k',marker = 's',alpha=(0.3),s = 100)
        plt.annotate("Job " + str([j['id']]), xy = (p[0]+2,p[1]  + 6))
        plt.annotate("Delivery: " + str(j['delivery']), xy = (p[0]+2,p[1]))
        
    p = positions[0]
    plt.scatter(p[0],p[1],c = 'b',marker = 's',alpha=(0.3),s = 150)
    plt.annotate("Depot", xy = (p[0]+2,p[1]  - 6),color = 'b')
    
    
    cycol = cycle('bgrcmk')   
    cylinestyle = cycle(['dashed', 'dashdot', 'dotted']) 
    
    f = open(output_json_file,)
    output_data = json.load(f)
    f.close()
    
    total_distance = output_data['total_delivery_duration']
    plt.title(output_json_file + " Total Cost: " + str(total_distance))  
    color = next(cycol)
    style = next(cylinestyle)
    for i in range(len(vehicles)):
        route = output_data['routes'][str(i+1)]['jobs']
        for j in range(len(route)):
            
            job = jobs[int(route[j])]
            
            if j == 0:
                vehicle = vehicles[i]
                x_0 = positions[vehicle['start_index']][0];
                y_0 = positions[vehicle['start_index']][1];
                
            else:
                x_0 = x_1
                y_0 = y_1
           
            x_1 = positions[job['location_index']][0];
            y_1 = positions[job['location_index']][1];
            x = [x_0,x_1]
            y = [y_0,y_1]
            plt.plot(x,y,c = color,linestyle = style)
            
        if(capacitated and len(route) > 0):
            x_0 = x_1
            y_0 = y_1
            x_1 = positions[0][0]
            y_1 = positions[0][1]
            x = [x_0,x_1]
            y = [y_0,y_1]
            plt.plot(x,y ,c = color,linestyle = style)


input_json_file = "input_case_5.json"
visualize_results(input_json_file,'output_bf.json',False)
visualize_results(input_json_file,'output_bf_capacitated.json',True)
visualize_results(input_json_file,'output_ga.json',False)
visualize_results(input_json_file,'output_ga_capacitated.json',True)