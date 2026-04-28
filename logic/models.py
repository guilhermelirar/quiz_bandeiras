from dataclasses import dataclass

@dataclass
class Player:
    sid: str
    name: str
    score: int
    status: str

@dataclass
class Round:
    flag_id: str
    options: list[tuple[str, str]]

