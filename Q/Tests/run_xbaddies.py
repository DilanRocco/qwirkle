import json
import sys

from jsonstream import loads

from Q.Referee.referee import Referee
from Q.Util.util import Util


def main():
    stream = loads(sys.stdin.read())
    j_state = next(stream)
    j_actors = next(stream)
    game_state = Util().convert_jstate_to_gamestate(jstate=j_state)
    players = Util().jactors_to_players(j_actors)
    pair_results = Referee().start_from_state(players, game_state)
    print(json.dumps(pair_results))


if __name__ == "__main__":
    main()
