variable "image_id" {
  type        = string
  default     = "ami-0f918f7e67a3323f0"
  description = "The ID of the AMI to use for the instance"
}

variable "instance_type" {
  type        = string
  default     = "t3.micro"
  description = "The type of instance to use"
}

variable "key" {
  type        = string
  default     = ""
  description = "The key pair to use for the instance"
}

variable "key_name" {
  type        = string
  default     = "aws_tf_key"
  description = "The name of the key pair to use for the instance"
}