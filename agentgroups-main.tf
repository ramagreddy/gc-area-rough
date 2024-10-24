
name,rename,description,type,visibility,rules_visible,owner_ids,member_ids,addresses.phone,addresses.type
dev-group1,,,,public,true,"user1,user2",,+123456789,GROUPRING
dev-group2,,,,public,true,user2,,+123456789,GROUPRING
dev-group3,,,,public,true,user3,,+123456789,GROUPRING


locals {
  csv_content = file("${path.module}/input.csv")
  decoded_csv = csvdecode(local.csv_content)
  
  # Create a map of groups using the "name" column, excluding empty names
  groups_map = { for row in local.decoded_csv : row["name"] => row if row["name"] != "" }
}

resource "genesyscloud_group" "sample_group" {
  for_each = local.groups_map

  # The group name
  name = each.key

  # Default to "false" if "rules_visible" is empty
  rules_visible = each.value["rules_visible"] != "" ? each.value["rules_visible"] : "false"

  # Default to an empty set if "member_ids" is empty
  member_ids = each.value["member_ids"] != "" ? toset(split(",", each.value["member_ids"])) : toset([])

  # Optional addresses block
   dynamic "addresses" {
    for_each = each.value["addresses.phone"] != "" ? [each.value] : []
    content {
      number = addresses.value["addresses.phone"]
      type   = addresses.value["addresses.type"] != "" ? addresses.value["addresses.type"] : "GROUPRING"
    }
  }
}
