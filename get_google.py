'''
Example request below, see documentation here:
https://developers.google.com/maps/documentation/distance-matrix/overview#maps_http_distancematrix_latlng-py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import requests

url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=40.6655101%2C-73.89188969999998&destinations=40.659569%2C-73.933783%7C40.729029%2C-73.851524%7C40.6860072%2C-73.6334271%7C40.598566%2C-73.7527626&key=YOUR_API_KEY"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

'''

import requests
import pandas as pd
import datetime
import calendar
import time


def generate_url(origins, destinations, api_key, dtime, mode='transit', tmode='bus|subway|tram'):
    if tmode is None:
        url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origins}&destinations={destinations}&mode={mode}&departure_time={dtime}&key={api_key}"
    else:
        url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origins}&destinations={destinations}&mode={mode}{'&transit_mode='+tmode}&departure_time={dtime}&key={api_key}"
    return url


api_key = 'XYZ'
payload={}
headers = {}
individuals = True


# Format of locations.csv: Orig_Long,Orig_Lat,Dest_Long,Dest_Lat

#locations = pd.read_csv(f'locations.csv')
locations = pd.read_excel('TransferLinks_v3.xlsx',sheet_name='Input', skiprows=19)
locations['Origins'] = locations.Orig_Lat.astype(str) +"%2C" + locations.Orig_Long.astype(str)
locations['Destinations'] = locations.Dest_Lat.astype(str) +"%2C" + locations.Dest_Long.astype(str)

# Time in GMT
txt_time = 'Wed Feb 2 17:45:00 2022'
nice_time = time.strptime(txt_time)
dtime = calendar.timegm(nice_time)


modes =  ['driving', 'transit', 'bicycling', 'walking']

if individuals:
    responses = []
    for mode in modes:
        if mode == 'transit':
            tmode = 'bus|subway|tram'
        else:
            tmode = None
        for index, row in locations.iterrows():
                url = generate_url(row.Origins, row.Destinations, api_key, dtime, mode, tmode)
                responses.append(requests.request("GET", url, headers=headers, data=payload).text)
        locations[mode] = responses
    locations.to_csv(f'GoogleDistanceMatrix_{txt_time.replace(":","-")}.csv')

else:
    orig_locs = locations.Origins.to_list()
    dest_locs = locations.Destinations.to_list()

    origins = '%7C'.join(orig_locs)
    destinations = '%7C'.join(dest_locs)
    for mode in modes:
        if mode == 'transit':
            tmode = 'bus|subway|tram'
        else:
            tmode = None
        url = generate_url(origins, destinations, api_key, dtime, mode, tmode)
        response = requests.request("GET", url, headers=headers, data=payload)
        response.text.to_csv(f'GoogleDistanceMatrix_{mode}_{txt_time.replace(":","-")}.csv')