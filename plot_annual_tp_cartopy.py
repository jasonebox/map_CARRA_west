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
# from mpl_toolkits.basemap import Basemap
import cartopy.crs as ccrs
import cartopy

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

def lon360_to_lon180(lon360):

    #reduce the angle  
    lon180 =  lon360 % 360 
    
    #force it to be the positive remainder, so that 0 <= angle < 360  
    lon180 = (lon180 + 360) % 360;  
    
    #force into the minimum absolute value residue class, so that -180 < angle <= 180  
    lon180[lon180 > 180] -= 360
    
    return lon180


AW=1
path='/Users/jason/Dropbox/CARRA/prog/map_CARRA_west/'
if AW:path='C:/Users/Pascal/Desktop/GEUS_2019/SICE_AW_JEB/SICE_AW_JEB/map_CARRA_west/'
os.chdir(path)

# global plot settings
th=1
font_size=18
plt.rcParams['axes.facecolor'] = 'k'
plt.rcParams['axes.edgecolor'] = 'k'
plt.rcParams["font.size"] = font_size
max_value=2000*3

# for a later version that maps the result
ni=1269
nj=1069

map_version=1 # 0 for simple raster map, 1 for projected map
    
if map_version:
    
    fn='./ancil/2.5km_CARRA_west_lat_1269x1069.npy'
    lat=np.fromfile(fn, dtype=np.float32, count=-1, sep='', offset=0)
    lat=lat.reshape(ni, nj)

    fn='./ancil/2.5km_CARRA_west_lon_1269x1069.npy'
    lon=np.fromfile(fn, dtype=np.float32, count=-1, sep='', offset=0)
    lon=lon.reshape(ni, nj)
    
    lat_to_add = 55.81 - np.nanmin(lat)
    lat = lat[::-1]
    lat += lat_to_add
    
    lon = lon360_to_lon180(lon)
    
    # m = Basemap(llcrnrlon=-55, llcrnrlat=55.8, urcrnrlon=80, urcrnrlat=80, lat_1=72, lat_0=72., lon_0=-36, resolution='l', projection='lcc') # carlos' version
    # m = Basemap(llcrnrlon=-56.76, llcrnrlat=57.363, urcrnrlon=33.255, urcrnrlat=79.526, lat_0=72, lon_0=-36, resolution='l', projection='lcc')
    # m = Basemap(llcrnrlon=-56.76, llcrnrlat=57.311, urcrnrlon=33.255, urcrnrlat=79.526, lat_0=72, lon_0=-36, resolution='l', projection='lcc')
    
    #plt.figure()
    # f = plt.figure(figsize=(8,4))
    m = ccrs.LambertConformal(central_longitude = -36, central_latitude = 72.)
    # img_extent = (-56.76, 33.255, 57.311, 79.526)
    
    # obtained with e.g.:
    # m.transform_point(src_crs=ccrs.PlateCarree(), x=33.255, y=79.526)
    img_extent = (-1305936.576584626, 1913601.457154332, 
                  -1704450.4812351097, 1907398.010098368)
    
    
    #ax = plt.subplot(111, projection=m)
    
    # # voir https://epsg.io/2154, cliquer sur proj.4
    # proj4_params = "+proj=lcc +lat_1=49 +lat_2=44 +lat_0=46.5 +lon_0=3 +x_0=700000 " + \
    #            "+y_0=6600000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
    
    # # Ne sert à rien si ce n'est à vérifier que le format est correct.    
    # import pyproj
    # lambert93 = pyproj.Proj(proj4_params)

    # Système de coordonnées de cartopy.
    # proj4_list = [(k, v) for k,v in map(parse_option_pyproj, proj4_params.split())]
    # crs_lambert93 = MyCRS(proj4_list, globe=None)
    
    # print('UL',lat[0,0],lon[0,0])
    print('LL',lat[ni-1,0],lon[ni-1,0])
    print('UR',lat[0,nj-1],lon[0,nj-1])
    # x, y = m(lat, lon)
    # m.fillcontinents(color='coral',lake_color='aqua')
    # draw parallels and meridians.

# read data
year='2016'
fn='./grids_to_map/tp_2.5km_CARRA_'+year+'.npy'
# os.system('ls -lF '+fn)
tot=np.fromfile(fn, dtype=np.float32)#, count=-1, sep='', offset=0)
tot=tot.reshape(ni, nj)

# %%
# plt.imshow(tot, extent=img_extent, aspect='auto')#,zorder=1)#, extent=(-56.76, 33.255, 57.311, 79.526), transform=ccrs.PlateCarree())
img_extent = (np.nanmin(lon) , np.nanmax(lon),
                  np.nanmin(lat), np.nanmax(lat))
plt.figure()
ax = plt.subplot(111, projection=ccrs.PlateCarree())
# plt.imshow(tot, extent=img_extent, aspect='auto', transform=ccrs.PlateCarree(),
#            origin='upper')
ax.contourf(lon, lat, tot, aspect='auto', transform=ccrs.PlateCarree())
ax.coastlines(resolution='50m', color='black', linewidth=1)


#%%
# custom color table, after https://www.dropbox.com/s/xvntyqnyulmd02c/Box_et_al_2004_JGR.pdf?dl=0
r=[188,108,76,0,      172,92,0,0,      255,255,255,220, 204,172,140,108, 255,255,255,236, 212,188,164,156, 255, 255]
g=[255,255,188,124, 255,255,220,156, 255,188,156,124,  156,124,92,60,   188,140,72,0,    148,124,68,28, 255, 255 ]
b=[255,255,255,255,  172,92,0,0,      172,60,0,0,       156,124,92,60,   220,196,164,0,  255,255,255,196, 0, 200 ]
r=[188,108,76,0,      172,92,0,0,      255,255,255,220, 204,172,140,108, 255,255,255,236, 212,188,164,156]
g=[255,255,188,124, 255,255,220,156, 255,188,156,124,  156,124,92,60,   188,140,72,0,    148,124,68,28]
b=[255,255,255,255,  172,92,0,0,      172,60,0,0,       156,124,92,60,   220,196,164,0,  255,255,255,196]
# ranges=[0,40,80,160,320,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000,2100,2200,2300,2400]
colors = np.array([r, g, b]).T / 255
n_bin = 24
# n_bin = 280
cmap_name = 'my_list'
# Create the colormap
cm = LinearSegmentedColormap.from_list(
    cmap_name, colors, N=n_bin)

# make graphic
ax = plt.subplot(111)
ax.set_title('CARRA total precipitation '+year)

if map_version==0:
    pp=plt.imshow(np.rot90(tot.T), interpolation='nearest', origin='lower', cmap=cm,vmin=0,vmax=max_value) ; plt.axis('off') 

if map_version:
    pp=m.imshow(np.rot90(tot.T), cmap = cm,vmin=0,vmax=max_value) 
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
#JJ when we get ranges working, the colorbar labels should be = ranges
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