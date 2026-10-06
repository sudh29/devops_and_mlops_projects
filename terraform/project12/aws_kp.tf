# Create a key pair
resource "aws_key_pair" "aws_tf_key" {
  key_name   = "aws_tf_key"
  public_key = file("${path.module}/awstf.pub")
}

output "keyname" {
  value = aws_key_pair.aws_tf_key.key_name
}
