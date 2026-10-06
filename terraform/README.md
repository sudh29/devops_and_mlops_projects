# Terraform Projects Collection

This repository contains various Terraform projects for infrastructure provisioning and management.

## Setup and Prerequisites

### Prerequisites

- [Terraform CLI](https://developer.hashicorp.com/terraform/install) (v1.5+ recommended) installed.
- AWS CLI configured with valid credentials (`aws configure` or environment variables `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`).

### AWS Authentication Setup

1. SSH Key Generation:

```bash
# Generate SSH key pair for AWS EC2 instances
ssh-keygen -t rsa -b 4096 -C "aws_tf_key"
```

2. AWS Credentials:
   - Configure AWS credentials using AWS CLI or environment variables
   - Ensure your AWS credentials are stored in `~/.aws/credentials` or set as environment variables

## Terraform Commands Reference

### Basic Workflow Commands

```bash
# Initialize and validate
terraform init        # Initialize Terraform working directory and download providers
terraform fmt        # Format the Terraform code for consistency
terraform validate   # Validate the configuration syntax and consistency

# Plan and apply changes
terraform plan       # Preview the infrastructure changes (always run this first)
terraform apply      # Apply the changes to create/modify infrastructure
terraform destroy    # Destroy all managed infrastructure

# Common flags
-auto-approve        # Skip interactive approval (use with caution)
-target=resource     # Target specific resource(s)
-var-file=file.tfvars # Use specific variable file
```

### Working with Variables

```bash
# Variable file usage
terraform plan -var-file=dev.tfvars           # Use dev environment variables
terraform plan -var-file=prod.tfvars          # Use production environment variables

# Environment variables
export TF_VAR_variable_name=value             # Set Terraform variables via environment
export AWS_PROFILE=profile_name               # Set AWS profile

# State management
terraform state list                          # List resources in state
terraform show                                # Show current state details
terraform output                              # Show output values
terraform refresh                             # Update state file against real resources
```

### Working with Workspaces

Workspaces help manage multiple states for the same configuration (e.g., dev, staging, prod):

```bash
# List and manage workspaces
terraform workspace list     # Show all workspaces
terraform workspace show    # Show current workspace
terraform workspace new dev    # Create and switch to new workspace
terraform workspace select dev # Switch to existing workspace
terraform workspace delete dev # Delete a workspace (must not be current)
```

### Additional Tools

```bash
# Visualization
terraform graph | dot -Tpdf > graph.pdf    # Generate infrastructure graph

# SSH Access
ssh -i <key_file> ubuntu@<instance_ip>    # SSH into EC2 instance
```

## Best Practices

1. **State Management**

   - Always backup state files
   - Use remote state storage (e.g., S3) in production
   - Enable state locking to prevent concurrent modifications

2. **Security**

   - Keep sensitive data in separate variable files
   - Never commit sensitive data to version control
   - Review security group configurations thoroughly
   - Use principle of least privilege for AWS IAM roles

3. **Development Workflow**

   - Always run `terraform fmt` before committing
   - Always run `terraform plan` before applying
   - Use workspaces to manage multiple environments
   - Use version control for all Terraform code
   - Document your infrastructure with comments

4. **Resource Management**
   - Use tags for resource organization
   - Implement proper resource naming conventions
   - Clean up unused resources to avoid costs
   - Use data sources instead of hardcoding values

## Important Notes

- Use `--auto-approve` flags with extreme caution in production
- Regularly update provider versions for security patches
- Consider using terragrunt for large infrastructures
- Implement proper backend configuration for state files
