# 1. Configura o provedor de nuvem (neste caso, a AWS)
provider "aws" {
  region = "us-east-1"
}

# 2. Define um "recurso", que é um objeto de infraestrutura
# Aqui, simulamos a criação de uma instância de servidor virtual (EC2)
resource "aws_instance" "app_server" {
  # Amazon Machine Image (AMI) - o sistema operacional da máquina
  # Este é um ID de exemplo para uma imagem do Amazon Linux 2
  ami = "ami-0c55b159cbfafe1f0" 

  # Tipo da instância - define a CPU e a memória da máquina
  # t2.micro é elegível no nível gratuito da AWS
  instance_type = "t2.micro"

  # Tags são etiquetas para organizar e identificar seus recursos
  tags = {
    Name        = "Servidor-Agente-IA"
    Project     = "Projeto-Final-IA"
    ManagedBy   = "Terraform"
  }

  # Bloco de provisionamento simulado para instalar o Docker e rodar o container
  provisioner "remote-exec" {
    inline = [
      "echo '--- ATUALIZANDO PACOTES ---'",
      "sudo yum update -y",
      "echo '--- INSTALANDO DOCKER ---'",
      "sudo amazon-linux-extras install docker -y",
      "sudo service docker start",
      "sudo usermod -a -G docker ec2-user",
      "echo '--- EXECUTANDO O CONTAINER DO AGENTE (SIMULADO) ---'",
      "docker run -d -p 80:8501 seu-usuario/projeto-final-ia"
    ]
  }
}

# 3. Define uma saída (output) para mostrar uma informação útil após a criação
output "ip_publico_servidor" {
  value       = aws_instance.app_server.public_ip
  description = "O endereço IP público do servidor da aplicação."
}