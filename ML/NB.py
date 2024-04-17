import pandas as pd
import numpy as np

class Naive_Bayes:
    def __init__(self):
        pass

    def fit(self,X,y):
        self.classes = y[y.columns[0]].unique()
        class_count = y[y.columns[0]].value_counts()

        # 类先验概率
        self.class_prior = class_count / len(y)
        # 计算类条件概率
        self.prior = dict()
        for col in X.columns:
            for j in self.classes:
                p_x_y = X[(y==j).values][col].value_counts() # 每一列中每一个元素的计数
                for i in p_x_y.index:
                    self.prior[(col, i,j)] = p_x_y[i] / class_count[j] # 每一列中每一个元素在y的不同值下的计数
        return self.classes, self.class_prior, self.prior

    def predict(self, X_test):
        res = []
        for c in self.classes:
            p_y = self.class_prior[c]
            p_x_y = 1
            for i in X_test.items():
                p_x_y = self.prior[tuple(list(i)+[c])]
            res.append(p_y * p_x_y)
        return self.classes[np.argmax(res)]

if __name__ == "__main__":
    x1 = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3]
    x2 = ['S', 'M', 'M', 'S', 'S', 'S', 'M', 'M', 'L', 'L', 'L', 'M', 'M', 'L', 'L']
    y = [-1, -1, 1, 1, -1, -1, -1, 1, 1, 1, 1, 1, 1, 1, -1]
    df = pd.DataFrame({'x1': x1, 'x2': x2, 'y': y})
    X = df[['x1', 'x2']]
    y = df[['y']]
    X_test = {'x1': 2, 'x2': 'S'}

    nb = Naive_Bayes()
    classes, class_prior, prior = nb.fit(X, y)
    print('测试数据预测类别为：', nb.predict(X_test))

