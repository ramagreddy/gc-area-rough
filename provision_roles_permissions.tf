provider "genesyscloud" {
  environment  = "us-east-1" # Replace with your region
  access_token = var.access_token
}

# External data source to load permission policies
data "external" "permission_policies" {
  program = ["python3", "parse_permissions.py", "permissions.csv"]
}

# Create the Auth Role
resource "genesyscloud_auth_role" "agent_role" {
  name        = "Agent Role"
  description = "Custom Role for Agents"
  default     = false

  # Use dynamic block to process flattened permission policies
  dynamic "permission_policies" {
    for_each = data.external.permission_policies.result
    content {
      domain      = split(":", permission_policies.value)[0]
      entity_name = split(":", permission_policies.value)[1]
      action_set  = split(",", split(":", permission_policies.value)[2])
    }
  }
}
