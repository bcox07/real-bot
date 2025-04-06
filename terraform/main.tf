terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region  = "us-east-2"
  profile = "superuser"
}

module "ecs" {
  source = "./modules/ecs"
}

module "s3" {
  source = "./modules/s3"
}

//module "auto_scaling" {
//  source = "./modules/auto_scaling"
//}

module "dynamodb" {
  source = "./modules/dynamo"
}

import {
  to = module.s3.aws_s3_bucket.lineup-clips
  id = "lineup-clips"
}
