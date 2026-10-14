terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "k12_data" {
  bucket = "k12-data-platform-gokhan"
}
resource "aws_s3_bucket_public_access_block" "k12_data" {
  bucket = aws_s3_bucket.k12_data.id

  block_public_acls       = true
  ignore_public_acls      = true
  block_public_policy     = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "k12_data" {
  bucket = aws_s3_bucket.k12_data.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_notification" "snowpipe_attendance" {
  bucket = aws_s3_bucket.k12_data.id

  queue {
    queue_arn     = var.snowpipe_sqs_arn
    events        = ["s3:ObjectCreated:*"]
    filter_prefix = "raw/attendance/"
  }
}