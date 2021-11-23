from copy import deepcopy


class State:
    def __init__(
        self,
        size,
        max_pos,
        min_pos,
        max_move,
        parent=None
    ):
        """
        State object holds information about specific game state.
        This object should never be initialized by user!
        """

        self._size = size
        self._max_pos = max_pos
        self._min_pos = min_pos
        self._parent = parent
        self._max_move = max_move
        self._successors = None
        self._is_terminal = False   # not determined yet
        self._successors_initialized = False
        self._payoff = 0    # not determined yet

        if parent:
            # state has previous state
            self._board = deepcopy(parent.board())
            if max_move:
                # if so, previous move was made by min player
                self._board.color_square(min_pos)
            else:
                # previous move was made by max player
                self._board.color_square(max_pos)

        else:
            # state is initial state
            self._board = Board(size)
            self._board.color_square(max_pos)
            self._board.color_square(min_pos)

    def board(self):
        """
        Returns an Board object
        """
        return self._board

    def table(self):
        """
        Returns a list
        """
        return self.board()._board

    def max_pos(self):
        return self._max_pos

    def min_pos(self):
        return self._min_pos

    def successors(self):
        return self._successors

    def successors_initialized(self):
        return self._successors_initialized

    def initialize_successors(self):
        """
        Sets attribute successors to list of successors
        Sets successors_initialized True to avoid unnecessary
        finding successors in the future
        """
        self._successors = self._find_successors()
        self._successors_initialized = True
        if len(self._successors) == 0:
            self._is_terminal = True

    def _find_payoff(self):
        """
        Finds payoff of state
        Sets _payoff attribute
        When calling this function, successors have to be initialized before
        """
        if self._max_move:
            if self._is_terminal:
                # max has lost, self is terminal state
                payoff = -10
            else:
                # return number of possible moves for max
                payoff = len(self._successors)

        else:   # if min move
            if self._is_terminal:
                # min has lost, self is terminal state
                payoff = 10
            else:
                payoff = (-1) * len(self._successors)

        self._payoff = payoff
        return payoff

    def _create_successor(self, new_pos, max_move):
        if max_move:
            max_new_pos = new_pos
            min_new_pos = self._min_pos
        else:  # min move
            min_new_pos = new_pos
            max_new_pos = self._max_pos

        successor = State(
            size=self._size,
            max_pos=max_new_pos,
            min_pos=min_new_pos,
            max_move=(not max_move),
            parent=self
        )
        return successor

    def _find_successors(self):
        """
        Function finds all possible states available from current state
        Returns a list of State() objects
        """
        max_move = self._max_move
        size = self._size
        player_xy = self._max_pos if max_move else self._min_pos
        x = player_xy[0]
        y = player_xy[1]

        successors = []
        # N, S, W, E - directions
        # check N
        if y != 0:  # checking if square exists
            new_pos = (x, y-1)
            if self._board.square(new_pos) != 1:  # check if square is legal

                # N square is legal
                successor = self._create_successor(new_pos, max_move)
                successors.append(successor)

        # check NE
        if y != 0 and x != size-1:  # checking if NE square exists
            new_pos = (x+1, y-1)
            if self._board.square(new_pos) != 1:  # check if sqare is legal

                # NE square is legal
                successor = self._create_successor(new_pos, max_move)
                successors.append(successor)

        # check E
        if x != size-1:  # checking if square exists
            new_pos = (x+1, y)
            if self._board.square(new_pos) != 1:  # check if square is legal

                # E square is legal
                successor = self._create_successor(new_pos, max_move)
                successors.append(successor)

        # check SE
        if x != size-1 and y != size-1:
            new_pos = (x+1, y+1)
            if self._board.square(new_pos) != 1:

                # SE square is legal
                successor = self._create_successor(new_pos, max_move)
                successors.append(successor)

        # check S
        if y != size-1:
            new_pos = (x, y+1)
            if self._board.square(new_pos) != 1:

                # S square is legal
                successor = self._create_successor(new_pos, max_move)
                successors.append(successor)

        # check SW
        if x != 0 and y != size-1:
            new_pos = (x-1, y+1)
            if self._board.square(new_pos) != 1:

                # SW square is legal
                successor = self._create_successor(new_pos, max_move)
                successors.append(successor)

        # check W
        if x != 0:
            new_pos = (x-1, y)
            if self._board.square(new_pos) != 1:

                # W square is legal
                successor = self._create_successor(new_pos, max_move)
                successors.append(successor)

        # check NW
        if x != 0 and y != 0:
            new_pos = (x-1, y-1)
            if self._board.square(new_pos) != 1:

                # NW square is legal
                successor = self._create_successor(new_pos, max_move)
                successors.append(successor)

        return successors

    def __str__(self):
        """
        A, a - position of player max
        B, b - position of player min
        capital letter - player on move
        """
        if self._max_move:
            max_symbol = 'A'
            min_symbol = 'b'
        else:
            max_symbol = 'a'
            min_symbol = 'B'

        to_return = ""
        for i in range(self._size):
            row = "|"
            for j in range(self._size):
                if self._max_pos == (j, i):
                    row += max_symbol
                elif self._min_pos == (j, i):
                    row += min_symbol
                else:
                    row += str(self._board.square((j, i)))
                row += "|"
            row += "\n"
            to_return += row

        return to_return

    def minimax(self, depth):
        """
        Performs minimax algorithm
        State evaluates itself
        """
        if not self._successors_initialized:
            self.initialize_successors()

        if self._is_terminal or depth == 0:
            return self._find_payoff() if self._payoff == 0 else self._payoff

        rates = []
        for successor in self._successors:
            rate = successor.minimax(depth-1)
            rates.append(rate)

        return max(rates) if self._max_move else min(rates)


class Board:
    def __init__(self, size):
        board = []
        for _ in range(size):
            row = [0 for _ in range(size)]
            board.append(row)

        self._board = board

    def square(self, coordinates):
        x = coordinates[0]
        y = coordinates[1]
        return self._board[y][x]

    def color_square(self, coordinates):
        x = coordinates[0]
        y = coordinates[1]
        self._board[y][x] = 1
