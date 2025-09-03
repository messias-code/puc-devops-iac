# Define o provedor que vamos usar (Azure) e garante que estamos usando uma versão compatível.
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0"
    }
  }
}

# Configura o provedor do Azure. Ele vai usar as credenciais que você configurou com o "az login".
provider "azurerm" {
  features {}
}

# 1. Grupo de Recursos: Uma caixa para organizar todos os nossos recursos.
resource "azurerm_resource_group" "rg_estudo" {
  name     = "rg-estudo-terraform"
  location = "Brazil South" # Sinta-se à vontade para mudar a região!
}

# 2. Rede Virtual (VNet): A rede privada onde nossa VM vai existir.
resource "azurerm_virtual_network" "vnet_estudo" {
  name                = "vnet-estudo"
  resource_group_name = azurerm_resource_group.rg_estudo.name
  location            = azurerm_resource_group.rg_estudo.location
  address_space       = ["10.0.0.0/16"]
}

# 3. Sub-rede: Uma "fatia" da nossa rede para conectar a VM.
resource "azurerm_subnet" "subnet_estudo" {
  name                 = "subnet-estudo"
  resource_group_name  = azurerm_resource_group.rg_estudo.name
  virtual_network_name = azurerm_virtual_network.vnet_estudo.name
  address_prefixes     = ["10.0.1.0/24"]
}

# 4. IP Público: Para conseguirmos acessar nossa VM pela internet.
resource "azurerm_public_ip" "ip_estudo" {
  name                = "ip-publico-estudo"
  resource_group_name = azurerm_resource_group.rg_estudo.name
  location            = azurerm_resource_group.rg_estudo.location
  allocation_method   = "Static"
  sku                 = "Standard"
}

# 5. Grupo de Segurança de Rede (NSG): O firewall que vai liberar a porta 80.
resource "azurerm_network_security_group" "nsg_estudo" {
  name                = "nsg-estudo"
  resource_group_name = azurerm_resource_group.rg_estudo.name
  location            = azurerm_resource_group.rg_estudo.location

  # Regra para permitir tráfego web na porta 80
  security_rule {
    name                       = "Allow_HTTP"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "80"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
  
  # Regra para permitir acesso remoto via SSH (porta 22) para gerenciarmos a VM
  security_rule {
    name                       = "Allow_SSH"
    priority                   = 110
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}

# 6. Interface de Rede (NIC): "Placa de rede" virtual que conecta tudo.
resource "azurerm_network_interface" "nic_estudo" {
  name                = "nic-estudo"
  location            = azurerm_resource_group.rg_estudo.location
  resource_group_name = azurerm_resource_group.rg_estudo.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.subnet_estudo.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.ip_estudo.id
  }
}

# 7. Associação do NSG com a NIC: Dizendo ao firewall para proteger nossa placa de rede.
resource "azurerm_network_interface_security_group_association" "assoc_nsg_nic" {
  network_interface_id      = azurerm_network_interface.nic_estudo.id
  network_security_group_id = azurerm_network_security_group.nsg_estudo.id
}

# 8. Máquina Virtual (VM) com Linux (Ubuntu)
resource "azurerm_linux_virtual_machine" "vm_estudo" {
  name                  = "vm-estudo-linux"
  resource_group_name   = azurerm_resource_group.rg_estudo.name
  location              = azurerm_resource_group.rg_estudo.location
  size                  = "Standard_B1s" # Um dos tamanhos mais baratos.
  admin_username        = "aluno"
  admin_password        = "SenhaSuperForte123!" # ATENÇÃO: Troque por uma senha que siga as regras do Azure.
  disable_password_authentication = false # Permitindo o login com a senha definida.

  network_interface_ids = [azurerm_network_interface.nic_estudo.id]

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts-gen2"
    version   = "latest"
  }
}

# Saída (output): Mostra o IP público da VM no final da execução.
output "ip_publico_da_vm" {
  value = azurerm_public_ip.ip_estudo.ip_address
}
