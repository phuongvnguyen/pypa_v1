"""
This file is to call algorithms for solving the problems of classification
authored: Phuong V. Nguyen
"""
import pandas as pd
import numpy as np
import warnings
import matplotlib.pyplot as plt
import seaborn as sns
# Linear agorithms
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.linear_model import LogisticRegression
# Non-linear algorithms
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
# Neural Networks
from sklearn.neural_network import MLPClassifier
# Metric
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import Pipeline
from typing import List, Tuple, Any, Union, Optional, Dict

warnings.filterwarnings("ignore")


def model_list():
    """
    this function is to call a list of potential models to compete
    :return models: list of models
    """
    models = [('Logistic', LogisticRegression(max_iter=1000)),
              ('Linear-Discriminant-Analysis', LinearDiscriminantAnalysis()),
              ('Gaussian_Naive_Bayes ', GaussianNB())]
              ('Support-Vector-Class', SVC()),
              ('K-Nearest-Class', KNeighborsClassifier()),
              ('Decision_Tree_Class', DecisionTreeClassifier()),
              ('Neural_Network', MLPClassifier(max_iter=2000))]
    return models


def models_comparer(list_of_model, x, y):
    """
    This function is to compare the performance of some selected models
    :param list_of_model: list of model for competition
    :param x: feature
    :param y: label
    :return results, names:
    """
    results = []
    names = []
    for name, model in list_of_model:
        kfold = KFold(n_splits=10, random_state=7)
        cv_results = cross_val_score(model, x, y.values.ravel(),
                                     cv=kfold, scoring='roc_auc')
        results.append(cv_results)
        names.append(name)
        msg = '%s: %f (%f)' % (name, cv_results.mean(), cv_results.std())
        print(msg)
    plot_result(results, names)
    return results, names


def plot_result(results, names):
    """
    This function is to plot the result of comparing performance among selected models
    :param results: score of performance
    :param names: name of competing model
    """

    fig = plt.figure(figsize=(10, 6))
    fig.suptitle('Model Performance Comparision (AUROC)')
    ax = fig.add_subplot(111)
    plt.boxplot(results)
    ax.set_xticklabels(names, rotation=80)
    ax.grid(True)
    plt.show()


# class model_selector():
#
#     def __init__(self):
#         self.models = self.model_list()
#         self.results, self.names = self.models_comparer(self.models, self.x, self.y)
#         self.plot_result(self.results, self.names)
#
#     def model_list(self):
#         """
#         This function is to configure a number of models which will compete with each other
#         . Each model has the default configuration
#         :return models: a group of model with default configuration
#         """
#         models = []
#         models.append(('Logistic', LogisticRegression(max_iter=1000)))
#         models.append(('Linear-Discriminant-Analysis', LinearDiscriminantAnalysis()))
#         models.append(('Gaussian_Naive_Bayes ', GaussianNB()))
#         models.append(('Support-Vector-Class', SVC()))
#         models.append(('K-Nearest-Class', KNeighborsClassifier()))
#         models.append(('Decision_Tree_Class', DecisionTreeClassifier()))
#         models.append(('Neural_Network', MLPClassifier(max_iter=2000)))
#         return models
#
#     def models_comparer(self, models, x, y):
#         """
#         This function is to compare the performance of some selected models
#         :param models: list of selected model
#         :param x: feature data
#         :param y: label data
#         :return results, names: result and names
#         """
#         results = []
#         names = []
#         for name, model in models:
#             kfold = KFold(n_splits=10, random_state=7)
#             cv_results = cross_val_score(model, x, y.values.ravel(), cv=kfold, scoring='roc_auc')
#             results.append(cv_results)
#             names.append(name)
#             msg = '%s: %f (%f)' % (name, cv_results.mean(), cv_results.std())
#             print(msg)
#         return results, names
#
#     def plot_result(self, results, names):
#         """
#         This function is to plot the result of comparing performance among selected models
#         :param results: score
#         :param names: model
#         :return:
#         """
#         fig = plt.figure(figsize=(10, 6))
#         fig.suptitle('Model Performance Comparision (AUROC)')
#         ax = fig.add_subplot(111)
#         plt.boxplot(results)
#         ax.set_xticklabels(names, rotation=80)
#         ax.grid(True)
#         plt.show()
#
#
# class main():
#     model_selector = model_selector()
#
#
# if __name__ == '__main__':
#     main()
#
# print("hello world")
