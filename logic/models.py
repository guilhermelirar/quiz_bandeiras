from dataclasses import dataclass

@dataclass
class Player:
    sid: str
    name: str
    score: int
    status: str

@dataclass
class Round:
    flag: str
    options: dict

@dataclass 
class Room:
    id: str
    players: list[Player]
    rounc_c: int
    round: Round

