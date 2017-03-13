#!/usr/bin/env python
#-*- coding:utf-8 -*-

""" MM
Multiples Mercury
This project uses the Swift integrator to simulate multiple Mercury-type planets.
Author: Sandro Ricardo De Souza: sandro.fisica@gmail.com """

# Import modules
import os
import glob
import numpy as np
import shutil
import pandas as pd

# Define names
# Name of the simulation
name_simulation = 'Mercury'

# Directory path
directory_path = "Input_data/"

# Name for each Mercury's cadidates varying the semi-axis
sufix_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

# Numbers of the Mercury's candidates varying the angles
number_canditates = 100

# Create director for data frames
try:
    os.stat('Planets')
except:
    os.mkdir('Planets')

# Read data from planets (8 planets)
planets = pd.read_csv('Planets/planets.csv', index_col='planets_name')


# Create directory of the input files and pl files
# For each mercury directory, to create subdirectory with a Mercury variation

def pl():
    preamble = """8
2.959139768995959E-04
0.0 0.0 0.0
0.0 0.0 0.0
 """ 
    with open('pl.in', 'w+') as f:
        f.write(preamble)
        for j in planets.index:
            
            # Create strings
            mass = str(planets.mass_grav[j]) + '\n'
            p_lines = str(planets.x[j]) + ' ' + str(planets.y[j]) + ' ' + str(planets.z[j]) + '\n'
            v_lines = str(planets.vx[j]) + ' ' + str(planets.vy[j]) + ' ' + str(planets.vz[j]) + '\n'
            
            # Write out 
            f.write(mass)
            f.write(p_lines)
            f.write(v_lines)

if os.path.exists(directory_path):
    shutil.rmtree(directory_path)
    os.mkdir(directory_path)
else:
    os.mkdir(directory_path)
        
os.chdir(directory_path)

for char in sufix_list:
    os.makedirs(name_simulation + char)
    os.chdir(name_simulation + char)
    for i in range(number_canditates):
        os.mkdir(name_simulation + char + str(i))
        os.chdir(name_simulation + char + str(i))
        pl()
        os.chdir('../')
    os.chdir('../')
os.chdir('../')

# Finish
print('Finish!')

