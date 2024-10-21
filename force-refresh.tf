resource "null_resource" "force_refresh" {
  triggers = {
    always_run = "${timestamp()}"  # Forces this resource to run every time
  }
}

data "genesyscloud_routing_wrapupcode" "example" {
  name = "Wrapup Code Example"
  
  # Depend on the null_resource so that this data block refreshes every run
  depends_on = [null_resource.force_refresh]
}
