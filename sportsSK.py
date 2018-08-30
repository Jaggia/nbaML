import numpy as np
import csv
import os
import pandas as pd
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
import matplotlib.pyplot as plt
# import theano.tensor as T
# import theano
# import pymc3 as pm


#x_indices = np.concatenate((np.arange(0,8), np.arange(9,18))).astype(np.int64)
x_indices = np.concatenate((np.arange(0,8), np.arange(9, 18)))
print(x_indices)
y_indices = 94

if not os.path.isfile("nba_season_data_cut.csv"):
    with open("nba_season_data.csv", "r") as nbaFile:
        with open("nba_season_data_cut.csv", "w") as nbaCutFile:
            reader = csv.reader(nbaFile, delimiter=",")
            writer = csv.writer(nbaCutFile, delimiter=",", lineterminator="\n")
            for row in reader:
                incomplete = False
                writeRow = []
                for i in x_indices:
                    if not row[i]:
                        incomplete = True
                    else:
                        writeRow = writeRow + [row[i]]
                if not row[y_indices]:
                    incomplete = True
                else:
                    writeRow = writeRow + [row[y_indices]]

                if incomplete:
                    continue

                writer.writerow(writeRow)
'''
nba = np.recfromcsv("nba_season_data_cut.csv", delimiter=",", names=True, usecols=np.arange(18))
tags = np.recfromcsv("nba_season_data_cut.csv", delimiter=",", names=True, usecols=np.arange(3))
x = np.recfromcsv("nba_season_data_cut.csv", delimiter=",", names=True, usecols=np.arange(3,17), skip_header=2)
y = np.recfromcsv("nba_season_data_cut.csv", delimiter=",", names=True, usecols=17)
years = nba['year']
teams = nba['tm']
names = nba['player']
print(nba.dtype)
print(x)
print(y)
'''

nba = pd.read_csv("nba_season_data_cut.csv")
print(nba)
print(nba.dtypes)
#print(nba["Year"])

num_train = np.round(nba.shape[0] * .8).astype(np.int64)
num_test = nba.shape[0] - num_train
trainX = nba.iloc[:num_train, 6:17].values
trainY = nba.iloc[:num_train, 17].values
testX = nba.iloc[num_train:, 6:17].values
testY = nba.iloc[num_train:, 17].values
print(nba.shape)
print(trainX)

c_arr = np.logspace(-4, 4, 3)
estimators =np.logspace(1, 3, 20).astype(np.int32)
rfr = RandomForestRegressor(n_jobs=-1)
scores = []
#for c in c_arr:
for n in estimators:
    #clf = svm.SVR(C=c, kernel='poly', degree=2)
    #clf.fit(trainX, trainY)
    #Pe = 1 - clf.score(testX, testY)
    #print("C: ", c, " Error: ", Pe, "asdf", clf.support_vectors_.shape)
    #print(clf.support_vectors_)

    rfr.set_params(n_estimators=n)
    rfr.fit(trainX, trainY)
    scores.append(rfr.score(testX, testY))
    print("Done with ", n)

# gam_arr = np.logspace(-7, -1, 3)
# degrees = np.arange(1, 8)
# for c in c_arr:
#     for gam in gam_arr:
#         for deg in degrees:
#             clf = svm.SVR(C=c, kernel='poly', epsilon=gam, degree=deg)
#             clf.fit(trainX, trainY)
#             Pe = 1 - clf.score(testX, testY)
#             print("C: ", c, " Gamma: ", gam, "Degree: ", deg, " Error: ", Pe, " Support vecs: ", clf.support_vectors_.shape)

plt.title("Effect of n_estimators")
plt.xlabel("n_estimator")
plt.ylabel("score")
plt.plot(estimators, scores)
plt.show()
