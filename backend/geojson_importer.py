# import geojson to prisma

import os
import json
import requests

base = os.path.dirname(__file__)
path = os.path.join(base, 'scratch', 'first_data.geojson')

# make post
def post_to_prisma(data):
    response = requests.post(
        "http://127.0.0.1:8000/places",
        json=data
    )


# Read GeoJSON file
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Create record to post
# results = []
n = 0
for feature in data['features']:
    props = feature['properties']
    record = {
        'place': props.get('place'),
        'latitude': props.get('latitude'),
        'longitude': props.get('longitude'),
        'pic_file': props.get('pic_file')
        
    }
    if n ==0:
        print (record)
    post_to_prisma(record)
    n = n+1