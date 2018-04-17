# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 15:24:02 2017

@author: hemlo
"""

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn import linear_model
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.metrics import roc_curve, auc
from sklearn.datasets import make_classification

#Import necessary r objects and packages.
import rpy2.robjects as ro
from rpy2.robjects.packages import importr

base = importr('base')
utils = importr('utils')
Ckmeans = importr('Ckmeans.1d.dp')

ro.r('''
     #Ckmeans clustering function
     #returns Ckmeans cluster with appropriate k value
     ck <- function(r, k=NULL, verbose=FALSE) {
        Ckmeans.1d.dp(r,k)
        }
     ''')
ck = ro.globalenv['ck']
os.chdir('D:\\TTU\\NEL Research\\SD Work\\TriageUpdated')

labels = ['AGE', 'ED_RESP', 'ED_PULSE', 'ED_BP', 'ED_EYE', 'ED_VRB', 'ED_MTR', 'ED_GCS', 'ED_TSARR', 'Gender', 'EDBPRTS', 'EDRespRTS', 'EDGCSRTS', 'EDRTSc', 'ISS16']
float_formatter = lambda x: "%.4f" % x

#RUNNING Random Forest Here, not Decision Trees!
dt = RandomForestClassifier(max_depth=5, n_jobs=-1)

X_full, y = make_classification(n_samples=5000, n_features=20, n_informative=4, n_redundant=0, shuffle=True, random_state = 1337)
dt.fit(X_full,y)

#get the most important feature
mf = np.argmax(dt.feature_importances_)
#convert X_full to dataframe to make dropping the column easier.
X_m = pd.DataFrame(X_full)
#drop that feature from the data
X_m.drop(mf, axis=1, inplace=True)
#return the dataframe as a numpy matrix.  
X = X_m.as_matrix()

#the number of iterations.  
r = 20

predictions = np.empty(shape=(X.shape[0], r))
probabilities = np.empty(shape=(X.shape[0], r))
decision_functions = np.empty(shape=(X.shape[0], r))

current_predictions = np.empty(y.shape)
current_probabilities = np.empty(y.shape)
correct_prediction_count = np.zeros(y.shape)

kf = StratifiedKFold(n_splits=10, shuffle=True)
lr = linear_model.LogisticRegression()

rf = RandomForestClassifier(max_depth=5, n_jobs=-1)
for i in range(r):  
    for train, test in kf.split(X, y):
        #lr.fit(X.iloc[train], y[train])
        current_predictions[test] = dt.fit(X[train], y[train]).predict(X[test])
        #current_probabilities[test] = dt.fit(X.iloc[train], y[train]).predict_proba(X.iloc[test])
        probas_ = dt.fit(X[train], y[train]).predict_proba(X[test])
        current_probabilities[test] = probas_[:, 1]


    print("Score for iteration " + str(i), np.mean(y == current_predictions))
    correct_prediction_count = correct_prediction_count + np.equal(current_predictions, y).astype(int)
    predictions[:, i:i+1] = np.vstack(current_predictions)
    probabilities[:, i:i+1] = np.vstack(current_probabilities)
    fpr, tpr, _ = roc_curve(y, current_probabilities )
    plt.plot(fpr, tpr, label="ROC iteration %d (AUC = %0.4f)" % (i, auc(fpr, tpr)))
plt.legend(loc="lower right")
plt.show()
np.savetxt("rf_synth_count.csv", correct_prediction_count, delimiter=",")

np.savetxt("rf_synth_probabilities.csv", probabilities, delimiter=",", fmt="%2.4f")
np.savetxt("rf_synth_predictions.csv", predictions, delimiter=",", fmt="%1d")
df = pd.DataFrame(data=X)
df['Stability'] = np.divide(correct_prediction_count, float(r))
df.to_csv("UQ_rf_synth_results.csv", index=False)

r_x = ro.FloatVector(df['Stability'])
c1_x = ck(r_x, 4)
c2_x = ck(r_x, 3)

c2 = np.array(ro.IntVector(c1_x[0]))
c3 = np.array(ro.IntVector(c2_x[0]))