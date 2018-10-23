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

compositeFile = 'nba-enhanced-stats/BBRef_Composite_1978_2016.xlsm'
if os.path.isfile(compositeFile):
    nba = pd.read_csv(compositeFile)
    print(nba)