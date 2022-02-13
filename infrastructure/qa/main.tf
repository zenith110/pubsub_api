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
 }
}

output backend_ip_address{
    value = data.terraform_remote_state.sync.outputs.ip_address
}



