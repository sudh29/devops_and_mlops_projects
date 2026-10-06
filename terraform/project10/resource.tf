resource "github_repository" "terraform_myrepo" {
  name        = "myrepo_by_terraform"
  description = "Liber codebase"
  visibility  = "public"
  auto_init   = true
}

output "repository_url" {
  value = github_repository.terraform_myrepo.html_url
}
