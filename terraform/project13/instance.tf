module "webserver" {
  source        = "./modules/webserver"
  key           = file("${path.module}/awstf")
  image_id      = var.image_name
  instance_type = var.instance_type
  key_name      = var.key_name
}

output "publicIP" {
  value = module.webserver.publicIP
}