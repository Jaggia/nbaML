import json
import os

for fname in os.listdir('matches/'):
    game = json.load(open('matches/' + fname))
    print(game.keys())
    [print(game[key]) for key in game.keys()]
    for team in ['home', 'away']:
        print(game[team])
        #print(game['home']['players']['Jeremy Lin'])