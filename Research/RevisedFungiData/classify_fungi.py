# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 21:18:25 2017

@author: hemlo
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
import sklearn.metrics as metrics
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GroupKFold, LeaveOneGroupOut
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_selection import SelectKBest, chi2
#from sklearn.metrics import average_precision_score

os.chdir("D:\\Research\\WalkerResearch\\Revised Fungi Data")
data = pd.read_csv('Fungi_data_with_evicted_pa.csv')
feature_selection_data = pd.read_csv('Fungi_data_with_evicted_pa.csv')
fs_full = feature_selection_data.drop(['Group', 'Treatment', 'Week', 'Mesocosm', 'Transition', 'Evicted'], axis=1).copy()


y = data['Treatment'].copy()

x_full_data = data.drop(['Group', 'Treatment', 'Week', 'Mesocosm', 'Transition', 'Evicted'], axis=1).copy()

#otus = ['Otu00004', 'Otu00014', 'Otu00018', 'Otu00023', 'Otu00026', 'Otu00075']

#x = x[otus]

#x = x_full_data.copy()

skb = SelectKBest(chi2, k=100)
#skb.fit(x_full_data, y)
skb.fit(fs_full, y)
feature_mask = skb.get_support()
features = x_full_data.columns[feature_mask]
#*******************************************************
x = x_full_data.loc[:, x_full_data.columns.isin(features)].copy()
#x = x_full_data.copy()
#*******************************************************
groups = data['Mesocosm'].ravel()
predictions = np.empty(y.shape)
probabilities = np.empty(shape=(y.shape[0], 2))
le = LabelEncoder()
le.fit(y.ravel())
yt = le.transform(y.ravel())

#gkf = GroupKFold(n_splits=5)
logo = LeaveOneGroupOut()
sv = svm.SVC(kernel='linear', cache_size=6000, class_weight='balanced', probability = True)
#sv = RandomForestClassifier(n_estimators = 10, n_jobs=-1)
#sv = MLPClassifier(max_iter = 2000)

print("Class counts initially: %1d, %1d" % (len(y[y == 'Present']), len(y[y=='Absent'])))
for train, test in logo.split(x, yt, groups):
    predictions[test] = sv.fit(x.iloc[train], yt[train]).predict(x.iloc[test])
    probabilities[test] = sv.predict_proba(x.iloc[test])

    
print("Initial classification scores:")
print("Accuracy", metrics.accuracy_score(yt, predictions))
print("Kappa", metrics.cohen_kappa_score(yt, predictions))
print(metrics.classification_report(yt, predictions))
print(metrics.confusion_matrix(yt, predictions))
fpr, tpr, _ = metrics.roc_curve(yt, probabilities[:, 1])
plt.plot(fpr, tpr, label="Initial Acc: %0.4f AUC: %0.4f  Kappa: %0.4f MCC %0.4f"  %  (metrics.accuracy_score(yt, predictions), metrics.auc(fpr, tpr), metrics.cohen_kappa_score(yt, predictions), metrics.matthews_corrcoef(yt, predictions)))

#convert Absent/Week 0 to Transition
absent = (data['Treatment'] == 'Absent') & (data['Week'] == 0) 
y.loc[absent] = 'Present'
skb.fit(fs_full, y)
feature_mask = skb.get_support()
features = x_full_data.columns[feature_mask]
#*******************************************************
x = x_full_data.loc[:, x_full_data.columns.isin(features)].copy()
#*******************************************************

le.fit(y.ravel())
yt = le.transform(y.ravel())

print("Class counts with Week 0 set to Absent: %1d, %1d" % (len(y[y == 'Present']), len(y[y=='Absent'])))
for train, test in logo.split(x, yt, groups):
    predictions[test] = sv.fit(x.iloc[train], yt[train]).predict(x.iloc[test])
    probabilities[test] = sv.predict_proba(x.iloc[test])
    
print("Scores with Absent Week 0 == Present: ")
print("Accuracy", metrics.accuracy_score(yt, predictions))
print("Kappa", metrics.cohen_kappa_score(yt, predictions))
print(metrics.classification_report(yt, predictions))
print(metrics.confusion_matrix(yt, predictions))
fpr, tpr, _ = metrics.roc_curve(yt, probabilities[:, 1])
plt.plot(fpr, tpr, label="Week 0 Acc: %0.4f AUC: %0.4f  Kappa: %0.4f MCC %0.4f"  %  (metrics.accuracy_score(yt, predictions), metrics.auc(fpr, tpr), metrics.cohen_kappa_score(yt, predictions), metrics.matthews_corrcoef(yt, predictions)))

j = 6
for i in range(1,7):
    # convert Absent/Week to Transition and Evicted/Week + 6 to Present
    absent = (data['Treatment'] == 'Absent') & (data['Week'] == i) & (data['Evicted'] == False)
    evicted = (data['Evicted'] == True) & (data['Week'] == i + j)

    y.loc[evicted] = 'Present'
    y.loc[absent] = 'Present'
    print("Class counts at iteration " + str(i) + " : %1d, %1d" % (len(y[y == 'Present']), len(y[y=='Absent'])))
    le.fit(y.ravel())
    yt = le.transform(y.ravel())
    #skb.fit(x_full_data, y)
    skb.fit(fs_full, y)
    feature_mask = skb.get_support()
    features = x_full_data.columns[feature_mask]
    #*******************************************************
    x = x_full_data.loc[:, x_full_data.columns.isin(features)].copy()
    #*******************************************************
    for train, test in logo.split(x, yt, groups):
        predictions[test] = sv.fit(x.iloc[train], yt[train]).predict(x.iloc[test])
        probabilities[test] = sv.predict_proba(x.iloc[test])


    print("Iteration", i)
    print("Accuracy", metrics.accuracy_score(yt, predictions))
    print("Kappa", metrics.cohen_kappa_score(yt, predictions))
    print(metrics.classification_report(yt, predictions))  
    print(metrics.confusion_matrix(yt, predictions))
    fpr, tpr, _ = metrics.roc_curve(yt, probabilities[:, 1] )
    plt.plot(fpr, tpr, label="Week %d Acc: %0.4f AUC: %0.4f  Kappa: %0.4f MCC %0.4f"  %  (i, metrics.accuracy_score(yt, predictions), metrics.auc(fpr, tpr), metrics.cohen_kappa_score(yt, predictions), metrics.matthews_corrcoef(yt, predictions)))
    
plt.legend(loc="lower right")
plt.show()
    

