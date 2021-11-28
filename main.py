import json
import os
from game import Game
# ========================== 1000 games ===================================

max_count = 0
min_count = 0

for _ in range(1000):
    game = Game(
        size=4,
        max_tactic='minimax',
        min_tactic='random',
        depth=5,
        max_move=True
        )

# =============== storing data ==================
    data = {
        'size': game.size(),
        'max_pos': game.max_pos(),
        'min_pos': game.min_pos(),
        'max_tactic': game.max_tactic(),
        'min_tactic': game.min_tactic(),
        'max_move': game.max_move(),
        'depth': game.depth()
    }

# =============== game execution ==============

    while not game.is_finished():
        game.make_move()

    if game.max_won():
        max_count += 1
    else:
        min_count += 1

data['max_result'] = max_count
data['min_result'] = min_count

print("Max result: ", max_count)
print("Min result: ", min_count)

# ================== saving to file ==================

fname = "info.json"

if not os.path.isfile(fname):
    a = []
    a.append(data)
    with open(fname, mode='w') as file_handle:
        file_handle.write(json.dumps(a, indent=2))
else:
    with open(fname) as feedsjson:
        feeds = json.load(feedsjson)

    feeds.append(data)
    with open(fname, mode='w') as file_handle:
        file_handle.write(json.dumps(feeds, indent=2))
