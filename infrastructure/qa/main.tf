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



