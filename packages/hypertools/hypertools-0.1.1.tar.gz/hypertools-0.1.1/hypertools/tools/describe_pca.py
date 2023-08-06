#!/usr/bin/env python

"""
Correlates raw data with PCA reduced data to get a sense for how well the data
can be summarized with n dimensions.  Useful for evaluating quality of PCA reduced
plots.

INPUTS:
-numpy array(s)
-list of numpy arrays

OUTPUTS:
-Dictionary with correlation values between raw data and PCA reduced data (optional)
"""

##PACKAGES##
from __future__ import division
import warnings
import numpy as np
from scipy.spatial.distance import pdist
from scipy.spatial.distance import cdist
import scipy.spatial.distance as sd
import matplotlib.pyplot as plt
import seaborn as sns
from .align import *
from .reduce import reduce as reduceD
from .._shared.helpers import format_data

##SET SEABORN STYLE##
sns.set(style="darkgrid")

##MAIN FUNCTION##
def describe_pca(x, show=True):
    warnings.warn('When input data is large, this computation can take a long time.')

    ##SUB FUNCTIONS##
    def PCA_summary(x,max_dims=None):
        if type(x) is list:
            x = np.vstack(x)
        if max_dims is None:
            max_dims = x.shape[1]
        cov_alldims = pdist(x,'correlation')
        corrs=[]
        for num in range(2,max_dims):
            cov_PCA = pdist(np.vstack(reduceD(x,num)),'correlation')
            corrs.append(np.corrcoef(cov_alldims, cov_PCA)[0][1])
            del cov_PCA
        return corrs

    x = format_data(x)

    attrs = {}
    attrs['PCA_summary'] = {}
    attrs['PCA_summary']['average'] = PCA_summary(x,x[0].shape[1])
    max_group = np.where(attrs['PCA_summary']['average']==np.max(attrs['PCA_summary']['average']))[0][0]
    attrs['PCA_summary']['individual'] = [PCA_summary(x_i,max_group) for x_i in x]

    if show:
        fig, ax = plt.subplots()
        ax = sns.tsplot(data=attrs['PCA_summary']['individual'], time=[i for i in range(2,max_group)], err_style="unit_traces")
        ax.set_title('Correlation with raw data by number of PCA components')
        ax.set_ylabel('Correlation')
        ax.set_xlabel('Number of PCA components')
        plt.show()
        return fig, ax, attrs
    else:
        return attrs
