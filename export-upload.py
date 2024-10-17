variable "local_folder_path" {
  default = "myfolder" # The folder containing files you want to upload
}

variable "s3_bucket" {
  default = aws_s3_bucket.my_bucket.bucket
}

# Get all files from the local folder
locals {
  files = fileset("${var.local_folder_path}", "**/*")
}

# Iterate over the files and upload each one
resource "aws_s3_bucket_object" "upload_files" {
  for_each = local.files

  bucket = var.s3_bucket
  key    = each.value   # This keeps the file path intact in the S3 bucket
  source = "${var.local_folder_path}/${each.value}" # The local file to upload
}
