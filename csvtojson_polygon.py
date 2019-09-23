import sys, getopt
import csv
import json

file = 'Klokan_zoomify.csv'
json_file = 'Klokan_zoomify.json'
format = 'pretty'

def read_csv(file, json_file, format):
    csv_rows = []
    geojsont = {
      "type": "FeatureCollection",
      "features": []
    }
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        title = reader.fieldnames
        for row in reader:
            csv_rows.extend([{title[i]:row[title[i]] for i in range(len(title))}])

        for row in csv_rows:

            feature = {
                "type": "Feature",
                "geometry": {
                  "type": "Polygon",
                  "coordinates": [[]]
                },
                "properties": {
                  "name": "",
                  "when": {
                    "timespans": [
                        {
                          "start": "",
                          "end": ""
                        }
                    ],
                    "periods": [{
                        "name": "",
                        "@id": ""
                      }
                    ],
                    "label": ""
                  },
                }
              }
            feature['properties']['id'] = row['id']
            feature['properties']['link'] = row['link']
            feature['properties']['title'] = row['title']
            feature['properties']['publisher'] = row['publisher']
            west = row['west']
            east = row['east']
            north = row['north']
            south = row['south']
            feature['geometry']['coordinates'][0].extend([[west, north], [west, south], [east, north], [east, south]])

            feature['properties']['when']['timespans'][0]['start'] = row['date_from']
            feature['properties']['when']['timespans'][0]['end'] = row['date_to']
            geojsont['features'].extend([feature])

        write_json(geojsont, json_file, format)

#Convert csv data into json and write it
def write_json(data, json_file, format):
    with open(json_file, "w") as f:
        if format == "pretty":
            f.write(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': ')))
        else:
            f.write(json.dumps(data))

read_csv(file, json_file, format)
