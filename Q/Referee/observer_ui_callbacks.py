

class ObserverUICallback:
    """
    Represents the functions an observer UI can call on the Observer
    """

    def switch(self, state: int):
        """
        switches to a new state
        ASSUMPTION: hasState has been called before this method to see if a particular state exists
        :param state: the state to switch to
        """
        pass

    def save_j_state(self, current_state: int, filepath: str):
        """
        the state you want to save at the given file path
        :param current_state: the saved states index that is being saved
        :param filepath: the placed in which the state is saved
        """
        pass

    def hasState(self, current_state: int) -> bool:
        """
        is the given state a possible state to jump to
        :param current_state: the state that is in question if it exists
        :return: true if the state exists in the observer, else false
        """
        pass
