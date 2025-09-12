# Apresentação Detalhada do Projeto Final – Etapa 2: Argos IA com DevOps e IaC

**Prezado Professor,**

Este documento serve como a apresentação completa e o relatório técnico da segunda etapa do nosso projeto final. Partindo do agente inteligente **Argos IA**, nosso objetivo foi aplicar um ciclo de desenvolvimento profissional, incorporando práticas essenciais de DevOps e Infraestrutura como Código (IaC).

Aqui, detalhamos não apenas a nossa estratégia e as ferramentas utilizadas, mas também apresentamos integralmente cada artefato de código desenvolvido, explicando sua função e estrutura.

## 1. O Coração do Projeto: O Agente Argos IA

Tudo começa com a nossa aplicação principal. O `main.py` é um aplicativo web construído com Streamlit que utiliza a API do Google Gemini para funcionar como um assistente de análise de código.

<details>
<summary>📄 <strong>Clique para ver o código: <code>main.py</code></strong></summary>

```python
# 1. Imports essenciais
import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# 2. Configuração da Página (Aba do Navegador)
st.set_page_config(
    page_title="Argos IA - Análise de Código",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 3. Carregamento e Verificação da API Key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("🔑 Chave da API do Gemini não encontrada. Verifique seu arquivo .env ou os secrets do ambiente.")
    st.stop()

# 4. Configuração da API do Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Função para inicializar o modelo
def init_gemini():
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.8,
        "top_k": 40,
        "max_output_tokens": 2048,
    }
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config
    )
    return model

# Função para gerar resposta do chatbot, incorporando a persona "Argos IA"
def generate_response(model, user_prompt):
    # Prompt do sistema que instrui o modelo a agir como o Argos IA
    system_prompt = """
    Você é o Argos IA, um assistente de engenharia de software especializado em análise de código.
    Sua tarefa é receber um trecho de código e retornar uma análise estruturada, clara e acionável.
    Sua resposta DEVE ser em formato Markdown e seguir estritamente as seguintes seções:

    ### 📝 Resumo de Alto Nível
    (Descreva em linguagem natural e de forma concisa o que o código faz.)

    ### 🎯 Principais Responsabilidades
    (Liste em bullet points as ações e lógicas específicas que o código executa.)

    ### 🔍 Insights e Pontos de Atenção
    (Destaque pontos críticos que um revisor humano procuraria. Use emojis para categorizar. Exemplos:)
    - ⚠️ **Risco de Segurança:** (Se houver uma vulnerabilidade clara.)
    - ⚙️ **Sugestão de Refatoração:** (Se o código puder ser mais limpo, eficiente ou menos complexo.)
    - 🔗 **Dependência Externa:** (Se o código interage com APIs, bancos de dados, etc.)
    - 💡 **Oportunidade de Melhoria:** (Qualquer outra sugestão para melhorar o código.)

    Analise o seguinte código:
    """
    
    # Combina o prompt do sistema com a entrada do usuário
    full_prompt = f"{system_prompt}\n```\n{user_prompt}\n```"

    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Erro ao gerar resposta: {str(e)}"

# --- Interface do Usuário ---
# ... (restante da interface Streamlit) ...
```
</details>

**Explicação da Lógica:**
* **Interface com Streamlit:** Define a interface web, incluindo o título, a barra lateral e a área de chat.
* **Gerenciamento de API Key:** Carrega a chave da API do Gemini de forma segura a partir de variáveis de ambiente (essencial para a segurança).
* **Função `generate_response`:** É o cérebro do agente. Ela recebe o código do usuário, o envolve em um *prompt* estruturado que define a persona "Argos IA" e envia para o modelo Gemini, tratando possíveis erros.

---

## 2. A Arquitetura DevOps: Os 4 Pilares da Nossa Solução

Com o código da aplicação definido, nosso foco foi construir um ecossistema robusto ao seu redor, baseado em quatro pilares fundamentais do DevOps.

