from flask import Flask, render_template, render_template_string, request
from flask_socketio import SocketIO, emit, join_room
import uuid
import random

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

PAISES = {
    "br": "Brasil", "us": "Estados Unidos", "fr": "França",
    "jp": "Japão", "de": "Alemanha", "it": "Itália",
    "ar": "Argentina", "ca": "Canadá", "mx": "México",
    "pt": "Portugal", "gb": "Reino Unido", "au": "Austrália"
}
waiting_room = None
rooms = {}

@app.route('/hello')
def hello():
    return render_template_string('<h1>Hello</h1>') 

@app.route('/')
def game():
    return render_template('index.html')

def new_room(id):
    return {
            "id": id,
            "players": {},
            "round_c": 0,
            "round": {}
    }

def new_round():
    global PAISES
    N_OPTIONS = 4
    options_sample = random.sample(list(PAISES.items()), k=N_OPTIONS)
    options = dict(options_sample)
    ans = random.choice(options_sample)[0]
    return {
        "options": options, 
        "flag": ans,
        "onecorrect": False
    }

@socketio.on('join_game')
def handle_join(data):
    global waiting_room

    player_name = data['username']
    sid = request.sid

    if waiting_room:
        room_id = waiting_room
        waiting_room = None
        
        rooms[room_id]["players"][sid] = { 
                 "username": player_name,
                 "sid":sid,
                 "score": 0,
                 "status": "waiting"
                 }


        rooms[room_id]["round"] = new_round()
        join_room(room_id)
        print(data, rooms[room_id])
        emit("game_start", rooms[room_id], to=room_id)
    else:
        room_id = str(uuid.uuid4())
        waiting_room = room_id

        join_room(room_id)

        rooms[room_id] = new_room(room_id)
        rooms[room_id]["players"][sid] = { 
                 "username": player_name,
                 "sid":sid,
                 "score": 0,
                 "status": "waiting"
                 }


        join_room(room_id)
        print(data, rooms[room_id])
        emit("waiting", {"msg": "Aguardando outro jogador..."})

@socketio.on('send_ans')
def handle_ans(data):
    room = rooms[data["room_id"]]
    ans = data["answer"] # br, pt etc
    sid = request.sid

    if ans == room["round"]["flag"]:
        if room["round"]["onecorrect"]:
            room["players"][sid]["score"] += 3
            room["round"] = new_round()
            room["round_c"] += 1
            emit("new_round", room, to=data["room_id"])
            print(room, "fim do round passado")
            return

        room["round"]["onecorrect"] = True
        room["players"][sid]["score"] += 5
        room["players"][sid]["status"] = "correct"
        emit("update_round", {
                    "selected_correct":sid
            }, to=data["room_id"])
        print(data, room, "acertou")

    else:
        room["players"][sid]["status"] = "incorrect"
        emit("update_round", {
                    "selected_incorrect":sid
            }, to=data["room_id"])
        print(data, room, "errou")
