import json
import sys

from jsonstream import loads

from Q.Referee.observer import Observer
from Q.Referee.referee import Referee
from Q.Util.util import Util


def main():
    stream = loads(sys.stdin.read())
    j_state = next(stream)
    j_actors = next(stream)
    game_state = Util().convert_jstate_to_gamestate(jstate=j_state)
    players = Util().jactors_to_players(j_actors)
    referee = Referee(observer=Observer()) if show_command() else Referee()
    pair_results = referee.start_from_state(players, game_state)
    print(json.dumps(pair_results))


def show_command():
    return len(sys.argv) > 1 and sys.argv[1] == "--show"


if __name__ == "__main__":
    main()
