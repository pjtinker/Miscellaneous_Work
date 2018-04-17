# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 19:37:16 2017

@author: hemlo
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 11:22:21 2017

@author: hemlo
"""

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn import linear_model
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.metrics import roc_curve, roc_auc_score, matthews_corrcoef, confusion_matrix
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif
from imblearn.under_sampling import RandomUnderSampler
from sklearn.preprocessing import LabelBinarizer

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

os.chdir('D:\\TTU\\NEL_Research\\SD Work\\PimaIndians')


clf = RandomForestClassifier()
rus = RandomUnderSampler(random_state=1337)
data = pd.read_csv('pima-indians-diabetes.csv')

data = data[data['Plasma-glucose'] != 0]
X = data.drop(['Class'], axis=1)
y = data.iloc[:, -1].ravel()
X = X[X['Plasma-glucose'] != 0]

features = SelectKBest(f_classif, k=1).fit(X, y)

# Grab most important feature
mif = np.argmax(features.scores_)
f = X.columns[mif]
print("Feature to drop is: ", f)
# Save it, then remove it from X.
X.iloc[:, mif].to_csv('dropped_feature.csv', index=False, header=[X.columns[mif]])
dropped_feature = X.iloc[:, mif]
#keepers = [6]
X.drop(X.columns[mif], axis=1, inplace=True)

#X = X.iloc[:, keepers]
print("X shape:", X.shape)
#X,y = rus.fit_sample(X, y)
#X = pd.DataFrame(X, columns=columns)
print("X len:", len(X))
r = 100

predictions = np.empty(shape=(X.shape[0], r))
probabilities = np.empty(shape=(X.shape[0], r))
decision_functions = np.empty(shape=(X.shape[0], r))

current_predictions = np.empty(y.shape)
current_probabilities = np.empty(y.shape)
correct_prediction_count = np.zeros(y.shape)
avg_accuracy = 0
avg_auc = 0
kf = StratifiedKFold(n_splits=10, shuffle=True)
#lr = linear_model.LogisticRegression()
#dt = tree.DecisionTreeClassifier(max_depth=3)
fig = plt.figure('uq', figsize=(7,7))
ax = fig.add_subplot(111)
for i in range(r):  
    for train, test in kf.split(X, y):
        clf.fit(X.iloc[train], y[train])
        current_predictions[test] = clf.predict(X.iloc[test])
        probas_ = clf.predict_proba(X.iloc[test])
        current_probabilities[test] = probas_[:, 1]

    accuracy = np.mean(y==current_predictions)
    mcc = matthews_corrcoef(y, current_predictions)
    avg_accuracy = avg_accuracy + accuracy
    print("Accuracy for iteration " + str(i), accuracy)
    print("MCC for iteration " + str(i), mcc)
    print(confusion_matrix(y, current_predictions))
    correct_prediction_count = correct_prediction_count + np.equal(current_predictions, y).astype(int)
    predictions[:, i:i+1] = np.vstack(current_predictions)
    probabilities[:, i:i+1] = np.vstack(current_probabilities)
    fpr, tpr, _ = roc_curve(y, current_probabilities)
    print("Length of fpr: %3d, tpr: %3d" % (len(fpr), len(tpr)))
    #auc = auc(fpr, tpr)
    auroc = roc_auc_score(y, current_probabilities)
    avg_auc = avg_auc + auroc
    plt.plot(fpr, tpr)
    current_probabilities = np.empty(len(y))
    current_predictions = np.empty(len(y))

plt.title("ROC Curve with " + str(f) + " Removed (Pima)")
plt.plot([0, 1], [0, 1], 'k--')  # random predictions curve
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])
ax.annotate('Avg. accuracy: %0.4f\nAvg. AUROC:   %0.4f'% (avg_accuracy /float(r), avg_auc / float(r)), xy=(0.95, 0.1), xytext=(0.65, 0.1))
plt.tight_layout()
plt.show()
print("Average accuracy:", (avg_accuracy / float(r)))
print("Average AUROC:", (avg_auc / float(r)))
np.savetxt("rf_count.csv", correct_prediction_count, delimiter=",")
X['Stability'] = np.divide(correct_prediction_count, float(r))
np.savetxt("rf_probabilities.csv", probabilities, delimiter=",", fmt="%2.4f")
np.savetxt("rf_predictions.csv", predictions, delimiter=",", fmt="%1d")
# Reattach ISS16 data to dataframe
X['Class'] = y
X.to_csv("UQ_rf_results.csv", index=False)

# Generate clusters via Ckmeans
r_x = ro.FloatVector(X['Stability'])
c1_x = ck(r_x, 2)
#c2_x = ck(r_x, 3)

# Convert clusters to numpy arrays and append to data
c2 = np.array(ro.IntVector(c1_x[0]))
X['Cluster2'] = c2
# c3 = np.array(ro.IntVector(c2_x[0]))
# X['Cluster3'] = c3
X.to_csv('UQ_rf_clusters_results.csv', index=False)
