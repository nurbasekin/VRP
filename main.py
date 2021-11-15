# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 10:44:48 2021

@author: ekin.nurbas
"""

from RouteOptimizer import BruteForce
from RouteOptimizer  import GeneticAlgortihm

print("Brute-Force Solution: ")
BF = BruteForce('my_test_2.json','output_bf.json')
BF.run()


print("Genetic Algorithm Solution: ")
GA = GeneticAlgortihm('my_test_2.json','output_ga.json',2000)
GA.run()

