resource "cloudflare_record" "server"{
    zone_id = var.cloudflare_zone_id
    name  = var.cloudflare_domain_name
    value = linode_instance.pubsub-qa.ip_address
    type = "A"
    proxied = false
}