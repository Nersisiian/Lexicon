# Terraform for Lexicon Infrastructure

Deploys: VPC, EKS, RDS PostgreSQL, MSK Kafka.

## Quick Start
1. Install Terraform: https://developer.hashicorp.com/terraform/downloads
2. Configure AWS credentials:
   ```bash
   export AWS_ACCESS_KEY_ID=...
   export AWS_SECRET_ACCESS_KEY=...
Initialize and apply:

bash
cd terraform
terraform init
terraform apply -var="db_username=admin" -var="db_password=yourpassword"
After apply, configure kubectl:

bash
aws eks update-kubeconfig --region us-east-1 --name lexicon
