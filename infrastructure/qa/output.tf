output "server_ip" {
  description = "server ip for the qa'd server"
  value = linode_instance.pubsub-qa.ip_address
}