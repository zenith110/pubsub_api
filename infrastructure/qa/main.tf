terraform{
    required_providers{
        linode = {
            source = "linode/linode"
            version = "1.16.0"
        }
        cloudflare = {
        source = "cloudflare/cloudflare"
        version = "~> 3.0"
    }
        aws = {
            source = "hashicorp/aws"
            version = "~> 3.0"
        }
    }
   backend "s3" {
   key            = "state/terraform.tfstate"
   region         = "us-east-2"
   encrypt        = true
   kms_key_id     = "alias/terraform-bucket-key"
 }
}

provider "linode" {
    token = var.linode_api_token
}
provider "aws"{
    region = "us-east-2"
    access_key = var.aws_access_key
    secret_key = var.aws_secret_key
}
provider "cloudflare"{
    email = var.cloudflare_email
    api_key = var.cloudflare_api_key
}

