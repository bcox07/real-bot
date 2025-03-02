provider "aws" {
  region = "us-east-2"
}

resource "aws_s3_bucket" "lineup-clips1" {
   bucket = "lineup-clips1"
}

resource "aws_s3_object" "lineup-clips-ancient" {
  bucket = aws_s3_bucket.lineup-clips1.id
  key    = "ancient/"
}

resource "aws_s3_object" "lineup-clips-anubis" {
  bucket = aws_s3_bucket.lineup-clips1.id
  key    = "anubis/"
}