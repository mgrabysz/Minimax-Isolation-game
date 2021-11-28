from classes import (
    Board,
    State,
)
from game import Game, PlayerPositionOutOfRange
import pytest


def test_player_out_of_range():
    with pytest.raises(PlayerPositionOutOfRange):
        Game(max_pos=(4, 2))


def test_color_square():
    board = Board(4)
    board.color_square((1, 0))
    board.color_square((2, 2))
    expected_board = [
        [0, 1, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 0],
    ]
    assert board._board == expected_board


def test_state_initialize():
    state = State(4, max_pos=(3, 3), min_pos=(0, 0), max_move=True)
    expected_board = [
        [1, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 1],
    ]
    assert state.table() == expected_board


def test_state_successors():
    state = State(4, max_pos=(3, 3), min_pos=(0, 0), max_move=True)
    successors = state._find_successors()
    assert len(successors) == 3
    n_suc_expected_table = [
        [1, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 0, 1],
    ]
    n_successor = successors[0]
    assert n_successor.table() == n_suc_expected_table

    w_suc_expected_table = [
        [1, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 1, 1],
    ]
    w_successor = successors[1]
    assert w_successor.table() == w_suc_expected_table

    nw_suc_expected_table = [
        [1, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ]
    nw_successor = successors[2]
    assert nw_successor.table() == nw_suc_expected_table


def test_find_payoff():
    state = State(4, max_pos=(3, 3), min_pos=(0, 0), max_move=True)
    state.initialize_successors()
    payoff = state._find_payoff()
    assert payoff == 3


def test_minimax_depth_0_max_move():
    state = State(4, max_pos=(3, 3), min_pos=(0, 0), max_move=True)
    payoff = state.minimax(0)
    assert payoff == 3


def test_minimax_depth_0_min_move():
    state = State(4, max_pos=(3, 3), min_pos=(0, 0), max_move=False)
    payoff = state.minimax(0)
    assert payoff == -3


def test_minimax_depth_1_max_move():
    state = State(4, max_pos=(3, 3), min_pos=(0, 0), max_move=True)
    payoff = state.minimax(1)
    assert payoff == -3


def test_minimax_depth_1_min_move():
    state = State(4, max_pos=(3, 3), min_pos=(0, 0), max_move=False)
    payoff = state.minimax(1)
    assert payoff == 3
