import PureCloudPlatformClientV2
from PureCloudPlatformClientV2.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization
config = PureCloudPlatformClientV2.Configuration()
config.access_token = 'your_access_token'  # Replace with your actual token

# Create an API client instance
api_instance = PureCloudPlatformClientV2.RoutingApi(PureCloudPlatformClientV2.ApiClient(config))

# Initial pagination parameters
page_size = 25  # Maximum number of skill groups per page
next_page_token = None  # Cursor for the next page
all_skill_groups = []  # List to collect all skill groups

try:
    # Loop to fetch each page of skill groups
    while True:
        # Fetch a page of skill groups
        api_response = api_instance.get_routing_skillgroups(
            page_size=page_size,
            after=next_page_token  # Use the 'after' parameter for cursor-based pagination
        )

        # Add the entities (skill groups) from this page to the collection
        if isinstance(api_response.entities, list):
            all_skill_groups.extend(api_response.entities)
        else:
            print("Unexpected data format:", type(api_response.entities))
            break

        # Check if there's a next page; if not, break the loop
        if not api_response.next_page:
            break

        # Update the cursor for the next request
        next_page_token = api_response.next_page

    # Display all collected skill groups
    for skill_group in all_skill_groups:
        pprint(skill_group)  # Prints each skill group's details

except ApiException as e:
    print("Exception when calling RoutingApi->get_routing_skillgroups: %s\n" % e)
