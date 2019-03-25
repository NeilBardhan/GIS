import os
import time
import shapely
import geopandas
import matplotlib.pyplot as plt
import mplleaflet
import numpy as np

path = os.getcwd()
swiss = geopandas.read_file(path + '\\shapefiles\\CHE_adm0.shp')
#swiss = geopandas.read_file('C:\\Users\\Neil Bardhan\\Desktop\\MEX_SHP\\encuesta_intercensal_2015\\all_states\\all_states_shp\\MEX_adm0.shp')
swissCRS = {'init' : 'epsg:4326'}

fig, ax = plt.subplots(1)
base = swiss.plot(ax=ax, color='white')

shpGeometry = swiss['geometry'].iloc[0]

bounds = swiss.bounds
minx = float(bounds['minx'].iloc[0])
miny = float(bounds['miny'].iloc[0])
maxx = float(bounds['maxx'].iloc[0])
maxy = float(bounds['maxy'].iloc[0])
xBins = np.arange(minx, maxx, 0.01)
yBins = np.arange(miny, maxy, 0.01)
print(len(xBins), len(yBins))
print(len(xBins) * len(yBins))

bottomLeft = (minx, miny)
topLeft = (minx, maxy)
bottomRight = (maxx, miny)
topRight = (maxx, maxy)

poly = shapely.geometry.Polygon((bottomLeft, topLeft, topRight, bottomRight))
corners = geopandas.GeoSeries(poly)
corners = geopandas.GeoSeries({"geometry": poly})
corners.crs = {'init': 'epsg:4326'}
corners.plot(ax = base, marker = "o", mfc = "red", markersize = 5, markeredgecolor = "black", alpha = 0.7)

ctr = 0
start = time.time()
for x in xBins:
    ctr += 1
    pt0 = (x, miny)
    point0 = shapely.geometry.Point(pt0)
    point0 = geopandas.GeoSeries(point0)
    point0.plot(ax = base, marker = 'x', mfc = 'blue', markersize = 7, markeredgecolor = 'blue', alpha = 1)

    pt1 = (x, maxy)
    point1 = shapely.geometry.Point(pt1)
    point1 = geopandas.GeoSeries(point1)
    point1.plot(ax = base, marker = 'x', mfc = 'blue', markersize = 7, markeredgecolor = 'blue', alpha = 1)

    plt.plot((pt1[0], pt0[0]), (pt1[1], pt0[1]), 'b-')

ctr = 0
for y in yBins:
    ctr += 1
    pt0 = (minx, y)
    point0 = shapely.geometry.Point(pt0)
    point0 = geopandas.GeoSeries(point0)
    point0.plot(ax = base, marker = 'x', mfc = 'green', markersize = 7, markeredgecolor = 'green', alpha = 1)

    pt1 = (maxx, y)
    point1 = shapely.geometry.Point(pt1)
    point1 = geopandas.GeoSeries(point1)
    point1.plot(ax = base, marker = 'x', mfc = 'green', markersize = 7, markeredgecolor = 'green', alpha = 1)

    plt.plot((pt1[0], pt0[0]), (pt1[1], pt0[1]), 'g-')
end = time.time() - start
               
print("Time Elapsed", round(end, 2))
mplleaflet.show(fig = ax.figure, crs = swiss.crs, tiles = 'cartodb_positron', path = 'swissmap_01.html')
