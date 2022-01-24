resource "cloudflare_record" "server"{
    zone_id = var.cloudflare_zone_id
    name  = var.cloudflare_domain_name
    value = linode_instance.pubsub-qa.ip_address
    type = "A"
    proxied = true
}

resource "cloudflare_record" "qa-graphql"{
    zone_id = var.cloudflare_zone_id
    name  = qa-grapqhl.pubsub-api.dev
    value = linode_instance.pubsub-qa.ip_address
    type = "A"
    proxied = true
}

resource "cloudflare_record" "qa-backend"{
    zone_id = var.cloudflare_zone_id
    name  = qa-backend.pubsub-api.dev
    value = linode_instance.pubsub-qa.ip_address
    type = "A"
    proxied = true
}