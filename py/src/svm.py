# conda activate ir
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
import numpy as np

import pandas as pd
from os import path
import os
import math

from lib.util import DataPreprocessing as dp
from lib.graph import graph as gf
from lib.svm import my_svm as svm

my_dp = dp()
my_gf = gf()

X_train, X_test, y_train, y_test = my_dp.read_data()
print('=================================')
print('X_train first:')
print(X_train[0])
print('=================================')
my_svm = svm(X_train, y_train, X_test, y_test)
print('=========The end=================')
