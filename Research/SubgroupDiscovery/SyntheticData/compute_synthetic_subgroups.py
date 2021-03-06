# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 14:54:27 2017

@author: hemlo
"""

import os
import pandas as pd
import numpy as np
import time
import datetime
from sklearn.model_selection import StratifiedKFold
from sklearn import linear_model
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier

import matplotlib.pyplot as plt
from scipy import stats
from sklearn.metrics import roc_curve, auc, roc_auc_score

## Import Orange data mining package
import Orange

## Import necessary r objects and packages.
import rpy2.robjects as ro
from rpy2.robjects.packages import importr

base = importr('base')
utils = importr('utils')
Ckmeans = importr('Ckmeans.1d.dp')

## Create Ckmeans function and make it accessible to our code.  
ro.r('''
     #Ckmeans clustering function
     #returns Ckmeans cluster with appropriate k value
     ck <- function(r, k=NULL, verbose=FALSE) {
        Ckmeans.1d.dp(r,k)

        }
     ''')
ck = ro.globalenv['ck']

os.chdir('D:\\TTU\\NEL_Research\\SD Work\\SyntheticData\\SGToCkmeans')
data = pd.read_csv('..\\UQ_rf_synth_results.csv')
dropped_feature = pd.read_csv('..\\dropped_feature.csv')
dropped_feature.columns = ['dropped_feature']

columns = ['SG', 'Rule', 'SG_size', 'count_Class_0', 'count_Class_1', 'Accuracy', 'AUROC', 'len_hf1', 'len_hf2', 'len_nothf', 'mean_hf1', 'mean_hf2', 'mean_nothf','hf1_tvalue_hf2', 'hf1_pvalue_hf2', 'hf1_tvalue_nothf', 'hf1_pvalue_nothf', 'hf1_tvalue_oneSamp','hf1_pvalue_oneSamp']
results = pd.DataFrame(columns = columns)

learner = Orange.classification.CN2SDUnorderedLearner()

learner.rule_finder.search_algorithm.beam_width = 5
learner.weighted_cover_and_remove = 0.7
learner.rule_finder.general_validator.max_rule_length= 5

classifier = learner(Orange.data.Table('sgtock-mifremoved-orange-format.csv'))

# Prepare ML Classifier for results
clf = RandomForestClassifier(n_jobs=-1)
kf = StratifiedKFold(n_splits=10, shuffle=True)

y = data.Class.ravel()
X = data.drop(['Class', 'Stability'], axis=1)
X['Cluster_feature'] = 0    
current_predictions = np.empty(y.shape)
current_probabilities = np.empty(y.shape)
#fo = open('SGToCkmeans_results.txt', 'w')
plt.figure(figsize=(7,7))
# This loop will use the top three SD Rules for Class == 0 to generate our SGs
for i in range(0,3):
    # Set sg equal to the samples that are covered by the rule
     sg = data[classifier.rule_list[i].covered_examples].copy()
     # Create a copy of Stability to be clustered by Ckmeans
     r_x = ro.FloatVector(sg['Stability'])
     # Call the clustering function for 2 clusters
     c1_x = ck(r_x, 2)
     # Retrieve the array of clusters generated by R
     c2 = np.array(ro.IntVector(c1_x[0]))
     # Create a Cluster2 feature in SG and save it.  
     sg['Cluster2'] = c2
     sg.to_csv("SG" + str(i) + "_class0.csv")
     
     print("SG" + str(i) +"_class0\n", sg.groupby('Class')['Class'].count())
     print("Cluster counts:", sg.groupby('Cluster2')['Cluster2'].count())
     # c is the instances of the sg that are in Cluster 1 (the low performance cluster)
     c = sg[sg.Cluster2 == 1]
     # Create a feature in the data based upon membership to the low performance sg cluster
     X.loc[c.index, 'Cluster_feature'] = 1
     # Create three sets using the dropped feature: 
     # One for those in the low performance sg cluster.  
     hf1 = dropped_feature.loc[c.index]

     # Get dropped features in the high performance sg cluster (cluster == 2)
     hf2 = dropped_feature.loc[sg[sg.Cluster2==2].index]
     # Get all of the dropped features not in the sg
     not_hf = dropped_feature.loc[~dropped_feature.index.isin(hf1.index)]
     # Run prediction, score, and plot.
     for train, test in kf.split(X, y):
        current_predictions[test] = clf.fit(X.iloc[train], y[train]).predict(X.iloc[test])
        probas_ = clf.predict_proba(X.iloc[test])
        current_probabilities[test] = probas_[:, 1]
     accuracy = np.mean(y == current_predictions)
     print("Score for SG" + str(i) +"_class0", accuracy)
     np.savetxt("SG" + str(i) + "_class0_predictions.csv", np.column_stack((current_predictions, y)), delimiter=",", fmt="%1d")
     fpr, tpr, _ = roc_curve(y, current_probabilities )
     plt.plot(fpr, tpr, label="ROC SG" + str(i) + "_class0 (AUC = %0.4f)" % roc_auc_score(y, current_probabilities))
     print(X.groupby('Cluster_feature')['Cluster_feature'].count())
     # Perform t-test using inner sg dropped_feature and low performance sg cluster vs the remaining dropped features.  
     one_samp = stats.ttest_1samp(hf1, np.mean(dropped_feature))
     ind_t_all = stats.ttest_ind(hf1, not_hf)
     ind_t_sg = stats.ttest_ind(hf1, hf2)
     
     tvalue_sg = ind_t_sg.statistic
     pvalue_sg = ind_t_sg.pvalue
     tvalue_all = ind_t_all.statistic
     pvalue_all = ind_t_all.pvalue
     tvalue_one = one_samp.statistic
     pvalue_one = one_samp.pvalue
     # Write it all to the results dataframe.  
     results = results.append({'SG':'SG' + str(i) +'_Class_0', 'Rule' : str(classifier.rule_list[i]), 'SG_size': sg.shape[0], 'count_Class_0': len(sg[sg.Class==0]), 'count_Class_1': len(sg[sg.Class==1]), 'Accuracy':accuracy, 'AUROC':roc_auc_score(y, current_probabilities), 'len_hf1':len(hf1), 'len_hf2':len(hf2), 'len_nothf': len(not_hf), 'mean_hf1':np.mean(hf1)[0], 'mean_hf2':np.mean(hf2)[0], 'mean_nothf':np.mean(not_hf)[0], 'hf1_tvalue_hf2': tvalue_sg[0],'hf1_pvalue_hf2': pvalue_sg[0], 'hf1_tvalue_nothf': pvalue_all[0], 'hf1_pvalue_nothf':pvalue_all[0], 'hf1_tvalue_oneSamp':tvalue_one[0],'hf1_pvalue_oneSamp':pvalue_one[0]}, ignore_index = True)
     X['Cluster_feature'] = 0

# This loop finds the index of the first rule for Class == 1     
count = 0
for rule in classifier.rule_list:
    if rule.target_class == 1:
        break
    count = count + 1
    
current_predictions = np.empty(y.shape)
current_probabilities = np.empty(y.shape)  
X['Cluster_feature'] = 0

# This is a repeat of the above process, now for Class == 1
for j in range(0,3):
    sg = data[classifier.rule_list[count + j].covered_examples].copy()
    
    r_x = ro.FloatVector(sg['Stability'])
    c1_x = ck(r_x, 2)
    c2 = np.array(ro.IntVector(c1_x[0]))

    sg['Cluster2'] = c2
    sg.to_csv("SG" + str(j) + "_class1.csv")
    print("SG" + str(j) +"_class1\n", sg.groupby('Class')['Class'].count())
    print("Cluster counts:", sg.groupby('Cluster2')['Cluster2'].count())
    c = sg[sg.Cluster2 == 1]

    X.loc[c.index, 'Cluster_feature'] = 1
    hf1 = dropped_feature.loc[c.index]
    #hf2 = dropped_feature.loc[~dropped_feature.index.isin(sg[sg.Cluster2 == 2].index)]
    hf2 = dropped_feature.loc[sg[sg.Cluster2==2].index]
    not_hf = dropped_feature.loc[~dropped_feature.index.isin(hf1.index)]
    
    for train, test in kf.split(X, y):
        current_predictions[test] = clf.fit(X.iloc[train], y[train]).predict(X.iloc[test])
        probas_ = clf.predict_proba(X.iloc[test])
        current_probabilities[test] = probas_[:, 1]
    accuracy = np.mean(y == current_predictions)
    print("Score SG" + str(j) + "_class1", accuracy)
    np.savetxt("SG" + str(j) + "_class1_predictions.csv", np.column_stack((current_predictions, y)), delimiter=",", fmt="%1d")
    fpr, tpr, _ = roc_curve(y, current_probabilities )

    plt.plot(fpr, tpr, label="ROC SG" + str(j) + "_class1 (AUC = %0.4f)" % roc_auc_score(y, current_probabilities))
    print(X.groupby('Cluster_feature')['Cluster_feature'].count())

    one_samp = stats.ttest_1samp(hf1, np.mean(dropped_feature))
    ind_t_all = stats.ttest_ind(hf1, not_hf)
    ind_t_sg = stats.ttest_ind(hf1, hf2)
     
    tvalue_sg = ind_t_sg.statistic
    pvalue_sg = ind_t_sg.pvalue
    tvalue_all = ind_t_all.statistic
    pvalue_all = ind_t_all.pvalue
    tvalue_one = one_samp.statistic
    pvalue_one = one_samp.pvalue
     
    # Write it all to the results dataframe.  
    results = results.append({'SG':'SG' + str(j) +'_Class_1', 'Rule' : str(classifier.rule_list[count + i]), 'SG_size': sg.shape[0], 'count_Class_0': len(sg[sg.Class==0]), 'count_Class_1': len(sg[sg.Class==1]), 'Accuracy':accuracy, 'AUROC':roc_auc_score(y, current_probabilities), 'len_hf1':len(hf1), 'len_hf2':len(hf2), 'len_nothf': len(not_hf), 'mean_hf1':np.mean(hf1)[0], 'mean_hf2':np.mean(hf2)[0], 'mean_nothf':np.mean(not_hf)[0], 'hf1_tvalue_hf2': tvalue_sg[0],'hf1_pvalue_hf2': pvalue_sg[0], 'hf1_tvalue_nothf': pvalue_all[0], 'hf1_pvalue_nothf':pvalue_all[0], 'hf1_tvalue_oneSamp':tvalue_one[0],'hf1_pvalue_oneSamp':pvalue_one[0]}, ignore_index = True)
    X['Cluster_feature'] = 0
     
st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H%M')
results.to_csv('sdtock-synthetic-results' + str(st) + '.csv', index=False)   
plt.legend(loc="lower right")
plt.title("Subgroup Discovery to Ckmeans ROC (Synthetic)")
plt.tight_layout()
plt.show()


#################################################################################
# Switch directories to Ckmeans To SD 
os.chdir('D:\\TTU\\NEL_Research\\SD Work\\SyntheticData\\CkmeansToSD')
# Run CN2-SD with target of Ckmeans clustering (2 clusters, high and low)
classifier = learner(Orange.data.Table('cktosd-mifremoved-orange-format.csv'))
data = pd.read_csv('..\\UQ_rf_synth_results_clusters.csv')
y = data.Class.ravel()
X = data.drop(['Class', 'Stability', 'Cluster2', 'Cluster3'], axis=1)
X['Cluster_feature'] = 0

columns = ['SG','Rule', 'SG_size', 'count_Class_0', 'count_Class_1', 'Accuracy', 'AUROC', 'len_hf1', 'len_nothf', 'mean_hf1', 'mean_nothf','hf1_tvalue_nothf', 'hf1_pvalue_nothf', 'hf1_tvalue_oneSamp','hf1_pvalue_oneSamp']
results = pd.DataFrame(columns = columns)
plt.figure(figsize=(7,7))
# Take the top five rules for the low performing cluster (cluster 1)
for j in range(0,5):
    # Get the sg based upon examples covered by the rules.  
    sg = data[classifier.rule_list[j].covered_examples].copy()
    print("Rule distributions for rule " + str(j) + ":", classifier.rule_list[j].curr_class_dist)
    sg.to_csv("SG" + str(j) + ".csv")
    print("SG" + str(j) +" actual distro count \n",sg.groupby('Cluster2')['Cluster2'].count())
    # Create a feature based upon membership to the sg
    X.loc[sg[sg.Cluster2 == 1].index, 'Cluster_feature'] = 1
    
    # Get dropped features for those in the sg and those not in the sg.
    hf1 = dropped_feature.loc[sg.index]
    not_hf = dropped_feature.loc[~dropped_feature.index.isin(hf1.index)]    
    for train, test in kf.split(X, y):
        current_predictions[test] = clf.fit(X.iloc[train], y[train]).predict(X.iloc[test])
        probas_ = clf.predict_proba(X.iloc[test])
        current_probabilities[test] = probas_[:, 1]
    accuracy = np.mean(y == current_predictions)
    print("Score SG" + str(j) + "", accuracy)
    np.savetxt("SG" + str(j) + "_predictions.csv", np.column_stack((current_predictions, y)), delimiter=",", fmt="%1d")
    fpr, tpr, _ = roc_curve(y, current_probabilities ) 
    plt.plot(fpr, tpr, label="ROC SG" + str(j) + " (AUC = %0.4f)" % roc_auc_score(y, current_probabilities))
    print(X.groupby('Cluster_feature')['Cluster_feature'].count())
    
    ind_t = stats.ttest_ind(hf1, not_hf)
    one_samp = stats.ttest_1samp(hf1, np.mean(dropped_feature))
    
    tvalue_all = ind_t.statistic
    pvalue_all = ind_t.pvalue
    tvalue_one = one_samp.statistic
    pvalue_one = one_samp.pvalue
     
    results = results.append({'SG':'SG' + str(j),'Rule': str(classifier.rule_list[j]), 'SG_size': sg.shape[0], 'count_Class_0': len(sg[sg.Class==0]), 'count_Class_1': len(sg[sg.Class==1]), 'Accuracy':accuracy, 'AUROC':roc_auc_score(y, current_probabilities), 'len_hf1':len(hf1), 'len_nothf': len(not_hf), 'mean_hf1':np.mean(hf1)[0], 'mean_nothf':np.mean(not_hf)[0], 'hf1_tvalue_nothf': tvalue_all[0], 'hf1_pvalue_nothf':pvalue_all[0], 'hf1_tvalue_oneSamp':tvalue_one[0],'hf1_pvalue_oneSamp':pvalue_one[0]}, ignore_index = True)    
    X['Cluster_feature'] = 0
st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H%M')
results.to_csv('cktosd-synthetic-results' + str(st) + '.csv', index=False)
plt.legend(loc="lower right")
plt.title("Ckmeans to Subgroup Discovery ROC (Synthetic)")
plt.tight_layout()
plt.show()

