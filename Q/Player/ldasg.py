from abc import ABC

from Q.Common.rulebook import Rulebook
from Q.Player.strategy import PlayerStrategy
from typing import List
from Q.Common.Board.pos import Pos
from Q.Common.map import Map
from Q.Common.Board.tile import Tile


class LDasg(PlayerStrategy, ABC):
    """
    Represents the LDASG (less dumb and still greedy) player strategy.
    From assignment specs: Chooses the player's smallest tile that can extend the current map.
    If there is more than one place, it picks the one that has the most existing neighbors, that is, the most
    constrained one.
    """

    def choose_placement(self, possible_positions: List[Pos], given_map: Map) -> Pos:
        """
        Chooses placement firstly by picking a position that has the most neighbors
        Tie breaks with the smallest placement (row-col order)
        """
        max_neighbors = 0
        positions_with_most_neighbors = []
        for position in possible_positions:
            neighbors = given_map.get_number_of_tile_neighbors(position)
            if neighbors > max_neighbors:
                max_neighbors = neighbors
                positions_with_most_neighbors = [position]
            elif neighbors == max_neighbors:
                positions_with_most_neighbors.append(position)

        return self.get_smallest_placement(positions_with_most_neighbors)

    def choose_tile_to_play(self, hand: List[Tile], given_map: Map, rulebook: Rulebook) -> Tile:
        return super().choose_tile_to_play(hand, given_map, rulebook)
