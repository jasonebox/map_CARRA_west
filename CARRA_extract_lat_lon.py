#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 08:08:56 2020

@author: Jason Box, GEUS, jeb@geus.dk

Output monthly ERA5 temperatures for regional polygons drawn unambiguously in photoshop with ocean buffer but obtaining land using ERA5 mask data

Lambert_Conformal()
    grid_mapping_name: lambert_conformal_conic
    standard_parallel: 72.0
    longitude_of_central_meridian: -36.0
    latitude_of_projection_origin: 72.0
    earth_radius: 6367470.0
    false_easting: 1334211.3405653758
    false_northing: 1584010.8994621644
    longitudeOfFirstGridPointInDegrees: 302.903
    latitudeOfFirstGridPointInDegrees: 55.81

"""
ly='x'

import matplotlib.pyplot as plt
from netCDF4 import Dataset
import os
import numpy as np
from osgeo import gdal, gdalconst
from netCDF4 import Dataset as NetCDFFile 
# import pandas as pd

ni=1269
nj=1069

# fn='/Users/jason/Dropbox/CARRA/ancil/lat_1269x1069.numpy.bin'
# lat=np.fromfile(fn, dtype=float, count=-1, sep='', offset=0)

# fn='/Users/jason/Dropbox/CARRA/ancil/lon_1269x1069.numpy.bin'
# lon=np.fromfile(fn, dtype=float, count=-1, sep='', offset=0)
AW=0
path='/Users/jason/Dropbox/CARRA/prog/map_CARRA_west/'
if AW:path='/Users/jason/Dropbox/CARRA/prog/map_CARRA_west/'
os.chdir(path)

du=1

fn='/Users/jason/0_dat/CARRA/CARRA-West_sample_with_long_and_lat_coordinates.nc'
nc = NetCDFFile(fn) # note this file is 2.5 degree, so low resolution data
time = nc.variables['time'][:]
n=len(time)

x = nc.variables['x'][:]
y = nc.variables['y'][:]

lat = nc.variables['latitude'][:,:]
lon = nc.variables['longitude'][:,:]
lat=np.asarray(lat)
lon=np.asarray(lon)
x=np.asarray(x)
y=np.asarray(y)
print(len(lat),len(lon))

plt.imshow(lat)
plt.imshow(lon)
plt.colorbar()
fh = Dataset(fn, mode='r')
print(fh.variables)
#%%
wo=1
if wo:
    # ofile='/Users/jason/Dropbox/CARRA/prog/map_CARRA_west/ancil/2.5km_CARRA_west_lat_1269x1069.npy'
    # lat.astype('float32').tofile(ofile)
    # ofile='/Users/jason/Dropbox/CARRA/prog/map_CARRA_west/ancil/2.5km_CARRA_west_lon_1269x1069.npy'
    # lon.astype('float32').tofile(ofile)
    ofile='/Users/jason/Dropbox/CARRA/prog/map_CARRA_west/ancil/2.5km_CARRA_west_x_1069.npy'
    x.astype('float32').tofile(ofile)        
    ofile='/Users/jason/Dropbox/CARRA/prog/map_CARRA_west/ancil/2.5km_CARRA_west_y_1269.npy'
    y.astype('float32').tofile(ofile)   


