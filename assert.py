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
            #authApi = PureCloudPlatformClientV2.AuthorizationApi(apiclient)
            api_instance = PureCloudPlatformClientV2.RoutingApi(apiclient)
            api_response = api_instance.get_routing_wrapupcodes()
            pprint(api_response.entities)
        else:
            raise Exception("The environment variable does not exist.")
    except Exception as error:
        print("Error: " + repr(error))
            #print(authApi.get_authorization_permissions())  
    return api_instance


# Read wrap-up codes from CSV
def read_wrapup_codes_from_csv(file_path):
    wrapup_codes = []
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            wrapup_codes.append(row['name'])
    return wrapup_codes


# Check if wrap-up codes exist in Genesys Cloud
def check_wrapup_codes(wrapup_api, wrapup_codes):
    all_codes = wrapup_api.get_routing_wrapupcodes().entities
    all_code_names = [code.name for code in all_codes]

    for code in wrapup_codes:
        if code in all_code_names:
            print(f"Wrap-up code '{code}' already exists in Genesys Cloud.")
        else:
            print(f"Wrap-up code '{code}' is NOT found in Genesys Cloud.")


if __name__ == "__main__":
    # Authenticate and get API handle
    wrapup_api = authenticate_genesyscloud()

    # Specify your CSV file path here
    csv_file_path = "wrapup_codes.csv"
    
    # Read wrap-up codes from the CSV file
    wrapup_codes = read_wrapup_codes_from_csv(csv_file_path)

    # Check if the wrap-up codes exist in Genesys Cloud
    check_wrapup_codes(wrapup_api, wrapup_codes)
