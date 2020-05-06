from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
import numpy as np

import pandas as pd
from os import path
import os
import math

from lib.nb_lib.util import DataPreprocessing as dp
from lib.nb_lib.util import common as cm
from lib.nb_lib.graph import graph as gf
from lib.nb_lib.util import nb as nb
from lib.nb_lib.util import MyMultinomialNB as mnb
from lib.nb_lib.nb_laplace import nb_laplace as nbl

my_dp = dp()
my_gf = gf()

X_train, X_test, y_train, y_test = my_dp.read_data()
X_train


my_nbl = nbl(X_train, y_train)
#evaluate all test
predictions = my_nbl.prediction(X_test, y_test)
print('===============================================')
print('#One test case for correct classification of awareness')
for i in range(len(y_test)):
    if predictions[i] == y_test[i] and y_test[i] =='awareness':
        print('predictions[i]: ', predictions[i], ', y_test[i]: ', y_test[i])
        x = X_test[i]
        y_i = y_test[i]
        x_has_int = any((my_nbl.word_has_int(word) for word in x))
        if not x_has_int:
            my_nbl.evaluate(x,y_i, show_results=True)        
            break
        
print('===============================================')

print('===============================================')
print('#One test case for misclassification of awareness')
for i in range(len(y_test)):
    if predictions[i] != y_test[i] and y_test[i] =='awareness':
        print('predictions[i]: ', predictions[i], ', y_test[i]: ', y_test[i])
        x = X_test[i]
        y_i = y_test[i]
        x_has_int = any((my_nbl.word_has_int(word) for word in x))
        if not x_has_int:
            my_nbl.evaluate(x,y_i, show_results=True)        
            break
print('===============================================')

print('===============================================')
print('#Visualization of each class label')
actual_text = {c:"" for c in my_nbl.c_all}
predicted_text = {c:"" for c in my_nbl.c_all}
# print('actual_text', actual_text)
for i in range(len(y_train)):
    actual_text[y_train[i]] += X_train[i].replace("#", "")
for i in range(len(y_test)):
    predicted_text[y_test[i]] += X_test[i].replace("#", "")
for c in actual_text:
    title = 'Actual ' + c
    my_gf.plot_cloud(actual_text[c], 'Actual ' + c)
    my_gf.plot_cloud(predicted_text[c], 'Predicted ' + c)

text_file = open("actual_awareness.txt", "w")
n = text_file.write(actual_text['awareness'])
text_file.close()
# for i in range(len(y_test)):
#     if predictions[i] != y_test[i] and y_test[i] =='awareness':

