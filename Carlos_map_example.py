'''
Make some plots for the CARRA CDS release
Based on the CERRA scripts provided by Semjon
'''

import pygrib

import numpy as np
import math

import matplotlib
matplotlib.use('Agg')


from mpl_toolkits.basemap import Basemap

from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt

from mpl_toolkits.basemap import interp

#import cdo
from cdo import *
cdo   = Cdo()

# Path to Grib data
root_grib = '/media/cap/7fed51bd-a88e-4971-9656-d617655b6312/data/carra_kpn/'
dom="East"
dom="West"
root_fig = dom+'_'
grib = root_grib + 'CW_Tskin_an2018021812+000.grib'
grbs = pygrib.open(grib)


def plotting(lons, lats, data, name, unit, level, color,dom):
    """
    function plotting europ map
    Return a figure for each parameter
    Modified from original CERRA scripts
    Still using basemap
    """
    plt.figure(figsize=(10, 10))   
    ax = plt.subplot(111)
    if dom=="West":
        m = Basemap(llcrnrlon=-55, llcrnrlat=55.8, urcrnrlon=80, urcrnrlat=80, lat_1=72, lat_0=72., lon_0=-36, resolution='h', projection='lcc')
    elif dom=="East":
        m = Basemap(resolution="i", width=3850000,height=3850000,  projection='aea',\
                   lon_0=34,lat_0=73.8,lat_1=70)
    x, y = m(lons, lats)
    #convert data to Celsius
    if name == 'Temperature':
        data = data - 273.15 
    # Plot data
    import matplotlib as mpl
    cmap = mpl.cm.coolwarm
    cmap = mpl.cm.RdBu_r
    print("min and max of data {} {}".format(min(data.flatten()),max(data.flatten())))
    minVal = min(data.flatten())
    maxVal = max(data.flatten())
    clev = np.arange(minVal,maxVal,level) #0.01)
    print("Plotting in levels {}".format(clev))
    if name == "Temperature":
        CS_tmp = m.contourf(x,y,data,clev,cmap=plt.cm.coolwarm)
        clb = plt.colorbar(CS_tmp,fraction=0.03,ticks=[-50,-40,-30,-20,-10,0,10,20])
    else:
        cmap = mpl.cm.coolwarm
        CS_tmp = m.contourf(x,y,data,clev,cmap=plt.cm.coolwarm)
        if unit == "m/s":
            use_ticks=list(np.arange(int(minVal),int(maxVal),level))
        else:
            use_ticks=list(np.arange(minVal,maxVal,level*10))
        print("Using ticks {}".format(use_ticks))
        clb = plt.colorbar(CS_tmp,fraction=0.03,ticks=use_ticks)
        clb.ax.set_title(unit)

    # Countries and coasts lines
    m.drawcountries(linewidth=0.4, color='k', zorder=4)
    m.drawcoastlines(linewidth=0.4, color='k', zorder=4)

    # Grid
    parallels = np.arange(0.,81,5.)
    m.drawparallels(parallels,labels=[True,False,False,False], fontsize=15, labelstyle='+/-', linewidth=0.2)
    meridians = np.arange(0.,360.,5.)
    m.drawmeridians(meridians,labels=[False,False,False,True], fontsize=15, labelstyle='+/-', linewidth=0.2)

    # fig.axes.get_xaxis().set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Title and labels
    if dom == 'West':
        plt_title=name
    else:
        plt_title=""
    plt.text(0.5,0.8,plt_title,fontsize=20,transform=ax.transAxes,
       horizontalalignment='center', verticalalignment='center')
    plt.ylabel(u'latitude', fontsize=20, labelpad=45)
    plt.xlabel(u'longitude', fontsize=20, labelpad=25)
    
    # Save figure
    plt.tight_layout()
    image_path = root_fig + name.replace(' ', '_').replace('/', '_').replace(',', '').replace(':', '_') + '.png'
    plt.savefig(image_path)
    plt.close('all')
    return image_path


if __name__ == '__main__':
    import sys
    variable = "Temperature"
    vlevel=0
    unit = 'K'
    level=0.01
    for grb in grbs:
        if grb.name == variable and grb.level==vlevel:
            data = grb.values
            lats, lons = grb.latlons()
            name = grb.name # + " 01/01/2019 06:00 AM"
            color = 'RdBu_r'
            print('Plotting figure for: ' + name)        
            image_path=plotting(lons, lats, data, name, unit, level, color,dom)
   

    



