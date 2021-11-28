# ================= single game with printing moves =======================
from game import Game

move_counter = 0
print(move_counter)

game = Game(
    size=4,
    max_tactic='minimax',
    min_tactic='random',
    depth=5,
    max_move=True,
    print_moves=True
    )

while not game.is_finished():
    move_counter += 1
    print(move_counter)
    game.make_move()

winner = "max" if game.max_won() else "min"
print("And the winner is " + winner)