### Pilar 1: Containerização com Docker (Robustez e Portabilidade)

Para resolver o problema de "na minha máquina funciona", adotamos o **Docker**. O `Dockerfile` abaixo é a receita que empacota nossa aplicação e todas as suas dependências em uma imagem portátil e consistente.

<details>
<summary>📄 <strong>Clique para ver o código: <code>Dockerfile</code></strong></summary>

```dockerfile
# 1. Escolha uma imagem base oficial do Python
FROM python:3.9-slim

# 2. Defina o diretório de trabalho dentro do container
WORKDIR /app

# 3. Copie o arquivo de dependências para o container
COPY requirements.txt .

# 4. Instale as dependências listadas no requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copie todos os outros arquivos do projeto para o diretório de trabalho
COPY . .

# 6. Exponha a porta que o Streamlit usa (padrão 8501)
EXPOSE 8501

# 7. Defina o comando para executar a aplicação quando o container iniciar
CMD ["streamlit", "run", "main.py"]
```
</details>

**Explicação do Arquivo:**
* **`FROM python:3.9-slim`**: Usa uma imagem base leve do Python para manter nosso container pequeno.
* **`WORKDIR /app`**: Define o diretório de trabalho padrão dentro do container.
* **`COPY` e `RUN`**: Copia o arquivo de dependências e as instala, garantindo que o ambiente tenha tudo o que é necessário.
* **`EXPOSE 8501`**: Informa ao Docker que a aplicação dentro do container estará escutando na porta 8501.
* **`CMD [...]`**: O comando que inicia o servidor do Streamlit quando o container é executado.

### Pilar 2: Infraestrutura como Código com Terraform (Automação e Escalabilidade)

Para automatizar a criação da infraestrutura, utilizamos o **Terraform**. O script abaixo **simula** o provisionamento de um servidor na AWS, demonstrando como a infraestrutura pode ser gerenciada de forma declarativa e versionável.

<details>
<summary>📄 <strong>Clique para ver o código: <code>terraform/main.tf</code></strong></summary>

```terraform
# 1. Configura o provedor de nuvem (neste caso, a AWS)
provider "aws" {
  region = "us-east-1"
}

# 2. Define um "recurso", que é um objeto de infraestrutura
# Aqui, simulamos a criação de uma instância de servidor virtual (EC2)
resource "aws_instance" "app_server" {
  ami           = "ami-0c55b159cbfafe1f0" # Imagem Amazon Linux 2
  instance_type = "t2.micro"             # Instância do nível gratuito da AWS

  tags = {
    Name      = "Servidor-Agente-IA"
    Project   = "Projeto-Final-IA"
    ManagedBy = "Terraform"
  }

  # Bloco de provisionamento simulado para instalar o Docker e rodar o container
  provisioner "remote-exec" {
    inline = [
      "echo '--- ATUALIZANDO PACOTES ---'",
      "sudo yum update -y",
      "echo '--- INSTALANDO DOCKER ---'",
      "sudo amazon-linux-extras install docker -y",
      "sudo service docker start",
      "echo '--- EXECUTANDO O CONTAINER DO AGENTE (SIMULADO) ---'",
      "docker run -d -p 80:8501 seu-usuario/projeto-final-ia"
    ]
  }
}

# 3. Define uma saída (output) para mostrar o IP público do servidor após a criação
output "ip_publico_servidor" {
  value = aws_instance.app_server.public_ip
}
```
</details>

**Explicação do Arquivo:**
* **`provider "aws"`**: Especifica que usaremos a Amazon Web Services.
* **`resource "aws_instance" "app_server"`**: Declara o desejo de criar um servidor virtual (EC2).
* **`provisioner "remote-exec"`**: Simula os comandos que seriam executados no servidor após sua criação para configurar o ambiente e rodar nossa aplicação Docker.

### Pilar 3: Testes Automatizados com Pytest (Confiabilidade)

