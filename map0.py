import os
import mplleaflet
import geopandas as gpd
#import matplotlib.pyplot as plt

path = os.getcwd()
swissShape = gpd.read_file(path + '/shapefiles/CHE_adm0.shp')
plot0 = swissShape.plot(color = 'red', alpha = 0.1)
mplleaflet.show(fig=plot0.figure, crs=swissShape.crs, tiles='cartodb_positron', path='swissMap.html')
