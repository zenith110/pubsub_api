resource "linode_instance" "pubsub-qa" {
    image = "linode/ubuntu21.04"
    label = var.qa_label
    group = var.qa_group
    region = var.linode_region
    swap_size = 1024
    root_pass = var.linode_password
    type = var.small_linode_instance
}
