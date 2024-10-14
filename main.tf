resource "null_resource" "run_python_script" {
  provisioner "local-exec" {
    command = "python3 ${path.module}/append_csv.py"
  }

  # Triggers force the resource to run if they change
  triggers = {
    always_run = "${timestamp()}"
  }
}

data "external" "wrapup_codes" {
  program = ["python3", "${path.module}/parse_csv.py", "${path.module}/wrapup_codes.csv"]
}

resource "genesyscloud_routing_wrapupcode" "wrapup_codes" {
  for_each = data.external.wrapup_codes.result

  # Decode the JSON string into a map
  name        = jsondecode(each.value)["name"]
}
