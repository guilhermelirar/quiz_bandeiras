from _typeshed import OptExcInfo
import random as rd
from app import new_room
from models import *
from uuid import uuid4

class Room:
    def __init__(self, players: list[Player], 
                 countries: list[tuple[str, str]]) -> None:
        self.id = str(uuid4())
        self.players: dict[str, Player] = {player.sid: player for player in players}
        self.countries = countries

        self.deck = list(countries)
        rd.shuffle(self.deck)
        
        self.round_c = 0
        self.round: Round | None
        

    def next_round(self):
        self.round_c += 1 

        # Recria deck se acabar
        if not self.deck:
            self.deck = list(self.countries)
            rd.shuffle(self.deck)

        ans = self.deck.pop()

        options_list = None
        # garantindo que a resposta não esteja dentro das outras alternativas
        while options_list is None or ans in options_list:
            options_list = rd.sample(self.countries, k=3)
       
        # garantindo que a resposta não será sempre a última alternativa 
        options_list.append(ans)
        rd.shuffle(options_list) 
        
        self.round = Round(ans[0], options_list)

    def submit_answer(self, ans: str, sid: str):
        if self.round is None:
            return

        if self.round.flag_id == ans:
            if all(p.status != "correct" for p in self.players.values()):
                self.players[sid].score += 5 
            else:
                self.players[sid].score += 3
            
            self.players[sid].status = "correct"

        else:
            self.players[sid].status = "incorrect"


    def is_round_over(self) -> bool:
        return all(p.status != "waiting" for p in self.players.values())


class GameManager:
    def __init__(self, countries) -> None:
        self.rooms = {}
        self.public_waiting_room: Room | None = None
        self.private_rooms = {}
        self.countries: list[tuple[str, str]] = countries

    def get_room(self, room_id) -> Room | None:
        return self.rooms.get(room_id)

    def new_room(self, players: list[Player]):
        return Room(players, self.countries)

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

