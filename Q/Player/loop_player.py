from abc import ABC
from typing import List
from Q.Common.map import Map
from Q.Common.Board.tile import Tile
from Q.Common.rulebook import Rulebook
from Q.Player.dag import Dag
from Q.Player.player import Player
from Q.Player.turn import Turn

from Q.Player.strategy import PlayerStrategy
from Q.Player.player_state import PlayerState


class LoopPlayer(Player, ABC):
    """
    # represents a Player of a game
    """

    def __init__(self, name, exn: str, count: int, strategy: PlayerStrategy = Dag(), hand: List[Tile] = [], rulebook: Rulebook = Rulebook()):
        """
        creates a player with an exn function that infinite loops on that function on the kth time where k = count
        """
        super().__init__(name=name, strategy=strategy, hand=hand,rulebook=rulebook)
        self.exn = exn
        self.count = count

    def loop(self):
        while True:
            pass

    def new_tiles(self, st: List[Tile]):
        if self.exn != "new-tiles":
            return super().new_tiles(st)
        self.count -= 1
        if self.count == 0:
            self.loop()

    def setup(self, state: PlayerState, tiles: List[Tile]):
        if self.exn != "setup":
            return super().setup(state, tiles)
        self.count -= 1
        if self.count == 0:
            self.loop()

    def win(self, w: bool):
        if self.exn != "win":
            return super().win(w)
        self.count -= 1
        if self.count == 0:
            self.loop()

    def take_turn(self, s: PlayerState) -> Turn:
        if self.exn != "take-turn":
            return super().take_turn(s)
        self.count -= 1
        if self.count == 0:
            self.loop()
