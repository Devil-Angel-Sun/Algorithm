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
        result_out = Connect(self.ip, self.username, self.password, self.port, 'dmidecode -t connector')
        results = Handle_format(result_out)
        results_block = Divide_block(results)
        return results_block
    
    def get_singleconnector(self):
        blocks = self.get_Processor()
        results = []
        for block in blocks:
            result = {}
            for j in block:
                if j.split(': ')[0] == 'Internal Reference Designator':
                    result['Internal Reference Designator'] = j.split(': ')[1]   
                elif j.split(': ')[0] == 'Internal Connector Type':
                    result['Internal Connector Type'] = j.split(': ')[1] 
                elif j.split(': ')[0] == 'External Reference Designator':
                    result['External Reference Designator'] = j.split(': ')[1] 
                elif j.split(': ')[0] == 'External Connector Type':
                    result['External Connector Type'] = j.split(': ')[1]  #厂商 
                elif j.split(': ')[0] == 'Port Type':
                    result['Port Type'] = j.split(': ')[1] 
            results.append(result)
        return results 
    
    def gather_information(self):
        results_singleconnector = self.get_singleconnector()
        results_all = {}
        for i in results_singleconnector:
            results_all['Single Connector {}'.format(i['Port Type']+i['External Reference Designator'])] = i
        Trans_json(results_all, 'Connector', self.ip)
        
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
    
        