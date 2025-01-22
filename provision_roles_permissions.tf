provider "genesyscloud" {
  environment  = "us-east-1" # Replace with your region
  access_token = var.access_token
}

# Load permissions from the external script
data "external" "permission_policies" {
  program = ["python3", "parse_permissions.py", "permissions.csv"]
}

# Create the Auth Role
resource "genesyscloud_auth_role" "agent_role" {
  name        = "Agent Role"
  description = "Custom Role for Agents"
  default     = false

  dynamic "permission_policies" {
    for_each = data.external.permission_policies.result["permission_policies"]
    content {
      domain      = permission_policies.value["domain"]
      entity_name = permission_policies.value["entity_name"]
      action_set  = permission_policies.value["action_set"]
    }
  }
}

