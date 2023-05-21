from copy import deepcopy
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SequentialFeatureSelector
from sklearn.model_selection import TimeSeriesSplit
 '''
Finding the Optimal Feature Subset using CFS (Correlation-based Feature Selection).
In our feature selection process, we aim to identify the best subset of features
that exhibit strong correlations with the target variable while having weak correlations
with each other. This helps us uncover the most informative and independent features for our model.
    '''

def get_best_cfs_features(df, features, target):
   

    features_left = features.copy()
    features_subset = []
    best_merit = 0

    while features_left:

        best_feature = None

        for feature in features_left:
            current_subset = features_subset + [feature]
            merit = get_cfs(df, current_subset, target)

            if merit > best_merit:
                best_feature = feature
                best_merit = merit

        if best_feature is None:
            break
        else:
            features_left.remove(best_feature)
            features_subset.append(best_feature)

    return features_subset, best_merit


def get_cfs(df, subset, label): # CFS for specific subset of features

    k = len(subset)

    all_corr = df[subset+[label]].corr()
    # average feature-class correlation
    rcf = (all_corr[label][subset]).abs().mean()

    # average feature-feature correlation
    corr = all_corr[subset].loc[subset]

    if corr.shape[0] > 1:
        corr.values[np.tril_indices_from(corr.values)] = np.nan

    corr = abs(corr)
    rff = corr.unstack().mean()

    return (k * rcf) / (k + k * (k-1) * rff) ** 0.5


def fit_default_model(model, X, y):
    model = deepcopy(model)
    model.fit(X, y)
    return model, X.columns


def fit_sfs_model(model, X, y, n_splits=3):

    sfs = SequentialFeatureSelector(model,
                                    cv=TimeSeriesSplit(n_splits),
                                    n_features_to_select=15,
                                    n_jobs=-1)
    model = Pipeline([('selection', sfs),
                      ('classifier', model)])

    model.fit(X, y)
    return model, X.columns


def fit_cfs_model(model, X, y):
    Xy = pd.concat((X, pd.DataFrame(y)), axis=1)
    features, _ = get_best_cfs_features(Xy, list(X.columns), y.name)
    model = deepcopy(model)
    model.fit(X[features], y)
    return model, features
