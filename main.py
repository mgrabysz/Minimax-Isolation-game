from game import Game

# game = Game(max_tactic=True, depth=2)

# while not game.is_finished():
#     game.make_move()

# winner = "max" if game.max_won() else "min"
# print("And the winner is " + winner)


max_count = 0
min_count = 0
for _ in range(100):
    game = Game(size=5, max_tactic=True, min_tactic=True, depth=2, max_move=False)

    while not game.is_finished():
        game.make_move()

    if game.max_won():
        max_count += 1
    else:
        min_count += 1

print("Max result: ", max_count)
print("Min result: ", + min_count)
