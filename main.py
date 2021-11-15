# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 10:44:48 2021

@author: ekin.nurbas
"""

from RouteOptimizer import BruteForce
from RouteOptimizer  import GeneticAlgortihm

BF = BruteForce('my_test_2.json')
BF.run()


GA = GeneticAlgortihm('my_test_2.json',2000)
GA.run()

