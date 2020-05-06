from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn import metrics

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV

from pprint import pprint
from time import time

from sklearn.model_selection import cross_val_score


from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA

from gensim.models.ldamodel import LdaModel as Lda

from lib.graph import graph as gf

class my_svm:
    def __init__(self, X, y, X_test, y_test):
        self.X, self.y = X, y
        self.X_test, self.y_test = X_test, y_test
        self.n = len(self.y) #number of examples
        self.n_test = len(self.y_test) #number of examples
        self.y_unique = sorted(np.unique(y)) #all class labels
        self.build_and_test(classifier=SVC())
        self.visualization()
        self.show_performance()
        print('self.y_unique', self.y_unique)

        

    def build_and_test(self, classifier=LinearSVC()):
        X, y = self.X, self.y


        pipeline = Pipeline([
            ('vect', CountVectorizer()),
            ('clf', classifier),
        ])

        parameters = {
            'clf__C': (1, 100, 1000),
            'clf__gamma': ('scale', 'auto'),
            'clf__kernel': ('linear', 'poly', 'rbf', 'sigmoid'),
        }
        grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1, verbose=1)

        print("Performing grid search...")
        print("pipeline:", [name for name, _ in pipeline.steps])
        print("parameters:")
        pprint(parameters)
        t0 = time()
        grid_search.fit(self.X, self.y)
        print("done in %0.3fs" % (time() - t0))
        print()

        print('====================================')
        all_param = grid_search.get_params()
        print('all_param:', all_param)
        print('====================================')

        print("Best score: %0.3f" % grid_search.best_score_)
        print("Best parameters set:")
        best_parameters = grid_search.best_estimator_.get_params()
        for param_name in sorted(parameters.keys()):
            print("\t%s: %r" % (param_name, best_parameters[param_name]))
        pipeline.fit(self.X,self.y)
        predicted = pipeline.predict(self.X_test)
        print('SVM - Accuracy:', np.mean(predicted == self.y_test))
        self.predicted = predicted

    def visualization(self):
        my_gf = gf()
        print('===============================================')
        print('#Visualization of each class label')
        actual_text = {c:"" for c in self.y_unique}
        predicted_text = {c:"" for c in self.y_unique}
        # print('actual_text', actual_text)
        for i in range(self.n):
            actual_text[self.y[i]] += self.X[i].replace("#", "")
        for i in range(self.n_test):
            if self.predicted[i] == self.y_test[i]:
                predicted_text[self.y_test[i]] += self.X_test[i].replace("#", "")
        for c in actual_text:
            title = 'SVM Actual ' + c
            my_gf.plot_cloud(actual_text[c], 'SVM Actual ' + c)
            my_gf.plot_cloud(predicted_text[c], 'SVM Predicted ' + c)

    def show_performance(self):
        print('=======================')   
        print(' with accuracy(%1.2f)' % np.mean(self.predicted == self.y_test))
        print(metrics.classification_report(self.y_test, self.predicted,
            target_names=self.y_unique))
        print('=======================')   


