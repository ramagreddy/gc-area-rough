import PureCloudPlatformClientV2
from PureCloudPlatformClientV2.rest import ApiException
import sys

# Configure OAuth2 access token for authorization
api_instance = PureCloudPlatformClientV2.RoutingApi()

# Function to fetch wrap-up codes and return a list of existing codes based on names
def search_wrapup_codes_by_name(wrapup_code_names):
    existing_wrapup_codes = []
    
    try:
        # Fetch all wrap-up codes
        response = api_instance.get_routing_wrapupcodes()
        # Iterate through the provided names and check if they exist in the fetched wrap-up codes
        for code_name in wrapup_code_names:
            for code in response.entities:
                if code.name == code_name:
                    existing_wrapup_codes.append(code_name)
                    print(f"Wrap-up code found: {code_name}")
                    break  # Exit the loop once found
    except ApiException as e:
        print(f"Error while fetching wrap-up codes: {e}")
        sys.exit(1)  # Exit with error status if an API exception occurs
    
    return existing_wrapup_codes

def main():
    # List of wrap-up code names to search for
    wrapup_code_names = ['Code1', 'Code2', 'Code3']  # Replace with your wrap-up code names

    # Search for the wrap-up codes by name
    existing_wrapup_codes = search_wrapup_codes_by_name(wrapup_code_names)

    # If any wrap-up codes are found, print them and fail the script
    if existing_wrapup_codes:
        print(f"Existing wrap-up codes: {existing_wrapup_codes}")
        sys.exit(1)  # Exit with error status to fail the pipeline
    else:
        print("No matching wrap-up codes found.")
        sys.exit(0)  # Success

if __name__ == "__main__":
    main()
