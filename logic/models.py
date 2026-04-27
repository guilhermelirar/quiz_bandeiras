from dataclasses import dataclass

@dataclass
class Player:
    sid: str
    name: str
    score: int
    status: str

@dataclass
class Options:
    a: str
    b: str
    c: str
    d: str

@dataclass
class Round:
    flag_id: str
    options: Options

@dataclass 
class Room:
    id: str
    players: list[Player]
    rounc_c: int
    round_ans: str 
    round: Round

