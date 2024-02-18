import unittest
from collections import defaultdict

from Q.Common.Board.pos import Pos
from Q.Common.Board.tile import Tile
from Q.Common.Board.tile_color import TileColor
from Q.Common.Board.tile_shape import TileShape
from Q.Common.map import Map
from Q.Player.cheat_player import CheatPlayer
from Q.Player.dag import Dag
from Q.Player.player_state import PlayerState
from Q.Player.turn_outcome import TurnOutcome


class TestObserver(unittest.TestCase):
    def setUp(self):
        tile1 = Tile(TileShape.STAR, TileColor.GREEN)
        tile2 = Tile(TileShape.CIRCLE, TileColor.RED)
        tile3 = Tile(TileShape.CLOVER, TileColor.RED)
        tile4 = Tile(TileShape.EIGHTSTAR, TileColor.BLUE)
        tile5 = Tile(TileShape.STAR, TileColor.YELLOW)
        tile6 = Tile(TileShape.SQUARE, TileColor.PURPLE)
        tile7 = Tile(TileShape.DIAMOND, TileColor.ORANGE)
        tile8 = Tile(TileShape.DIAMOND, TileColor.YELLOW)
        tile9 = Tile(TileShape.CLOVER, TileColor.BLUE)
        tile10 = Tile(TileShape.EIGHTSTAR, TileColor.GREEN)
        pos00 = Pos(0, 0)
        pos01 = Pos(0, 1)
        pos10 = Pos(1, 0)
        pos11 = Pos(1, 1)
        pos21 = Pos(2, 1)
        pos12 = Pos(1, 2)
        pos20 = Pos(2, 0)
        pos30 = Pos(3, 0)
        self.hand1 = [tile1, tile2, tile3]
        self.hand2 = [tile3, tile4, tile5]
        self.config1 = defaultdict(Tile,
                                   {
                                       pos00: tile1,
                                       pos01: tile5,
                                       pos10: tile10,
                                   })
        self.config2 = defaultdict(Tile,
                                   {
                                       pos10: tile10,
                                   })

        self.m1 = Map(config=self.config1)
        self.m2 = Map()
        self.m3 = Map(config=self.config2)
        self.pub1 = PlayerState(20, self.m1, {"dilan": 10, "evan": 5})
        self.pub2 = PlayerState(100, self.m2, {"dilan": 20})
        self.pub3 = PlayerState(10, self.m3, {"dilan": 20})
        self.pub4 = PlayerState(1, self.m3, {"dilan": 20})
        pass

    def test_non_adjacent_coordinate_cheat1(self):
        player2 = CheatPlayer(name="evan", strategy=Dag(), hand=self.hand2.copy(), cheat="non-adjacent-coordinate")
        turn = player2.take_turn(self.pub1)

        all_blank_neighbors = []
        for pos, tile in turn.placements.items():
            neighbors = self.pub1.current_map.get_neighbors(pos)
            all_blank_neighbors.append((all(self.pub1.current_map.tiles.get(neigh) is None for neigh in neighbors)))

        self.assertEqual(True, any(all_blank_neighbors))

    def test_non_adjacent_coordinate_cheat2(self):
        player2 = CheatPlayer(name="evan", strategy=Dag(), hand=self.hand2.copy(), cheat="non-adjacent-coordinate")
        turn = player2.take_turn(self.pub2)

        all_blank_neighbors = []
        for pos, tile in turn.placements.items():
            neighbors = self.pub1.current_map.get_neighbors(pos)
            all_blank_neighbors.append((all(self.pub1.current_map.tiles.get(neigh) is None for neigh in neighbors)))

        self.assertEqual(True, any(all_blank_neighbors))

    def test_tile_not_owned_cheat1(self):
        player2 = CheatPlayer(name="dilan", strategy=Dag(), hand=self.hand1.copy(), cheat="tile-not-owned")
        turn = player2.take_turn(self.pub1)

        tile_not_in_hand = []
        for pos, tile in turn.placements.items():
            tile_not_in_hand.append(False if tile in self.hand1.copy() else True)

        self.assertEqual(True, any(tile_not_in_hand))

    def test_tile_now_owned_cheat2(self):
        player2 = CheatPlayer(name="dilan", strategy=Dag(), hand=self.hand2.copy(), cheat="tile-not-owned")
        turn = player2.take_turn(self.pub1)

        tile_not_in_hand = []
        for pos, tile in turn.placements.items():
            tile_not_in_hand.append(False if tile in self.hand1.copy() else True)

        self.assertEqual(True, any(tile_not_in_hand))

    def test_not_a_line_cheat1(self):
        player = CheatPlayer(name="dilan", strategy=Dag(), hand=self.hand2.copy(), cheat="not-a-line")
        turn = player.take_turn(self.pub1)
        x_values = [pos.x for pos in turn.placements.keys()]
        y_values = [pos.y for pos in turn.placements.keys()]
        self.assertEqual(True, len(set(x_values)) > 1 or len(set(y_values)) > 1)

    def test_not_a_line_cheat2(self):
        player = CheatPlayer(name="dilan", strategy=Dag(), hand=self.hand2.copy(), cheat="not-a-line")
        turn = player.take_turn(self.pub3)
        x_values = [pos.x for pos in turn.placements.keys()]
        y_values = [pos.y for pos in turn.placements.keys()]
        self.assertEqual(True, len(set(x_values)) > 1 or len(set(y_values)) > 1)

    def test_bad_ask_for_tiles_cheat1(self):
        player = CheatPlayer(name="dilan", strategy=Dag(), hand=self.hand2.copy(), cheat="bad-ask-for-tiles")
        turn = player.take_turn(self.pub4)
        self.assertEqual(turn.turn_outcome, TurnOutcome.REPLACED)
        self.assertEqual(True, self.pub4.num_ref_tiles < len(self.hand2))

    def test_bad_ask_for_tiles_cant_cheat1(self):
        player = CheatPlayer(name="dilan", strategy=Dag(), hand=self.hand2.copy(), cheat="bad-ask-for-tiles")
        turn = player.take_turn(self.pub3)
        self.assertEqual(TurnOutcome.REPLACED, turn.turn_outcome)
        # can't cheat here
        self.assertEqual(False, self.pub3.num_ref_tiles < len(self.hand2))

    def test_no_fit_cheat1(self):
        player = CheatPlayer(name="dilan", strategy=Dag(), hand=self.hand2.copy(), cheat="no-fit")
        turn = player.take_turn(self.pub3)
        any_no_fit = []
        for pos, tile in turn.placements.items():
            neighbors = self.pub1.current_map.get_neighbors(pos)
            non_empty_neighbors = [x for x in neighbors.values() if x is not None]
            any_no_fit.append((any(neigh.color != tile.color or
                                   neigh.shape != tile.shape for neigh in non_empty_neighbors)))

        self.assertEqual(True, any(any_no_fit))

    def test_no_fit_cheat2(self):
        player = CheatPlayer(name="dilan", strategy=Dag(), hand=self.hand2.copy(), cheat="no-fit")
        turn = player.take_turn(self.pub3)
        any_no_fit = []
        for pos, tile in turn.placements.items():
            neighbors = self.pub1.current_map.get_neighbors(pos)
            non_empty_neighbors = [x for x in neighbors.values() if x is not None]
            any_no_fit.append((any(neigh.color != tile.color or
                                   neigh.shape != tile.shape for neigh in non_empty_neighbors)))

        self.assertEqual(True, any(any_no_fit))



if __name__ == '__main__':
    unittest.main()
