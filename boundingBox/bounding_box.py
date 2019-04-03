import os
import time
import random
import mplleaflet
# import fiona
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import shape
from shapely import geometry
# from geopandas.tools import sjoin

path = os.getcwd()

swiss = gpd.read_file(path + '/shapefiles/CHE_adm0.shp')
# italy = gpd.read_file('C:\\Users\\Neil Bardhan\\Desktop\\Learn Python\\GIS\\gadm36_ITA_shp\\gadm36_ITA_0.shp')
fig, ax = plt.subplots(1)
base = swiss.plot(ax = ax, color = 'blue')

for i in range(len(swiss)):    
    bounds = shape(swiss.loc[i, 'geometry']).bounds
    x1, y1 = bounds[0], bounds[1]
    x2, y2 = bounds[-2],bounds[-1]

pointList = [geometry.Point(x1, y1), geometry.Point(x2,y1), geometry.Point(x2, y2), geometry.Point(x1, y2)]
# print(pointList)
poly = geometry.Polygon([[p.x, p.y] for p in pointList])

corners = gpd.GeoSeries(poly)
corners = gpd.GeoSeries({"geometry": poly})
corners.crs = {'init': 'epsg:4326'}
corners.plot(ax = base, marker = "o", mfc = "black",
             markersize = 4, markeredgecolor = "black",
             alpha = 0.5, color = "white")

numPoints = 1000

pts = []
start = time.time()
for i in range(numPoints):
    x = random.uniform(x1, x2)
    y = random.uniform(y1, y2)
    pt = geometry.Point(x, y)
    pnt = pt
    pt = gpd.GeoSeries(pt)
    if pnt.within(shape(swiss.loc[0, 'geometry'])):
        pts.append(pt)
        pt.plot(ax = base, marker = "x",
                  markersize = 5,
                  markeredgecolor = "green", alpha = 0.5)
    else:
        # continue
        pt.plot(ax = base, marker = "x",
                  markersize = 5,
                  markeredgecolor = "red", alpha = 0.5)
stop = time.time()
numpip = len(pts)
# ctr = swiss.loc[0, 'geometry'].centroid
# ctr = gpd.GeoSeries(ctr)
# ctr.plot(ax = base, marker = "x",
#                   markersize = 15,
#                   markeredgecolor = "black", alpha = 1)
# italy.plot(ax = ax, color = 'blue')
mplleaflet.show(fig = ax.figure, crs = swiss.crs, tiles = 'cartodb_positron', path = 'swissBoxMap.html')

print("Time elapsed ->", round(stop - start, 2), "seconds.")
