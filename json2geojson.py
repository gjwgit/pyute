#! usr/bin/env python

# Originally loned from 
# https://github.com/ACT-COVID-19-TRACKER/privatekit-data-granularity-assessment/blob/master/json-to-geojson.py

from sys import argv
from os.path import exists
import simplejson as json 

script, in_file, out_file = argv

data = json.load(open(in_file))

geojson = {
    "type": "FeatureCollection",
    "features": [
    {
        "type": "Feature",
        "geometry" : {
            "type": "Point",
            "coordinates": [d["longitude"], d["latitude"]],
            },
        "properties" : d,
     } for d in data]
}


output = open(out_file, 'w')
json.dump(geojson, output)

# print geojson
