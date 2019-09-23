import sys, getopt
import csv
import json

file = 'EAP.csv'
json_file = 'EAP.json'
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
                  "type": "Point",
                  "coordinates": []
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
            feature['properties']['id'] = row['Project_Ref']
            # feature['properties']['link'] = row['link']
            feature['properties']['name'] = row['Name ']
            feature['properties']['institution'] = row['Award_Institution ']
            long = row['Longitude ']
            lat = row['Latitude ']
            feature['geometry']['coordinates'].extend([long, lat])

            feature['properties']['when']['timespans'][0]['start'] = row['Award_Date ']
            feature['properties']['when']['timespans'][0]['end'] = row['Award_Date ']
            geojsont['features'].extend([feature])

        write_json(geojsont, json_file, format)

#Convert csv data into json and write it
def write_json(data, json_file, format):
    with open(json_file, "w") as f:
        if format == "pretty":
            # TODO Sort double quotes
            f.write(json.dumps(data, sort_keys=False, indent=2, separators=(',', ': ')))
        else:
            f.write(json.dumps(data))

read_csv(file, json_file, format)
