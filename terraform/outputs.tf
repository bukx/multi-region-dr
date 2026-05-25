output "primary_bucket_name" {
  value = aws_s3_bucket.primary.bucket
}

output "secondary_bucket_name" {
  value = aws_s3_bucket.secondary.bucket
}

output "dynamodb_table_name" {
  value = aws_dynamodb_table.orders.name
}

output "failover_record_fqdn" {
  value       = var.record_name
  description = "DNS name used for Route 53 failover."
}
