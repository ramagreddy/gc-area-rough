variable "division_ids_list" {
  description = "Map of wrap-up codes and their corresponding division IDs"
  type        = set(string)
  default     = ["Home","Training","All"]
}

# Fetch division information dynamically using name from a set of names
data "genesyscloud_auth_division" "divisions" {
  for_each = var.division_ids_list
  name     = each.value  # Fetch division by name
}
