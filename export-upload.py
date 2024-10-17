provider "aws" {
  region = "us-west-2"
}

resource "aws_s3_bucket" "example" {
  bucket = "my-bucket-for-forced-object"
  acl    = "private"
}

resource "null_resource" "force_create" {
  # This will trigger every time based on the timestamp
  triggers = {
    always_run = timestamp()
  }

  # Use the local-exec provisioner to run any shell commands if needed (optional)
  provisioner "local-exec" {
    command = "echo 'Forcing S3 object upload on every run'"
  }

  depends_on = [aws_s3_bucket.example]
}

resource "aws_s3_object" "example" {
  bucket = aws_s3_bucket.example.bucket
  key    = "myfile.txt"
  source = "path/to/your/local/file.txt"
  etag   = filemd5("path/to/your/local/file.txt") # This keeps track of changes to the file content

  # Depends on the null_resource to force execution on every run
  depends_on = [null_resource.force_create]
}
