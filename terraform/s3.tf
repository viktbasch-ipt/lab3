resource "aws_s3_bucket" "start" {
  bucket = "s3-start"
}

resource "aws_s3_bucket" "finish" {
  bucket = "s3-finish"
}