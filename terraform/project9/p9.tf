provider "github" {
  token = ""
}

resource "github_repository" "terraform_myrepo" {
  name        = "myrepo_by_terraform"
  description = "Liber codebase"
  visibility  = "public"
  auto_init   = true
}