import pytest
from unittest.mock import MagicMock
from main import generate_response

# 1. O que é um "Mock"?
# Um Mock é um objeto simulado que imita o comportamento de objetos reais de forma controlada.
# Usamos o 'mocker' do pytest-mock para substituir a chamada real à API do Gemini.

def test_generate_response_success(mocker):
    """
    Testa se a função generate_response formata o prompt corretamente
    e retorna a resposta do modelo quando a chamada à API é bem-sucedida.
    """
    # 2. Preparação (Arrange)
    
    # Crie um objeto de resposta falso que o modelo da API deveria retornar
    mock_response = MagicMock()
    mock_response.text = "Esta é uma análise de código gerada com sucesso."
    
    # Crie um modelo falso
    mock_model = MagicMock()
    # Configure o método 'generate_content' do modelo falso para retornar nossa resposta falsa
    mock_model.generate_content.return_value = mock_response
    
    # Simule a função init_gemini para retornar nosso modelo falso
    # (Não estamos testando init_gemini, então podemos ignorá-la)
    
    user_prompt = "def hello():\n    print('hello world')"
    
    # 3. Ação (Act)
    # Chame a função que estamos testando com o modelo falso
    response = generate_response(mock_model, user_prompt)
    
    # 4. Verificação (Assert)
    # Verifique se o método generate_content foi chamado uma vez
    mock_model.generate_content.assert_called_once()
    
    # Verifique se a resposta retornada é a que esperamos
    assert response == "Esta é uma análise de código gerada com sucesso."

def test_generate_response_api_error(mocker):
    """
    Testa se a função generate_response lida com uma exceção
    da API e retorna uma mensagem de erro amigável.
    """
    # 2. Preparação (Arrange)
    mock_model = MagicMock()
    # Configure o método 'generate_content' para levantar uma exceção quando for chamado
    error_message = "Erro de autenticação na API"
    mock_model.generate_content.side_effect = Exception(error_message)
    
    user_prompt = "código inválido"
    
    # 3. Ação (Act)
    response = generate_response(mock_model, user_prompt)
    
    # 4. Verificação (Assert)
    # Verifique se a resposta contém a mensagem de erro esperada
    assert "Erro ao gerar resposta" in response
    assert error_message in response