from abc import ABC
from typing import List
from Q.Common.Board.pos import Pos
from Q.Common.map import Map
from Q.Common.Board.tile import Tile
from Q.Common.rulebook import Rulebook

from Q.Player.strategy import PlayerStrategy


class Dag(PlayerStrategy, ABC):
    """
    Represents the dag (dumb and greedy) player strategy.
    From assignment specs: Chooses the player's smallest tile that can extend the current map.
    If there is more than one place, it breaks the tie using the row-column order for the coordinates.
    """
    def choose_placement(self, possible_positions: List[Pos], given_map: Map) -> Pos:
        return super().choose_placement(possible_positions, given_map)

    def choose_tile_to_play(self, hand: List[Tile], given_map: Map, rulebook: Rulebook) -> Tile:
        return super().choose_tile_to_play(hand, given_map, rulebook)
