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