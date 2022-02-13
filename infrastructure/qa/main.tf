terraform{
    required_providers{
        linode = {
            source = "linode/linode"
            version = "1.16.0"
        }
    }
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

provider "linode" {
    token = var.linode_api_token
}
output ip_address{
    value = linode_instance.pubsub-qa.ip_address
}



