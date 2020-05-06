from lib.util import DataPreprocessing as dp
from lib.dl import dl

my_dp = dp()

X_train, X_test, y_train, y_test = my_dp.read_data()
print('=================================')
print('X_train first:')
print(X_train[0])
print('=================================')
my_dl = dl(X_train, y_train, X_test, y_test)
print('=========The end=================')
