from abc import ABC
from typing import List


from Q.Common.Board.pos import Pos
from Q.Common.Board.tile import Tile
from Q.Common.Board.tile_color import TileColor
from Q.Common.Board.tile_shape import TileShape
from Q.Common.map import Map
from Q.Common.rulebook import Rulebook
from Q.Player.dag import Dag
from Q.Player.player import Player
from Q.Player.player_state import PlayerState
from Q.Player.strategy import PlayerStrategy
from Q.Player.turn import Turn
from Q.Player.turn_outcome import TurnOutcome


class CheatPlayer(Player, ABC):
    """
    Represents a player that cheats in the game of Q
    """
    def __init__(self, name, strategy: PlayerStrategy = Dag(), hand: List[Tile] = [], rulebook: Rulebook = Rulebook(),
                 cheat: str = ""):
        super().__init__(name, strategy, hand, rulebook)
        self.jcheat = cheat

    def place_non_adjacent_coordinate(self, s: PlayerState) -> Turn:
        """
        creates a turn where a particular tile does not neighbor any other tile
        :param s: the public knowledge of the game
        :return: the invalid turn
        """
        if s.current_map.tiles:
            max_pos_x = max(list(s.current_map.tiles.keys()), key=lambda pos: pos.x).x
        else:
            max_pos_x = 0
        placement = {Pos(max_pos_x + 2, 10): self.hand.pop()}
        return Turn(TurnOutcome.PLACED, placement)

    def place_tile_not_owned(self, s:PlayerState) -> Turn:
        for color in TileColor:
            for shape in TileShape:
                fake_tile = Tile(color, shape)
                if fake_tile not in self.hand:
                    legal_positons = self.rulebook.get_legal_positions(s.current_map, fake_tile, [])
                    if legal_positons:
                        return Turn(TurnOutcome.PLACED, {legal_positons[0]: fake_tile})
                    else:
                        return Turn(TurnOutcome.PLACED, {Pos(0, 0): fake_tile})

    def place_not_a_line(self, s: PlayerState) -> Turn:
        """
        creates a turn that does not place tiles in same row row col
        :param s: the public knowledge of the player
        :return: the invalid turn
        """
        tile1 = Tile(TileShape.STAR, color=TileColor.BLUE)
        tile2 = Tile(TileShape.SQUARE, color=TileColor.BLUE)
        pos1 = Pos(0, 0)
        pos2 = Pos(10, 14)
        for i in range(len(self.hand)):
            for j in range(i, len(self.hand)):
                tile1 = self.hand[i]
                tile2 = self.hand[j]
                positions1 = self.rulebook.get_legal_positions(s.current_map, tile1, [])
                positions2 = self.rulebook.get_legal_positions(s.current_map, tile2, [])
                for p1 in positions1:
                    for p2 in positions2:
                        if pos1.x != pos2.x and pos2.y != pos2.y:
                            pos1 = p1
                            pos2 = p2
        placements = {pos1: tile1, pos2:tile2}
        return Turn(TurnOutcome.PLACED, placements)

    def exchange_bad_ask_for_tiles(self, s: PlayerState):
        """
        creates a turn that may ask for an exchange of tiles when the rules don't allow
        :param s: the public knowledge of the game
        :return: the (potentially) invalid turn
        """
        return Turn(TurnOutcome.REPLACED)

    def place_no_fit(self, s: PlayerState) -> Turn:
        """
        creates a turn that will potentially not fit on the board by attempting to place a tile that may
        not fit according to Q rules.
        :param s: the public knowledge of the game
        :return: the (potentially) invalid turn
        """
        for tile_in_hand in self.hand:
            for pos_in_map, tile_in_map in s.current_map.tiles.items():
                if tile_in_hand.color == tile_in_map.color and tile_in_hand.shape == tile_in_map.shape:
                    continue
                neighbors = s.current_map.get_neighbors(pos_in_map)
                for neighbor in neighbors:
                    if s.current_map.tiles.get(neighbor) is None:
                        return Turn(TurnOutcome.PLACED, {neighbor: tile_in_hand})
        return Turn(TurnOutcome.PASSED)

    def take_turn(self, s: PlayerState) -> Turn:
        """
        takes a turn for a player
        :param s: the public state
        :return: the turn the player does
        """
        if self.jcheat == "non-adjacent-coordinate":
            return self.place_non_adjacent_coordinate(s)
        if self.jcheat == "tile-not-owned":
            return self.place_tile_not_owned(s)
        if self.jcheat == "not-a-line":
            return self.place_not_a_line(s)
        if self.jcheat == "bad-ask-for-tiles":
            return self.exchange_bad_ask_for_tiles(s)
        if self.jcheat == "no-fit":
            return self.place_no_fit(s)
        raise Exception("Not a valid cheat")


    def new_tiles(self, st: List[Tile]):
        super().new_tiles(st)

    def setup(self, state: PlayerState, tiles: List[Tile]):
        super().setup(state, tiles)

    def win(self, w: bool):
        super().win(w)





