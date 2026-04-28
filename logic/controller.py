from app import new_room
from models import *
from uuid import uuid4

class Room:
    def __init__(self, players: list[Player]) -> None:
        self.id = str(uuid4())
        self.players: dict[str, Player] = {player.sid: player for player in players}
        self.deck = {}
        self.round: Round | None
        
    def next_round(self):
        pass

class GameManager:
    def __init__(self, countries) -> None:
        self.rooms = {}
        self.public_waiting_room: Room | None = None
        self.private_rooms = {}
        self.countries = countries

    def get_room(self, room_id):
        return self.rooms.get(room_id)

    def new_room(self, players: list[Player]):
        return Room(players)

    def new_player(self, username: str, sid: str):
        return Player(sid=sid, name=username, 
                      score=0, status="waiting")

    def join_1v1(self, username: str, sid: str):
        if self.public_waiting_room:
            room: Room = self.public_waiting_room
            room.players[sid] = self.new_player(username, sid)
            self.public_waiting_room = None 
            self.rooms[room.id] = room
            return room

        room =  self.new_room([self.new_player(username, sid)]) 
        self.public_waiting_room = room
        return room

