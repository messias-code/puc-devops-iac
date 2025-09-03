# Projeto de API Simples com IaC no Azure

Este projeto demonstra a criação e implantação de uma API web simples desenvolvida em Python com Flask. Toda a infraestrutura necessária na nuvem Azure é provisionada de forma automatizada usando Terraform.

O objetivo é servir como um guia prático para um fluxo de trabalho básico de DevOps, cobrindo desde a Infraestrutura como Código (IaC) até a execução da aplicação em uma máquina virtual.

---

## 🚀 Tecnologias Utilizadas

*   **Nuvem:** Microsoft Azure
*   **Infraestrutura como Código (IaC):** Terraform
*   **Linguagem da Aplicação:** Python 3
*   **Framework Web:** Flask

---

## 📂 Estrutura do Projeto

*   `main.tf`: Arquivo principal do Terraform que define toda a infraestrutura a ser criada no Azure (rede, máquina virtual, regras de segurança, etc.).
*   `app.py`: O código da aplicação web em Python/Flask que será executada na máquina virtual.
*   `README.md`: Este documento.

---

## 📋 Pré-requisitos

Antes de começar, garanta que você tenha as seguintes ferramentas instaladas e configuradas no seu ambiente local:

1.  [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli)
2.  [Azure CLI](https://docs.microsoft.com/cli/azure/install-azure-cli)
3.  Uma conta ativa no Azure com permissões para criar recursos.

---

## ⚙️ Guia de Execução

Siga os passos abaixo para provisionar a infraestrutura e implantar a aplicação.

### 1. Provisionar a Infraestrutura com Terraform

Estes comandos devem ser executados no seu terminal, na raiz deste projeto.

**a. Faça login na sua conta do Azure:**
```bash
az login
```

**b. Inicialize o Terraform:**
Este comando prepara seu diretório de trabalho para o Terraform.
```bash
terraform init
```

**c. Planeje e revise as mudanças:**
O Terraform mostrará o que será criado, alterado ou destruído.
```bash
terraform plan
```

**d. Aplique a configuração para criar os recursos no Azure:**
Confirme a execução digitando `yes` quando solicitado.
```bash
terraform apply
```
> 🔑 **Guarde o IP!** Ao final, o Terraform exibirá o IP público da máquina virtual em `ip_publico_da_vm`. Você precisará dele para os próximos passos.

### 2. Executar a API na Máquina Virtual

**a. Conecte-se à VM recém-criada via SSH:**
Substitua `<IP_PUBLICO_DA_VM>` pelo endereço de IP obtido no passo anterior. A senha é a que está definida no arquivo `main.tf` (padrão: `SenhaSuperForte123!`).

```bash
ssh aluno@<IP_PUBLICO_DA_VM>
```

**b. Dentro da VM, prepare o ambiente (só precisa ser feito uma vez):**
```bash
# Atualiza a lista de pacotes
sudo apt update

# Instala o gerenciador de pacotes do Python (pip)
sudo apt install python3-pip -y

# Instala o Flask
sudo pip3 install Flask
```

**c. Crie o arquivo da aplicação:**
Ainda dentro da VM, crie o arquivo `app.py` com o seguinte conteúdo:
```bash
nano app.py
```
Cole o código abaixo, salve e feche o editor (Ctrl+X, depois Y, e Enter).

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Olá, Mundo! Minha API está no ar!"

if __name__ == '__main__':
    # Roda a aplicação na rede local, acessível externamente pela porta 80
    app.run(host='0.0.0.0', port=80)
```

**d. Inicie o servidor da API:**
```bash
sudo python3 app.py
```

### 3. Acessar a API

Abra seu navegador e acesse o IP público da VM. Você deverá ver a mensagem:
> Olá, Mundo! Minha API está no ar!

`http://<IP_PUBLICO_DA_VM>`

---

## 🧹 Limpeza

Para **destruir todos os recursos** criados no Azure e evitar custos desnecessários, execute o seguinte comando no seu terminal local (na raiz do projeto):

```bash
terraform destroy
```
Confirme a operação digitando `yes` quando solicitado.