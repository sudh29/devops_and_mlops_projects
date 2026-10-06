# Create an S3 bucket for Terraform backend storage
#   Bucket name: "terrabackendtest"
#
# Create a DynamoDB table for state locking
#   Table name: "terrabackendtest-table"
#   Primary key (partition key): "LockID"


terraform {
  backend "s3" {
    bucket         = "terrabackendtest"
    key            = "terraform.tfstate"
    region         = "ap-south-1"
    dynamodb_table = "terrabackendtest-table"
  }
}

variable "access_key" {
  type        = string
  description = "AWS access key"
}

variable "secret_key" {
  type        = string
  description = "AWS secret key"
}

provider "aws" {
  region     = "ap-south-1"
  access_key = var.access_key
  secret_key = var.secret_key
}

resource "aws_instance" "web" {
  ami           = "ami-0f918f7e67a3323f0"
  instance_type = "t3.micro"
}
