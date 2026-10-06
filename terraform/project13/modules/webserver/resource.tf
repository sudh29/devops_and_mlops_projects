# Create a key pair
resource "aws_key_pair" "aws_tf_key" {
  key_name   = var.key_name
  public_key = file("${path.module}/awstf.pub")
}

# Create the EC2 instance
resource "aws_instance" "web" {
  ami           = var.image_id
  instance_type = var.instance_type
  key_name      = aws_key_pair.aws_tf_key.key_name
  #   vpc_security_group_ids = [aws_security_group.allow_tls.id]

}
