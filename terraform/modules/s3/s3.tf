provider "aws" {
  region  = "us-east-2"
  profile = "superuser"
}

resource "aws_s3_bucket" "lineup-clips2" {
  bucket = "lineup-clips2"
  lifecycle {
    prevent_destroy = true
  }
}

variable "s3_object_names" {
  type    = list(string)
  default = ["ancient/", "anubis/", "dust2/", "inferno/", "mirage/", "train/", "cache/"]
}

resource "aws_s3_object" "lineup-clips-object" {
  count = length(var.s3_object_names)
  bucket = aws_s3_bucket.lineup-clips2.id
  key = var.s3_object_names[count.index]
}
