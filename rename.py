import PureCloudPlatformClientV2
from PureCloudPlatformClientV2.rest import ApiException
from pprint import pprint
import os
import csv
import pytest


region = PureCloudPlatformClientV2.PureCloudRegionHosts.eu_west_2
PureCloudPlatformClientV2.configuration.host = region.get_api_host()

oauth_id_env_name = "TF_VAR_GENESYSCLOUD_OAUTHCLIENT_ID"
oauth_secret_env_name = "TF_VAR_GENESYSCLOUD_OAUTHCLIENT_SECRET"

# Authenticate with Genesys Cloud
def authenticate_genesyscloud():
    # Genesys Cloud Authentication
    try:
        if oauth_id_env_name in os.environ and oauth_secret_env_name in os.environ:

            apiclient = PureCloudPlatformClientV2.api_client.ApiClient().get_client_credentials_token(
                os.environ[oauth_id_env_name], os.environ[oauth_secret_env_name])
            api_instance = PureCloudPlatformClientV2.RoutingApi(apiclient)
            api_response = api_instance.get_routing_wrapupcodes()
        else:
            raise Exception("The environment variable does not exist.")
    except Exception as error:
        print("Error: " + repr(error))
    return api_instance


# Function to rename wrap-up code
def rename_wrapup_code(old_name, new_name):
    try:
        # Search for the wrap-up code by name (you might need to implement a search by name if API supports it)
        wrapup_codes = api_instance.get_routing_wrapupcodes(name=old_name)
        
        if wrapup_codes.entities:
            code_id = wrapup_codes.entities[0].id  # Assuming the first result is the correct one
            body = PureCloudPlatformClientV2.WrapupCodeRequest()
            body.name = new_name  # Set the new name

            # Update wrap-up code
            api_response = api_instance.put_routing_wrapupcode(code_id, body)
            pprint(api_response)
        else:
            print(f"Wrap-up code '{old_name}' not found.")
    
    except ApiException as e:
        print(f"Exception when renaming wrap-up code '{old_name}': {e}")

# Read the CSV file
def process_csv_and_rename(csv_file):
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)  # Reads the CSV into a dictionary
        for row in reader:
            old_name = row['name']
            new_name = row['rename']
            rename_wrapup_code(old_name, new_name)




if __name__ == "__main__":
    # Authenticate and get API handle
    api_instance = authenticate_genesyscloud()

    # Specify your CSV file path here
    csv_file_path = "rename_wrapup_codes.csv"

    # Process the CSV and rename wrap-up codes
    process_csv_and_rename(csv_file_path)
