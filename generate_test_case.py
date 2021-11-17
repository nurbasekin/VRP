# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 00:59:47 2021

@author: ekin.nurbas
"""

import random
import math
import numpy as np
import json
import matplotlib.pyplot as plt
%matplotlib inline


V = [0 , 1 , 2, 3 , 4, 5, 6, 7, 8, 9,10,11,12,13,14,15]
P = [(random.randint(-50, 50),random.randint(-50, 50)) for v in V]
# P = [(0, 0),
#   (22, 44),
#   (-31, 50),
#   (16, 4),
#   (16, -48),
#   (-26, 25),
#   (-10, 7),
#   (43, 44),
#   (22, -25),
#   (-12, -36)]

C = [math.sqrt(pow(P[i][0] - P[j][0],2) + pow(P[i][1] - P[j][1],2)) for i in V for j in V]
C = np.reshape(C,(len(P),len(P)))       
V = [1 , 2, 3 , 4, 5, 6, 7, 8, 9]
V = [1 , 2, 3 , 4, 5, 6, 7, 8, 9,10,11,12,13,14,15]
n = 3
m = 3


input_json = {}
vehicles = []
for i in range(n):
    vehicle = {}
    vehicle['id'] = i + 1
    vehicle['start_index'] = V[m+i]
    vehicle['capacity'] = [random.randint(3, 5)]
    vehicles.append(vehicle)
    

jobs = []
for i in range(m):
    job = {}
    job['id'] = i
    job['location_index'] = V[i]
    job['delivery'] = [random.randint(1,2)]
    jobs.append(job)
    

input_json['vehicles'] = vehicles
input_json['jobs'] = jobs
input_json['matrix'] = C.tolist()
input_json['positions'] = P

f = open('input.json', 'w')
json.dump(input_json, f,indent = 4, sort_keys=True)
f.close()
