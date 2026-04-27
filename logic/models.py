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


