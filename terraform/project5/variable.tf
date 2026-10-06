variable "username" {
  type = string
}

variable "userid" {
  type    = number
  default = 123
}

variable "users" {
  type    = list(string)
  default = ["user1", "user2", "user3"]
}