from game import Game

game = Game()
print(game.initial_state())

while not game.is_finished():
    game.make_move()

winner = "max" if game.max_won() else "min"
print("And the winner is " + winner)
