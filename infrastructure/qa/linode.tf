resource "linode_instance" "pubsub-qa" {
    image = "linode/ubuntu21.04"
    label = var.qa_label
    group = var.qa_group
    region = var.linode_region
    swap_size = 1024
    root_pass = var.linode_password
    type = var.small_linode_instance
}

resource "linode_firewall" "pubsub-qa-firewall"{
    label = var.qa_label
    inbound {
      label = "allow-http"
      action = "ACCEPT"
      protcol = "TCP"
      ports = "80"
      ipv4 = ["0.0.0.0/0"]
      ipv6 = ["::/0"]
    }

    inbound {
    label    = "allow-https"
    action   = "ACCEPT"
    protocol = "TCP"
    ports    = "443"
    ipv4     = ["0.0.0.0/0"]
    ipv6     = ["::/0"]
  }
}
