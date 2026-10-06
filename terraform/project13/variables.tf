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

variable "instance_type" {
  description = "The type of instance to use"
  type        = string
}

variable "image_name" {
  description = "The name of the AMI to use for the instance"
  type        = string
}

variable "key_name" {
  description = "The name of the key pair to use for the instance"
  type        = string
}