from sklearn import linear_model
from sklearn.linear_model import Ridge
from sklearn import metrics

import gameParser

def main():
    teamStats, lebronStats = gameParser.get_feature_list()
    ridgerino = Ridge(alpha=.5)
    ridgerino.fit(X=teamStats, y=lebronStats)
    prediction = ridgerino.predict(X=teamStats)
    print("Accuracy: ", metrics.accuracy_score(lebronStats, prediction))
    print("F1 score: ", metrics.f1_score(lebronStats, prediction, average='micro'))


if __name__ == "__main__":
    main()

