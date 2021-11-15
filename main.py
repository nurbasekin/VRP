# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 10:44:48 2021

@author: ekin.nurbas
"""

import RouteOptimizer
import BruteForce
import GeneticAlgortihm

BF = BruteForce('my_test.json')
BF.run()


GA = GeneticAlgortihm('my_test.json',200)
GA.run()

