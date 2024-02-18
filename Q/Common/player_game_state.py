from dataclasses import dataclass
from typing import List

from Q.Common.Board.tile import Tile
from Q.Player.turn_outcome import TurnOutcome


@dataclass
class PlayerGameState:
    """
    Information the game state knows about the referee
    """
    hand: List[Tile]
    points: int
    misbehaved: bool
    last_move: TurnOutcome
