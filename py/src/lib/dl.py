# DL

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn import metrics

import numpy as np

from lib.graph import graph as gf


from keras.models import Sequential
from keras.layers import Dense, Conv1D, Flatten
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from keras.utils import to_categorical

from keras.layers import Input, Dense, LSTM, GRU, multiply, concatenate, Activation, Masking, Reshape
from keras.layers import Conv1D, BatchNormalization, GlobalAveragePooling1D, Permute, Dropout
from keras.layers import Add, GRU, RepeatVector, Bidirectional, Conv2D, MaxPooling2D, MaxPooling1D, UpSampling1D,Flatten

from keras.models import Model


class dl:
    def __init__(self, X, y, X_test, y_test):
        self.X, self.y = X, y
        self.c_set = set(y)
        self.c_dict = {'awareness': 0, 'news': 1, 'myth': 2}
        self.c_dict_keys = {0:'awareness', 1:'news', 2:'myth'}
        self.X_test, self.y_test = X_test, y_test
        self.n = len(self.y) #number of examples
        self.n_test = len(self.y_test) #number of examples
        self.y_unique = sorted(np.unique(y)) #all class labels
        self.build_and_test()
        self.visualization()
        self.show_performance()
        print('self.y_unique', self.y_unique)

        

    def build_and_test(self):
        X, y = self.X, self.y

        X_train, y_train, X_test, y_test = self.vectorization(X, y, self.X_test, self.y_test)
        self.create_NN_model(X_train, y_train, X_test, y_test)

    def visualization(self):
        my_gf = gf()
        print('===============================================')
        print('#DL Visualization of each class label')
        actual_text = {c:"" for c in self.y_unique}
        predicted_text = {c:"" for c in self.y_unique}
        # print('actual_text', actual_text)
        for i in range(self.n):
            actual_text[self.y[i]] += self.X[i].replace("#", "")
        for i in range(self.n_test):
            if self.predicted[i] == self.y_test[i]:
                predicted_text[self.y_test[i]] += self.X_test[i].replace("#", "")
        for c in actual_text:
            title = 'DL-CNN deep learning Actual ' + c
            my_gf.plot_cloud(actual_text[c], 'DeepLearning Actual ' + c)
            my_gf.plot_cloud(predicted_text[c], 'DeepLearning Predicted ' + c)

    def show_performance(self):
        print('=======================')   
        print('DL with accuracy(%1.2f)' % np.mean(self.predicted == self.y_test))
        print(metrics.classification_report(self.y_test, self.predicted,
            target_names=self.y_unique))
        print('=======================')   

    def vectorization(self, X, y, X_test, y_test):
        # list of text documents
        text = X
        # create the transform
        vectorizer = CountVectorizer()
        # tokenize and build vocab
        vectorizer.fit(text)
        vector = vectorizer.transform(text)
        # summarize encoded vector
        print(vector.shape)
        print(type(vector))
        # print(vector.toarray()) 
        X_vect = vector.toarray() 
        X_vect_test = vectorizer.transform(X_test).toarray() 
        print('#####X_vect', X_vect[:2])
        print('#####X_vect_test', X_vect_test[:2])

        print('self.c_set', self.c_set)
        print('self.c_dict', self.c_dict)
        y_vect = np.array([self.c_dict[c] for c in y])
        y_vect_test = np.array([self.c_dict[c] for c in y_test])
        print('Y_vect', y_vect[:5], y[:5])

        return X_vect, y_vect, X_vect_test, y_vect_test


    def create_NN_model(self, X_train, y_train, X_test, y_test):
        max_tweet_length = X_train.shape[1]#150
        print('X_train.shape[1]', X_train.shape[1])
        print('X_test.shape[1]', X_test.shape[1])

        num_classes = len(self.y_unique)
        varietal_list = to_categorical(y_train)
        y_int = y_train
        y_binary = to_categorical(y_int)
        # print('varietal_list:', varietal_list)
        print('##test, ', y_binary)


        epochs = 150#30#80#500 #6#3
        batch_size = 128#128
        input_dim = self.n#1884#2500
        embedding_vector_length = batch_size#128#300#64 #150
        model_filename = 'dl_model.h5'
        model = Sequential()
        model.add(Embedding(max_tweet_length, embedding_vector_length, input_length=max_tweet_length))
        model.add(Conv1D(32, 8))
        model.add(Flatten())
        model.add(Dense(512, activation='relu'))
        model.add(Dropout(0.3))

        model.add(Dense(512, activation='relu'))
        model.add(Dropout(0.3))
        model.add(Dense(512, activation='relu'))
        model.add(Dropout(0.3))



        model.add(Dense(100, activation='relu'))
        model.add(Dense(num_classes, activation='softmax'))

        print('model NN:')
        print(model.summary())
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        model.fit(X_train, y_binary, epochs=epochs, batch_size=batch_size)
        y_binary = to_categorical(y_test)
        y_score = model.predict(X_test)
        print('1:y_score', y_score)
        pred = [np.argmax(y) for y in y_score]
        # print('2:pred', pred)
        print('Accuracy', np.mean(pred==y_test))
        predicted = np.array([self.c_dict_keys[c] for c in pred])
        self.predicted = predicted

    def create_NN_model_hashim(self, X_train, y_train, X_test, y_test):
        max_tweet_length = X_train.shape[1]#150
        print('X_train.shape[1]', X_train.shape[1])
        print('X_test.shape[1]', X_test.shape[1])

        embedding_vector_length = 150
        num_classes = len(self.y_unique)
        varietal_list = to_categorical(y_train)
        y_int = y_train
        y_binary = to_categorical(y_int)
        print('##test, ', y_binary)

        MAX_NB_VARIABLES_V = 1
        MAX_TIMESTEPS = max_tweet_length
        NB_CLASS = num_classes
        input_shape = X_train.shape
        model = self.generate_model_hashim(NB_CLASS, MAX_NB_VARIABLES_V, MAX_TIMESTEPS, input_shape)




        print('model NN:')
        print(model.summary())
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc', self.f1_m, self.precision_m, self.recall_m])
        model.fit(X_train, y_binary, epochs=20, batch_size=64)
        y_binary = to_categorical(y_test)
        y_score = model.predict(X_test)
        print('1:y_score', y_score)
        pred = [np.argmax(y) for y in y_score]
        print('2:pred', pred)
        print('Accuracy', np.mean(pred==y_test))







    from keras import backend as K

    def recall_m(self, y_true, y_pred):
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
        recall = true_positives / (possible_positives + K.epsilon())
        return recall

    def precision_m(self, y_true, y_pred):
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
        precision = true_positives / (predicted_positives + K.epsilon())
        return precision

    def f1_m(self, y_true, y_pred):
        precision = precision_m(y_true, y_pred)
        recall = recall_m(y_true, y_pred)
        return 2*((precision*recall)/(precision+recall+K.epsilon()))