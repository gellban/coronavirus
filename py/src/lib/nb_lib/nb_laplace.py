from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

class nb_laplace:
    def __init__(self, X, y):
        self.X, self.y = X, y
        self.n = len(self.y) #number of examples
        self._generate_feature_set()
        self.print_feature_set()
        self.calc_p_c()
        self.calc_p_w_c()
        # x = X[0]
        # y_i = y[0]
        # self.evaluate(x,y_i, show_results=True)
        

    def _generate_feature_set(self):
        X, y = self.X, self.y
        vectorizer = CountVectorizer()
        self.vector = vectorizer.fit_transform(X)
        print('self.vector.shape', self.vector.shape)
        print('type(self.vector)', type(self.vector))
        print('self.vector', self.vector[:1])
        self.f_set_2d = self.vector.toarray()
        print('self.f_set_2d[:1]', self.f_set_2d[:1])
        self.voc = vectorizer.vocabulary_ #{word1:key1,...}
        print('type(self.voc)', type(self.voc))
        self.voc_by_index = {value:key for key, value in self.voc.items()}
        print('type(self.voc_by_index)', type(self.voc_by_index))
        # print('voc', voc)
        self.voc_len = self.vector.shape[1]#vocubulary length = |V|
        print('####Number of vocabulary terms:', self.voc_len)        
        # print('f_set_2d', f_set_2d[:3,:10]) 
        # return f_set_2d
        c_all = np.unique(y)
        self.c_all = c_all
        print('c_all (all features)', c_all)
        feature_set = dict()
        for c in c_all:
            print('feature:', c)
            feature_set[c] = np.zeros(self.voc_len)
        
        # print('feature_set', feature_set)
        i = 0
        for ex in self.f_set_2d:
            # if i > 5:
            #     break
            c = y[i]
            feature_set[c] = np.add(ex, feature_set[c])
            # print('i', i, 'ex', ex, 'sum', sum(ex),'sum of feature_set[c]', np.sum(feature_set[c]))
            i += 1
        for c in c_all:
            print('feature (%s), sum:%4.2f'%(c, sum(feature_set[c])))
        self.feature_set = feature_set
        print('feature_set', feature_set)
        


        # for i in 
        # x_conditional_probability = np.zeros((len(data.y.unique()),len(set(data['x'+str(i)]))))   
    def print_feature_set(self):
        for c in self.feature_set:
            print('feature:', c, 'sum of counts', sum(self.feature_set[c]))
            j = 0
            j_displayed = 0
            print('word: val')
            for v in self.feature_set[c]:
                word = self.get_word_in_voc(j)
                # print('word.isnumeric()', word.isnumeric())
                word_has_int = self.word_has_int(word)#any(char.isdigit() for char in word)
                # if not word.isnumeric() and v > 0.0:
                if not word_has_int and v > 0.0:
                    print(word + ':' + str(int(v)))
                    j_displayed += 1
                j += 1
                if j_displayed > 10:
                    break
    #get word in vocabulary
    def get_word_in_voc(self, j):
        return self.voc_by_index.get(j)

    #get index of a word in vocabulary
    def get_key_in_voc(self, word):
        return self.voc.get(word)

    def calc_p_c(self):
        feature_counts = {c:(self.y==c).sum() for c in self.feature_set}
        p_c = {c:feature_counts.get(c)/self.n for c in feature_counts}
        print('n=', self.n)
        print('feature_counts', feature_counts)
        print('p_c',p_c)
        self.p_c = p_c

    def word_has_int(self, word):
         return any(char.isdigit() for char in word)

    def calc_p_w_c(self):
        p_w_c = dict() 
        #for all class labels
        for c in self.feature_set:
            #vector of counts per word
            word_count_2d = self.feature_set.get(c)
            #sum of count(w,c) for all words in V
            all_w_c_count = word_count_2d.sum()
            j = 0
            for count in word_count_2d:
                word = self.get_word_in_voc(j)
                j += 1
                prob = (count + 1) / (all_w_c_count + self.voc_len) 
                #the probabilty(w_i,c)
                p_w_c[(word, c)] = prob
        self.p_w_c = p_w_c

    def prediction(self, X, y):
        predictions = []
        for i in range(len(y)):
            x = X[i] 
            y_i = y[i]
            pred = self.evaluate(x, y_i)
            predictions.append(pred)
        predicted = np.array(predictions)
        title = 'Titile'
        print('=======================')   
        print(title + ' with accuracy(%1.2f)' % np.mean(predicted == y))
        print(metrics.classification_report(y, predicted,
            target_names=self.c_all))
        print('=======================')   
        
        return predicted

    def evaluate(self, x, y_i, show_results=False):
        tokens = set(x.split(' '))
        if show_results:
            print('evaluate:')
            print('query:', x)
            # print('tokens:', tokens)
        
        probs = dict()
        for c in self.feature_set:
            prob = self.p_c.get(c)
            
            for word in tokens:
                p_w_c = self.p_w_c.get((word, c))
                if p_w_c is None:
                    p_w_c = 1.0 
                prob *=  p_w_c
                if show_results and y_i==c and p_w_c!=1.0:
                    print('p(%s|%s)= %1.12f'%(word, c, p_w_c))
            probs[c] = prob
        probs_inverse = [(value, key) for key, value in probs.items()]
        pred = max(probs_inverse)[1]
        if show_results:
            print('probs:', probs)
            print('predicted class:', max(probs_inverse)[1], ', actual class:', y_i)
        return pred