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
    }
}
provider "linode" {
    token = var.linode_api_token
}
output "server_ip" {
  value = linode_instance.pubsub-qa.ip_address
}
provider "cloudflare"{
    email = var.cloudflare_email
    api_key =  var.cloudflare_api_key
}

