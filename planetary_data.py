#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
Planetary data
This program provides the planetary data for the simulation
Author: Sandro Ricardo De Souza: sandro.fisica@gmail.com
"""

# Import modules
import numpy as np
import pandas as pd
import math
import oe2pv
import os 

# Create planets data (J2000)
# 
# Data from https://nssdc.gsfc.nasa.gov/planetary/
# Data sequence: 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus',
#  'Neptune'.

# Planet's names
planets_name = pd.Series(['Venus', 'Earth', 'Mars', 'Jupiter', \
	'Saturn', 'Uranus', 'Neptune'])

# Semi-axis [au]
a = pd.Series([0.72333199, 1.00000011, 1.52366231, 5.20336301, \
	9.53707032, 19.19126393, 30.06896348])

# Eccentricity
e =pd.Series([0.00677323, 0.01671022, 0.09341233, 0.04839266, \
	0.05415060, 0.04716771, 0.00858587])

# Inclination [deg]
i = pd.Series([3.39471, 0.00005, 1.85061, 1.30530, 2.48446, 0.76986,\
	1.76917])

# Long. of ascending node [deg]
capom = pd.Series([76.68069, -11.26064, 49.57854, 100.55615, \
	113.71504, 74.22988, 131.72169])

# arg. of peri. [deg]
omega = pd.Series([131.53298, 102.94719, 336.04084, 14.75385, \
	92.43194, 170.96424, 44.97135])

# Mean anomaly [deg]
M = pd.Series([181.97973, 100.46435, 355.45332, 34.40438, 49.94432, \
	313.23218, 304.88003])

# Mass [kg]
mass = pd.Series([4.8675, 5.9723, 0.64171, 1898.19, 568.34, 86.813, \
	102.413]) * 1e24

# Equatorial radius [km]
radio = pd.Series([6051.8, 6378.137, 3396.2, 71492, 60268, 25559,\
	24764])

# Period [days]
period = pd.Series([224.701, 365.256, 686.980, 4332.589, 10759.22, \
	30685.4, 60189])


# Create a data frame from data series
planets = pd.DataFrame({'planets_name': planets_name, 'a': a, 'e': e, \
	'i': i, 'capom': capom, 'omega': omega, 'M': M, 'mass': mass, \
	'radio': radio, 'period': period})
	
# Make planets_name index
planets = planets.set_index('planets_name')

# Changing the order of the columns.
planets = planets[['a', 'e', 'i', 'capom', 'omega', 'M', 'mass', \
	'radio', 'period']]
	
#Create new column, considering G = 1
# Mass of the Sum, in kg
mass_sun_kg = 1988500e24

# Mass of the Sun, with G = 1
mass_sun_grav = 2.959139768995959e-04

# Conic section is ellipse
ialpha = -1

# Gravitational factor of the Sun
gm =  2.959139768995959e-04

# Create mass_grav column
planets['mass_grav'] = planets.mass * mass_sun_grav / mass_sun_kg

# Create gmpl
planets['gmpl'] = gm + planets.mass_grav

# Creating variables to use the "orbel" function
gm = planets['gmpl']
a = planets['a']
e = planets['e']
inc = planets['i']
capom = planets['capom']
omega = planets['omega']
capm = planets['M']
P = planets['period']
rpl = planets['radio']
ialpha = -1

# Create position and velocity columns
#
# The module eo2pv.so, constructed from the Swift conversion subroutine,
# will be used.

len_planets = len(planets)

x = np.zeros(len_planets)
y = np.zeros(len_planets)
z = np.zeros(len_planets)
vx = np.zeros(len_planets)
vy = np.zeros(len_planets)
vz = np.zeros(len_planets)

for j in range(len(planets)):
    x[j], y[j], z[j], vx[j], vy[j], vz[j] = oe2pv.orbel_el2xv(gm[j],\
											ialpha, a[j],e[j],\
											math.radians(inc[j]),\
                                            math.radians(capom[j]),\
                                            math.radians(omega[j]),\
                                            capm[j])

# Create colums x, y, v, vx, vy and vz
planets['x'] = x
planets['y'] = y
planets['z'] = z
planets['vx'] = vx
planets['vy'] = vy
planets['vz'] = vz

#if os.mkdir('Planets'):
	#planets.to_csv('Planets/planets.csv')
#else:
	#os.chdir('Planets')
	#planets.to_csv('Planets/planets.csv')

# Create csv files from planetary data
planets.to_csv('Planets/planets.csv')
