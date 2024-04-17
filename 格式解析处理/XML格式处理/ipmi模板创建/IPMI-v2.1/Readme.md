分步运行步骤：

step 1： 运行create_host.py和create_ipmi.py

step 2： 运行push_template.py，将host和ipmi模板推送到zabbix

step 3： 运行get_information.py，将ipmi模板连接到host中，并取得ipmi.get数据，最后删除模板

step 4： 运行create_template.py,将用ipmi.get获取的数据生成模板

step 5： 运行push_template.py，将所有模板都推送到zabbix上

step 6： 运行link_template，将最终模板链接到响应的host上

注意：sensor.py 一般不用，除非有新的类型出现

整体运行步骤：
直接运行main.py文件

``` python
python main.py --excel_path './host.xlsx' --html 'http://192.168.50.100:18080'
```

v1.0 版本是最早期版本，具体识别了item的数值和状态两种情况
v2.0 版本将v1.0中获取到的数据变成了袁术的字典格式的数据输出
v2.1 版本基于v2.0，修改了key值存在的bug，即当获取的id相同时，zabbix只能获取一个值，因此将key中自动获取的id变为自动获取name