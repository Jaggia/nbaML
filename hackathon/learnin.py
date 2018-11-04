from sklearn import linear_model
from sklearn.linear_model import Ridge
from sklearn import metrics
import numpy as np
import gc
import gameParser

def main():
    teamStats, lebronStats, maxGamePlayers = gameParser.get_feature_list()
    flatten = True
    if flatten:
        flatTeamStats = np.zeros((teamStats.shape[0], teamStats.shape[1]*teamStats.shape[2]))
        flatLebronStats = np.zeros((lebronStats.shape[0], lebronStats.shape[1]*lebronStats.shape[2]))
        for numGame in range(teamStats.shape[0]):
            flatTeamStats[numGame, :] = teamStats[numGame, :, :].flatten(order='F')
            flatLebronStats[numGame, :] = lebronStats[numGame, :, :].flatten()

        (teamStats, lebronStats) = (flatTeamStats, flatLebronStats)
        del flatTeamStats
        del flatLebronStats
        gc.collect()
    else: #average over team and opponents
        #avgTeamStats = np.concatenate(())
        pass

    ridgerino = Ridge(alpha=.5)
    ridgerino.fit(X=teamStats, y=lebronStats)
    prediction = ridgerino.predict(X=teamStats)
    print("Accuracy: ", metrics.accuracy_score(lebronStats, prediction))
    print("F1 score: ", metrics.f1_score(lebronStats, prediction, average='micro'))


if __name__ == "__main__":
    main()

