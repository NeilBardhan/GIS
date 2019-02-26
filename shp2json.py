import fiona
import time
import json
import os

def shp2json(source):
    country = fiona.open(source)
    itr = 0
    data = {"index" : {"_index" : "census_ar", "_type" : "ign", "_id" : "" }}
    temp = {"Name" : "", "Category" : "Cou", "Country" : "AR", "Attributes" : {}, "geometry" : {}}
    destination = "updatedJSON.txt"
    with open(destination, "w") as dfile:
        for elem in country:
            try:
                mvid = elem['properties']['MICROCODE']
                data['index']['_id'] = 'AR_' + str(mvid)
                #temp['Name'] = elem['properties']['NAM']
                temp['Name'] = str(mvid)
                temp['Attributes'] = dict(elem['properties'])
                cdnts = []
                for point in elem['geometry']['coordinates']:
                    newPt = []
                    for sublst in point:
                        if isinstance(sublst, tuple):
                            sub = list(sublst)
                            newPt.append([round(float(val), 6) for val in sub])
                        if isinstance(sublst, list):
                            for i in sublst:
                                if isinstance(i, tuple):
                                    newPt.append([round(float(val), 6) for val in i])
                            newPt = [newPt]
                    cdnts.append(newPt)
                temp['geometry'] = {'type': elem['geometry']['type'], 'coordinates' : cdnts}
                json.dump(data, dfile)
                dfile.write('\n')
                json.dump(temp, dfile)
                dfile.write('\n')
                itr += 1
                if(itr%10000 == 0):
                    print("Completed -> ", itr)
            except Exception as ex:
                print("Exception at ->", itr)
                print(ex)
                pass
        return os.getcwd() + '\\' + destination

def main():
    ### Enter source file directory here
    source = "C:\\Users\\Neil Bardhan\\Desktop\\LatLongSBD\\MBI_MarketData_2016_AR_Fracciones\\fracciones.shp"
    start = time.time()
    destinationPath = shp2json(source)
    print("Time Elapsed ->", time.time() - start)
    print("New file at ->", destinationPath)

if __name__ == '__main__':
    main()
