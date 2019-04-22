import csv
import time
import pandas as pd
import multiprocessing as mp
from math import sin, cos, atan2, sqrt, radians

def haversine(row):
    
    lat1 = radians(float(row[0]))
    lon1 = radians(float(row[1]))
    lat2 = radians(float(row[-2]))
    lon2 = radians(float(row[-1]))
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    d = R * c
    row.append(d)
    # return(round(d, 2))
    return row
    
if __name__ == '__main__':
    fname = 'points1M.csv'
    
    with open(fname, newline = "") as fp:
        reader = csv.reader(fp)
        header = next(reader, None)
        headerLen = len(header)
        if(headerLen == 4):
            header.append('distance')
            start = time.time()
            pool = mp.Pool(mp.cpu_count())
            res = pool.map(haversine, [row for row in reader])
            pool.close()
            
            print("Parallelized time : ", round(time.time() - start, 3), "seconds.")
            df = pd.DataFrame(res, columns = header)
            df.to_csv('distances1M.csv', index = False)
