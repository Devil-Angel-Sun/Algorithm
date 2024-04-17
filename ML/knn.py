import numpy as np
from collections import Counter
import random
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.utils import shuffle

plt.rcParams['figure.figsize'] = (10.0, 8.0)
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'

class kNearestNeighbor:
    def __init__(self):
        pass

    def train(self, X, y):
        self.X_train = X
        self.y_train = y

    def compute_distance(self,X):
        """ L2 距离度量 """
        num_test = X.shape[0]
        num_train = self.X_train.shape[0]
        dists = np.zeros((num_test, num_train))

        M = np.dot(X,self.X_train.T)
        te = np.square(X).sum(axis = 1)
        tr = np.square(self.X_train).sum(axis = 1)
        dists = np.sqrt(-2 * M +tr + np.matrix(te).T)
        return dists

    def predict_labels(self, dists, k = 1):
        num_test = dists.shape[0]
        y_pred = np.zeros(num_test)
        for i in range(num_test):
            closest_y = []
            labels = self.y_train[np.argsort(dists[i,:])].flatten()
            closest_y = labels[0:k]

            c = Counter(closest_y)
            y_pred[i] = c.most_common(1)[0][0]
        return y_pred

    def cross_validation(self, X_train, y_train):
        num_folds = 5
        k_choices = [1, 3, 5, 8, 10, 12, 15, 20, 50, 100]
        
        X_train_folds = []
        y_train_folds = []
        
        X_train_folds = np.array_split(X_train, num_folds)
        y_train_folds = np.array_split(y_train, num_folds)
        k_to_accuracies = {}
        for k in k_choices:    
            for fold in range(num_folds):
                # 对传入的训练集单独划出一个验证集作为测试集
                validation_X_test = X_train_folds[fold]
                validation_y_test = y_train_folds[fold]
                temp_X_train = np.concatenate(X_train_folds[:fold] + X_train_folds[fold + 1:])
                temp_y_train = np.concatenate(y_train_folds[:fold] + y_train_folds[fold + 1:])      
                # 计算距离
                temp_dists = self.compute_distance(validation_X_test)
                temp_y_test_pred = self.predict_labels(temp_dists, k=k)
                temp_y_test_pred = temp_y_test_pred.reshape((-1, 1))      
                # 查看分类准确率
                num_correct = np.sum(temp_y_test_pred == validation_y_test)
                num_test = validation_X_test.shape[0]
                accuracy = float(num_correct) / num_test
                k_to_accuracies[k] = k_to_accuracies.get(k,[]) + [accuracy]

        for k in sorted(k_to_accuracies):    
            for accuracy in k_to_accuracies[k]:
                print('k = %d, accuracy = %f' % (k, accuracy))
        
        accuracies_mean = np.array([np.mean(v) for k,v in sorted(k_to_accuracies.items())])
        best_k = k_choices[np.argmax(accuracies_mean)]
        print('最佳 k 值为{}'.format(best_k))
        return best_k

### 数据集
iris = datasets.load_iris()
X, y = shuffle(iris.data, iris.target, random_state = 13)
X = X.astype(np.float32)
y = y.reshape((-1,1))
offset = int(X.shape[0] * 0.7)
X_train, y_train = X[:offset], y[:offset]
X_test, y_test = X[offset:], y[offset:]
y_train = y_train.reshape((-1,1))
y_test = y_test.reshape((-1,1))

knn_classifier = kNearestNeighbor()
knn_classifier.train(X_train, y_train)
best_k = knn_classifier.cross_validation(X_train, y_train)
dists = knn_classifier.compute_distance(X_test)
y_test_pred = knn_classifier.predict_labels(dists, k = best_k)
y_test_pred = y_test_pred.reshape((-1,1))
num_correct = np.sum(y_test_pred == y_test)
accuracy = float(num_correct) / X_test.shape[0]