Para garantir a qualidade e a confiabilidade do nosso código, implementamos testes unitários com **Pytest**. O destaque aqui é o uso de **mocking** para testar a função que interage com a API do Gemini sem fazer uma chamada de rede real, tornando os testes rápidos e independentes.

<details>
<summary>📄 <strong>Clique para ver o código: <code>tests/test_main.py</code></strong></summary>

```python
import pytest
from unittest.mock import MagicMock
from main import generate_response

def test_generate_response_success(mocker):
    """
    Testa se a função generate_response formata o prompt corretamente
    e retorna a resposta do modelo quando a chamada à API é bem-sucedida.
    """
    # Arrange: Prepara um modelo e uma resposta falsos
    mock_response = MagicMock()
    mock_response.text = "Esta é uma análise de código gerada com sucesso."
    
    mock_model = MagicMock()
    mock_model.generate_content.return_value = mock_response
    
    user_prompt = "def hello():\n    print('hello world')"
    
    # Act: Executa a função a ser testada
    response = generate_response(mock_model, user_prompt)
    
    # Assert: Verifica se o resultado é o esperado
    mock_model.generate_content.assert_called_once()
    assert response == "Esta é uma análise de código gerada com sucesso."

def test_generate_response_api_error(mocker):
    """
    Testa se a função lida com uma exceção da API e retorna uma mensagem de erro.
    """
    # Arrange: Configura o modelo falso para lançar um erro
    mock_model = MagicMock()
    error_message = "Erro de autenticação na API"
    mock_model.generate_content.side_effect = Exception(error_message)
    
    user_prompt = "código inválido"
    
    # Act: Executa a função
    response = generate_response(mock_model, user_prompt)
    
    # Assert: Verifica se a mensagem de erro foi retornada corretamente
    assert "Erro ao gerar resposta" in response
    assert error_message in response
```
</details>

**Explicação do Arquivo:**
* **`test_generate_response_success`**: Simula o caminho feliz, onde a API do Gemini retorna uma resposta esperada.
* **`test_generate_response_api_error`**: Simula um cenário de falha, garantindo que nossa função trate o erro de forma elegante e informe o usuário.

### Pilar 4: Automação de CI/CD com GitHub Actions (Qualidade e Agilidade)

Para automatizar todo o processo de verificação, criamos um pipeline de CI/CD com **GitHub Actions**. Este "guardião da qualidade" executa uma série de validações a cada nova alteração no código, garantindo a integração contínua.

<details>
<summary>📄 <strong>Clique para ver o código: <code>.github/workflows/pipeline.yml</code></strong></summary>

```yaml
name: CI/CD Pipeline - Agente de IA

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout do Repositório
        uses: actions/checkout@v3

      - name: Configurar Python 3.9
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Instalar Dependências
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      
      - name: Rodar Testes com Pytest
        run: pytest tests/

      - name: Simular Build da Imagem Docker
        run: |
          echo "Simulando o build da imagem Docker..."
          docker build . --file Dockerfile --tag meu-agente-ia:latest
```
</details>

**Explicação do Arquivo:**
* **`on`**: Define os gatilhos do pipeline (a cada `push` ou `pull request` para a branch `main`).
* **`jobs` e `steps`**: Define as tarefas a serem executadas sequencialmente: baixar o código, configurar o ambiente Python, instalar as dependências, rodar os testes e, por fim, simular a construção da imagem Docker.

---

## 3. Arquivos de Suporte e Configuração

Por fim, temos os arquivos que dão suporte ao projeto, gerenciando dependências e segurança.

<details>
<summary>📄 <strong>Clique para ver o código: <code>requirements.txt</code></strong></summary>

```
streamlit
google-generativeai
python-dotenv
pytest
pytest-mock
```
</details>
**Explicação:** Este arquivo simplesmente lista todas as bibliotecas Python que nosso projeto precisa para funcionar.

<details>
<summary>📄 <strong>Clique para ver o código: <code>.gitignore</code></strong></summary>

