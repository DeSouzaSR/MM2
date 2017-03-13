#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
Mercury data

This program provides the Mercury data for the simulation
Author: Sandro Ricardo De Souza: sandro.fisica@gmail.com 
"""

# Import modules
import numpy as np
import pandas as pd
import oe2pv
import math

# Name for each Mercury's cadidates varying the semi-axis
sufix_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

# Numbers of the Mercury's candidates varying the angles
candidates_per_dist = 100

# Conic section is ellipse (see Swift documentation)
ialpha = -1

# Gravitational factor of the Sun
gm =  2.959139768995959e-04

# Define semi-axis
mercury_distances = np.arange(0.05, 0.55, 0.05)
a = np.repeat(mercury_distances, candidates_per_dist)

# Define column Mercury Name
mercury_name = []

for char in sufix_list:
    for number in range(candidates_per_dist):
        name = 'mercury' + char + str(number)
        mercury_name.append(name)

mercury_name = pd.Series(mercury_name)

# Define e, i
low_e = 0
high_e = 0.05 

low_i = 0
high_i = 0.05

numbers_mercurys = len(sufix_list) * candidates_per_dist

e = pd.Series(np.random.uniform(low_e, high_e, numbers_mercurys))
i = pd.Series(np.random.uniform(low_i, high_i, numbers_mercurys))

# Define capom omega e M
capom = np.random.uniform(0, 360, numbers_mercurys)
omega = np.random.uniform(0, 360, numbers_mercurys)
M = np.random.uniform(0, 360, numbers_mercurys)

# Gerando o Data Frame inicial
mercury = pd.DataFrame({'mercurys': mercury_name, 'a': a, 'e':e, \
	'i':i, 'capom':capom, 'omega':omega, 'M':M})
mercury = mercury.set_index('mercurys')


# Including mass, radio and mass_grav (equals to the Earth)
mass = 5.972300e+24
mercury['mass'] = np.repeat(mass, numbers_mercurys)
radio = 6378.137
mercury['radio'] = np.repeat(radio, numbers_mercurys)
mass_grav = 8.887539e-10
mercury['mass_grav'] = np.repeat(mass_grav, numbers_mercurys) 

# Including period for each mercury
def periodKepler(semi_axis, M_planet):
    """
    Calculate the period using Kepler's third law
    Input
        semi_axis: semi-axis [au]
        M_planet: mass of the planet [kg]
    Output
        period [days]
    """
    M_sol_kg = 1.9891e30
    M_sol_G = 2.959139768995959e-04
    M_grav = M_sol_G * M_planet / M_sol_kg
    period = np.sqrt(((2 * np.pi)**2 * semi_axis**3) / (M_sol_G + M_grav))
    return(period)
    
period = periodKepler(mercury.a, mercury.mass)

mercury['period'] = period

# Determine position and velocity
x = np.zeros(numbers_mercurys)
y = np.zeros(numbers_mercurys)
z = np.zeros(numbers_mercurys)
vx = np.zeros(numbers_mercurys)
vy = np.zeros(numbers_mercurys)
vz = np.zeros(numbers_mercurys)

for j in range(len(mercury)):
        x[j], y[j], z[j], vx[j], vy[j], vz[j] = oe2pv.orbel_el2xv(gm,ialpha,\
                                            a[j],e[j],math.radians(i[j]),\
                                            math.radians(capom[j]),\
                                            math.radians(omega[j]),M[j])
                                            

# Create colums x, y, v, vx, vy and vz in data frame
mercury['x'] = x
mercury['y'] = y
mercury['z'] = z
mercury['vx'] = vx
mercury['vy'] = vy
mercury['vz'] = vz

# Create csv files from Mercury data
mercury.to_csv('Planets/mercury.csv')
