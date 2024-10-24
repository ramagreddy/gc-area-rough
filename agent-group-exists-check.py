# Initialize the API client
api_instance = PureCloudPlatformClientV2.GroupsApi()

def get_agent_groups():
    """Fetches all agent groups in Genesys Cloud."""
    try:
        groups = []
        # Paginate through all groups if necessary
        page_number = 1
        page_size = 50  # Adjust as needed
        while True:
            group_list = api_instance.get_groups(page_number=page_number, page_size=page_size)
            groups.extend(group_list.entities)

            # Check if more pages exist
            if not group_list.page_count or page_number >= group_list.page_count:
                break
            page_number += 1

        return groups
    except ApiException as e:
        print(f"Error fetching agent groups: {e}")
        return []

def check_group_exists(group_name, groups):
    """Checks if a given group name exists in the list of groups."""
    for group in groups:
        if group.name == group_name:
            return True
    return False

if __name__ == "__main__":
    group_name_to_check = "Test"  # Replace with the name you want to check

    # Fetch agent groups
    agent_groups = get_agent_groups()

    # Check if the given group name exists
    if check_group_exists(group_name_to_check, agent_groups):
        print(f"Group '{group_name_to_check}' exists.")
    else:
        print(f"Group '{group_name_to_check}' does not exist.")
