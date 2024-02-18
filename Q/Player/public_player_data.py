from dataclasses import dataclass
from typing import List

from Q.Common.Board.tile import Tile


@dataclass
class PublicPlayerData:
    """
    Represents the public data that the player knows about themselves
    """
    score: int
    name: str
    tiles: List[Tile]
