# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 13:14:52 2017

@author: hemlo
"""

import os
import pandas as pd
import numpy as np

from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn import linear_model
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
from scipy import stats
from sklearn import metrics
from sklearn.datasets import make_classification

os.chdir('D:\\TTU\\NEL Research\\SD Work\\TestBed')

x, y = make_classification(n_samples = 5000, n_features=20, n_informative=4, n_redundant = 0, shuffle=True)
preds = np.empty(y.shape)


rf = RandomForestClassifier()
skf = StratifiedKFold(n_splits=10, shuffle=True)

rf.fit(x,y)
fi = rf.feature_importances_
feature = np.argmax(fi)

x_m = pd.DataFrame(x)
x_m.drop(feature, axis=1, inplace=True)
x = x_m.as_matrix()

for train,test in skf.split(x,y):
    preds[test] = rf.fit(x[train], y[train]).predict(x[test])
    
print(metrics.accuracy_score(y, preds))

