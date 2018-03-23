# -*- coding:utf-8 -*-

import argparse
import random
import itertools

# ********** PARAMETERS

parser = argparse.ArgumentParser(description='Stochastic NIM solver.')
parser.add_argument('trials', metavar='trials', type=int, nargs='?', default=100000, help='Number of games played for statistics.')
parser.add_argument('rows', metavar='rows', type=int, nargs='?', default=3, help='Number of rows.')
parser.add_argument('min_pin_count', metavar='pin_cnt', type=int, nargs='?', default=3, help='Number of pins on the row with less pins.')
parser.add_argument('players', type=int, nargs='?', default=2, help='Number of players playing.')
args = parser.parse_args()

PLAYER_COUNT = args.players
ROW_COUNT = args.rows
MIN_PIN_COUNT = args.min_pin_count
TRIALS = args.trials

# ********** CLASSES

class Row:
    def __init__(self, pin_count : int) -> int :
        self.pin_count = pin_count
    
    def take(self, pins : int) -> int :
        '''
        returns how many pins were actually removed
        (and removes them)
        '''
        if self.pin_count < 1:
            raise ValueError('Cannot remove pins from empty row!')
        pins = max(1, min(self.pin_count, pins))
        self.pin_count -= pins
        return pins
    
    def get_pins(self) -> int :
        return self.pin_count

class Player:
    def __init__(self):
        self.plays = []
    
    def register_play(self, board_configuration, row_played, removal_count):
        play = (board_configuration, (row_played, removal_count))
        self.plays.append(play)
    
    def get_plays(self):
        return self.plays

# ********** CONTENTS

# board configuration in (row_1_pins, row_2_pins, ...) -> 
#   -> play in format (row, pins_removed) ->
#       -> statistical score
statistics = {}
for configuration in itertools.product(*(range(0, MIN_PIN_COUNT+row+1) for row in range(ROW_COUNT))):
    
    statistics[configuration] = {}

    for row in range(ROW_COUNT):
        for pins_removed in range(1, configuration[row] + 1):
            statistics[configuration][(row, pins_removed)] = 0


for trial in range(TRIALS):
    # rows = [Row(3), Row(4), Row(5), ...]
    rows = list(Row(MIN_PIN_COUNT + i) for i in range(ROW_COUNT))

    def total_pins():
        return sum(row.get_pins() for row in rows)

    def next_player(current_player, total_players):
        return (current_player + 1)%total_players
    
    def prev_player(current_player, total_players):
        return (current_player-1)%total_players

    players = []
    for i in range(PLAYER_COUNT):
        players.append(Player())

    current_player_index = -1

    while total_pins() > 0:
        # Move to next player
        current_player_index = next_player(current_player_index, PLAYER_COUNT)
        current_player = players[current_player_index]

        # Find the available choices
        current_board_config = tuple(row.get_pins() for row in rows)
        available_choices = list(statistics[current_board_config].keys())

        # Find the best choices
        def get_score_of (choice):
            return statistics[current_board_config][choice]
        
        best_choice_value = get_score_of( max(available_choices, key= lambda choice: get_score_of(choice)) )
        best_choices = tuple ( filter(lambda choice: get_score_of(choice) == best_choice_value, available_choices) )

        # Choose an action
        # (row to remove from, number of pins in that row, how many pins to remove)
        play = random.choice(best_choices)
        row_to_remove_from = play[0]
        pins_to_remove = play[1]

        # Do and register stuff
        current_player.register_play(tuple(row.get_pins() for row in rows), row_to_remove_from, pins_to_remove)
        rows[row_to_remove_from].take(pins_to_remove)
    
    # Game over, update statistics
    won = players[prev_player(current_player_index, PLAYER_COUNT)]
    lost = filter(lambda player: player != won, players)

    for winning_play in won.get_plays():
        board_config = winning_play[0]
        play = winning_play[1]
        statistics[board_config][play] += PLAYER_COUNT - 1
    
    for losing_player in lost:
        for losing_play in losing_player.get_plays():
            board_config = winning_play[0]
            play = winning_play[1]
            statistics[board_config][play] -= 1

# Print final statistics

print("Board configuration:  (pins in row1,  pins in row2,  pins in row3, ...)")
print("Best plays: (from row I, remove X pins), ...")

for configuration in statistics:
    # Find all best plays
    def get_score_of(play):
        return statistics[configuration][play]
    
    if len(statistics[configuration]) == 0:
        continue

    best_play_score = get_score_of( max(statistics[configuration], key=get_score_of) )
    best_plays = tuple( filter(lambda play: get_score_of(play) == best_play_score, statistics[configuration]) )

    print("Board configuration: " + str(configuration))
    print("Best plays: " + " ".join(map(lambda x: str(x), best_plays)))