```
# Arquivos de ambiente - NUNCA ENVIE PARA O REPOSITÓRIO!
.env

# Cache e arquivos compilados do Python
__pycache__/
*.pyc

# Diretórios de ambiente virtual
.venv/
venv/
```
</details>
**Explicação:** Este é um arquivo de segurança crucial. Ele instrui o Git a **ignorar** arquivos sensíveis como `.env` (que contém nossa chave de API) e pastas de cache, mantendo nosso repositório limpo e seguro.

---

## 4. Demonstração Prática: Como Executar e Avaliar o Projeto

A forma mais simples de avaliar nosso trabalho é utilizando o **GitHub Codespaces**.

1.  **Inicie o Codespace:** No repositório, clique em `<> Code` e inicie um novo Codespace.
2.  **Configure a Chave de API:** Adicione a `GEMINI_API_KEY` como um "secret" no ambiente do Codespaces.
3.  **Execute a Aplicação Web:** No terminal, execute `streamlit run main.py`. Uma aba será aberta no seu navegador com a aplicação funcionando.
4.  **Verifique os Componentes DevOps:**
    * **Testes:** `pytest`
    * **Infraestrutura:** `cd terraform && terraform init && terraform plan`

### Pilar 5: Ambiente de Desenvolvimento como Código com GitHub Codespaces

* **O Problema:** Como garantir que toda a equipe de desenvolvimento (ou o avaliador do projeto) tenha um ambiente de desenvolvimento idêntico e funcional com todas as ferramentas necessárias (Python, Docker, Terraform) sem um longo e complexo processo de instalação manual?
* **Nossa Solução:** Adotamos o **GitHub Codespaces** e o definimos como código através do arquivo `devcontainer.json`. Este arquivo automatiza a criação de um ambiente de desenvolvimento na nuvem, pré-configurado e pronto para usar em segundos.
* **Resultado:** Com um único clique, qualquer pessoa pode lançar um ambiente de desenvolvimento completo e padronizado diretamente no navegador. Nosso arquivo de configuração cuida de tudo: instala o Terraform, as extensões corretas do VS Code e até mesmo as dependências do Python. Isso representa o auge da prática de "Infraestrutura como Código", aplicada ao próprio ambiente de desenvolvimento.

<details>
<summary>📄 <strong>Clique para ver o código: <code>.devcontainer/devcontainer.json</code></strong></summary>

```json
{
    "name": "Projeto Final IA - Ambiente DevOps",
    // Usamos uma imagem universal da Microsoft que já vem com muitas ferramentas
    "image": "[mcr.microsoft.com/devcontainers/universal:2](https://mcr.microsoft.com/devcontainers/universal:2)",
    "features": {
        // Adiciona a ferramenta de linha de comando do Terraform
        "ghcr.io/devcontainers/features/terraform:1": {
            "version": "latest"
        }
    },
    // Instala extensões essenciais do VS Code automaticamente
    "customizations": {
        "vscode": {
            "extensions": [
                "ms-python.python",
                "ms-azuretools.vscode-docker",
                "hashicorp.terraform"
            ]
        }
    },
    // Instala as dependências do Python automaticamente após a criação
    "postCreateCommand": "pip install -r requirements.txt",
    // Expõe a porta do Streamlit e a abre em uma aba de preview
    "forwardPorts": [8501],
    "portsAttributes": {
        "8501": {
            "label": "Streamlit App",
            "onAutoForward": "openPreview"
        }
    }
}
```
</details>

## 5. Conclusão

Nesta etapa, transformamos um agente de IA em um projeto de software sustentável, aplicando os princípios de DevOps que aprendemos. Cada ferramenta e arquivo de código foi escolhido e desenhado para resolver desafios reais do ciclo de vida de desenvolvimento, resultando em um sistema mais robusto, confiável e automatizado.

Agradecemos a orientação e a oportunidade de desenvolver este projeto.

Atenciosamente,

**Ihan Messias Nascimento dos Santos**