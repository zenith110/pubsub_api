resource "cloudflare_record" "qa-graphql"{
    zone_id = var.cloudflare_zone_id
    name  = var.qa-graphql
    value = linode_instance.pubsub-qa.ip_address
    type = "A"
    proxied = true
}

resource "cloudflare_record" "qa-backend"{
    zone_id = var.cloudflare_zone_id
    name  = var.qa-backend
    value = linode_instance.pubsub-qa.ip_address
    type = "A"
    proxied = true
}

resource "cloudflare_record" "qa-frontend"{
    zone_id = var.cloudflare_zone_id
    name  = var.qa-frontend
    value = vercel_deployment.example.url
    type = "A"
    proxied = true
}