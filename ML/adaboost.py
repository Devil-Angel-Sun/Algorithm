# 数据测试
from sklearn import datasets
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
data = datasets.load_digits()
X = data.data
y = data.target

digit1 = 1
digit2 = 8
idx = np.append(np.where(y == digit1)[0],np.where(y == digit2)[0])
y = data.target[idx]
y[y == digit1] = -1
y[y == digit2] = 1
X = data.data[idx]
X_train, X_test,y_train, y_test = train_test_split(X, y, test_size = 0.7)
#############################################################################

import numpy as np
from sklearn.tree import DecisionTreeClassifier

class Adaboost:
    def __init__(self, n_estimators = 50):
        self.n_estimators = n_estimators # 基学习器个数
        self.estimators = [] # 保存基学习器模型
        self.estimator_weights = np.zeros(n_estimators) # 保存基学习器的权重
        self.estimator_error = np.zeros(n_estimators)   # 保存基学习器的错误率

    def fit(self, X, y):
        n_samples, n_features = X.shape

        w = np.full(n_samples, 1/n_samples) # 初始化基学习器权重

        for i in range(self.n_estimators):
            # 拟合基学习器
            tree = DecisionTreeClassifier(max_depth = 1)
            tree.fit(X, y, sample_weight = w)
            y_pred = tree.predict(X)

            # 计算错误率并更新权重
            err = np.sum(w[y_pred != y])
            alpha = 0.5 * np.log((1-err)/err)
            w *= np.exp(-alpha * y * y_pred)
            w /= np.sum(w)

            # 保存基学习器和其权重
            self.estimators.append(tree)
            self.estimator_error[i] = err
            self.estimator_weights[i] = alpha

    def predict(self,X):
        n_samples = X.shape[0]
        y_pred = np.zeros(n_samples)
        for i in range(self.n_estimators):
            y_pred += self.estimator_weights[i] * self.estimators[i].predict(X)
        return np.sign(y_pred)

# train an Adaboost classifier
clf = Adaboost(n_estimators=50)
clf.fit(X_train, y_train)

# make predictions on the test set
y_pred = clf.predict(X_test)

# calculate the accuracy of the classifier
acc = accuracy_score(y_test, y_pred)
print("Accuracy:", acc)

###################################################
# 另一种实现

class DecisionDump:
    def __init__(self):
        self.polarity = 1 # 基于划分阈值决定样本分类为 1 还是 -1
        self.feature_index = None # 特征索引
        self.threshold = None # 特征划分阈值
        self.alpha = None # 指示分类准确率的值

class AdaBoost:
    def __init__(self, n_estimators):
        self.n_estimators = n_estimators
    
    def fit(self, X, y):
        n_samples, n_features = X.shape
        w = np.full(n_samples, (1/n_samples)) # 初始化权重
        self.estimators = []

        # 根据最小分类误差选择最优划分特征
        for _ in range(self.n_estimators):
            clf = DecisionDump()     # 训练一个基分类器
            min_error = float('inf') # 设定一个最小化误差

            for feature_i in range(n_features):
                feature_values = np.expand_dims(X[:,feature_i], axis = 1) # 将(n,)维数据变成(1,n)
                unique_values = np.unique(feature_values) # 取该属性下数值的唯一值

                for threshold in unique_values:
                    p = 1                                       # 假定为正类
                    prediction = np.ones(np.shape(y))           # 初始化所有预测值为 1
                    prediction[X[:,feature_i] < threshold] = -1 # 低于划分阈值，预测值为 -1
                    error = np.sum(w[y != prediction])          # 错误率

                    # 如果分类误差大于 0.5，则进行正负类反翻转
                    if error > 0.5:
                        error = 1 - error
                        p = -1
                    
                    if error < min_error:
                        clf.polarity = p
                        clf.feature_index = feature_i
                        clf.threshold = threshold
                        min_error = error

            # 计算基分类器权重
            clf.alpha = 0.5* np.log((1.0 - min_error)/(min_error+1e-10))
            prediction = np.ones(np.shape(y)) # 初始化所有预测值为 1
            negative_idx = (clf.polarity * X[:,clf.feature_index]<clf.polarity * clf.threshold)
            prediction[negative_idx] = -1     # 将负类设置为 -1
            # 更新权重
            w += np.exp(-clf.alpha * y * prediction)
            w /= np.sum(w)

            self.estimators.append(clf)
        
    def predict(self,X):
        n_samples = X.shape[0]
        y_pred = np.zeros((n_samples,1)) # 初始化预测值为 0
        
        # 计算么一个基分类器的预测值
        for clf in self.estimators:
            predictions = np.ones(np.shape(y_pred))
            negative_idx = (clf.polarity * X[:,clf.feature_index]<clf.polarity * clf.threshold)
            predictions[negative_idx] = -1 
            y_pred += clf.alpha * predictions

        y_pred = np.sign(y_pred).flatten()

clf = AdaBoost(n_estimators = 5)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

accurary = accuracy_score(y_test, y_pred)

########################################################
# sklearn
from sklearn.ensemble import AdaBoostClassifier
clf_ = AdaBoostClassifier(n_estimators = 5, random_state = 0)
clf_.fit(X_train, X_test)
y_pred_ = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred_)