provider "aws" {
  region  = "us-east-2"
  profile = "superuser"
}

resource "aws_dynamodb_table" "lineup-table" {
  name           = "Lineups"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "Map"

  attribute {
    name = "Map"
    type = "S"
  }
}