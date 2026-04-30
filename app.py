import json
from flask import Flask, render_template
from flask_socketio import SocketIO
from logic.controller import GameManager
from events.game_handlers import register_game_handlers

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui' # Importante para o SocketIO

socketio = SocketIO(app, cors_allowed_origins="*")

def load_countries():
    with open('paises.json', 'r', encoding='utf-8') as f:
        return json.load(f)

countries_dict = load_countries()

manager = GameManager(list(countries_dict.items()))

register_game_handlers(socketio, manager)

# 5. Rotas HTTP
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Use o socketio.run em vez do app.run
    socketio.run(app, debug=True)

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

