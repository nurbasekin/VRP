# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 10:44:48 2021

@author: ekin.nurbas
"""

from RouteOptimizer import BruteForce
from RouteOptimizer  import GeneticAlgortihm

input_json_file = "input_case_5.json"

print("Brute-Force Solution (Not Capacitated): ")
BF = BruteForce(input_json_file,'output_bf.json',False)
BF.run()

print("Brute-Force Solution: (Capacitated)")
BF = BruteForce(input_json_file,'output_bf_capacitated.json',True)
BF.run()

print("Genetic Algorithm Solution: (Not Capacitated)")
GA = GeneticAlgortihm(input_json_file,'output_ga.json',2000,False)
GA.run()

print("Genetic Algorithm Solution: (Capacitated)")
GA = GeneticAlgortihm(input_json_file,'output_ga_capacitated.json',2000,True)
GA.run()



