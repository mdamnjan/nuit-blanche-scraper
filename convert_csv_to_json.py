import csv
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

exhibits = []
with open('exhibits.csv', newline='') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"', skipinitialspace=True)
    headers = next(csv_reader)
    for row in csv_reader:
        title, exhibit_number, address, link, artists, medium, physical_access, project_type = row

        # fetch coords from mapbox api
        res = requests.get('https://api.mapbox.com/geocoding/v5/mapbox.places/{}.json?access_token={}'.format(address, os.getenv('MAPBOX_API_KEY')))
        response = json.loads(res.text)
        coordinates = response['features'][0]['geometry']['coordinates']

        exhibits.append({
            'title': title,
            'exhibitNumber': exhibit_number,
            'address': address,
            'link': link,
            'artists': artists,
            'medium': medium,
            'physicalAccess': physical_access,
            'projectType': project_type,
            'coordinates': coordinates
            })

with open("exhibits.json", "w") as outfile:
    json.dump(exhibits, outfile)
        