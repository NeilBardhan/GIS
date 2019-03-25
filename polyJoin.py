import os
import fiona
import math
import time
import pyproj
import pandas as pd
import geopandas as gpd
import unicodecsv as csv
from shapely.geometry import Polygon, MultiPoint, shape

path = os.getcwd()

gridFile = fiona.open(path + '\\mexGRID.shp')
blockFile = fiona.open(path + '\\all_states.shp')

def calc_distance(gridCentroid, blockCentroid):
    R = 6371000 # earth radius in meters
    lat1_r = gridCentroid["lat"] * math.pi / 180
    lat2_r = blockCentroid["lat"] * math.pi / 180
    x = (gridCentroid["long"] - blockCentroid["long"]) * math.pi / 180
    x *= math.cos( (lat1_r + lat2_r) / 2)
    y = (lat1_r - lat2_r)
    d = math.sqrt(x * x + y * y) * R
    return(round(d, 2))

def main():
    header = ['grid_id', 'xmin', 'xmax', 'ymin', 'ymax', 'CVEGEO']
    csvfile = open(path + '\\polyJoin1.csv', 'wb+')
    writer = csv.writer(csvfile, delimiter = ',')
    writer.writerow(header)
    st = time.time()
    ctr = 0
    for grid in gridFile:
        try:
            df = []
            df.append(grid['properties']['id'])
            df.append(grid['properties']['xmin'])
            df.append(grid['properties']['xmax'])
            df.append(grid['properties']['ymin'])
            df.append(grid['properties']['ymax'])
            ctr += 1
            gridPoly = shape(grid['geometry'])
            hits = list(blockFile.items(bbox=gridPoly.bounds))
            # print(len(hits))
            if(len(hits) == 0):
                # print("Empty GRID. No MVID.")
                mvid = -1
                df.append(mvid)
                continue
            elif(len(hits) == 1):
                mvid = hits[0][1]['properties']['CVEGEO']
                df.append(mvid)
            else:
                minDist = 1200
                gridCentroid0 = shape(grid['geometry']).centroid
                x, y = gridCentroid0.coords.xy
                x, y = x.tolist(), y.tolist()
                gridCentroid = {"long":x[0], "lat":y[0]}
                for i in range(len(hits)):
                    blockCentroid = {"long":0, "lat":0}
                    tempCentroid = shape(hits[i][1]['geometry']).centroid
                    x, y = tempCentroid.coords.xy
                    x, y = x.tolist(), y.tolist()
                    blockCentroid['long'] = x[0]
                    blockCentroid['lat'] = y[0]
                    tempDist = calc_distance(gridCentroid, blockCentroid)
                    if(tempDist <= minDist):
                        minDist = tempDist
                        tempMVID = hits[i][1]['properties']['CVEGEO']
                mvid = tempMVID
                df.append(mvid)
            writer.writerow(df)
            if(ctr % 10000 == 0):
                print("Processed ->", ctr, "in", round(time.time() - st, 2), "seconds.")
        except Exception as ex:
            print("Exception Raised at", ctr)
            print(ex)
            print(grid)
            pass
    csvfile.close()
    en = time.time() - st
    print("Total Time for", ctr, "grids ->", round(en, 2), "seconds.")

if __name__ == '__main__':
    main()
