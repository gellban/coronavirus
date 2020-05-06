from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

# naive_bayes
class nb:
    def __init__(self):
        self.a = ''
        self.y_unique = None

    # build a model of data of pd type contains x1,...xm,y for each record
    def train(self, data):
        # Step 1: Calculate Prior Probability
        y_unique = sorted(data.y.unique())
        print('data.shape[1]', data.shape[1], 'y_unique', y_unique)
        prior_probability = np.zeros(len(data.y.unique()))
        for i in range(0,len(y_unique)):
            prior_probability[i]=sum(data['y']==y_unique[i])/len(data['y'])
        
        # Step 2: Calculate Conditional Probability
        conditional_probability = {}
        for i in range(1,data.shape[1]):
            x_unique = list(set(data['x'+str(i)]))
            print('i', i, 'x_unique', x_unique)
            x_conditional_probability = np.zeros((len(data.y.unique()),len(set(data['x'+str(i)]))))
            for j in range(0,len(y_unique)):
                for k in range(0,len(x_unique)):
                    x_conditional_probability[j,k]=data.loc[(data['x'+str(i)]==x_unique[k])&(data['y']==y_unique[j]),].shape[0]/sum(data['y']==y_unique[j])
        
            x_conditional_probability = pd.DataFrame(x_conditional_probability,columns=x_unique,index=y_unique)   
            conditional_probability['x'+str(i)] = x_conditional_probability       
            self.y_unique = y_unique
            self.prior_probability = prior_probability
            self.conditional_probability = conditional_probability
        return y_unique,prior_probability,conditional_probability

    ####################
    # Prediction
    ####################
    def prediction(self,X_test, y_test):
        title = 'Laplace: only q data'
        pred_list = []
        for i in range(len(y_test)):
            pred = self._single_prediction(list(X_test[i]), self.y_unique)
            pred_list.append(pred)
            # print('i', i, 'X_test[i]', X_test[i], 'y_test[i]', y_test[i], 'pred', pred)
        #     if y_test[i] == pred:
        #         accuracy += 1
        # accuracy /= len(y_test)
        predicted = list(pred_list)
        print('=======================')   
        print(title + ' with accuracy(%1.2f)' % np.mean(predicted == y_test))
        print(metrics.classification_report(y_test, predicted,
            target_names=self.y_unique))
        print('=======================')   

    ####################
    # one example Prediction
    ####################
    def _single_prediction(self, X, y_unique):
        unique_classes = y_unique
        max_prob = -1
        y_pred = 'awareness'

        c_i = 0
        try:
            for c in unique_classes:
                p_c = self.prior_probability[c_i]
                v_i = 1
                for x in X:
                    p_c *= self.conditional_probability['x'+str(v_i)][x][c_i]
                    v_i += 1
                # print('c', c, 'p_c', p_c)
                c_i += 1
                if max_prob < p_c:
                    max_prob = p_c
                    y_pred = c
        except:
            print("An exception occurred: maybe no value are the same")

        
        return y_pred



class MyMultinomialNB:
    def build_test_nb(X_train, y_train, X_test, y_test, y_unique, title):
        clf = MultinomialNB()
        clf.fit(X_train, y_train)
        clf.predict(X_test)
        predicted = clf.predict(X_test)
        print('=======================')   
        print(title + ' with accuracy(%1.2f)' % np.mean(predicted == y_test))
        print(metrics.classification_report(y_test, predicted,
            target_names=y_unique))
        print('=======================')   

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
        print('======')
        print('d[:2]:', d[:2])

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