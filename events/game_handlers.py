from flask_socketio import SocketIO, emit, join_room
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
                "options": room.round.options,
            },
             to=room.id)


    @socketio.on('join_1v1')
    def handle_join_1v1(data):
        room: Room = manager.join_1v1(data['username'], sid())
        join_room(room.id)

        if len(room.players) == 2:
            return new_round(room)
         
        emit('waiting_players', {'message': "Aguardando novos jogadores"},
             to=room.id)
        

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

        room.submit_answer(data['ans'], sid())

        if room.is_round_over():
            emit('interval', 
            { 
                "players": [asdict(p) for p in room.players.values()],
                "flag": room.round.flag_id,
                "options": room.round.options
            }, to=room.id) 
            pass
    

