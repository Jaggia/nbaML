import json
import os
import operator

# Remember to divide by minutes played
# PTS may not be necessary
feature_list = ['FG', 'FGA', '3P', '3PA', 'FT', 'FTA', 'ORB', 'DRB',
                'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']

minutesPlayed = {}
for fname in os.listdir('matches/2010-2011/'):
    game = json.load(open('matches/2010-2011/' + fname))
    # print(game.keys())
    # [print(game[key]) for key in game.keys()]
    for team in ['home', 'away']:
        # print(game[team])
        # print(len(game['home']['players'].keys()))
        for player in game[team]['players'].keys():
            if player not in minutesPlayed:
                minutesPlayed[player] = float(game[team]['players'][player]['MP'])
            else:
                if game[team]['players'][player]['MP'] is not None:
                    minutesPlayed[player] += float(game[team]['players'][player]['MP'])

minutesPlayed = sorted(minutesPlayed.items(), key=operator.itemgetter(1))[::-1]
print(minutesPlayed)

# game = json.load(open('matches/2010-2011/201010260BOS.json'))
# home = game['home']
