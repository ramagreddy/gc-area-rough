import csv
import sys
import json

def parse_csv(file_path):
    policies = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Convert the 'action_set' field to a list of strings
            actions = row["action_set"].split(",")
            policies.append({
                "domain": row["domain"],
                "entity_name": row["entity_name"],
                "action_set": actions  # Ensure it's a list
            })
    return policies

if __name__ == "__main__":
    file_path = sys.argv[1]
    print(json.dumps({"permission_policies": parse_csv(file_path)}))

