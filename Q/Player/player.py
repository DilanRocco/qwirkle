from abc import ABC, abstractmethod
from copy import deepcopy
from typing import List, Dict, Optional, Tuple

from Q.Common.Board.pos import Pos
from Q.Common.Board.tile import Tile
from Q.Common.map import Map
from Q.Common.rulebook import Rulebook
from Q.Player.dag import Dag
from Q.Player.player_state import PlayerState
from Q.Player.strategy import PlayerStrategy
from Q.Player.turn import Turn
from Q.Player.turn_outcome import TurnOutcome


class Player(ABC):


    @abstractmethod
    def __init__(self, name, strategy: PlayerStrategy = Dag(), hand: List[Tile] = [], rulebook: Rulebook = Rulebook()):
        """
        # initializes a player with a given name, strategy and hand for the Q Game
        """
        self.strategy = strategy
        self._name = name
        self.hand = hand
        self.rulebook = rulebook

    def name(self) -> str:
        """
        Returns the player's name
        """
        return self._name

    @abstractmethod
    def setup(self, state: PlayerState, tiles: List[Tile]):
        """
        Sets up the game by giving the player their tiles. We do not need to use the given_map but are keeping the
        parameter as this is a public API.
        """
        self.hand = tiles

    @abstractmethod
    def take_turn(self, s: PlayerState) -> Turn:
        """
        takes a turn for a player
        :param s: the public state
        :return: the turn the player does
        """
        return self.get_tile_placement_choices(s)

    @abstractmethod
    def win(self, w: bool) -> None:
        """
        From specs: the player is informed whether it won or not
        :param w: boolean value to be used to inform the player whether they won
        """
        pass

    @abstractmethod
    def new_tiles(self, st: List[Tile]):
        """
        From specs: The player is handed a new set of tiles
        :param st: set of tiles to be handed to the player
        """
        self.hand = st

    def choose_move_type(self, pub_data: PlayerState, tiles_to_place: Dict[Pos, Tile]) -> Turn:
        """
        Returns the move type depending on the strategy and public data.
        :param pub_data: the public data about the game that player knows to determine the move type
        """
        if len(tiles_to_place):
            return Turn(TurnOutcome.PLACED, tiles_to_place)
        if pub_data.num_ref_tiles < len(self.hand):
            return Turn(TurnOutcome.PASSED)
        return Turn(TurnOutcome.REPLACED)

    def get_tile_placement_choices(self, pub_data: PlayerState) -> Turn:
        """
        Gets the placements of the given tiles in the players hand on the given map
        :param pub_data: the public data about the game that player knows to determine the move
        :return a dictionary of position to tile
        """
        tiles_to_place = {}
        copy_hand = deepcopy(self.hand)

        while len(copy_hand):
            placement = self.get_placement(pub_data, self.strategy, copy_hand)
            if not placement:
                break
            pos, tile = placement
            new_hand = tiles_to_place.copy()
            new_hand.update({pos: tile})
            valid = self.rulebook.valid_placement(pub_data.current_map, pos, tile, new_hand)
            if not valid:
                return self.choose_move_type(pub_data, tiles_to_place)
            copy_hand.remove(tile)
            pub_data.current_map.add_tile_to_board(tile, pos)
            tiles_to_place = new_hand.copy()

        return self.choose_move_type(pub_data, tiles_to_place)

    def get_placement(self, pub_data: PlayerState, strategy: PlayerStrategy, hand: List[Tile]) -> Optional[Tuple[Pos, Tile]]:
        """
        Determines a single placement for the given public data state with some given strategy
        :param pub_data: the public data for the player to make the move
        :param strategy: the given strategy to make the move
        :param hand: the legal hand of tiles that can be placed.
        ASSUMPTION: hand is not empty
        """
        tile = strategy.choose_tile_to_play(hand, pub_data.current_map, self.rulebook)
        if not tile:
            return None
        positions = self.rulebook.get_legal_positions(pub_data.current_map, tile, [])

        if not len(positions):
            return None
        position_to_place_tile = strategy.choose_placement(list(positions), pub_data.current_map)

        return position_to_place_tile, tile
