from game import (
    Game,
    Board,
    State,
    PlayerPositionOutOfRange
)
import pytest


def test_initialize_game_default():
    game = Game()
    expected_board = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]
    assert game.table() == expected_board
    assert game.max_pos() == (0, 0)
    assert game.min_pos() == (3, 3)


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
    successors = state.find_successors()
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
    payoff = state.find_payoff()
    assert payoff == 3
