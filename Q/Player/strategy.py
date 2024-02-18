from abc import ABC, abstractmethod
from typing import List
from Q.Common.Board.pos import Pos
from Q.Common.Board.tile import Tile
from Q.Common.map import Map
from Q.Common.rulebook import Rulebook


class PlayerStrategy(ABC):
    """
    The abstract class (ABC) for automated player strategies.
    """
    @abstractmethod
    def choose_placement(self, possible_positions: List[Pos], given_map: Map) -> Pos:
        """
        Calls get_smallest_placement by default
        ASSUMPTION: possible positions is not empty

        """
        return self.get_smallest_placement(possible_positions)

    @abstractmethod
    def choose_tile_to_play(self, hand: List[Tile], given_map: Map, rulebook: Rulebook) -> Tile:
        """
        Defaults to choosing the smallest tile
        :returns: smallest tile in hand
        """
        hand.sort(key=lambda tile: (tile.shape.value, tile.color.value))
        for tile in hand:
            if len(rulebook.get_legal_positions(given_map, tile, [], break_early=True)):
                return tile
        return None

    def get_smallest_placement(self, possible_positions: List[Pos]) -> Pos:
        """
        Chooses smallest placement by row-column order
        ASSUMPTION: possible positions is not empty
        """
        smallest_row = min([position.y for position in possible_positions])
        positions_with_smallest_row = [position for position in possible_positions if position.y == smallest_row]

        return min(positions_with_smallest_row, key=lambda position: position.x)
