data "terraform_remote_state" "sync"{
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

output backend_ip_address{
    value = data.terraform_remote_state.sync.ip_address
}



