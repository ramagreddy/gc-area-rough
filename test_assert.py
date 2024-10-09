import PureCloudPlatformClientV2
from pprint import pprint
import os
import csv
import pytest
from PureCloudPlatformClientV2 import RoutingApi, ApiClient
from PureCloudPlatformClientV2.rest import ApiException
import logging

# Set logging level to DEBUG for the test session
logging.basicConfig(level=logging.DEBUG)

def test_example():
    logging.debug("This is a debug log")
    assert 1 == 1

region = PureCloudPlatformClientV2.PureCloudRegionHosts.eu_west_2
PureCloudPlatformClientV2.configuration.host = region.get_api_host()

oauth_id_env_name = "TF_VAR_GENESYSCLOUD_OAUTHCLIENT_ID"
oauth_secret_env_name = "TF_VAR_GENESYSCLOUD_OAUTHCLIENT_SECRET"



# Function to load wrap-up codes from CSV
def load_wrapup_codes_from_csv(csv_file):
    wrapup_codes = []
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:

            wrapup_codes.append({
                'name': row['name']
            })
    return wrapup_codes



@pytest.fixture
def genesys_api():
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

# Function to fetch wrap-up codes from Genesys Cloud
def fetch_wrapup_codes_from_genesys(api_instance, page_size=100, page_number=1):
    try:
        response = api_instance.get_routing_wrapupcodes(page_size=page_size, page_number=page_number)
        return response.entities
    except ApiException as e:
        print(f"Exception when calling RoutingApi->get_routing_wrapupcodes: {e}")
        return None


def test_wrapup_codes_exist_in_genesys(genesys_api):
    # Load wrap-up codes from CSV
    csv_wrapup_codes = load_wrapup_codes_from_csv('wrapup_codes.csv')

    # Fetch wrap-up codes from Genesys Cloud
    genesys_wrapup_codes = fetch_wrapup_codes_from_genesys(genesys_api)

    # Check if all CSV wrap-up codes exist in Genesys Cloud
    for csv_code in csv_wrapup_codes:
        assert any(gc.name == csv_code['name'] for gc in genesys_wrapup_codes), f"Wrap-up code {csv_code['name']} not found in Genesys Cloud"

