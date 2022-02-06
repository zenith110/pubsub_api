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
        vercel = {
            source = "vercel/vercel"
            version = "~> 0.1"
        }
    }
}
output ip_address{
    value = linode_instance.pubsub-qa.ip_address
}
output vercel_deployment_url{
    value = vercel_deployment.example.url
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
provider "vercel"{
    api_token = var.vercel_api_token
}
