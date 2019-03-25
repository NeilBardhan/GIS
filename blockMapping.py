import os
import re
import math
import json
import mplleaflet
import pyproj
import random
import geopandas as gpd
import unicodecsv as csv
from shapely import geometry
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import Polygon, MultiPoint

def centroid(polygon):
    xTot = 0
    yTot = 0
    zTot = 0
    for elem in polygon:
        lat = math.radians(elem["lat"])
        lon = math.radians(elem["long"])
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
    dict = {"lat": round(lat, 6), "long": round(lon, 6)}
    return dict

def calc_avg_distance(geom, ctr):
    distances = []
    for elem in geom:
        R = 6371000 # earth radius in meters
        lat1_r = elem["lat"] * math.pi / 180
        lat2_r = ctr["lat"] * math.pi / 180
        x = (elem["long"] - ctr["long"]) * math.pi / 180
        x *= math.cos( (lat1_r + lat2_r) / 2)
        y = (lat1_r - lat2_r)
        d = math.sqrt(x * x + y * y) * R
        distances.append(d)
    return(round(sum(distances)/len(distances), 5))

def plot_circle(longitude, latitude,
                        segments, distance_m,
                        geom_type=MultiPoint):
    """
    Creates a buffer in meters around a point given as long, lat in WGS84
    Uses the geodesic, so should be more accurate over larger distances

    :param longitude: center point longitude
    :param latitude: center point latitude
    :param segments: segments to approximate (more = smoother)
    :param distance_m: distance in meters
    :param geom_type: shapely type (e.g. Multipoint, Linestring, Polygon)
    :return: (WKT of buffer geometry)
    """
    geodesic = pyproj.Geod(ellps='WGS84')
    coords = []
    for i in range(0, segments):
        angle = (360.0 / segments) * float(i)
        x1, y1, z1 = geodesic.fwd(lons=longitude,
                                  lats=latitude,
                                  az=angle,
                                  dist=distance_m,
                                  radians=False)
        coords.append((x1, y1))

    ring = geom_type(coords)
    return ring

def main():
    path = os.getcwd()
    header = ['block_id', 'block_corners', 'centroid_latitude', 'centroid_longitude']
    csvfile = open(path + "\\" + "tmp_cameo.csv", 'wb+')
    writer = csv.writer(csvfile, delimiter = ',')
    writer.writerow(header)

    with open('cameo.json') as data_file:
        data = json.load(data_file)
        swiss = gpd.read_file('C:\\Users\\Neil Bardhan\\Desktop\\LatLongProsa\\TMP_CAMEO\\CHE_adm_shp\\CHE_adm0.shp')
        swiss.crs = {'init': 'epsg:4326'}
        fig, ax = plt.subplots(1)
        base = swiss.plot(ax=ax, color='white')
        
        places = pd.read_csv("sample0.csv")
        placesLatLong = places[["uid", "latitude","longitude"]]
        places = []
        for i in range(len(placesLatLong)):
            temp = (float(placesLatLong["longitude"][i]), float(placesLatLong["latitude"][i]))
            pt = geometry.Point(temp)
            places.append(pt)
            pt = gpd.GeoSeries(pt)
            pt.plot(ax=base, marker="o", mfc="steelblue", markersize=6, markeredgecolor="steelblue", alpha=1)
        
        for item in data["items"]:
            block_id = item["ogr_fid"]
            geom = item["ora_geometry"]
            temp = geom.find('ORDINATE_ARRAY(')
            geom = geom[temp:]
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
            geom = []

            for elem in polygon:
                geomDict = {"lat": 0.0, "long": 0.0}
                geomDict["lat"] = elem[1]
                geomDict["long"] = elem[0]
                geom.append(geomDict)

            ctr = centroid(geom)
            print("Block ID ->", block_id, ":: Centroid ->", ctr)

            avg_dist = calc_avg_distance(geom, ctr)
            print("Average Distance ->", avg_dist, "metres.")

            df = []
            df.append(block_id)
            df.append(geom)
            df.append(ctr["lat"])
            df.append(ctr["long"])
            writer.writerow(df)

            ctrTup = (ctr["long"], ctr["lat"])
            ctrPt = geometry.Point(ctrTup)
            ctrPt = gpd.GeoSeries(ctrPt)

            poly = geometry.Polygon([[p[0], p[1]] for p in polygon])
            
            ct = 0
            inDict = {"block_id":block_id, "pt_cnt":0, "points":[]}
            for pt in places:
                if(poly.contains(pt)):
                    inDict["points"].append(pt)
                    ct += 1
            inDict["pt_cnt"] = ct
            if(ct > 0):
                print(inDict)
                print("\n")
            else:
                print("No points.\n")
            corners = gpd.GeoSeries(poly)
            corners = gpd.GeoSeries({"geometry": poly})
            corners.crs = {'init': 'epsg:4326'}
            corners.plot(ax = base, marker = "o", mfc = "red", markersize = 5, markeredgecolor = "black", alpha = 0.7)

            ctrPt.plot(ax=base, marker="x", mfc="black", markersize=7, markeredgecolor="black", alpha=1)

            wkt = plot_circle(ctr["long"], ctr["lat"], 64, avg_dist, Polygon)
            x, y = wkt.exterior.coords.xy
            ring = gpd.GeoSeries(wkt)
            i = random.randint(0, len(x)-1)
            ax.plot((ctr["long"], x[i]), (ctr["lat"], y[i]), linestyle='dashed', color = "black", marker=".", markersize=2)
            ring = gpd.GeoSeries({"geometry": wkt})
            ring.crs = {'init': 'epsg:4326'}
            ring.plot(ax = base, color = '#f5f5dc', alpha = 1)

    csvfile.close()
    mplleaflet.show(fig = ax.figure, crs = swiss.crs, tiles = 'cartodb_positron', path = 'swissmap.html')

if __name__ == '__main__':
    main()
