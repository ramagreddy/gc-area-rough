locals {
  csv_content = file("${path.module}/input.csv")
  decoded_csv = csvdecode(local.csv_content)
  # Create a map of wrap-up codes by using the "Name" column
  wrapup_codes_map = { for row in local.decoded_csv : row["name"] => row if row["name"] != "" }
  divisions_map = {
    "Home" = {
      division_id   = "3c33ce24-8085-4728-afdb-a48b6a362adc"
    }
    "Training" = {
      division_id   = "126544af-2d81-43dd-9186-740c7bf4327b"
    }
    "All" = {
      division_id   = "*"
    }
  }
}

resource "genesyscloud_routing_wrapupcode" "dev-wrapup-codes" {
  for_each = local.wrapup_codes_map

  name = each.key # 'each.key' refers to the wrap-up code name (from the CSV)
  division_id = local.divisions_map[each.value.division]["division_id"]
  
  # Add any additional fields you need from the CSV, e.g.
  # division = each.value["division"] 
}
