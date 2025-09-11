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
    st.error("🔑 Chave da API do Gemini não encontrada. Verifique seu arquivo .env.")
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

# Configuração da sidebar
with st.sidebar:
    st.header("⚙️ Controles")
    if st.button("🗑️ Limpar Conversa"):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.subheader("📊 Estatísticas")
    st.metric("Mensagens trocadas", len(st.session_state.get('messages', [])))

# Inicialização do modelo na sessão
if 'model' not in st.session_state:
    with st.spinner("🔄 Inicializando o Argos IA..."):
        st.session_state.model = init_gemini()

# Título e descrição principal
st.image("https://i.imgur.com/8a2eY4v.png", width=100) # Exemplo de logo, pode ser removido
st.title("🛡️ Argos IA")
st.write("Seu assistente para análise e revisão de código. Cole um trecho de código abaixo para receber insights.")

# Inicialização do histórico de mensagens
if 'messages' not in st.session_state:
    st.session_state.messages = []
    # Mensagem de boas-vindas do Argos
    st.session_state.messages.append({
        "role": "assistant",
        "content": """👋 Olá! Eu sou o Argos IA. 
        
Estou pronto para analisar seu código. Cole uma função, classe ou script no campo abaixo e eu fornecerei um resumo estruturado com responsabilidades e pontos de atenção."""
    })

# Exibição do histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input do usuário
if prompt := st.chat_input("Cole seu código aqui..."):
    # Adicionar mensagem do usuário ao histórico e à tela
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f"```\n{prompt}\n```")
    
    # Gerar e exibir resposta do assistente
    with st.chat_message("assistant"):
        with st.spinner("🔍 Analisando o código..."):
            response = generate_response(st.session_state.model, prompt)
            st.markdown(response)
    
    # Adicionar resposta do assistente ao histórico
    st.session_state.messages.append({"role": "assistant", "content": response})