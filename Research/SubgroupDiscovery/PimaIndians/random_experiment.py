# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 16:22:59 2017

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
from sklearn.metrics import roc_curve, roc_auc_score, confusion_matrix
from sklearn.utils import resample

os.chdir('D:\\TTU\\NEL_Research\\SD Work\\PimaIndians')
data = pd.read_csv('UQ_rf_clusters_results.csv')
dropped_feature = pd.read_csv('dropped_feature.csv')
data_c1 = data[data.Cluster2 == 1]

columns = ['SG', 'random-acc', 'random-auc','len_hf1', 'len_sample', 'count-class-0', 'count-class-1', 'mean_hf1',  'mean_nothf', 'hf1_tvalue_nothf', 'hf1_pvalue_nothf', 'hf1_tvalue_oneSamp','hf1_pvalue_oneSamp']
results = pd.DataFrame(columns = columns)
lens = [158, 216, 132, 164, 184]
#lens = [41, 40, 127, 137, 178, 175]
clf = RandomForestClassifier(n_jobs=-1)
kf = StratifiedKFold(n_splits=10, shuffle=True)

y_random = data.Class.ravel()
X_random = data.drop(['Class', 'Stability', 'Cluster2'], axis=1)
X_random['Random_feature'] = 0
count = 0
for i in range(0,5):
    filename = "CkmeansToSD\\SG"+str(i)+".csv"
    sg = pd.read_csv(filename, index_col = 0)
    sg_name = "SG" + str(i)
    sample = resample(data_c1, n_samples=lens[i], replace=False) 
    print("Sample length:", len(sample))
    
    X_random.loc[sample.index, 'Random_feature'] = 1
    print("Random feature length:", len(np.where(X_random['Random_feature']==1)[0]))
    
    random_predictions = np.empty(len(y_random))
    random_probabilities = np.empty(len(y_random))
    
    for train, test in kf.split(X_random, y_random):
       random_predictions[test] = clf.fit(X_random.iloc[train], y_random[train]).predict(X_random.iloc[test])
       probas_ = clf.predict_proba(X_random.iloc[test])
       random_probabilities[test] = probas_[:, 1]
       
    sg_index = sg[sg.Cluster2 == 1].index
    
    hf1 = dropped_feature.loc[sample.index]
    not_hf = dropped_feature.loc[~dropped_feature.index.isin(hf1.index)]
    
    one_samp = stats.ttest_1samp(hf1, np.mean(dropped_feature))
    ind_t_all = stats.ttest_ind(hf1, not_hf)

    tvalue_all = ind_t_all.statistic
    pvalue_all = ind_t_all.pvalue
    tvalue_one = one_samp.statistic
    pvalue_one = one_samp.pvalue
    
    sg_diff = len(sg_index) - len(np.where(sg_index.isin(sample.index))[0])
    print("Difference in selected sample from sg" + str(i), sg_diff)   
    random_acc = np.mean(y_random == random_predictions)
    print("Accuracy for random SG" + str(i), random_acc)
    fpr, tpr, _ = roc_curve(y_random, random_probabilities)
    random_auc = roc_auc_score(y_random, random_probabilities) 
    print("AUROC for random SG" + str(i), random_auc)
    print(confusion_matrix(y_random, random_predictions))
    print("\n")
    X_random['Random_feature'] = 0  
    results = results.append({'SG': sg_name + '-cktosd', 'random-acc': random_acc, 'random-auc': random_auc, 'len_hf1': lens[i], 'len_sample': len(sample), 'count-class-0':len(np.where(sample.Class == 0)[0]), 'count-class-1': len(np.where(sample.Class==1)[0]), 'mean_hf1':np.mean(hf1)[0], 'mean_nothf':np.mean(not_hf)[0], 'hf1_tvalue_nothf': tvalue_all[0], 'hf1_pvalue_nothf':pvalue_all[0], 'hf1_tvalue_oneSamp':tvalue_one[0],'hf1_pvalue_oneSamp':pvalue_one[0]}, ignore_index=True)
    count = count + 1
    
st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H%M')
low_clu = dropped_feature.loc[data[data.Cluster2 == 1].index]
remainder = dropped_feature.loc[~dropped_feature.index.isin(low_clu.index)]
all_samp = stats.ttest_ind(low_clu, remainder)
print("p-value for low cluster vs all: %2.4f, t-value: %4.4f" % (all_samp.pvalue, all_samp.statistic))
results.to_csv('random-exp-results-' + str(st) +'.csv', index=False)