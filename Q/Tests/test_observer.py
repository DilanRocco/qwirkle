import unittest

from Q.Common.Board.pos import Pos
from Q.Common.Board.tile import Tile
from Q.Common.Board.tile_color import TileColor
from Q.Common.Board.tile_shape import TileShape
from Q.Common.game_state import GameState
from Q.Common.map import Map
from Q.Common.player_game_state import PlayerGameState
from Q.Player.ldasg import LDasg
from Q.Player.in_housep_player import InHousePlayer
from Q.Referee.observer import Observer
from Q.Referee.referee import Referee


class TestObserver(unittest.TestCase):
    def setUp(self):
        self.tile1 = Tile(TileShape.CIRCLE, TileColor.BLUE)
        self.tile2 = Tile(TileShape.STAR, TileColor.BLUE)
        self.tile3 = Tile(TileShape.CLOVER, TileColor.GREEN)
        self.player1 = InHousePlayer(strategy=LDasg(), name="bob1", hand=[self.tile2, self.tile3])
        self.pgs1 = PlayerGameState([self.tile2, self.tile3],0,False, None)
        self.player2 = InHousePlayer(strategy=LDasg(), name="bob2", hand=[self.tile2, self.tile3])
        self.pgs2 = PlayerGameState([self.tile2, self.tile3],0,False, None)
        self.player3 = InHousePlayer(strategy=LDasg(), name="bob3", hand=[self.tile2, self.tile3])
        self.pgs3 = PlayerGameState([self.tile2, self.tile3],0,False, None)
        pass

    def test_run_gui(self):
        ref = Referee(observer=Observer())
        pgss = {"bob1":self.pgs1, "bob2":self.pgs2, "bob3":self.pgs3}
        congfig = {
            Pos(0,0) :Tile(TileShape.CIRCLE, TileColor.BLUE)
        }
        map = Map(config=congfig)
        ref.start_from_state([self.player1, self.player2, self.player3], GameState(random_seed=2,player_game_states=pgss,given_map=map))

if __name__ == '__main__':
    unittest.main()
