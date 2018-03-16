# -*- coding:utf-8 -*-

import argparse
import random

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
    
    def register_play(self, row_index, pins_before_removal, removed):
        play = (row_index, pins_before_removal, removed)
        self.plays.append(play)
    
    def get_plays(self):
        return self.plays

# ********** CONTENTS

# (row index, pins in that row, pin removal count)
statistics = {}
for row in range(ROW_COUNT):                                        # For each row...
    row_pin_count = MIN_PIN_COUNT + row                             # ... which has `row_pin_count` pins...
    for possible_pin_count in range(1, row_pin_count + 1):          # ... for each possible number of pins remaining ...
        for pin_remove_count in range(1, possible_pin_count + 1):   # ... for each pin removal count ...
            key = (row, possible_pin_count, pin_remove_count)       # ... initialize score to 0
            value = 0
            statistics[key] = value

for trial in range(TRIALS):

    # rows = [Row(3), Row(4), Row(5)]
    rows = list(Row(MIN_PIN_COUNT + i) for i in range(ROW_COUNT))

    def total_pins():
        return sum(row.get_pins() for row in rows)

    def next_player(current_player, total_players):
        return (current_player + 1)%total_players

    players = []
    for i in range(PLAYER_COUNT):
        players.append(Player())

    current_player_index = -1

    while total_pins() > 0:
        # Move to next player
        current_player_index = next_player(current_player_index, PLAYER_COUNT)
        current_player = players[current_player_index]

        # Find the available choices
        available_choices = list( filter( lambda choice: rows[choice[0]].get_pins() == choice[1] , statistics ) )

        # Find the best choices
        best_choice_value = statistics[ max(available_choices, key = lambda choice: statistics[choice]) ]
        best_choices = list( filter( lambda choice: statistics[choice] == best_choice_value , available_choices ) )

        # Choose an action
        # (row to remove from, number of pins in that row, how many pins to remove)
        play = random.choice(best_choices)
        row_to_remove_from = play[0]
        pins_to_remove = play[2]

        # Do and register stuff
        current_player.register_play(row_to_remove_from, rows[row_to_remove_from].get_pins(), pins_to_remove)
        rows[row_to_remove_from].take(pins_to_remove)
    
    # Game over, update statistics
    won = current_player
    lost = filter(lambda player: player != won, players)

    for winning_play in won.get_plays():
        statistics[winning_play] += PLAYER_COUNT - 1
    
    for losing_player in lost:
        for losing_play in losing_player.get_plays():
            statistics[losing_play] -= 1

# Print final statistics
print("""

Game board:

-------------------------
|                       |
|       X X X           |
|                       |
|       X X X X         |
|                       |
|       X X X X X       |
|                       |
-------------------------

Pins are removed right to left.

X = Optimal number of pins to remove from this position
    ( - means no good choice)
    ( (x,y) means any is good)
""")

output = ''
for row in range(0, ROW_COUNT):
    output += '\t'
    row_pin_count = MIN_PIN_COUNT + row
    for possible_pin_count in range(1, row_pin_count + 1):
        possible_plays = list((row, possible_pin_count, pin_removal_count) for pin_removal_count in range(1, possible_pin_count + 1))
        best_play_score = statistics[max(possible_plays, key=lambda x: statistics[x])]
        
        if best_play_score < 0:
            output += '-'
        else:
            best_plays = list( filter(lambda play: statistics[play] == best_play_score, possible_plays) )
            if len(best_plays) == 1:
                output += str(best_plays[0][2])
            else:
                output += str(tuple(play[2] for play in best_plays))
        output += '\t\t'
    output += '\n\n'

print(output)