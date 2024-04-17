import paramiko, json
import pandas as pd
from util import Connect, Handle_format, Trans_json, Divide_block

class Handle_Memory:
    
    def __init__(self, ip, username, password, port = 22):
        self.ip = ip
        self.username = username
        self.password = password
        self.port = port
        
    def get_Memory(self):
        result_out = Connect(self.ip, self.username, self.password, self.port, 'dmidecode -t memory')
        results = Handle_format(result_out)
        results_block = Divide_block(results)
        return results_block
    
    def get_blocks(self):
        results_block = self.get_Memory()
        main_memory = []
        for i in results_block:
            if i[1] == 'Physical Memory Array':
                main_memory = i
                results_block.remove(i)
        return main_memory, results_block
        
    def get_single_memory(self):
        main, results_memory = self.get_blocks()
        results_single_memory = []
        for result_memory in results_memory:
            key = 'Size: No Module Installed'
            if key not in result_memory:
        #         print(result_memory)
                result = {}
                for j in result_memory:
                    if j.startswith('Size'):
                        result['Size'] = j.split(':')[1]   # 内存条大小
                    elif j.startswith('Form Factor'):
                        result['Form Factor'] = j.split(': ')[1] # 连接器名称
                    elif j.startswith('Locator'):
                        result['Locator'] = j.split(': ')[1] # 连接器位置
                    elif j.startswith('Type:'):
                        result['Type'] = j.split(': ')[1] # 内存条类型
                    elif j.startswith('Speed'):
                        result['Speed'] = j.split(': ')[1] # 内存条本身速度
                    elif j.startswith('Configured Memory Speed'):
                        result['Configured Memory Speed'] = j.split(': ')[1] # 内存条实际使用速度
                    elif j.startswith('Rank'):
                        result['Rank'] = j.split(': ')[1] # 列数：单列还是双列
                    elif j.startswith('Manufacturer'):
                        result['Manufacturer'] = j.split(': ')[1]  # 厂商
                    elif j.startswith('Serial Number'):
                        result['Serial Number'] = j.split(': ')[1]  # 序列号
                    elif j.startswith('Part Number'):
                        result['Part Number'] = j.split(': ')[1]  # 部件编码
                    elif j.startswith('Total Width'):
                        result['Total Width'] = j.split(': ')[1]  # 位宽
                    elif j.startswith('Type Detail'):
                        result['Type Detail'] = j.split(': ')[1] # 技术
                results_single_memory.append(result) 
        return results_single_memory
    
    def count_memory(self):
        results_single_memory = self.get_single_memory()
        num = []
        for result in results_single_memory:
            if len(result['Size'].split(' ')) == 3:
                num.append(int(result['Size'].split(' ')[1]))
                unit = result['Size'].split(' ')[2]
            elif len(result['Size'].split(' ')) == 2:
                num.append(int(result['Size'].split(' ')[0]))
                unit = result['Size'].split(' ')[1]
        total = 0  
        for ele in range(0, len(num)):
            total = total + num[ele]
        total = '{} {}'.format(total, unit)
        return total
    
    def get_physical_memory(self):
        main,results_memory = self.get_blocks()
        total_num = self.count_memory()
        result_physical_memory = {}
        for i in main:
            if i.startswith('Location'):
                result_physical_memory['Location'] = i.split(': ')[1]    # 获取所在位置
            elif i.startswith('Maximum Capacity'):
                result_physical_memory['Max Capacity'] = i.split(':')[1] # 最大容量
            elif i.startswith('Number Of Devices'):
                result_physical_memory['Num Device'] = i.split(': ')[1]  # 可用插槽数
        total = self.count_memory()
        result_physical_memory['Actual Num Device'] = total_num
        return result_physical_memory
    
    def gather_information(self):
        result_physical_memory = self.get_physical_memory()
        results_single_memory = self.get_single_memory()
        results_all = {}
        results_all['Physical Memory'] = result_physical_memory
        for i in results_single_memory:
            results_all['Single Memory {}'.format(i['Locator'])] = i
        Trans_json(results_all, 'Memory', self.ip)
    
if __name__ == '__main__':
#     ip = '192.168.50.188'
#     username = 'root'
#     password = 'Dacheng@123'
#     hm = Handle_Memory(ip = ip, username = username, password = password)
#     hm.gather_information()
    data = pd.read_excel('host.xlsx')
    data = data.to_dict(orient = 'index')
    for i in data:
        for j in data[i]:
            hm = Handle_Memory(ip = data[i]['name'].split(': ')[1], username = data[i]['username'], password =  data[i]['shell'])
            hm.gather_information()
    