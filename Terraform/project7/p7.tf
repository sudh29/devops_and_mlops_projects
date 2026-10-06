output "userage" {
  value = "My name is  user1 and my age is ${lookup(var.usersage, "user1")}"
}

output "useragedynamic" {
  value = "My name is  ${var.username} and my age is ${lookup(var.usersage, var.username)}"
}