# Importa a classe Flask e a função jsonify da biblioteca flask
from flask import Flask, jsonify

# Cria uma instância da aplicação web.
app = Flask(__name__)

# Rota principal que já tínhamos
@app.route('/')
def hello_world():
    return '<h1>Olá, Mundo! Minha API está no ar!</h1>'


# --- INÍCIO DA NOVA ROTA ---

# Define a nova rota "/status"
@app.route('/status')
def get_status():
    # Cria um dicionário Python que representa nossa resposta
    response = {
        "status": "ok"
    }
    # Usa a função jsonify para converter o dicionário em uma resposta JSON
    # e envia o código de status HTTP 200 (OK)
    return jsonify(response), 200

# --- FIM DA NOVA ROTA ---


# Esta linha verifica se o script está sendo executado diretamente
if __name__ == '__main__':
    # Inicia o servidor da aplicação
    app.run(host='0.0.0.0', port=80)