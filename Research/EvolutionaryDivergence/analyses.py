# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 10:16:55 2018

@author: hemlo
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.cluster.hierarchy import cophenet
from scipy.spatial.distance import pdist
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from collections import Counter
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'brown', 'hotpink']
os.chdir("D:\Research\WalkerResearch")
data = pd.read_csv('BacteraMicrobiome.csv')
gut = data[data['Skin/Gut'] == 'gut'].copy()
skin = data[data['Skin/Gut'] == 'skin'].copy()
skin = skin.loc[:, (skin != 0).any(axis=0)]
gut = gut.loc[:, (gut != 0).any(axis=0)]
counter = Counter()

skin_clade_variance = skin.groupby('Species ').var()
skin_clade_variance.drop(['Lat', 'Lon'], axis=1, inplace=True)
skin_variance = skin.iloc[:, 6:].var()

skin_clade_count = pd.Series(0, index=skin.columns[6:])
gut_clade_count = pd.Series(0, index=gut.columns[6:])

for index, row in skin_clade_variance.iterrows():
    row_variance = row.divide(skin_variance).between(0.0, 0.26, inclusive=False)
    #counter.update(row_variance.index[row_variance==True])
    skin_clade_count[row_variance[row_variance == True].index] += 1

#skin_otus = skin.iloc[:, 6:].copy()
#gut_otus = gut.iloc[:, 6:].copy()
skin_otus = skin[skin_clade_count[skin_clade_count > 3].index]
skin_Z = linkage(skin_otus, 'weighted', metric='braycurtis')
c, coph_dists = cophenet(skin_Z, pdist(skin_otus, metric='braycurtis'))
print(c)

idx = data['Specimen'].index.isin(skin.index)
skin.index = data['Specimen'][idx]

plt.figure(figsize=(12, 8))
plt.title('Skin Microbiome (Cophenetic Coefficient %0.3f)' % c)
plt.xlabel('Specimen')
plt.ylabel('Distance (Bray-Curtis)')
dendrogram(
    skin_Z,
    #color_threshold=0.95,
    labels = skin.index,
    leaf_rotation=90.,  # rotates the x axis labels
    leaf_font_size=8.,  # font size for the x axis labels
)
plt.show()

counter.clear()
gut_clade_variance = gut.groupby('Species ').var()
gut_clade_variance.drop(['Lat', 'Lon'], axis=1, inplace=True)
gut_variance = gut.iloc[:, 6:].var()

for index, row in gut_clade_variance.iterrows():
    row_variance = row.divide(gut_variance).between(0.0, 0.26, inclusive=False)
    gut_clade_count[row_variance[row_variance == True].index] += 1

gut_otus = gut[gut_clade_count[gut_clade_count > 3].index]
gut_Z = linkage(gut_otus, 'weighted', metric='braycurtis')
c, coph_dists = cophenet(gut_Z, pdist(gut_otus, metric='braycurtis'))
idx = data['Specimen'].index.isin(gut.index)
gut.index = data['Specimen'][idx]

plt.figure(figsize=(12, 8))
plt.title('Gut Microbiome (Cophenetic Coefficient %0.3f)' % c)
plt.xlabel('Specimen')
plt.ylabel('Distance (Bray-Curtis)')
dendrogram(
    gut_Z,
    #color_threshold=0.95,
    labels = gut.index,
    leaf_rotation=90.,  # rotates the x axis labels
    leaf_font_size=8.,  # font size for the x axis labels
)
plt.show()