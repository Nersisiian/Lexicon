output "eks_cluster_endpoint" {
  value = module.eks.cluster_endpoint
}

output "rds_endpoint" {
  value = aws_db_instance.postgres.endpoint
}

output "msk_bootstrap_brokers" {
  value = module.msk.bootstrap_brokers
}
