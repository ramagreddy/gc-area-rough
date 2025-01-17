provider "genesyscloud" {
  environment  = "us-east-1" # Replace with your region
  access_token = var.access_token
}

# External data source to fetch role permissions from CSV files
data "external" "roles" {
  program = ["python3", "parse_roles.py", "roles"]
}

# Iterate over the roles and create resources dynamically
resource "genesyscloud_auth_role" "dynamic_roles" {
  for_each = data.external.roles.result["roles"]

  name        = each.key
  description = "Role created from CSV: ${each.key}"
  default     = false

  dynamic "permissions" {
    for_each = each.value
    content {
      value = permissions.value
    }
  }
}
