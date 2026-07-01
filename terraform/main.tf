terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.23"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.12"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC и подсети
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"

  name = "lexicon-vpc"
  cidr = "10.0.0.0/16"
  azs  = ["${var.aws_region}a", "${var.aws_region}b", "${var.aws_region}c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
  enable_nat_gateway = true
  single_nat_gateway = true
}

# EKS кластер
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "19.16.0"

  cluster_name    = "lexicon"
  cluster_version = "1.27"
  subnet_ids      = module.vpc.private_subnets

  vpc_id = module.vpc.vpc_id

  eks_managed_node_groups = {
    main = {
      min_size     = 2
      max_size     = 10
      desired_size = 3
      instance_types = ["t3.medium"]
    }
  }
}

# RDS PostgreSQL
resource "aws_db_instance" "postgres" {
  identifier = "lexicon-db"
  engine     = "postgres"
  engine_version = "16.1"
  instance_class = "db.t3.micro"
  db_name  = "lexicon"
  username = var.db_username
  password = var.db_password
  skip_final_snapshot = true
}

# MSK (Kafka)
module "msk" {
  source = "clowdhaus/msk/aws"
  version = "1.0.0"

  cluster_name   = "lexicon-msk"
  kafka_version  = "3.6.0"
  number_of_broker_nodes = 3
  broker_instance_type  = "kafka.t3.small"
  subnet_ids     = module.vpc.private_subnets
}
