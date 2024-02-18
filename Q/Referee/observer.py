import json
from typing import List

from Q.Common.game_state import GameState
from Q.Common.render import Render
from Q.Referee.observer_ui import ObserverUI
from Q.Referee.observer_ui_callbacks import ObserverUICallback
from Q.Util.util import Util
import pathlib


class Observer(ObserverUICallback):
    """
    Represents a game observer of the Q Game
    """

    def __init__(self):
        self.states: List[GameState] = []
        self.image_name_counter = 0
        self.observer_ui = ObserverUI(self)

    def save_states(self, state, curr_player):
        """
        saves a state to the directory {proj-dir-name}/8/tmp/x.png where x is a sequential number starting at 0.
        :param state: the state that we will save
        :EFFECT updates the image name counter
        """
        public_data = state.extract_player_state(curr_player)
        img = Render(public_data)
        name = self.get_image_path(str(self.image_name_counter))
        img.save(name)
        self.image_name_counter += 1

    def get_image_path(self, name) -> str:
        """
        gets the absolute image path for the tmp files to be saved in proj-dir/8/tmp
        :param name: the file name to be saved
        :return: the absolute path of where to save
        """
        curr_dir = pathlib.Path(__file__).parent.resolve()
        return str(curr_dir) + "/../../8/tmp/" + name + ".png"

    def receive_a_state(self, state: GameState, player_name: str):
        """
        receives a particular state
        :param state: the given state to be saved
        """
        self.states.append(state)
        self.save_states(state, player_name)

    def receive_a_game_over(self):
        """
        receives a notification that the game is over
        """
        self.start_ui()

    def switch(self, state: int):
        """
        goes to the previous state
        """
        fp = self.get_image_path(str(state))
        self.observer_ui.receive_new_image(fp)

    def save_j_state(self, current_state: int, filepath: str):
        if not filepath:
            return
        j_state = Util().convert_gamestate_to_jstate(self.states[current_state])
        j_state_json = json.dumps(j_state)
        with open(filepath, 'w') as f:
            json.dump(j_state_json, f)

    def hasState(self, current_state: int) -> bool:
        return 0 <= current_state < len(self.states)

    def start_ui(self):
        self.observer_ui.run()
