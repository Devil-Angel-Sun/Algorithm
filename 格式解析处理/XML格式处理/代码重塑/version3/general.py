import json

### 书写一些普遍的信息
class information():
    '''
    输入模板的基本信息
    Arg:
        data:待处理的基本信息，字典格式
            主要涉及：zabbix版本,模板的名字两种名字，模板的描述，所属的模板组别，以及应用集
    return:
        general_information.json:在当前目录下输出json格式的文件
    '''
    def __init__(self,data):
        self.data = data

    def write_json(self):
        with open('general_information.json', 'w') as wf:
            json.dump(self.data,wf)
        print('data写入数据成功')
        print('---------------')

    def read_json(self):
        with open('general_information.json', 'r') as rf:
            data = json.load(rf)
        return data

    def translate_json(self):
        try:
            return json.dumps(self.data, separators = [',', ':'], sort_keys = True)
        except Exception as e:
            print(e)
        return None
    
    def final(self):
        data = self.translate_json()
        if data:
            self.write_json()
            read_data = self.read_json()
            print('读取的数据：')
            print(read_data)
        return read_data
            
if __name__ == '__main__':
    d = {'template':'LINUX_SNMP', 'description':'the template of snmp in linux', 'applications':['name', 'Network Interface', 'Storage', 'CPU', 'Memory']}
    infor = information(d)
    data = infor.translate_json()

    if data:
        infor.write_json()
        read_data = infor.read_json()
        print('读取的数据：')
        print(read_data)
