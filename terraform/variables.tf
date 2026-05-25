variable "project_name" {
  type        = string
  description = "Name prefix for tagged resources."
  default     = "multi-region-dr"
}

variable "primary_region" {
  type    = string
  default = "us-east-1"
}

variable "secondary_region" {
  type    = string
  default = "us-west-2"
}

variable "primary_bucket_name" {
  type        = string
  description = "Globally unique S3 bucket name for the primary region."
}

variable "secondary_bucket_name" {
  type        = string
  description = "Globally unique S3 bucket name for the secondary region."
}

variable "dynamodb_table_name" {
  type    = string
  default = "dr-orders"
}

variable "route53_zone_id" {
  type        = string
  description = "Hosted zone ID for the failover record."
  default     = ""
}

variable "record_name" {
  type        = string
  description = "Fully qualified DNS name for the failover record."
  default     = ""
}

variable "primary_endpoint" {
  type        = string
  description = "Primary application DNS endpoint used by Route 53 failover."
  default     = ""
}

variable "secondary_endpoint" {
  type        = string
  description = "Secondary application DNS endpoint used by Route 53 failover."
  default     = ""
}

variable "health_check_path" {
  type    = string
  default = "/health"
}

variable "health_check_port" {
  type    = number
  default = 443
}

variable "health_check_type" {
  type    = string
  default = "HTTPS"
}

variable "tags" {
  type    = map(string)
  default = {}
}

variable "enable_deletion_protection" {
  type    = bool
  default = true
}
