# 🛡️ Argos IA - Análise de Código com DevOps e IaC

Este projeto apresenta o **Argos IA**, um agente inteligente especializado em análise e revisão de código, construído com a API do Google Gemini. O projeto foi evoluído para incorporar práticas profissionais de DevOps, incluindo Infraestrutura como Código (IaC), containerização com Docker e um pipeline de CI/CD simulado com GitHub Actions.

## 📝 Descrição do Agente

O Argos IA é uma aplicação web construída com Streamlit que recebe um trecho de código do usuário e fornece uma análise estruturada em formato Markdown, dividida em:

* **Resumo de Alto Nível:** Uma explicação concisa sobre a função do código.
* **Principais Responsabilidades:** Uma lista detalhada das ações que o código executa.
* **Insights e Pontos de Atenção:** Sugestões de refatoração, alertas de segurança e oportunidades de melhoria.

## 🧱 Infraestrutura como Código (IaC)

A infraestrutura necessária para hospedar este agente é gerenciada como código usando **Terraform**.

* **Arquivo de Configuração:** `terraform/main.tf`
* **O que ele faz:** O script simula o provisionamento de uma instância **AWS EC2 (t2.micro)** na região `us-east-1`. Ele também inclui um provisionador `remote-exec` que simula a instalação do Docker e a execução do container da aplicação no servidor recém-criado.

**Como executar a simulação IaC (no Codespaces ou localmente):**

```bash
# 1. Navegue até o diretório do Terraform
cd terraform

# 2. Inicialize o Terraform (baixa o provedor da AWS)
terraform init

# 3. Veja o plano de execução (o que o Terraform faria)
terraform plan

# 4. Aplique a configuração (para criar a infraestrutura real - requer credenciais AWS)
# ATENÇÃO: Este passo criará recursos na AWS e pode gerar custos.
terraform apply
```

## 🐳 Containerização com Docker

A aplicação é empacotada em uma imagem Docker para garantir consistência e portabilidade entre diferentes ambientes.

* **Arquivo de Configuração:** `Dockerfile`

**Como construir e executar o container (no Codespaces ou localmente):**

```bash
# 1. Construa a imagem Docker a partir do Dockerfile
docker build -t argos-ia .

# 2. Execute o container a partir da imagem criada
# Você precisa de um arquivo .env com a GEMINI_API_KEY
docker run -p 8501:8501 --env-file .env argos-ia
```
Acesse a aplicação em `http://localhost:8501` no seu navegador.

## 🔄 Pipeline de CI/CD com GitHub Actions

O projeto utiliza um pipeline de CI/CD simulado para automatizar a verificação de qualidade e o processo de build.

* **Arquivo de Configuração:** `.github/workflows/pipeline.yml`

**O pipeline é acionado em cada `push` ou `pull request` para a branch `main` e executa as seguintes etapas:**

1.  **Checkout do Código:** Baixa a versão mais recente do repositório.
2.  **Configuração do Python:** Prepara o ambiente Python.
3.  **Instalação de Dependências:** Instala todas as bibliotecas do `requirements.txt`.
4.  **Execução de Testes:** Roda os testes unitários com `pytest` para validar as funções principais.
5.  **Simulação de Build Docker:** Executa `docker build` para garantir que a imagem do container pode ser construída sem erros.
6.  **Simulação de Deploy:** Imprime mensagens indicando que o build foi bem-sucedido e está pronto para deploy.

## 🧪 Testes Automatizados

Os testes automatizados foram implementados com **Pytest** para garantir a confiabilidade do agente.

* **Arquivo de Testes:** `tests/test_main.py`
* **O que é testado:** A função `generate_response` é testada de forma isolada usando "mocks" para simular as respostas da API do Gemini, tanto em cenários de sucesso quanto de erro.

**Como executar os testes manualmente:**
```bash
pytest
```

## 🚀 Como usar no GitHub Codespaces

Este projeto está totalmente configurado para ser executado no GitHub Codespaces, proporcionando um ambiente de desenvolvimento e simulação completo e padronizado na nuvem.

1.  **Abra o projeto:** Clique no botão `<> Code` no repositório e selecione "Create codespace on main".
2.  **Configure a Chave de API:** O Codespaces pedirá para configurar os secrets do repositório. Adicione sua `GEMINI_API_KEY` conforme solicitado. Se não pedir, vá em **Settings > Secrets and variables > Codespaces** e crie um novo secret.
3.  **Execute a Aplicação:** O terminal do Codespaces estará pronto. Execute o seguinte comando para iniciar o agente:
    ```bash
    streamlit run main.py
    ```
    O Codespaces irá automaticamente redirecionar a porta e fornecer um link para você abrir a aplicação no navegador.
4.  **Teste os outros componentes:** Você pode usar o terminal para rodar os comandos do Terraform, Docker e Pytest descritos nas seções acima.