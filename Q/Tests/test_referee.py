import unittest

from Q.Common.Board.tile_color import TileColor
from Q.Common.Board.tile_shape import TileShape
from Q.Common.map import Map
from Q.Common.Board.tile import Tile
from Q.Common.Board.pos import Pos
from Q.Common.game_state import GameState
from Q.Common.player_game_state import PlayerGameState
from Q.Common.rulebook import Rulebook
from Q.Player.in_housep_player import InHousePlayer
from Q.Player.dag import Dag
from Q.Player.ldasg import LDasg
from Q.Player.in_housep_player import PlayerState
from Q.Player.turn import Turn
from Q.Player.turn_outcome import TurnOutcome
from Q.Referee.pair_results import Results
from Q.Referee.referee import Referee
from Q.Common.render import Render

class TestReferee(unittest.TestCase):
    def setUp(self):
        self.tile1 = Tile(TileShape.CIRCLE, TileColor.BLUE)
        self.tile2 = Tile(TileShape.STAR, TileColor.BLUE)
        self.tile3 = Tile(TileShape.CLOVER, TileColor.BLUE)
        self.tile4 = Tile(TileShape.SQUARE, TileColor.BLUE)
        self.tile5 = Tile(TileShape.EIGHTSTAR, TileColor.BLUE)
        self.tile6 = Tile(TileShape.DIAMOND, TileColor.BLUE)
        self.tile7 = Tile(TileShape.STAR, TileColor.GREEN)
        self.tile8 = Tile(TileShape.SQUARE, TileColor.PURPLE)
        self.tiles = [self.tile2, self.tile3, self.tile4, self.tile5, self.tile6]
        self.positions = [Pos(0, 1), Pos(0, 2), Pos(0, 3), Pos(0, 4), Pos(0, 5)]
        self.config1 = {Pos(0, 1): self.tile2,
                        Pos(0, 2): self.tile3,
                        Pos(0, 3): self.tile4,
                        Pos(0, 4): self.tile5,
                        Pos(0, 5): self.tile6}

        self.player1 = InHousePlayer(strategy=Dag(), name="bob", hand=self.tiles)
        self.player2 = InHousePlayer(strategy=LDasg(), name="bob2", hand=[self.tile3, self.tile7])
        self.ref_tile = {Pos(0, 0): self.tile1}
        self.m1 = Map(config=self.ref_tile)
        self.ppd = PlayerState(20, self.m1, {})
        self.gs = GameState(self.ppd)
        self.gs.place_tiles(tiles=self.config1)

        self.config2 = {Pos(0, 1): self.tile5, Pos(1, 0): self.tile4, Pos(1, 1): self.tile3}
        self.m2 = Map(config=self.config2)

        self.config3 = {Pos(0, 0): self.tile5,
                        Pos(0, 1): self.tile6,
                        Pos(1, 1): self.tile6,
                        Pos(2, 1): self.tile6}
        self.m3 = Map(config=self.config3)
        self.ppd3 = PlayerState(1080, self.m3, {})
        self.player3 = InHousePlayer(strategy=LDasg(), name="bob3", hand=[self.tile2, self.tile3])

        self.config4 = {
            Pos(0, 0): self.tile1,
            Pos(0, 1): self.tile1,
            Pos(0, 2): self.tile1,
            Pos(1, 2): self.tile1,
            Pos(2, 2): self.tile1,
            Pos(2, 1): self.tile1,
            Pos(2, 0): self.tile1,
            Pos(1, 0): self.tile1,
        }
        self.m4 = Map(config=self.config4)
        self.ppd4 = PlayerState(1080, self.m4, {})
        self.player4 = InHousePlayer(strategy=LDasg(), name="bob4", hand=[self.tile8])
        self.player5 = InHousePlayer(strategy=LDasg(), name="bob5", hand=[self.tile8, self.tile1])
        self.player6 = InHousePlayer(strategy=LDasg(), name="bob6", hand=[self.tile1, self.tile2])
        self.player7 = InHousePlayer(strategy=LDasg(), name="bob7", hand=[self.tile1, self.tile2])

    def test_run(self):
        """
        Runs the game with two dags
        """
        referee = Referee()
        player1 = InHousePlayer(strategy=Dag(), name="bob", hand=self.tiles)
        player2 = InHousePlayer(strategy=Dag(), name="dan", hand=self.tiles)

        pgs = {
            "bob": PlayerGameState(self.player1.hand, 0, False, None),
            "dan": PlayerGameState(self.tiles, 0, False, None)
        }
        gs = GameState(given_map=self.m1, tiles=self.tiles, random_seed=1234, player_game_states=pgs)
        players = [player1, player2]
        pair_results = referee.start_from_state(players, gs)
        self.assertEqual(pair_results, Results(winners={'bob'}, misbehaved=set()))

    def test_signup(self):
        """
        Tests to see if you can sign up 2 players
        """
        referee = Referee()
        player_list = [InHousePlayer(strategy=Dag(), name="dag"), InHousePlayer(strategy=LDasg(), name="ldasg")]
        referee.signup_players(player_list=player_list, game_state=self.gs)
        self.assertEqual(len(self.gs.players), 2)

    def test_signup2(self):
        """
        Tests to see if you cant signup more than 4 players
        """
        referee = Referee()
        player_list = [
            InHousePlayer(strategy=Dag(), name="dag1"),
            InHousePlayer(strategy=LDasg(), name="ldasg1"),
            InHousePlayer(strategy=Dag(), name="dag2"),
            InHousePlayer(strategy=LDasg(), name="ldasg2"),
            InHousePlayer(strategy=LDasg(), name="extra_player"),
        ]
        referee.signup_players(player_list=player_list, game_state=self.gs)
        self.assertEqual(player_list.gs.players, 4)

    def test_game_with_one_player(self):
        """
        Tests the game with one player added
        """
        referee = Referee()
        player1 = InHousePlayer(strategy=Dag(), name="bob", hand=self.tiles)

        pgs = {
            "bob": PlayerGameState(self.player1.hand, 0, False, None)
        }
        gs = GameState(given_map=self.m1, tiles=self.tiles, random_seed=1234, player_game_states=pgs)
        pair_results = referee.start_from_state([player1], gs)
        self.assertEqual(pair_results, Results(winners={'bob'}, misbehaved=set()))

    def test_round(self):
        #TODO
        pass

    def test_turn(self):
        #TODO
        pass




if __name__ == '__main__':
    unittest.main()
