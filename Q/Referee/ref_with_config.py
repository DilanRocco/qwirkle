from typing import List
from Q.Player.player import Player
from Q.Referee.observer import Observer
from Q.Referee.referee import Referee
from Q.Referee.referee_config import RefereeConfig


class RefereeWithConfig(Referee):
    """
    represents a referee with some sort of configuration
    """
    def __init__(self, referee_config: RefereeConfig):
        self.referee_config = referee_config

        observer = Observer() if self.referee_config.observe else None
        super().__init__(observer)

    def main(self, player_list: List[Player]) -> List[List[str]]:
        return self.start_from_state(player_list, self.referee_config.state0)



