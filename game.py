from classes import State
from random import choice


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
    _max_tactic : string
        "random", "minimax" or "user"
    _min_tactic : string
        "random", "minimax" or "user"
    _initial_state : State
        initial state
    _current_state : State
        current state
    _is_finished : bool
        is True if game is finished
    _max_won : bool
        is True if max has won (otherwise min has won)
    _print_moves : bool
        if is True, every move will be printed
    """

    def __init__(
        self,
        size=4,
        max_pos=None,
        min_pos=None,
        max_tactic="random",
        min_tactic="random",
        max_move=True,
        depth=2,
        print_moves=False
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

        if max_tactic not in ["random", "minimax", "user"]:
            raise Exception
        if max_tactic not in ["random", "minimax", "user"]:
            raise Exception

        self._max_tactic = max_tactic
        self._min_tactic = min_tactic
        self._size = size
        self._max_move = max_move
        self._is_finished = False
        self._max_won = False  # not valid while is_finished is False
        self._depth = depth
        self._print_moves = print_moves

        self._initial_state = State(
            size=size,
            max_pos=self._max_pos,
            min_pos=self._min_pos,
            max_move=self._max_move
        )

        self._current_state = self._initial_state
        self._current_state.initialize_successors()

        if self._print_moves:
            print(self._current_state)

# =================== getters =======================

    def initial_state(self):
        return self._initial_state

    def is_finished(self):
        return self._is_finished

    def max_won(self):
        return self._max_won

    def max_tactic(self):
        return self._max_tactic

    def min_tactic(self):
        return self._min_tactic

    def max_move(self):
        return self._max_move

    def depth(self):
        return self._depth

    def size(self):
        return self._size

    def max_pos(self):
        return self._max_pos

    def min_pos(self):
        return self._min_pos

# ==================== main methods =======================

    def make_move(self):
        """
        Makes move of the actual player
        Using minimax algorithm if player_tactic is True
        Otherwise randomly
        """
        if self._max_move:
            if self._max_tactic == "minimax":
                self._move_minimax()
            elif self._max_tactic == "random":
                possible_states = self._current_state.successors()
                new_state = choice(possible_states)
                self._current_state = new_state
            else:   # user plays
                self._move_user()

        else:   # min move
            if self._min_tactic == "minimax":
                self._move_minimax()
            elif self._min_tactic == "random":
                possible_states = self._current_state.successors()
                new_state = choice(possible_states)
                self._current_state = new_state
            else:   # user plays
                self._move_user()

        if self._print_moves:
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
        current_best_states = []
        random_state = choice(self._current_state.successors())
        current_best_states.append(random_state)
        current_best_rate = random_state.minimax(self._depth)

        for successor in self._current_state.successors():
            rate = successor.minimax(self._depth)

            if rate == current_best_rate:
                current_best_states.append(successor)
            elif self._max_move:
                if rate > current_best_rate:
                    current_best_states.clear()
                    current_best_states.append(successor)
                    current_best_rate = successor.minimax(self._depth)
            else:    # min move
                if rate < current_best_rate:
                    current_best_states.clear()
                    current_best_states.append(successor)
                    current_best_rate = successor.minimax(self._depth)

        self._current_state = choice(current_best_states)

    def _move_user(self):
        """
        This function should not be called by user
        Function assumes that current state is initialized
        """

        directions = {}

        if self._max_move:
            curr_pos = self._current_state.max_pos()
        else:
            curr_pos = self._current_state.min_pos()

        for successor in self._current_state.successors():
            if self._max_move:
                new_pos = successor.max_pos()
            else:
                new_pos = successor.min_pos()

            vector = (new_pos[0] - curr_pos[0], new_pos[1] - curr_pos[1])

            if vector == (0, -1):   # N
                dir = 'N'
            elif vector == (1, -1):
                dir = 'NE'
            elif vector == (1, 0):
                dir = 'E'
            elif vector == (1, 1):
                dir = 'SE'
            elif vector == (0, 1):
                dir = 'S'
            elif vector == (-1, 1):
                dir = 'SW'
            elif vector == (-1, 0):
                dir = 'W'
            elif vector == (-1, -1):
                dir = 'NW'
            else:
                raise Exception

            directions[dir] = successor

        input_is_valid = False

        while not input_is_valid:
            user_input = input("> ")
            if user_input in directions:
                input_is_valid = True

        self._current_state = directions[user_input]
