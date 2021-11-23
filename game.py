from classes import State
from random import choice, random


class PlayerPositionOutOfRange(Exception):
    def __init__(self):
        super().__init__("Player position out of range")


class Game():
    """
    Attributes
    ----------
    _max_pos : tuple
        position of player max
    _min_pos : tuple
        position of player min
    _max_move : bool
        is True if max player is on move
    _max_tactic : bool
        is True if max player uses minimax algorithm
    _min_tactic : bool
        is True if min player uses minimax algorithm
    _initial_state : State
        initial state
    _current_state : State
        current state
    _is_finished : bool
        is True if game is finished
    _max_won : bool
        is True if max has won (otherwise min has won)
    """

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
        self._is_finished = False
        self._max_won = False  # not valid while is_finished is False

        self._initial_state = State(
            size=size,
            max_pos=self._max_pos,
            min_pos=self._min_pos,
            max_move=self._max_move
        )

        self._current_state = self._initial_state
        self._current_state.initialize_successors()

    def initial_state(self):
        return self._initial_state

    def is_finished(self):
        return self._is_finished

    def max_won(self):
        return self._max_won

    def make_move(self):
        """
        Makes move of the actual player
        Using minimax algorithm if player_tactic is True
        Otherwise randomly
        """
        if self._max_move:
            if self._max_tactic:
                self._move_minimax()
            else:   # max plays randomly
                if not self._current_state.successors():
                    self._current_state.initialize_successors()

                possible_states = self._current_state.successors()
                new_state = choice(possible_states)
                self._current_state = new_state
                print(self._current_state)

        else:   # min move
            if self._min_tactic:
                self._move_minimax()
            else:   # min plays randomly
                if not self._current_state.successors():
                    self._current_state.initialize_successors()

                possible_states = self._current_state.successors()
                new_state = choice(possible_states)
                self._current_state = new_state
                print(self._current_state)

        self._max_move = not self._max_move
        self._current_state.initialize_successors()

        if not self._current_state.successors():
            self._is_finished = True
            self._max_won = False if self._max_move else True

    def _move_minimax(self):
        """
        This function should not be called by user
        Function assumes that current state is initialized
        """
        current_best_state = choice(self._current_state.successors())
        current_best_rate = current_best_state.minimax()

        for successor in self._current_state.successors():
            rate = successor.minimax()

            if rate == current_best_rate and random() < 0.5:
                current_best_state = successor
                current_best_rate = current_best_state.minimax()
            elif self._max_move:
                if rate > current_best_rate:
                    current_best_state = successor
                    current_best_rate = current_best_state.minimax()
            else:    # min move
                if rate < current_best_rate:
                    current_best_state = successor
                    current_best_rate = current_best_state.minimax()

        self._current_state = current_best_state
