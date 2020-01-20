import os
import csv
import json
import time
import requests

file = 'osmData.csv'
outfile = open("osmResults.csv", 'w+', newline = '')
writer = csv.writer(outfile, delimiter = ',')

with open(file, newline = '') as fp:
    reader = csv.reader(fp)
    header = next(reader, None)
    header = list(filter(None, header))
    header.append('latitude')
    header.append('longitude')
    writer.writerow(header)
    headerLen = len(header)
    success = 0
    failed = 0
    cnt = 0
    url = 'https://nominatim.openstreetmap.org/search?q='
    suffix = '&format=json&polygon=1&addressdetails=1'
    start = time.time()
    for row in reader:
        row = list(filter(None, row))
        # print(row)
        cnt += 1
        try:
            primaryAddress = row[2].strip().replace(" ", "+")
            city = row[3].strip()
            state = row[4].strip()
            zipCode = row[5].strip().split('-')[0]
            params = [primaryAddress, city, state, zipCode]
            params = "+".join(params)
            response = requests.get(url + params + suffix)
            # print(params)
            responseCode = str(response.status_code)
            if responseCode == '429':
                print("Too Many Requests (blocked by API:( )")
                # print(response.json())
                break
            # print("Status Code : " + str(response.status_code))
            if(responseCode == '200'):
                data = response.json()
                if(data):
                    # print(data)
                    success += 1
                    row.append(data[0]['lat'])
                    row.append(data[0]['lon'])
                    writer.writerow(row)
                    print(1)
                    # print(row)
                    # print(data[0]['lat'], data[0]['lon'])
                    # print(data[0]['lon'])
                else:
                    print("response 200, but no data")
                    failed += 1
            else:
                print("response != 200")
                failed += 1
        except Exception as err:
            print("Exception Raised!", err)
            # break
            pass
        if(cnt == 200):
            time.sleep(1)
    stop = time.time()
    print("# of Successes", success)
    print("Success Rate", round(success/(success + failed), 2) * 100, "%")
    print("# of Failures", failed)
    print("Failure Rate", round(failed/(success + failed), 2) * 100, "%")
    print("Time Elapsed ->", round(stop - start, 2), "seconds.")
outfile.close()
