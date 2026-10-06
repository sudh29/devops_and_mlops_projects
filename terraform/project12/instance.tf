data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical
  filter {
    name   = "name"
    values = ["${var.image_name}"]
  }
  filter {
    name   = "root-device-type"
    values = ["ebs"]
  }
  filter {
    name   = "architecture"
    values = ["x86_64"]
  }
}

# Create the EC2 instance
resource "aws_instance" "web" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.instance_type
  key_name               = aws_key_pair.aws_tf_key.key_name
  vpc_security_group_ids = [aws_security_group.allow_tls.id]
  tags = {
    Name = "first_tf_instance"
  }
  user_data = file("${path.module}/script.sh")

  connection {
    type        = "ssh"
    host        = self.public_ip
    user        = "ubuntu"
    private_key = file("${path.module}/awstf")
  }
  # file, local-exec, remote-exec
  provisioner "file" {
    source      = "${path.module}/script.sh" # terraform machine
    destination = "/tmp/script.sh"           # remote machine

  }
  provisioner "file" {
    content     = "This is test content."
    destination = "/tmp/test.md" # remote machine
  }

  provisioner "local-exec" {
    on_failure  = continue
    working_dir = path.module
    command     = "echo ${self.public_ip} > instance_ip.txt"
  }

  provisioner "local-exec" {
    command = "echo 'At create'"
  }

  provisioner "local-exec" {
    when    = destroy
    command = "echo 'At destroy'"
  }

  provisioner "remote-exec" {
    inline = [
      "ip addr show > /tmp/ip_addr.output",
      "echo 'This is a remote execution' > /tmp/remote_execution.text"
    ]
  }

  provisioner "remote-exec" {
    script = "${path.module}/test.sh"
  }
}