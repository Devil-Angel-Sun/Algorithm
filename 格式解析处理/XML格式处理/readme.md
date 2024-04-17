# 2021.1.5 version1 agent
此版本对item只增加了item_name,key,description,value_type,units,application（详见zabbix_system.xlsx)
此版本所导出的xml格式包含了版本号，模板名称，主机群组等信息

需要改进之处：
1. mapping映射，有些数据是0，1值，是"是与否"的关系
2. triggers触发器设置
3. 图形设置
4. 单位设置 例如units若为B，那么1024B = 1KB，会自动换算；如果在units为!B，那么1024B = 1024B，不会自动换算

# 2021.1.8 version2 snmp
此版本对item增加了type的判断，以此来添加由于type不同而产生的一些新的指标

需要改进之处：
将handle_xml封装成类

# 单模板解析
主要用于匹配来自对方公司的模板与官网模板之间指标的异同

# 多模板解析
主要针对zabbix中导出的模板的所需要的信息

# 国网模板解析
主要针对国网的zabbix指标进行解析

# 模板创建
主要创建个性化模板