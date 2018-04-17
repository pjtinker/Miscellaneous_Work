# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 12:51:11 2018

@author: hemlo
"""

import itertools
import os
import pandas as pd
import numpy as np
from scipy import linalg
import matplotlib.pyplot as plt
import matplotlib as mpl

from sklearn import mixture

color_iter = itertools.cycle(['navy', 'c', 'cornflowerblue', 'gold',
                              'darkorange', 'orange', 'brown', 'purple', 'magenta'])


def plot_results(X, Y_, means, covariances, index, title):
    splot = plt.subplot(2, 1, 1 + index)
    for i, (mean, covar, color) in enumerate(zip(
            means, covariances, color_iter)):
        v, w = linalg.eigh(covar)
        v = 2. * np.sqrt(2.) * np.sqrt(v)
        u = w[0] / linalg.norm(w[0])
        # as the DP will not use every component it has access to
        # unless it needs it, we shouldn't plot the redundant
        # components.
        if not np.any(Y_ == i):
            continue
        plt.scatter(X[Y_ == i, 0], X[Y_ == i, 1], .8, color=color)

        # Plot an ellipse to show the Gaussian component
        angle = np.arctan(u[1] / u[0])
        angle = 180. * angle / np.pi  # convert to degrees
        ell = mpl.patches.Ellipse(mean, v[0], v[1], 180. + angle, color=color)
        ell.set_clip_box(splot.bbox)
        ell.set_alpha(0.5)
        splot.add_artist(ell)

    plt.xlim(-9., 5.)
    plt.ylim(-3., 6.)
    plt.xticks(())
    plt.yticks(())
    plt.title(title)


os.chdir("D:\Research\WalkerResearch")
data = pd.read_csv('BacteraMicrobiome.csv')
gut = data[data['Skin/Gut'] == 'gut'].copy()
gut.shape
skin = data[data['Skin/Gut'] == 'skin'].copy()
skin.shape

skin_otus = skin.iloc[:, 6:].copy()
gut_otus = gut.iloc[:, 6:].copy()

# Fit a Gaussian mixture with EM using five components
#gmm = mixture.GaussianMixture(n_components=9, covariance_type='full').fit(skin_otus)
#plot_results(skin_otus.as_matrix(), gmm.predict(skin_otus), gmm.means_, gmm.covariances_, 0,'Gaussian Mixture')

# Fit a Dirichlet process Gaussian mixture using five components
dpgmm = mixture.BayesianGaussianMixture(n_components=9,
                                        covariance_type='full').fit(skin_otus)
plot_results(skin_otus.as_matrix(), dpgmm.predict(skin_otus), dpgmm.means_, dpgmm.covariances_, 1,
             'Bayesian Gaussian Mixture with a Dirichlet process prior')

plt.show()