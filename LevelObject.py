import GameElement
from dataclasses import dataclass

@dataclass
class LevelObject:
    gameElement: GameElement
    value: int