output "first_block" {
  value       = "This is first block"
  sensitive   = true
  description = "description first block"
  depends_on  = []
}

output "second_block" {
  value       = "This is second block"
  sensitive   = true
  description = "description second block"
  depends_on  = []
}

output "third_block" {
  value       = "This is third block"
  sensitive   = false
  description = "description third block"
  depends_on  = []
}