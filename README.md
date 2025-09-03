# Projeto DevOps: API em Python com Infraestrutura como Código no Azure

## 1. Objetivo do Projeto

Este projeto demonstra um ciclo de vida de desenvolvimento e operações (DevOps) de ponta a ponta. O objetivo principal é provisionar automaticamente a infraestrutura na nuvem Microsoft Azure usando **Terraform** (Infraestrutura como Código), implantar uma API web simples desenvolvida em **Python (Flask)** e validar continuamente o código de infraestrutura através de um pipeline de CI/CD com **GitHub Actions**.

O resultado é uma aplicação funcional rodando na nuvem, cujo ambiente pode ser criado e destruído de forma rápida, confiável e repetível.

---

## 2. Como Rodar o Projeto

Siga os passos abaixo para provisionar a infraestrutura e executar a aplicação.

### Pré-requisitos

* Uma conta ativa na [Microsoft Azure](https://azure.microsoft.com/).
* [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli) instalado localmente.
* [Azure CLI](https://docs.microsoft.com/cli/azure/install-azure-cli) instalado e autenticado (`az login`).

### Passos para Execução

1.  **Clone o Repositório**
    ```bash
    git clone [https://github.com/messias-code/puc-devops-iac.git](https://github.com/messias-code/puc-devops-iac.git)
    cd puc-devops-iac
    ```

2.  **Provisione a Infraestrutura com Terraform**
    Execute os seguintes comandos no seu terminal local:
    ```bash
    # Inicializa os plugins do Terraform
    terraform init

    # (Opcional) Revisa o plano de execução
    terraform plan

    # Cria os recursos na Azure (confirme com 'yes')
    terraform apply
    ```
    > Ao final, o Terraform exibirá o endereço de IP público da VM (`ip_publico_da_vm`). Guarde este valor.

3.  **Acesse a Máquina Virtual**
    Use o IP público para se conectar à VM via SSH.
    ```bash
    ssh aluno@<SEU_IP_PUBLICO>
    ```
    > A senha é a que está definida no arquivo `main.tf`.

4.  **Execute a API dentro da VM**
    Uma vez conectado na VM, execute os seguintes comandos:
    ```bash
    # (Apenas na primeira vez) Instala o Flask
    sudo pip3 install Flask

    # Inicia o servidor da API
    # (Use o repositório clonado dentro da VM ou crie o arquivo app.py)
    sudo python3 app.py
    ```

5.  **Teste a API**
    Abra seu navegador e acesse os seguintes endpoints:
    * `http://<SEU_IP_PUBLICO>/` - Deve retornar a mensagem de "Olá, Mundo!".
    * `http://<SEU_IP_PUBLICO>/status` - Deve retornar o JSON `{"status": "ok"}`.

6.  **Limpeza (Destruir a Infraestrutura)**
    Para evitar custos, destrua todos os recursos criados com um único comando:
    ```bash
    terraform destroy
    ```

---

## 3. Como Funciona a Infraestrutura

A infraestrutura deste projeto é totalmente descrita como código no arquivo `main.tf` e gerenciada pelo Terraform. Ao executar `terraform apply`, os seguintes recursos são criados e configurados no Azure:

* **Grupo de Recursos (`azurerm_resource_group`):** Um contêiner lógico para agrupar todos os recursos do projeto, facilitando o gerenciamento e a limpeza.
* **Rede Virtual e Sub-rede (`azurerm_virtual_network`, `azurerm_subnet`):** Criam uma rede privada isolada na nuvem para a nossa máquina virtual, garantindo um ambiente seguro.
* **IP Público (`azurerm_public_ip`):** Aloca um endereço de IP estático e público na internet para que possamos acessar nossa API e a VM via SSH.
* **Grupo de Segurança de Rede (`azurerm_network_security_group`):** Atua como um firewall virtual para a VM. Ele está configurado com regras de entrada (`inbound`) para permitir tráfego nas seguintes portas:
    * **Porta 22 (TCP):** Para permitir conexões SSH.
    * **Porta 80 (TCP):** Para permitir tráfego HTTP para nossa API.
* **Interface de Rede (`azurerm_network_interface`):** Conecta a máquina virtual à sub-rede, ao IP público e ao grupo de segurança.
* **Máquina Virtual (`azurerm_linux_virtual_machine`):** O servidor Linux (Ubuntu) onde nossa aplicação Python/Flask é executada.

---

## 4. Como Funciona o CI/CD

O pipeline de Integração Contínua (CI) é orquestrado pelo **GitHub Actions** e está definido no arquivo `.github/workflows/terraform.yml`.

### Gatilho (Trigger)
O fluxo de trabalho é acionado automaticamente a cada `push` de código para a branch `main` do repositório.

### Processo de Validação
Quando acionado, o pipeline executa os seguintes passos em um ambiente virtual (`ubuntu-latest`) fornecido pelo GitHub:

1.  **Autenticação Segura:** O workflow se autentica na Azure de forma não-interativa usando um **Service Principal**. As credenciais (`Client ID`, `Client Secret`, `Tenant ID`, etc.) estão armazenadas de forma segura como **GitHub Secrets**, e não diretamente no código.

2.  **Checkout do Código:** O código do repositório é baixado para o ambiente virtual.

3.  **Setup do Terraform:** A versão especificada do Terraform é instalada.

4.  **Terraform Init:** O comando `terraform init` é executado para inicializar o Terraform e baixar os providers necessários.

5.  **Terraform Plan:** O comando `terraform plan` é executado. Este é o passo de validação mais importante. Ele verifica a sintaxe do código e gera um plano de execução, confirmando que a infraestrutura descrita é válida e pode ser aplicada.

O objetivo deste pipeline de CI não é aplicar as mudanças (`terraform apply`), mas sim **garantir que o código de infraestrutura na branch principal esteja sempre em um estado válido e planejável**, prevenindo erros antes que cheguem a um ambiente de produção.