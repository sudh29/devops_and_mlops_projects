variable "usersage" {
  type = map(number)
  default = {
    user1 = 25
    user2 = 30
  }
}

variable "username" {
  type = string
}
