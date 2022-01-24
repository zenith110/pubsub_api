variable "linode_api_token" {}
variable "linode_password" {}
# variable "ssh_key" {}
variable "small_linode_instance" {}
variable "linode_region" {
    default = "us-east"
}
variable "cloudflare_zone_id" {}
variable "cloudflare_domain_name" {}
variable "qa_label" {}
variable "qa_group" {}
variable "cloudflare_email" {}
variable "cloudflare_api_key" {}
variable "aws_s3_bucket_name" {}
variable "aws_s3_key" {}
variable "aws_region" {}
variable "aws_access_key"
variable "aws_secret_key"
variable "dynamob_table" {}