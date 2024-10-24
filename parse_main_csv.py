import csv
import json
import sys

#csv_file = sys.argv[1]
csv_file = "wrapup_codes.csv"

wrapup_codes = {}

with open(csv_file, mode='r') as file:
    csv_reader = csv.DictReader(file)
    for index, row in enumerate(csv_reader):
        wrapup_codes[f"wrapup_code_{row['name']}"] = json.dumps({
            "name": row['name'],
            "rename": row['rename'],
            "division": row['division'] if row['division'] else "All",
        })        

# Output the JSON data as a map of string keys and string values
print(json.dumps(wrapup_codes))
