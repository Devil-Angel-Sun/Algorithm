import matplotlib.pyplot as plt
import numpy as np
class Hard_Margin_SVM:
    def __init__(self, visualization = True):
        self.visualization = visualization
        self.color = {1:'r', -1:'g'}
        if self.visualization:
            self.fig = plt.figure()
            self.ax = self.fig.add_subplot(1,1,1)

    def train(self, data):
        '''定义训练函数'''
        self.data = data
        opt_dict = {} # 参数字典 { ||w||: [w,b] }
        transforms = [[1,1], [-1,1], [-1,-1], [1,-1]] # 数据转换列表
        all_data = [] # 从字典中获取所有数据
        for yi in self.data:
            for featureset in self.data[yi]:
                for feature in featureset:
                    all_data.append(feature) 
        self.max_feature_value = max(all_data)
        self.min_feature_value = min(all_data)

        step_sizes = [self.max_feature_value * 0.1, self.max_feature_value*0.01, self.max_feature_value*0.001] # 定义一个学习率列表
        # 参数 b 的范围设置
        b_range_multiple = 2
        b_multiple = 5
        latest_optimum = self.max_feature_value * 10

        # 基于不同学习率训练优化
        for step in step_sizes:
            w = np.array([latest_optimum, latest_optimum])
            # 凸优化
            optimized = False
            while not optimized:
                for b in np.arange(-1*(self.max_feature_value*b_range_multiple),self.max_feature_value*b_range_multiple,step*b_multiple):
                    for transformation in transforms:
                        w_t = w*transformation
                        found_option = True
                        for i in self.data:
                            for xi in self.data[i]:
                                yi = i
                                if not yi*(np.dot(w_t,xi)+b) >= 1:
                                    found_option = False
                        if found_option:
                            opt_dict[np.linalg.norm(w_t)] = [w_t, b]
                if w[0] < 0:
                    optimized = True
                    print('Optimized a step!')
                else:
                    w = w - step
        
            norms = sorted([n for n in opt_dict])
            opt_choice = opt_dict[norms[0]]
            self.w = opt_choice[0]
            self.b = opt_choice[1]
            latest_optimum = opt_choice[0][0] + step * 2
        
        for i in self.data:
            for xi in self.data[i]:
                yi = i
                print(xi,':',yi*(np.dot(self.w,xi)+self.b))
    
    def predict(self, features):
        classification = np.sign(np.dot(np.array(features),self.w)+self.b)
        if classification != 0 and self.visualization:
            self.ax.scatter(features[0], features[1], s=200, marker = '^', c = self.color[classification])
        return classification

    def visualize(self):
        [[self.ax.scatter(x[0], x[1], s = 100, color = self.color[i]) for x in data_dict[i]] for i in data_dict] # 画出散点图
        def hyperplane(x,w,b,v):
            return (-w[0]*x-b+v) / w[1]

        datarange = (self.min_feature_value*0.9,self.max_feature_value*1.1)
        hyp_x_min = datarange[0]
        hyp_x_max = datarange[1]

        # (w.x+b) = 1
        # 正支持向量
        psv1 = hyperplane(hyp_x_min, self.w, self.b, 1)
        psv2 = hyperplane(hyp_x_max, self.w, self.b, 1)
        self.ax.plot([hyp_x_min,hyp_x_max],[psv1,psv2], 'k')

        # (w.x+b) = -1
        # 负支持向量
        nsv1 = hyperplane(hyp_x_min, self.w, self.b, -1)
        nsv2 = hyperplane(hyp_x_max, self.w, self.b, -1)
        self.ax.plot([hyp_x_min,hyp_x_max],[nsv1,nsv2], 'k')

        # (w.x+b) = 0
        # 线性分隔超平面
        db1 = hyperplane(hyp_x_min, self.w, self.b, 0)
        db2 = hyperplane(hyp_x_max, self.w, self.b, 0)
        self.ax.plot([hyp_x_min,hyp_x_max],[db1,db2], 'y--')

        plt.show()

data_dict = {-1:np.array([[1,7],
                          [2,8],
                          [3,8],]),
             
             1:np.array([[5,1],
                         [6,-1],
                         [7,3],])}

svm = Hard_Margin_SVM()
svm.train(data=data_dict)

predict_us = [[0,10],
              [1,3],
              [3,4],
              [3,5],
              [5,5],
              [5,6],
              [6,-5],
              [5,8],
              [2,5], 
              [8,-3]]

for p in predict_us:
    svm.predict(p)

svm.visualize()