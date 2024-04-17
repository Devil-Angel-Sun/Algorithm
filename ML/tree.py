humility = ['high','high','high','high','normal','normal','normal','high','normal','normal','normal','high','normal','high']
outlook = ['sunny','sunny','overcast','rainy','rainy','rainy','overcast','sunny','sunny','rainy','sunny','overcast','overcast','rainy']
play = ['no','no','yes','yes','yes','no','yes','no','yes','yes','yes','yes','yes','no']
temp = ['hot','hot','hot','mild','cool','cool','cool','mild','cool','mild','mild','mild','hot','mild']
windy = ['False','True','False','False','False','True','True','False','False','False','True','True','False','True']

import pandas as pd
import numpy as np
import math
data = pd.DataFrame({'humility':humility,'outlook':outlook,'play':play,'temp':temp,'windy':windy})

def entropy(ele):
    """定义熵：entropy = -sum(p*log(p))"""
    probs = [ele.count(i)/len(ele) for i in set(ele)] # 计算值的分布
    print(probs)
    entropy = -np.sum([prob*math.log(prob,2) for prob in probs])
    return entropy
# Example:
entropy(data['play'].tolist())

def spilt_Dataframe(data, col):
    """根据特征和特征值进行数据划分"""
    unique_values = data[col].unique()
    result_dict = {elem:pd.DataFrame for elem in unique_values}
    for key in result_dict.keys():
        result_dict[key] = data[:][data[col]==key]
    return result_dict
# Example:
# spilt_Dataframe(data,'temp')

## 根据熵计算信息增益来选择最佳特征的过程
def choose_best_col(data, label):
    entropy_D = entropy(data[label].tolist())
    cols = [col for col in data.columns if col not in [label]]
    max_value, best_col = -999,None
    max_spilted = None
    
    for col in cols:
        spilted_set = spilt_Dataframe(data, col)
        entropy_DA = 0
        for subset_col, subset in spilted_set.items():
            entropy_D1 = entropy(subset[label].tolist())
            entropy_DA += len(subset)/len(data)*entropy_D1
        info_gain = entropy_D - entropy_DA
        if info_gain > max_value:
            max_value, best_col = info_gain, col
            max_spilted = spilted_set
        return max_value, best_col, max_spilted
# Example:
# choose_best_col(data, 'play')
## 定义ID3
class ID3Tree:
    class Node:
        def __init__(self, name):
            self.name = name
            self.connections = {}

        def connect(self, label, node):
            self.connections[label] = node
        
    def __init__(self, data, label):
        self.columns = data.columns
        self.data = data
        self.label = label
        self.root = self.Node("Root")

    def print_tree(self, node,tabs):
        print(tabs+node.name)
        for connection, child_node in node.connections.items():
            print(tabs + "\t"+"("+connection+")")
            self.print_tree(child_node, tabs+"\t\t")

    def construct_tree(self):
        self.construct(self.root, "",self.data, self.columns)

    def construct(self, parent_node, parent_connection_label, input_data, columns):
        max_value, best_col, max_spilted = choose_best_col(input_data[columns], self.label)
        if not best_col:
            node = self.Node(input_data[self.label].iloc[0])
            parent_node.connect(parent_connection_label, node)
        return

        node = self.Node(best_col)
        parent_node.connect(parent_connection_label, node)

        new_columns = [col for col in columns if col != best_col]
        for spilted_value, spilted_data in max_spilted.items():
            self.construct(node, spilted_value, spilted_data, new_columns)


tree1 = ID3Tree(data, 'play')
tree1.construct_tree()
tree1.print_tree(tree1.root,"") 

### 导入包
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier, export_graphviz
import graphviz
iris = load_iris()
clf = DecisionTreeClassifier(criterion = "entropy",splitter = "best")
clf = clf.fit(iris.data, iris.target)
dot_data = export_graphviz(clf, out_file=None, feature_names=iris.feature_names,class_names=iris.target_names, filled=True, rounded=True, special_characters=True)
graph = graphviz.Source(dot_data)
graph
