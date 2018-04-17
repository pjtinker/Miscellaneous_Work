# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 15:24:02 2017

@author: hemlo
"""
import os
import pandas as pd
import numpy as np

from sklearn.model_selection import KFold
from sklearn import linear_model
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
from scipy import stats

os.chdir('D:\\TTU\\NEL Research\\SD Work\\Trauma Triage Data\\ed\\outcome01')

labels = ['AGE', 'ED_RESP', 'ED_PULSE', 'ED_BP', 'ED_EYE', 'ED_VRB', 'ED_MTR', 'ED_GCS', 'ED_TSARR', 'Gender', 'EDBPRTS', 'EDRespRTS', 'EDGCSRTS', 'EDRTSc', 'EDShock', 'EDRespTri', 'EDGCSTri', 'EDACS', 'Class']
float_formatter = lambda x: "%.4f" % x
#np.set_printoptions(formatter={'float': float_formatter})

data = pd.read_csv('ed.data', names=labels)
data = data[data.Gender != '?']

X = data.iloc[:, :-1]
y = data['Class'].ravel()

ta = np.empty(3)
probabilities = np.empty([20, X.shape[0]])
predictions = np.empty([6, X.shape[0]])
pred_total = np.empty(y.shape[0])
ypred = np.empty(y.shape[0])
yprob = np.empty(y.shape[0])
#prob_total = np.zeros(y.shape[0])
y_pred = np.zeros(y.shape[0])
prev_prob = np.zeros(y.shape[0])
curr_prob = np.zeros(y.shape[0])

lr = linear_model.LogisticRegression()

for i in range(3):
    
    #lr = tree.DecisionTreeClassifier()
    #lr = RandomForestClassifier()
    cv = KFold(n_splits=10, shuffle=True)
    for train_index, test_index in cv.split(X):
        
        lr.fit(X.iloc[train_index], y[train_index])
        ypred = lr.predict(X.iloc[test_index])
        yprob = lr.predict_proba(X.iloc[test_index])
        y_pred[test_index] = ypred
        curr_prob.flat[test_index] = yprob

            
    np.savetxt("pred" + str(i) + ".csv", y_pred, delimiter=",")    
    #pred_total = pred_total + np.logical_and(y_pred == y, y == y_pred).astype(int)
    pred_total = pred_total + np.equal(y_pred, y).astype(int)
    print("Prediction totals:", pred_total[4])
    probabilities[i] = curr_prob
    predictions[i] = y_pred
    
predictions[5] = y
np.savetxt("predictions.csv", predictions, delimiter=",")
X['Certainty'] = pred_total/3.0
X.to_csv("UQ_results_LR.csv")
