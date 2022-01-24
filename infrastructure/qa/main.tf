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
    backend "s3"{
        # Bucket config
        bucket = var.aws_s3_bucket_name
        key = var.aws_s3_key
        region = var.aws_region

        # DynamoDB table name
        dynamodb_table = var.dynamob_table
        encrypt = true
    }
}

provider "linode" {
    token = var.linode_api_token
}
provider "aws"{
    region = "us-east-1"
    access_key = var.aws_access_key
    secret_key = var.aws_secret_key
}
provider "cloudflare"{
    email = var.cloudflare_email
    api_key = var.cloudflare_api_key
}

