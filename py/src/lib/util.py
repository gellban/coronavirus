from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split 

class DataPreprocessing:
    def __init__(self):
        fig_path = './figures/'
        file_name_input = '../../dataset/corona_class_only_hw3.csv'
        file_delimiter_input = ','
        df = pd.read_csv(file_name_input, delimiter=file_delimiter_input, encoding = "ISO-8859-1")
        print('shape df:', df.shape)
        d_class = df["class"].values#convert to np 
        print('d_class:', d_class[:2])
        self.d_class = d_class

        # //corona_stem_only
        file_name_input = '../../dataset/corona_stem_only_hw3.csv'
        # file_delimiter_input = ','
        df = pd.read_csv(file_name_input, delimiter=file_delimiter_input, encoding = "ISO-8859-1")
        # df["stem"]
        d = df["stem"].values.tolist()#convert to np then to list
        self.d = d
        # print('======')
        # print('d[:2]:', d[:2])

        q = ['corona', 'china', 'peopl', 'spread', 'coronaoutbreak', 
        'quarantin', 'infect', 'wuhan'
        , 'hand', 'border']
        self.q = q

        # d_str = ' '.join(d)
        # d_org_str = ' '.join(d_org)
        # print('q len:', len(q))
        pipe = Pipeline([('count', CountVectorizer(vocabulary=q)),
                        ('tfid', TfidfTransformer())]).fit(d)
        count_2d = pipe['count'].transform(d).toarray()
        self.count_2d = count_2d
        # print('count_2d[:10]')
        # print(count_2d[:10])
    def split_train_test(self, X, y):
        return train_test_split(
            X, y, test_size=0.20, random_state=42)
    def read_data(self):
        X, y = self.d, self.d_class
        # X_train, X_test, y_train, y_test = self.split_train_test(X, y)
        print('read_data: len(X), len(y)', len(X), len(y))
        return self.split_train_test(X, y)

    def read_data_q_only(self):
        X, y = self.count_2d, self.d_class
        print('read_data_q_only: len(X), len(y)', len(X), len(y))
        return self.split_train_test(X, y)    

class common:
    def np_to_pd(X, y):
        # Step 2: Calculate Conditional Probability
        conditional_probability = {}

        x_col_names = ['x'+str(i+1) for i in range(X.shape[1])]
        x_col_names.append('y')
        print('x_col_names', x_col_names)
        Xy = np.column_stack( (X,y) )#merge X with y to have 2d
        data = pd.DataFrame(Xy,columns=x_col_names) 
        return data