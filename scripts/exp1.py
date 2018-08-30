import sys
from time import time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# Standardising the data.
from sklearn.preprocessing import scale
from sklearn import preprocessing

pd.options.mode.chained_assignment = None
from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import f1_score

# df16 = pd.read_csv("../nba-enhanced-stats/2016-17_teamBoxScore.csv")  #, index_col="gmDate")
# df17 = pd.read_csv("../nba-enhanced-stats/2017-18_teamBoxScore.csv")  #, index_col="gmDate")
# df = pd.concat((df16, df17))

# df = pd.read_csv("../nba-enhanced-stats/2017-18_teamBoxScore-numerics.csv")
# df = pd.read_csv("../nba-enhanced-stats/2017-18_teamBoxScore-numerics.csv")
df = pd.read_csv("../2016-17_teamBoxScore.csv")

n_matches = df.shape[0]
n_features = df.shape[1] - 1

X_all = df.drop(["teamRslt"], 1)
X_all = df.drop(["teamPTS"], 1)
y_all = df['teamRslt']
print(n_matches, n_features)

# get all numerical fields only
# we want continous vars that are integers for our input data, so lets remove any categorical vars
def preprocess_features_RIP_GPU(X):
    ''' Preprocesses the football data and converts catagorical variables into dummy variables. '''

    # Initialize new output DataFrame
    output = pd.DataFrame(index=X.index)
    # Investigate each feature column for the data
    for col, col_data in X.iteritems():
        # If data type is categorical, convert to dummy variables
        if col_data.dtype == object:
            col_data = pd.get_dummies(col_data, prefix=col)
        print(col)
        # Collect the revised columns
        output = output.join(col_data)
    return output


for col, col_data in X_all.iteritems():
    X_all[col] = scale(X_all[col])

# Shuffle and split the dataset into training and testing set.
X_train, X_test, y_train, y_test = train_test_split(X_all, y_all,
                                                    test_size=2,
                                                    random_state=2,
                                                    stratify=y_all)

def train_classifier(clf, X_train, y_train):
    ''' Fits a classifier to the training data. '''

    # Start the clock, train the classifier, then stop the clock
    start = time()
    clf.fit(X_train, y_train)
    end = time()

    # Print the results
    print "Trained model in {:.4f} seconds".format(end - start)


def predict_labels(clf, features, target):
    ''' Makes predictions using a fit classifier based on F1 score. '''

    # Start the clock, make predictions, then stop the clock
    start = time()
    y_pred = clf.predict(features)
    end = time()
    # Print and return results
    print "Made predictions in {:.4f} seconds.".format(end - start)

    return f1_score(target, y_pred, pos_label=1), sum(target == y_pred) / float(len(y_pred))


def train_predict(clf, X_train, y_train, X_test, y_test):
    ''' Train and predict using a classifer based on F1 score. '''

    # Indicate the classifier and the training set size
    print "Training a {} using a training set size of {}. . .".format(clf.__class__.__name__, len(X_train))

    # Train the classifier
    train_classifier(clf, X_train, y_train)

    # Print the results of prediction for both training and testing
    f1, acc = predict_labels(clf, X_train, y_train)
    print f1, acc
    print "F1 score and accuracy score for training set: {:.4f} , {:.4f}.".format(f1, acc)

    f1, acc = predict_labels(clf, X_test, y_test)
    print "F1 score and accuracy score for test set: {:.4f} , {:.4f}.".format(f1, acc)


# Initialize the three models (XGBoost is initialized later)
clf_A = LogisticRegression(random_state=42)
print(clf_A)
clf_B = SVC(random_state=912, kernel='rbf')
# Boosting refers to this general problem of producing a very accurate prediction rule
# by combining rough and moderately inaccurate rules-of-thumb
clf_C = xgb.XGBClassifier(seed = 82)

train_predict(clf_A, X_train, y_train, X_test, y_test)
print ''
train_predict(clf_B, X_train, y_train, X_test, y_test)
print ''
train_predict(clf_C, X_train, y_train, X_test, y_test)
print ''
