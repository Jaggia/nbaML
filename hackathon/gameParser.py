import json
import os
import operator
import numpy as np

# Remember to divide by minutes played
# PTS may not be necessary
featureList = ['FG', 'FGA', '3P', '3PA', 'FT', 'FTA', 'ORB', 'DRB',
                'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']

minutesPlayed = {}
maxGamePlayers = 0
gameCounter = 0
for fname in os.listdir('matches/2010-2011/'):
    game = json.load(open('matches/2010-2011/' + fname))
    for team in ['home', 'away']:
        # count number of games LeBron is in
        if 'LeBron James' in game[team]['players'].keys():
            gameCounter += 1

        # print(game[team])
        # print(len(game['home']['players'].keys()))

        # count the max number of players in a game
        maxGamePlayers = maxGamePlayers if \
            len(game[team]['players'].keys()) < maxGamePlayers \
            else len(game[team]['players'].keys())

        # count minutes played for each player
        for player in game[team]['players'].keys():
            if player not in minutesPlayed:
                minutesPlayed[player] = float(game[team]['players'][player]['MP'])
            else:
                if game[team]['players'][player]['MP'] is not None:
                    minutesPlayed[player] += float(game[team]['players'][player]['MP'])

minutesPlayed = sorted(minutesPlayed.items(), key=operator.itemgetter(1))[::-1]
print(minutesPlayed)
print('Max Players ', maxGamePlayers)

# game = json.load(open('matches/2010-2011/201010260BOS.json'))
# home = game['home']
input('Continue')

teamStats = np.zeros((2 * maxGamePlayers - 1, len(featureList), gameCounter))
print(teamStats.shape)
totalGames = gameCounter
gameCounter = 0
for fname in os.listdir('matches/2010-2011/'):
    game = json.load(open('matches/2010-2011/' + fname))

    found = False
    # find game with LeBron
    for team in ['home', 'away']:
        if 'LeBron James' in game[team]['players'].keys():
            found = True
            playerHomeTeam = team
            print('Found him ', team)
            break

    if found:
        playerIndex = 0
        for player in game[playerHomeTeam]['players'].keys():
            if player is not 'LeBron James':
                for fnum, feature in enumerate(featureList):
                    teamStats[playerIndex, fnum, gameCounter] = game[playerHomeTeam]['players'][player][feature]

                playerIndex += 1

        if playerIndex < maxGamePlayers - 1:
            avgStats = np.mean(teamStats[:playerIndex, :, gameCounter], axis=0)
            print(avgStats.shape)
            for i in range(playerIndex, maxGamePlayers - 1):
                teamStats[i, :, gameCounter] = avgStats

        playerAwayTeam = 'away' if playerHomeTeam is 'home' else 'home'
        playerIndex = maxGamePlayers - 1
        for player in game[playerAwayTeam]['players'].keys():
            for fnum, feature in enumerate(featureList):
                teamStats[playerIndex, fnum, gameCounter] = game[playerAwayTeam]['players'][player][feature]

            playerIndex += 1

        if playerIndex < 2 * maxGamePlayers - 1:
            avgStats = np.mean(teamStats[maxGamePlayers-1:playerIndex, :, gameCounter], axis=0)
            for i in range(playerIndex, 2*maxGamePlayers-1):
                teamStats[i, :, gameCounter] = avgStats

        teamStats[maxGamePlayers-1:, :, gameCounter] *= -1
        print(teamStats[:,:,gameCounter])
        gameCounter += 1

# teamStats axis 0 = players
#           axis 1 = features
#           axis 2 = games
print('Done')