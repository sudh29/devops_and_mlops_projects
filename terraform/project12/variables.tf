variable "access_key" {
  description = "AWS Access Key"
  type        = string
  sensitive   = true
}

variable "secret_key" {
  description = "AWS Secret Key"
  type        = string
  sensitive   = true
}

variable "ports" {
  type = list(number)
}

variable "instance_type" {
  description = "The type of instance to use"
  type        = string
}

variable "image_name" {
  description = "The name of the AMI to use for the instance"
  type        = string
}