# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 10:44:48 2021

@author: ekin.nurbas
"""



from RouteOptimizer import BruteForce
from RouteOptimizer  import GeneticAlgortihm

# Input File Name

input_json_file = "getir_algo_input.json"

#Brute-Force for VRP (Not Capacitated)
print("Brute-Force Solution (Not Capacitated): ")
#Generating BruteForce object with parameters input_json_file, output file, capacitated = False
BF = BruteForce(input_json_file,'output_bf.json',False)
BF.run() # Runing Brute-Force Algorithm for VRP 

#Brute-Force for VRP (Capacitated)
print("Brute-Force Solution: (Capacitated)")
#Generating BruteForce object with parameters input_json_file, capacitated = True
BF = BruteForce(input_json_file,'output_bf_capacitated.json',True)
BF.run() # Runing Brute-Force VRP algorithm


# Genetic Algorithm for VRP(Not capacitated)
print("Genetic Algorithm Solution: (Not Capacitated)")
#Generating GeneticAlgorithm object with parameters input_json_file, output file,population size,number of iterations capacitated = False
GA = GeneticAlgortihm(input_json_file,'output_ga.json',2000,20,0.1,False)
GA.run() # Runing Genetic Algorithm for VRP 

# Genetic Algorithm for VRP(Capacitated)
print("Genetic Algorithm Solution: (Capacitated)")
#Generating GeneticAlgorithm object with parameters input_json_file, output file,population size,number of iterations capacitated = True
GA = GeneticAlgortihm(input_json_file,'output_ga_capacitated.json',2000,20,0.1,True)
GA.run() # Runing Genetic Algorithm for VRP 

    




