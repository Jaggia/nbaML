# coding=utf-8
import os
import json
import operator

rootdir = '/Users/jaggia/Desktop/Projects/nbaML/hackathon/matches/'
minutesPlayed = {}
teamGamesPlayed = {}

# VORP = [BPM – (-2.0)] * (% of minutes played)*(team games/82)

# for subdir, dirs, files in os.walk(rootdir):
#     for file in files:
#         game = json.load(open(os.path.join(subdir, file)))
for folder in next(os.walk('matches'))[1]:  # directories in matches/
    for fname in os.listdir('matches/' + folder + '/'):
        game = json.load(open('matches/' + folder + '/' + fname))
        for team in ['home', 'away']:
            # count minutes played for each player
            for player in game[team]['players'].keys():
                player_min_played = game[team]['players'][player]['MP']
                if player not in minutesPlayed:
                    if player_min_played is not None:
                        minutesPlayed[player] = float(player_min_played)
                elif player_min_played is not None:
                    minutesPlayed[player] += float(player_min_played)

            team_name = game[team]['name']
            if team_name not in teamGamesPlayed.keys():
                teamGamesPlayed[team_name] = 1
            else:
                teamGamesPlayed[team_name] += 1

# for folder in next(os.walk('matches'))[1]:  # directories in matches/
#     for fname in os.listdir('matches/' + folder + '/'):
#
#
#
minutesPlayed = sorted(minutesPlayed.items(), key=operator.itemgetter(1))[::-1]
teamGamesPlayed = sorted(teamGamesPlayed.items(), key=operator.itemgetter(1))[::-1]
print(minutesPlayed)
print(teamGamesPlayed)

