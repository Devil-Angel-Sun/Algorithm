输入的内容有三样：

inFile：数据集输入，迭代器
minSupport：最小支持度阈值，作者推荐：0.1-0.2之间
minConfidence：最小置信度阈值，作者推荐：0.5-0.7之间

输出内容两样：

items ，支持度表，形式为：(tuple, support)，一个词的支持度、一对词的支持度【无指向】
rules ，置信度表，形式为((pretuple, posttuple), confidence)，（起点词，终点词），置信度【有指向】

想法：
1.针对单个用户在每一秒内的操作类型进行关联分析

时间  操作类型
      S,S,S,S