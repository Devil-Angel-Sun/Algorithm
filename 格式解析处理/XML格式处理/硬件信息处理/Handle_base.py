import paramiko, json
import pandas as pd
from util import Connect, Handle_format, Trans_json

class Handle_Basic:
    
    def __init__(self, ip, username, password, port = 22):
        self.ip = ip
        self.username = username
        self.password = password
        self.port = port
    
    def get_chassis(self):
        result_out = Connect(self.ip, self.username, self.password, self.port, 'dmidecode -t chassis')
        results = Handle_format(result_out)
        
        information_chassis = {}
        for i in results:
            if i.split(': ')[0] == 'Type':
                information_chassis['Type'] = i.split(': ')[1]
            elif i.split(': ')[0] == 'Serial Number':
                information_chassis['Serial Number'] = i.split(': ')[1]
            elif i.split(': ')[0] == 'Version':
                information_chassis['Version'] = i.split(': ')[1]
            elif i.split(': ')[0] == 'Manufacturer':
                information_chassis['Manufacturer'] = i.split(': ')[1]
        return information_chassis
    
    def get_system(self):
        result_out = Connect(self.ip, self.username, self.password, self.port, 'dmidecode -t system')
        results = Handle_format(result_out)   
        
        information_system = {}
        for i in results:
            if i.split(': ')[0] == 'Type':
                information_system['Type'] = i.split(': ')[1]
            elif i.split(': ')[0] == 'Product Name':
                information_system['Product Name'] = i.split(': ')[1]
            elif i.split(': ')[0] == 'Serial Number':
                information_system['Serial Number'] = i.split(': ')[1]
            elif i.split(': ')[0] == 'Version':
                information_system['Version'] = i.split(': ')[1]
            elif i.split(': ')[0] == 'Manufacturer':
                information_system['Manufacturer'] = i.split(': ')[1]
            elif i.split(': ')[0] == 'Wake-up Type':
                information_system['Wake-up Type'] = i.split(': ')[1]
        return information_system
    
    def get_bios(self):
        result_out = Connect(self.ip, self.username, self.password, self.port, 'dmidecode -t bios')
        results = Handle_format(result_out)   
        
        information_bios = {}
        for i in results:
            if i.split(': ')[0] == 'Version':
                information_bios['Version'] = i.split(': ')[1]
        return information_bios
    
    def gather_information(self):
        information_chassis = self.get_chassis()
        information_system = self.get_system()
        information_bios = self.get_bios()
        results_all = {}
        results_all['Chassis'] = information_chassis
        results_all['System'] = information_system
        results_all['bios'] = information_bios
        Trans_json(results_all, 'basic', self.ip)
            
if __name__ == '__main__':
#     ip = '192.168.50.188'
#     username = 'root'
#     password = 'Dacheng@123'
#     hm = Handle_Basic(ip = ip, username = username, password = password)
#     hm.gather_information()
    data = pd.read_excel('host.xlsx')
    data = data.to_dict(orient = 'index')
    for i in data:
        for j in data[i]:
            hm = Handle_Basic(ip = data[i]['name'].split(': ')[1], username = data[i]['username'], password =  data[i]['shell'])
            hm.gather_information()