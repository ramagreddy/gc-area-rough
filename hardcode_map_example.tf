resource "genesyscloud_routing_wrapupcode" "wrapup_codes_new3" {
  for_each = data.external.wrapup_codes.result

  # Decode the JSON string into a map
  name           = "dev-test3"
  division_id    = var.division_ids["All"]

}
#data "genesyscloud_routing_wrapupcode" "existing-wrapupcodes" {
#  for_each = data.external.wrapup_codes.result

  # Decode the JSON string into a map
#  name        = jsondecode(each.value)["name"]
#}
//
variable "division_ids" {
  description = "Map of wrap-up codes and their corresponding division IDs"
  type        = map(string)
  default = {
    "Home"      = "3c33ce24-8085-4728-afdb-a48b6a362adc"
    "Training"  = "126544af-2d81-43dd-9186-740c7bf4327b"
    "All"         = "*"
  }
}
