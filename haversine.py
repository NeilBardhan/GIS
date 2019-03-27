import csv
import math
import time

def calc_distance(point1, point2):
	R = 6371000 # earth radius in meters
	lat1_r = point1[0] * (math.pi / 180)
	lat2_r = point2[0] * (math.pi / 180)
	x = (point1[1] - point2[1]) * (math.pi / 180)
	x *= math.cos((lat1_r + lat2_r) / 2)
	y = (lat1_r - lat2_r)
	d = math.sqrt(x * x + y * y) * R
	return(round(d, 2))

fname = "points.csv"

outfile = open("results.csv", 'w+', newline = '')
writer = csv.writer(outfile, delimiter = ',')

with open(fname, newline = "") as fp:
    reader = csv.reader(fp)
    header = next(reader, None)
    headerLen = len(header)
    if(headerLen == 4):
        start = time.time()
        header.append('distance')
        writer.writerow(header)
        for row in reader:
            point1 = (float(row[0]), float(row[1]))
            point2 = (float(row[-2]), float(row[-1]))
            distance = calc_distance(point1,point2)
            row.append(distance)
            writer.writerow(row)
        print("Time Elapsed", round(time.time() - start, 3), "seconds.")
