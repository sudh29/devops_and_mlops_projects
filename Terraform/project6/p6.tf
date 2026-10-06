output "print_users" {
  value       = "Hello, ${join("-->", var.users)}"
  sensitive   = false
  description = "description"
  depends_on  = []
}

output "print_users_lower" {
  value       = "Hello, ${join("-->", [for u in var.users : lower(u)])}"
  sensitive   = false
  description = "description"
  depends_on  = []
}

output "print_users_upper" {
  value       = "Hello, ${join("-->", [for u in var.users : upper(u)])}"
  sensitive   = false
  description = "description"
  depends_on  = []
}