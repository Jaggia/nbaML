import json
import os
import operator
import numpy as np

# Remember to divide by minutes played
# PTS may not be necessary

def get_feature_list():
    featureList = ['FG', 'FGA', '3P', '3PA', 'FT', 'FTA', 'ORB', 'DRB',
                   'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
    # featureList = ['FG', '3P', 'FT', 'ORB', 'DRB',
    #                'AST', 'STL', 'BLK', 'TOV']

    minutesPlayed = {}
    maxGamePlayers = 0
    gameCounter = 0
    for folder in next(os.walk('matches'))[1]: # directories in matches/
        for fname in os.listdir('matches/' + folder + '/'):
            game = json.load(open('matches/' + folder + '/' + fname))
            for team in ['home', 'away']:
                # count number of games LeBron is in
                if 'LeBron James' in game[team]['players'].keys():
                    gameCounter += 1

                # count the max number of players in a game
                maxGamePlayers = max(maxGamePlayers, len(game[team]['players'].keys()))

                # count minutes played for each player
                for player in game[team]['players'].keys():
                    if player not in minutesPlayed:
                        #minutesPlayed[player] = float(game[team]['players'][player]['MP'])
                        pass
                    else:
                        if game[team]['players'][player]['MP'] is not None:
                            minutesPlayed[player] += float(game[team]['players'][player]['MP'])

    minutesPlayed = sorted(minutesPlayed.items(), key=operator.itemgetter(1))[::-1]
    print(minutesPlayed)
    print('Max Players ', maxGamePlayers)

    totalGames = gameCounter
    gameCounter = 0
    minMinutes = 2

    lebronStats = np.zeros((1, len(featureList), totalGames))
    teamStats = np.zeros((2 * maxGamePlayers - 1, len(featureList), totalGames))
    #allPlayerStats = np.zeros((len(minutesPlayed), len(featureList)))
    print(teamStats.shape)

    for folder in next(os.walk('matches'))[1]: # directories in matches/
        for fname in os.listdir('matches/' + folder + '/'):
            game = json.load(open('matches/' + folder + '/' + fname))

            found = False
            # find game with LeBron
            for team in ['home', 'away']:
                if 'LeBron James' in game[team]['players'].keys():
                    for fnum, feature in enumerate(featureList):
                        lebronStats[0, fnum, gameCounter] = \
                            game[team]['players']['LeBron James'][feature] / \
                            game[team]['players']['LeBron James']['MP']
                    found = True
                    playerHomeTeam = team
                    # print('Found him ', team)
                    break

            if found:
                playerIndex = 0
                # add Lebron's teammates stats
                for player in game[playerHomeTeam]['players'].keys():
                    if player is not 'LeBron James':
                        if game[playerHomeTeam]['players'][player]['MP'] is not None and \
                                float(game[playerHomeTeam]['players'][player]['MP']) > minMinutes:
                            for fnum, feature in enumerate(featureList):
                                teamStats[playerIndex, fnum, gameCounter] = \
                                    game[playerHomeTeam]['players'][player][feature] / \
                                    game[playerHomeTeam]['players'][player]['MP']
                            playerIndex += 1

                # add average of teammates if he doesn't have 11 teammates
                if playerIndex < maxGamePlayers - 1:
                    avgStats = np.mean(teamStats[:playerIndex, :, gameCounter], axis=0)
                    # print(avgStats.shape)
                    for i in range(playerIndex, maxGamePlayers - 1):
                        teamStats[i, :, gameCounter] = avgStats

                # add opponents stats
                playerAwayTeam = 'away' if playerHomeTeam is 'home' else 'home'
                playerIndex = maxGamePlayers - 1
                for player in game[playerAwayTeam]['players'].keys():
                    if game[playerAwayTeam]['players'][player]['MP'] is not None and \
                            float(game[playerAwayTeam]['players'][player]['MP']) > minMinutes:
                        for fnum, feature in enumerate(featureList):
                            teamStats[playerIndex, fnum, gameCounter] = \
                                game[playerAwayTeam]['players'][player][feature] / \
                                game[playerAwayTeam]['players'][player]['MP']
                        playerIndex += 1

                # add average of opponents if he doesn't have 12 opponents
                if playerIndex < 2 * maxGamePlayers - 1:
                    avgStats = np.mean(teamStats[maxGamePlayers - 1:playerIndex, :, gameCounter], axis=0)
                    for i in range(playerIndex, 2 * maxGamePlayers - 1):
                        teamStats[i, :, gameCounter] = avgStats

                gameCounter += 1

    # teamStats axis 0 = players
    #           axis 1 = features
    #           axis 2 = games

    teamStats = teamStats.swapaxes(0, 2)
    lebronStats = lebronStats.swapaxes(0, 2)
    return teamStats, lebronStats, maxGamePlayers

if __name__ == '__main__':
    ts, ls = get_feature_list()
    print('Done')