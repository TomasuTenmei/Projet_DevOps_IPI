# Ce fichier contient la configuration Terraform pour créer une instance EC2 sur AWS
provider "aws" {
  region = "eu-west-3" # Paris
}

resource "aws_instance" "ubuntu" {
  ami           = "ami-00fb6bcd39604eed6" # AMI Ubuntu Server 22.04
  instance_type = "t2.micro" # Type d'instance EC2 (gratuit)

  key_name = "EC2Key_Projet_DevOps" # Clé SSH pour accès à l'instance

  vpc_security_group_ids = ["sg-0e8027e30aa86962e"] # ID du groupe de sécurité

  tags = {
    Name = "Projet_DevOps"
  }
}

output "instance_ip" {
  value = aws_instance.ubuntu.public_ip
}