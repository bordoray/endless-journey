# import geojson to prisma

import os
import json
import requests

base = os.path.dirname(__file__)
path = os.path.join(base, 'scratch', 'first_data.geojson')

# make post
def post_to_prisma(data):
    response = requests.post(
        "http://localhost:8000/todos",
        json=data
    )


# Read GeoJSON file
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Create record to post
# results = []
for feature in data['features']:
    props = feature['properties']
    record = {
        'place': props.get('place'),
        'pic_file': props.get('pic_file'),
        'longitude': props.get('longitude'),
        'latitude': props.get('latitude')
    }
    post_to_prisma(record)