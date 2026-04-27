from flask_socketio import SocketIO, emit
from logic.controller import GameManager, Room
from flask import request
from dataclasses import asdict

def register_game_handlers(socketio: SocketIO, manager: GameManager):
    def sid():
        return request.sid # type: ignore

    def new_round(room: Room):
        room.next_round()
        
        if room.round is None:
            return
        
        emit('new_round', 
            { 
                "players": [asdict(p) for p in room.players.values()],
                "flag": room.round.flag_id,
                "options": asdict(room.round.options),
            })


    @socketio.on('join_1v1')
    def handle_join_1v1(data):
        room: Room = manager.join_1v1(data['username'], sid())
        
        if room is not None and len(room.players) == 2:
            new_round(room)


    @socketio.on('ready')
    def handle_ready(data):
        room = manager.get_room(data['room_id'])
        
        if room is None:
            return

        room.players[sid()].status = "ready"

        if all(p.status == "ready" for p in room.players.values()):
            new_round(room)

    @socketio.on('send_ans')
    def handle_ans(data): 
        room = manager.get_room(data['room_id'])
        
        if room is None or room.round is None:
            return

        ans = data['ans']

        if room.round.ans == ans:
            if all(p.status != "correct" for p in room.players.values()):
                room.players[sid()].score += 5 
            else:
                room.players[sid()].score += 3
            
            room.players[sid()].status = "correct"

        else:
            room.players[sid()].status = "incorrect"


        if all(p.status != "waiting" for p in room.players.values()):
            # TODO intervalo 
            pass
