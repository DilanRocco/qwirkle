from dataclasses import dataclass
from typing import List

from Q.Common.map import Map
from Q.Player.public_player_data import PublicPlayerData


@dataclass
class PlayerState:
    """
    Represents public information that the player can know about the game.
    num_ref_tiles: is the number of tiles the ref currently had
    current_map: the current map of this game
    score: is a mapping from name to number of player points
    """
    num_ref_tiles: int
    current_map: Map
    player_data: PublicPlayerData
    scores: List[int]

