# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 12:22:13 2017

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


os.chdir('D:\\TTU\\NEL_Research\\SD Work\\SyntheticData')

data = pd.read_csv('UQ_rf_synth_results.csv')

SG1_class0 = data.query('Fifteen >= -0.343546779 and Four <= 2.393726282 and Fifteen >= -0.007783632 and Four >= -0.461010186 and Thirteen <= 3.527759281 ')
SG1_class0.to_csv('.\\SGToCkmeans\\SG1_class0.csv')
print("SG1_class0\n", SG1_class0.groupby('Class')['Class'].count())

SG2_class0 = data.query('Fifteen >= -0.134387922 and Four <= 1.710508525 and Seven >= -0.615572152 and Eight <= 2.602101004 and Six <= 2.721477765')
SG2_class0.to_csv('.\\SgToCkmeans\\SG2_class0.csv')
print("SG2_class0\n", SG2_class0.groupby('Class')['Class'].count())

SG3_class0 = data.query('Fifteen >= -0.134387922 and Fifteen <= 4.446826786 and Four <= 2.395054669 and Fourteen <= 1.869253149 and Seventeen >= -1.96549274')
SG3_class0.to_csv('.\\SgToCkmeans\\SG3_class0.csv')
print("SG3_class0\n", SG3_class0.groupby('Class')['Class'].count())

SG1_class1 = data.query('Fifteen <= -0.018422395 and Four <= 2.244633079 and Four >= -1.190353439')
SG1_class1.to_csv('.\\SGToCkmeans\\SG1_class1.csv')
print("SG1_class1\n", SG1_class1.groupby('Class')['Class'].count())

SG2_class1 = data.query('Fifteen <= -0.134387922 and Four <= 2.527531532 and Four >= -0.464371319 and Fourteen >= -3.017924403 and Eight >= -2.316872261')
SG2_class1.to_csv('.\\SGToCkmeans\\SG2_class1.csv')
print("SG2_class1\n", SG2_class1.groupby('Class')['Class'].count())

SG3_class1 = data.query('Seven <= 0.671267187 and Four <= -0.211022993 and Seven <= 0.104821716 and Fifteen >= -0.594878702 and Four >= -3.0327124')
SG3_class1.to_csv('.\\SGToCkmeans\\SG3_class1.csv')
print("SG3_class1\n", SG3_class1.groupby('Class')['Class'].count())

