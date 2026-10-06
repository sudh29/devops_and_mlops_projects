# Static user lookup
output "userage" {
  value = "My name is user1 and my age is ${var.usersage["user1"]}"
}

# Dynamic user lookup
output "useragedynamic" {
  value = "My name is ${var.username} and my age is ${var.usersage[var.username]}"
}
