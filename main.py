from game import Game

game = Game()
print(game.initial_state())
for _ in range(10):
    game.make_move()

