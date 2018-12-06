import time
from sklearn.linear_model import Ridge
import numpy as np
import gc
import gameParser
from sklearn.model_selection import RepeatedKFold
from sklearn.decomposition import PCA

class Learner():
    def __init__(self):
        self.learner = None

    def train_classifier(self, train_data, train_labels):
        # train model and save the trained model to self.classifier
        self.learner = Ridge(alpha=.5)
        self.learner.fit(X=train_data, y=train_labels)

    def predict(self, data):
        prediction = self.learner.predict(X=data)
        return prediction

    def k_folding(self, data_raw, data_labels):
        # x is the data
        # y r the labels
        random_num = int(time.time())
        rkf = RepeatedKFold(n_splits=4, n_repeats=4, random_state=random_num)
        data_split = rkf.split(X=data_raw, y=data_labels)
        x_train = []
        x_test = []
        y_train = []
        y_test = []
        for train, test in data_split:
            x_train, y_train = data_raw[train], data_labels[train]
            x_test, y_test = data_raw[test], data_labels[test]
        return x_train, y_train, x_test, y_test

    def PCA(self, train_data):
        mean = np.mean(train_data, axis=0).reshape((1, train_data.shape[1]))
        mean = np.tile(mean, (train_data.shape[0], 1))
        covar = 1 / (train_data.shape[0] - 1) * np.matmul((train_data - mean).T, (train_data - mean))
        vals, vecs = np.linalg.eig(covar)
        print(vals)
        pca = PCA(n_components=10)
        pca.fit(train_data)
        return pca.transform(train_data)

if __name__ == "__main__":
    teamStats, lebronStats, maxGamePlayers = gameParser.get_feature_list()
    average = False
    if not average:
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
        teamStats = np.concatenate((np.mean(teamStats[:,:,:maxGamePlayers-1],axis=2),
                                       np.mean(teamStats[:,:,maxGamePlayers-1:],axis=2)), axis=1)

        flatLebronStats = np.zeros((lebronStats.shape[0], lebronStats.shape[1]*lebronStats.shape[2]))
        for numGame in range(teamStats.shape[0]):
            flatLebronStats[numGame, :] = lebronStats[numGame, :, :].flatten()

        lebronStats = flatLebronStats
        del flatLebronStats
        gc.collect()

    print('teamStats shape {}, lebronStats shape {} '.format(teamStats.shape, lebronStats.shape))
    Ridgerino = Learner()
    teamStats = Ridgerino.PCA(teamStats)
    x_train, y_train, x_test, y_test = Ridgerino.k_folding(data_raw=teamStats, data_labels=lebronStats)
    print("x_train shape: ", x_train.shape)
    print("y_train shape: ", y_train.shape)
    print("x_test shape: ", x_test.shape)
    print("y_test shape: ", y_test.shape)
    Ridgerino.train_classifier(x_train, y_train)

    inSamplePredicted = Ridgerino.predict(x_train)
    print("\nTraining results")
    print("=============================")
    # print("LBJ : ", lebronStats.shape)
    # print(lebronStats)
    # print("Prediction : ", prediction.shape)
    # print(prediction)
    print("Score: ", Ridgerino.learner.score(x_train, y_train))

    # test model
    outSamplePredicted = Ridgerino.predict(x_test)
    print("\nTesting results")
    print("=============================")
    # print("LBJ : ", y_test.shape)
    # print(y_test)
    # print("Prediction : ", outSamplePredicted.shape)
    # print(outSamplePredicted)
    print("Score: ", Ridgerino.learner.score(x_test, y_test))
