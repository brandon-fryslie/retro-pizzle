
// Provision ec2 instance
resource "aws_instance" "service" {
  # The connection block tells our provisioner how to
  # communicate with the resource (instance)
  connection {
    user = "centos"
    host = self.public_ip

    # Important: this connection requires the SSH key be added to the sshAgent before this code runs
  }

  # use a data provider to get the newest AMI
  ami = var.ami_id
  instance_type = var.instance_type
  key_name = var.key_pair
  associate_public_ip_address = true

  # Our Security group to allow HTTP and SSH access
  vpc_security_group_ids = [
    data.terraform_remote_state.general-networking.outputs.services_sg_id,
  ]

  tags = merge({Name = "review-extractor"}, local.base_tags)

  subnet_id = data.terraform_remote_state.general-networking.outputs.subnet_public_id

  # Regular fs data that will go away when we destroy the instance
  root_block_device {
    volume_type = "gp2"
    volume_size = 200
    delete_on_termination = true
  }
}
