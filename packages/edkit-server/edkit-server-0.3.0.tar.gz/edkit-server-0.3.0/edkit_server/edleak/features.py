import numpy as np
from sklearn import linear_model
from sklearn import preprocessing


def normalize(dataset):
    '''Applies mean normalization to the provided dataset in the range [-1 1].

    arguments:
    dataset --  A list of input points that must be normalized.
    '''
#    return preprocessing.scale(dataset)
    return preprocessing.MinMaxScaler().fit_transform(dataset)
    '''
    max_val = max(dataset)
    min_val = min(dataset)
    deviation = max_val - min_val
    mean = sum(dataset) / len(dataset)
    normalized_dataset = [ (x-mean)/deviation for x in dataset]
    return normalized_dataset
    '''

def lin_reg_2nd_order(x,y):
    '''Computes a second order polynom via linear regression.

    arguments:
    x -- numpy array of features. dimension is n_samples x 1. 2nd order features are automatically extracted.
    y -- numpy array of target. dimension is n_samples x n_targets.
    '''
    x2 = np.array([x, x ** 2]).transpose()
    model = linear_model.LinearRegression()
    model.fit(x2,y)
    return np.concatenate([[model.intercept_], model.coef_])

def extract_linreg_feature(dataset):
    for entry in dataset:
        y = normalize(entry['mem'])
        x = np.array(normalize(list(range(len(y)))) )
        linreg_coef = lin_reg_2nd_order(x,y)
        entry['linreg_coef'] = linreg_coef
