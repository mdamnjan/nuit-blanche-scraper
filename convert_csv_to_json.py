import csv
import json

exhibits = []
with open('exhibits.csv', newline='') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"', skipinitialspace=True)
    headers = next(csv_reader)
    for row in csv_reader:
        title, exhibit_number, address, link, artists, medium, physical_access, project_type = row

        exhibits.append({
            'title': title,
            'exhibitNumber': exhibit_number,
            'address': address,
            'link': link,
            'artists': artists,
            'medium': medium,
            'physicalAccess': physical_access,
            'projectType': project_type
            })

with open("exhibits.json", "w") as outfile:
    json.dump(exhibits, outfile)
        