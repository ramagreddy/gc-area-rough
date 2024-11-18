import PureCloudPlatformClientV2
from PureCloudPlatformClientV2.rest import ApiException
from pprint import pprint
import os
import csv
import pytest
import pandas as pd

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
            api_instance = PureCloudPlatformClientV2.UsersApi(apiclient)
        else:
            raise Exception("The environment variable does not exist.")
    except Exception as error:
        print("Error: " + repr(error))
    return api_instance

api_instance = authenticate_genesyscloud()

# Set initial pagination parameters
page_size = 25         # Number of users per page (maximum is usually around 100)
page_number = 1        # Start at the first page
all_users = []         # List to collect all users

try:
    # Paginate through all users
    while True:
        # Fetch a page of users
        api_response = api_instance.get_users(
            page_size=page_size,
            page_number=page_number,
            sort_order='ASC',
            state='active'
        )
        
        # Add the users from this page to the all_users list
        all_users.extend(api_response.entities)
        
        # Check if there are more pages
        if api_response.page_number * api_response.page_size >= api_response.total:
            # If we've reached the last page, break the loop
            break
        
        # Increment the page number to fetch the next page
        page_number += 1
    # Display all collected users
    for user in all_users:
        pprint(user.id)  # Prints each user's details        

    # Print or process all retrieved users
    #pprint(all_users)
    #pprint(api_response.total)

except ApiException as e:
    print("Exception when calling UsersApi->get_users: %s\n" % e)
