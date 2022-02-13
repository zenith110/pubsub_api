terraform{
    required_providers{
        aws = {
            source = "hashicorp/aws"
            version = "~> 3.0"
        }
    }
   backend "s3" {
   key            = "state/terraform.tfstate"
   region         = "us-east-2"
   encrypt        = true
 }
}

data "terraform_remote_state" "sync"{
   backend = "s3"
   config = {
   bucket = var.aws_s3_bucket_name
   key            = "state/terraform.tfstate"
   region         = "us-east-2"
   encrypt        = true
   access_key = var.aws_access_key
   secret_key = var.aws_secret_key
 }
}




