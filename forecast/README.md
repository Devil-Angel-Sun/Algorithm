# 功能
1. 针对泰隆数据（业务数据、机器性能zabbix数据）开发的趋势预测接口
2. 基于Flask框架的web服务
3. 最终结果写入ElasticSearch
4. 训练数据：业务数据建议6个月的历史数据，机器数据建议3个月的历史数据
5. 需要每年更新节假日

# 环境
1. Linux
2. python==3.7.6
3. fbprophet==0.7.1
4. uwsgi==2.0.19.1
5. elasticsearch==7.8.1
6. Flask==1.1.2

# 安装
1. fbprophet的安装：
   * pip install pystan==2.18#
   * pip install fbprophet
   * pip install plotly
