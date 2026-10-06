variable "usersage" {
  type = map(any)
  default = {
    user1 = 25
    user2 = 30
  }
}

variable "username" {
  type = string
}