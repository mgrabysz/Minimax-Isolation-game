from classes import State
from random import choice


class PlayerPositionOutOfRange(Exception):
    def __init__(self):
        super().__init__("Player position out of range")


class Game():
    def __init__(
        self,
        size=4,
        max_pos=None,
        min_pos=None,
        max_tactic=False,
        min_tactic=False,
        max_move=True,
        depth=2,
    ):

        if not max_pos:
            self._max_pos = (0, 0)
        else:
            if max_pos[0] > size-1 or max_pos[1] > size-1:
                raise PlayerPositionOutOfRange
            self._max_pos = max_pos

        if not min_pos:
            self._min_pos = (size-1, size-1)
        else:
            if min_pos[0] > size-1 or min_pos[1] > size-1:
                raise PlayerPositionOutOfRange
            self._min_pos = min_pos

        self._max_move = max_move
        self._max_tactic = max_tactic
        self._min_tactic = min_tactic

        self._initial_state = State(
            size=size,
            max_pos=self._max_pos,
            min_pos=self._min_pos,
            max_move=self._max_move
        )

        self._current_state = self._initial_state

    def initial_state(self):
        return self._initial_state

    def make_move(self):
        if self._max_move:
            if self._max_tactic:
                pass
            else:   # max plays randomly
                if not self._current_state.successors():
                    self._current_state.initialize_successors()

                possible_states = self._current_state.successors()
                new_state = choice(possible_states)
                self._current_state = new_state
                print(self._current_state)

        else:   # min move
            if self._min_tactic:
                pass
            else:   # min plays randomly
                if not self._current_state.successors():
                    self._current_state.initialize_successors()

                possible_states = self._current_state.successors()
                new_state = choice(possible_states)
                self._current_state = new_state
                print(self._current_state)

        self._max_move = not self._max_move

    def minimax(self):
        pass
