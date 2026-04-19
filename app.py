from flask import Flask, render_template, render_template_string, request
from flask_socketio import SocketIO, emit, join_room
import uuid, random, json

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

def carregar_paises():
    with open('paises.json', 'r', encoding='utf-8') as f:
        return json.load(f)

PAISES = carregar_paises()

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

def goto_next_round(room):
#    for player in room["players"]:
#        room["players"][player]["status"] = "waiting"
    
    room["round"] = new_round()
    room["round_c"] += 1
    emit("new_round", room, to=room["id"])

@socketio.on('ready')
def handle_ready(data):
    room = rooms[data["room_id"]]
    room["players"][request.sid]["status"] = "waiting"
    
    if all((room["players"][p]["status"]=="waiting") 
        for p in room["players"]):
        goto_next_round(room)
        return

    emit('interval', {
            "answer": PAISES[room["round"]["flag"]], 
            "placar": room["players"]
        }, to=data["room_id"])


@socketio.on('send_ans')
def handle_ans(data):
    room = rooms[data["room_id"]]
    ans = data["answer"] # br, pt etc
    sid = request.sid

    if ans == room["round"]["flag"]:
        room["players"][sid]["status"] = "correct"
        
        if room["round"]["onecorrect"]:
            room["players"][sid]["score"] += 3
        else:
            room["players"][sid]["score"] += 5
            room["round"]["onecorrect"] = True

    else:
        room["players"][sid]["status"] = "incorrect"

       
    if all((room["players"][p]["status"]!="waiting") 
        for p in room["players"]):
        emit('interval', {
            "answer": PAISES[room["round"]["flag"]], 
            "placar": room["players"]
        }, to=data["room_id"])

        return

    emit("update_round", room["players"], to=data["room_id"])
    

