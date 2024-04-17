import paramiko, json
import pandas as pd
from util import Connect, Handle_format, Trans_json, Divide_block

class Handle_Processor:
    
    def __init__(self, ip, username, password, port = 22):
        self.ip = ip
        self.username = username
        self.password = password
        self.port = port
        
    def get_Processor(self):
        result_out = Connect(self.ip, self.username, self.password, self.port, 'dmidecode -t processor')
        results = Handle_format(result_out)
        results_block = Divide_block(results)
        return results_block
    
    def get_singlecpu(self):
        blocks = self.get_Processor()
        results = []
        for block in blocks:
            result = {}
            for j in block:
                if j.split(': ')[0] == 'Socket Designation':
                    result['Socket Designation'] = j.split(': ')[1]   
                elif j.split(': ')[0] == 'Type':
                    result['Type'] = j.split(': ')[1] 
                elif j.split(': ')[0] == 'Family':
                    result['Family'] = j.split(': ')[1] 
                elif j.split(': ')[0] == 'Manufacturer':
                    result['Manufacturer'] = j.split(': ')[1]  #厂商 
                elif j.split(': ')[0] == 'Serial Number':
                    result['Serial Number'] = j.split(': ')[1] 
                elif j.split(': ')[0] == 'Part Number':
                    result['Part Number'] = j.split(': ')[1]
                elif j.split(': ')[0] == 'Version':
                    result['Version'] = j.split(': ')[1]
                elif j.split(': ')[0] == 'Max Speed':
                    result['Max Speed'] = j.split(': ')[1]
                elif j.split(': ')[0] == 'Current Speed':
                    result['Current Speed'] = j.split(': ')[1] 
                elif j.split(': ')[0] == 'Status':
                    result['Status'] = j.split(': ')[1] 
                elif j.split(': ')[0] == 'External Clock':
                    result['External Clock'] = j.split(': ')[1] 
                elif j.split(': ')[0] == 'Core Count':
                    result['Core Count'] = j.split(': ')[1] 
                elif j.split(': ')[0] == 'Core Enabled':
                    result['Core Enabled'] = j.split(': ')[1] 
                elif j.split(': ')[0] == 'Thread Count':
                    result['Thread Count'] = j.split(': ')[1] 
                elif j.split(': ')[0] == 'ID':
                    result['ID'] = j.split(': ')[1] # 处理器ID
            results.append(result)
        return results 
    
    def gather_information(self):
        results_singlecpu = self.get_singlecpu()
        results_all = {}
        for i in results_singlecpu:
            results_all['Single Processer {}'.format(i['Socket Designation'])] = i
        Trans_json(results_all, 'Processor', self.ip)
        
if __name__ == '__main__':
#     ip = '192.168.50.188'
#     username = 'root'
#     password = 'Dacheng@123'
#     hm = Handle_Processor(ip = ip, username = username, password = password)
#     hm.gather_information()
    data = pd.read_excel('host.xlsx')
    data = data.to_dict(orient = 'index')
    for i in data:
        for j in data[i]:
            hm = Handle_Processor(ip = data[i]['name'].split(': ')[1], username = data[i]['username'], password =  data[i]['shell'])
            hm.gather_information()
        