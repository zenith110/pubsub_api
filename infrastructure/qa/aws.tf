resource "aws_s3_bucket" "terraform-state"{
    bucket = var.aws_s3_bucket_name
    versioning {
      enabled = true
    }
    server_side_encryption_configuration {
      rule{
          apply_server_side_encryption_by_default{
              sse_algorithm = "AES256"
          }
      }
    }
}
resource "aws_dynamodb_table" "terraform_locks"{
    hash_key = "LOCKID"
    name = var.dynamodb_table
    billing_mode = "PAY_PER_REQUEST"
    attribute {
      name = "LockID"
      type = "S"
    }
}