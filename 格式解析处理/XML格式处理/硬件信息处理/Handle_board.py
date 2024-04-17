import paramiko, json
import pandas as pd
from util import Connect, Handle_format, Trans_json, Divide_block

class Handle_Board:
    
    def __init__(self, ip, username, password, port = 22):
        self.ip = ip
        self.username = username
        self.password = password
        self.port = port
        
    def get_Board(self):
        result_out = Connect(self.ip, self.username, self.password, self.port, 'dmidecode -t baseboard')
        results = Handle_format(result_out)
        results_block = Divide_block(results)
        return results_block
    
    def get_mainboard(self):
        results_block = self.get_Board()
        main_board = []
        for i in results_block:
            if i[1] == 'Base Board Information':
                main_board = i
                results_block.remove(i)
        
        information_system = {}
        for i in main_board:
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
            elif i.split(': ')[0] == 'Product Name':
                information_system['Product Name'] = i.split(': ')[1]
        return information_system, results_block
    
    def get_singleboard(self):
        mainboard,blocks = self.get_mainboard()
        results = []
        for block in blocks:
            result = {}
            for j in block:
                if j.split(': ')[0] == 'Reference Designation':
                    result['Reference Designation'] = j.split(': ')[1]   
#                 elif j.split(': ')[0] == 'Type':
#                     result['Type'] = j.split(': ')[1] 
                elif j.split(': ')[0] == 'Status':
                    result['Status'] = j.split(': ')[1] 
                elif j.split(': ')[0] == 'Type:':
                    result['Type'] = j.split(': ')[1] 
                elif j.split(': ')[0] == 'Type Instance':
                    result['Type Instance'] = j.split(': ')[1] 
            results.append(result)
        return results 
    
    def gather_information(self):
        result_mainboard, block = self.get_mainboard()
        results_singleboard = self.get_singleboard()
        results_all = {}
        results_all['Main Board'] = result_mainboard
        for i in results_singleboard:
            results_all['Single Board {}'.format(i['Reference Designation'])] = i
        Trans_json(results_all, 'Board', self.ip)
        
if __name__ == '__main__':
#     ip = '192.168.50.188'
#     username = 'root'
#     password = 'Dacheng@123'
#     hm = Handle_Board(ip = ip, username = username, password = password)
#     hm.gather_information()
    data = pd.read_excel('host.xlsx')
    data = data.to_dict(orient = 'index')
    for i in data:
        for j in data[i]:
            hm = Handle_Board(ip = data[i]['name'].split(': ')[1], username = data[i]['username'], password =  data[i]['shell'])
            hm.gather_information()
    
    