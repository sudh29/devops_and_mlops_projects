output "print_username" {
  value       = "Hello, ${var.username}"
  sensitive   = false
  description = "description"
  depends_on  = []
}


output "print_user_id" {
  value       = "Hello, ${var.userid}"
  sensitive   = false
  description = "description"
  depends_on  = []
}

output "print_users" {
  value       = "Hello, ${join(", ", var.users)}"
  sensitive   = false
  description = "description"
  depends_on  = []
}

# terraform plan
# terraform plan -var 'username=JohnDoe'
# terraform plan -var 'username=JohnDoe' -var 'userid=456'
# terraform plan -var 'username=JohnDoe' -var 'userid=456' -var 'users=["Alice", "Bob", "Charlie"]'