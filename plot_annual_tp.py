#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 12:04:02 2021

@author: jeb and AW
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import os
from mpl_toolkits.basemap import Basemap

# CARRA grid
# Lambert_Conformal()
#     grid_mapping_name: lambert_conformal_conic
#     standard_parallel: 72.0
#     longitude_of_central_meridian: -36.0
#     latitude_of_projection_origin: 72.0
#     earth_radius: 6367470.0
#     false_easting: 1334211.3405653758
#     false_northing: 1584010.8994621644
#     longitudeOfFirstGridPointInDegrees: 302.903
#     latitudeOfFirstGridPointInDegrees: 55.81

AW=0
path='/Users/jason/Dropbox/CARRA/prog/map_CARRA_west/'
if AW:path='/Users/jason/Dropbox/CARRA/prog/map_CARRA_west/'
os.chdir(path)

# global plot settings
th=1
font_size=18
plt.rcParams['axes.facecolor'] = 'k'
plt.rcParams['axes.edgecolor'] = 'k'
plt.rcParams["font.size"] = font_size

# for a later version that maps the result
ni=1269
nj=1069

map_version=0 # 0 for simple raster map, 1 for projected map
    
if map_version:
    fn='./ancil/lat_1269x1069.numpy.bin'
    lat=np.fromfile(fn, dtype=float, count=-1, sep='', offset=0)
    # lat=lat.reshape(ni, nj)

    fn='./ancil/lon_1269x1069.numpy.bin'
    lon=np.fromfile(fn, dtype=float, count=-1, sep='', offset=0)
    # lon=lon.reshape(ni, nj)

    # f = plt.figure(figsize=(8,4))
    
    # 57.31100000000001 79.52600000000001
    # -56.76 33.255
    
    # 79.391 57.363
    # -104.62700000000001 -14.544
    
    m = Basemap(llcrnrlon=-55, llcrnrlat=55.8, urcrnrlon=80, urcrnrlat=80, lat_1=72, lat_0=72., lon_0=-36, resolution='l', projection='lcc') # carlos' version
    # m = Basemap(llcrnrlon=-56.76, llcrnrlat=57.363, urcrnrlon=33.255, urcrnrlat=79.526, lat_0=72, lon_0=-36, resolution='l', projection='lcc')
    x, y = m(lat, lon)
    # ------------------------------------------------------------- image map
    # m.fillcontinents(color='coral',lake_color='aqua')
    # draw parallels and meridians.


# read data
year='2016'
fn='./grids_to_map/tp_2.5km_CARRA_'+year+'.npy'
# os.system('ls -lF '+fn)
tot=np.fromfile(fn, dtype=np.float32)#, count=-1, sep='', offset=0)
tot=tot.reshape(ni, nj)

# custom color table
r=[188,108,76,0,      172,92,0,0,      255,255,255,220, 204,172,140,108, 255,255,255,236, 212,188,164,156, 255, 255]
g=[255,255,188,124, 255,255,220,156, 255,188,156,124,  156,124,92,60,   188,140,72,0,    148,124,68,28, 255, 0 ]
b=[255,255,255,255,  172,92,0,0,      172,60,0,0,       156,124,92,60,   220,196,164,0,  255,255,255,196, 0, 255 ]
# ranges=[0,40,80,160,320,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000,2100,2200,2300,2400]
colors = np.array([r, g, b]).T / 255
n_bin = 28
cmap_name = 'my_list'
# Create the colormap
cm = LinearSegmentedColormap.from_list(
    cmap_name, colors, N=n_bin)

# make graphic
ax = plt.subplot(111)
ax.set_title(fn)

if map_version==0:
    pp=plt.imshow(np.rot90(tot.T), interpolation='nearest', origin='lower', cmap=cm) ; plt.axis('off') 

if map_version:
    pp=m.imshow(np.rot90(tot.T), cmap = cm) 
    # m.axis('off')
    m.drawcoastlines(color='k',linewidth=0.5)
    m.drawparallels([66.6,83.65],color='gray')
    m.drawparallels([60,70,80,83.65],dashes=[2,4],color='k')
    m.drawmeridians(np.arange(0.,420.,10.))
    # m.drawmapboundary(fill_color='aqua')
    ax = plt.gca()     
    # plt.title("Lambert Conformal Projection")
    # plt.show()

# colorbar
cbar_min=0
cbar_max=10000
cbar_step=1000
cbar_num_format = "%d"

cbar = plt.colorbar(pp, orientation='vertical', ticks=np.arange(cbar_min, cbar_max+cbar_step, cbar_step), format=cbar_num_format)
cbar.ax.set_ylabel('mm', fontsize = font_size)
cbar.ax.set_yticklabels(np.arange(cbar_min, cbar_max+cbar_step, cbar_step), fontsize=font_size)

 # ######################################################## Annotate    
 # cc=0
 # xx0=0.14 ; yy0=0.96 ; dy2=-0.04
 # mult=1
 # color_code='w'
 # plt.text(xx0, yy0+cc*dy2,varname, fontsize=font_size*mult,
 #   transform=ax.transAxes,color=color_code) ; cc+=1. 
 
 # plt.text(xx0, yy0+cc*dy2,"C3S Arctic regional reanalysis", fontsize=font_size*mult,
 #   transform=ax.transAxes,color=color_code) ; cc+=1. 
 
 # plt.text(xx0, yy0+cc*dy2,str(time[i]), fontsize=font_size*mult,
 #   transform=ax.transAxes,color=color_code) ; cc+=1. 

 # cc=0
 # xx0=0.95 ; yy0=0.01 ; dy2=-0.04
 # mult=0.6
 # color_code='k'
 # plt.text(xx0, yy0+cc*dy2,"@Climate_Ice", fontsize=font_size*mult,
 #   transform=ax.transAxes,color=color_code) ; cc+=1. 
 
 # ######################################################## Color Bar    
 # clb = plt.colorbar(fraction=0.046/2.,pad=0.04)
 # clb.ax.set_title('mm\n',fontsize=font_size,c='k')
 # plt.clim(0,15)
 
ly='x'
if ly == 'x':
    plt.show()
 
DPI=72
# DPI=300

if ly == 'p':
    figpath='./Fig/'
    figname=figpath+file
    plt.savefig(figname+'.png', bbox_inches='tight', dpi=DPI)