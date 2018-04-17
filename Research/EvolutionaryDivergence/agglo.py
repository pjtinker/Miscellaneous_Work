# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 13:30:12 2018

@author: hemlo
"""

from time import time

import numpy as np
from scipy import ndimage
from matplotlib import pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA
from sklearn import manifold, datasets




#----------------------------------------------------------------------
# Visualize the clustering
def plot_clustering(X_red, X, labels, title=None):
    x_min, x_max = np.min(X_red, axis=0), np.max(X_red, axis=0)
    X_red = (X_red - x_min) / (x_max - x_min)

    plt.figure(figsize=(6, 4))
    for i in range(X_red.shape[0]):
        plt.text(X_red[i, 0], X_red[i, 1], str(y[i]),
                 color=plt.cm.spectral(labels[i] / 10.),
                 fontdict={'weight': 'bold', 'size': 9})

    plt.xticks([])
    plt.yticks([])
    if title is not None:
        plt.title(title, size=17)
    plt.axis('off')
    plt.tight_layout()

os.chdir("D:\Research\WalkerResearch")
data = pd.read_csv('BacteraMicrobiome.csv')
gut = data[data['Skin/Gut'] == 'gut'].copy()
gut.shape
skin = data[data['Skin/Gut'] == 'skin'].copy()
skin.shape
y = skin['Specimen'].as_matrix()
skin_otus = skin.iloc[:, 6:].copy()
gut_otus = gut.iloc[:, 6:].copy()

print("Computing embedding")
X_red = manifold.SpectralEmbedding(n_components=2).fit_transform(skin_otus)
print("Done.")

from sklearn.cluster import AgglomerativeClustering

for linkage in ('ward', 'average', 'complete'):
    clustering = AgglomerativeClustering(linkage=linkage, n_clusters=9)
    t0 = time()
    clustering.fit(X_red)
    print("%s : %.2fs" % (linkage, time() - t0))

    plot_clustering(X_red, skin_otus.as_matrix(), clustering.labels_, "%s linkage" % linkage)


plt.show()