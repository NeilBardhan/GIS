import math
import json
import re
import geopandas as gpd
import matplotlib.pyplot as plt
import mplleaflet
from shapely import geometry
#from pylab import figure, text, scatter, show

def centroid():
    xTot = 0
    yTot = 0
    zTot = 0
    for tup in polygon:
        lat = math.radians(tup[1])
        lon = math.radians(tup[0])
        x = math.cos(lat) * math.cos(lon)
        y = math.cos(lat) * math.sin(lon)
        z = math.sin(lat)
        xTot += x
        yTot += y
        zTot += z
    x = round(xTot/4, 6)
    y = round(yTot/4, 6)
    z = round(zTot/4, 6)
    Lon = math.atan2(y, x)
    hyp = math.sqrt(x * x + y * y)
    Lat = math.atan2(z, hyp)
    lat = math.degrees(Lat)
    lon = math.degrees(Lon)
#    return(round(lat, 6), round(lon, 6))
    return(round(lon, 6), round(lat, 6))

with open('cameo.json') as data_file:
    data = json.load(data_file)
    swiss = gpd.read_file('C:\\Users\\Neil Bardhan\\Desktop\\LatLongProsa\\TMP_CAMEO\\CHE_adm_shp\\CHE_adm0.shp')
    swiss.crs = {'init': 'epsg:4326'}
    fig, ax = plt.subplots(1)
    base = swiss.plot(ax=ax, color='white')
    k = 0
    for item in data["items"]:
        block_id = item["ogr_fid"]
        
        geom = item["ora_geometry"]
        i = geom.find('ORDINATE_ARRAY(')
        geom = geom[i:]
        outer = re.compile("\((.+)\)")
        m = outer.search(geom)
        geom = m.group(1)
        geom = geom[:-1]
        geom = geom.split(',')
        ls = ()
        polygon = []
        for elem in geom:
            temp = elem.strip()
            if temp == '0':
                polygon.append(ls)
                ls = ()
            else:
                ls = ls + tuple([float(temp)])
        polygon = polygon[:-1]
        k+=1
    
#polygon = [(46.498013, 9.837799), (46.497986, 9.839101), (46.498885, 9.839141), (46.498912, 9.837839)]

#        print("The points of the polygon are - ")
#        
#        for tup in polygon:
#            print(tup[1], tup[0])
#        print('\n')
        z = centroid()
        print(z)
        print("Block ID -> {} :: Centroid -> {}".format(block_id, z))
        ctr = geometry.Point(z)
#        print("The Centroid of the polygon is - ", z)
#        print('\n****************************\n')
        ctr = gpd.GeoSeries(ctr)
        poly = geometry.Polygon([[p[0], p[1]] for p in polygon])
#        print(type(poly))
#        print(poly.wkt)
        
        corners = gpd.GeoSeries(poly)
        corners = gpd.GeoSeries({"geometry": poly})
        corners.crs = {'init': 'epsg:4326'}

        corners.plot(ax=base, marker="o", 
                     mfc="red", markersize=5, 
                     markeredgecolor="black", alpha=0.5)
        ctr.plot(ax=base, marker="x", 
                     mfc="black", markersize=7, 
                     markeredgecolor="black", alpha=1)
#        ax.text(z[0], z[1], block_id, horizontalalignment='center', verticalalignment='center', fontsize='10', color='blue', transform=ax.transAxes)
#        for n in range(len(polygon)):
#            ax.plot((z[0], polygon[n][0]), (z[1], polygon[n][1]), linestyle='dashed', color = "gray", marker=".", markersize=2)
#        _ = ax.axis('off')
        ax.set_title("Polygons and Centroids in Switzerland")
    print("Num blocks - ", k)

mplleaflet.show(fig=ax.figure, crs=swiss.crs, tiles='cartodb_positron', path='swissmap.html')
