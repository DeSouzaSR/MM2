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
import yaml
import subprocess

def preamble():
	preamble = '8\n2.959139768995959E-04\n0.0 0.0 0.0\n0.0 0.0 0.0\n'
	with open('pl.in', 'a') as f:
		f.write(preamble)

def mercury_in(j):
	with open('pl.in', 'a') as f:
		mass = str(mercury.mass_grav[j]) + '\n'
		p_lines = str(mercury.x[j]) + ' ' + str(mercury.y[j]) + \
			' ' + str(mercury.z[j]) + '\n'
		v_lines = str(mercury.vx[j]) + ' ' + str(mercury.vy[j]) + \
			' ' + str(mercury.vz[j]) + '\n'

		# Write out 
		f.write(mass)
		f.write(p_lines)
		f.write(v_lines)

def pl_in():
	with open('pl.in', 'a') as f:
		for j in planets.index:           
			# Create strings
			mass = str(planets.mass_grav[j]) + '\n'
			p_lines = str(planets.x[j]) + ' ' + str(planets.y[j]) + \
				' ' + str(planets.z[j]) + '\n'
			v_lines = str(planets.vx[j]) + ' ' + str(planets.vy[j]) + \
				' ' + str(planets.vz[j]) + '\n'

			# Write out 
			f.write(mass)
			f.write(p_lines)
			f.write(v_lines)
            
        
def pl_three():
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
			preamble()
			mercury_in(name_simulation + char + str(i))
			pl_in()
			os.chdir('../')
		os.chdir('../')
	os.chdir('../')

if __name__ == '__main__':
	
	with open('planets_input_data.yaml', 'r') as yamlfile:
		 input_data = yaml.load(yamlfile)
	
	# Define names
	# Name of the simulation
	name_simulation = input_data['name_simulation']

	# Directory path
	directory_path = input_data['directory_path']

	# Name for each Mercury's cadidates varying the semi-axis
	sufix_list = input_data['sufix_list']

	# Numbers of the Mercury's candidates varying the angles
	number_canditates = input_data['number_canditates']

	# Create director for initial data frames
	try:
		os.stat('Planets')
	except:
		os.mkdir('Planets')
		
	
	# Create planetary data
	subprocess.call(['./planetary_data.py'])
	
	# Create mercury data
	subprocess.call(['./mercury_data.py'])

	# Read data from planets (8 planets)
	planets = pd.read_csv('Planets/planets.csv', \
		index_col='planets_name')
		
	# Read data from planets (8 planets)
	mercury = pd.read_csv('Planets/mercury.csv', index_col='mercurys')

	# Create directory of the input files and pl files
	# For each mercury directory, to create subdirectory with a Mercury variation
	
	pl_three()

	# Finish
	print('Game Over!')

