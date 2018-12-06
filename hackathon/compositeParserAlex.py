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

class StatParser:
    def __init__(self, inFname='Historical.csv'):
        self.fname = inFname
        self.nba = pd.read_csv(self.fname)
        #self.nba.dropna()
        #self.nba.drop(columns=['Year'])

    def getYears(self, startYear, endYear=None):
        if endYear is None:
            return self.nba[self.nba['Year'] >= startYear]
        else:
            temp = self.nba[startYear <= self.nba['Year']]
            return temp[temp['Year'] < endYear]

    def getLabels(self, labels):
        return self.nba[labels]

    def getColumns(self):
        return self.nba.columns


#compositeFile = '../nba-enhanced-stats/BBRef_Composite_1978_2016.xlsm'
compositeFile = 'Historical.csv'

x = StatParser()
print('Loaded file')

[print(col) for col in x.getColumns()]

mlData = x.getYears(2000, 2016)
#print(mlData)

print(mlData[mlData['Tm'] == 'SEA'][mlData['Year'] == 2008.0])

# ML Stuff
importantFields = ['Age', 'G', 'MP', 'PER']
