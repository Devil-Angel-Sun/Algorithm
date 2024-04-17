from zabbix单模板解析 import simple_zabbix
import pandas as pd

class check_items:
    def __init__(self, file_total,file_simple,Module):
        self.file_total = file_total
        self.file_simple = file_simple
        self.Module = Module
        
    def get_data(self):
        data = pd.read_excel(self.file_total, sheet_name = '所有item项')
        return data
        
    def get_informations(self):
        infor_data = simple_zabbix(self.file_simple)
        informations = infor_data.transform_dataframe()
        return informations
    
    def eq(self):
        df = pd.DataFrame()
        informations = self.get_informations()
        data = self.get_data()
        new_data = data[data['Module'] == self.Module]
        for i in informations['key']:
            if i  not in list(new_data['key']):
                pd.set_option('Display.max_rows',None)
                pd.set_option('max_colwidth',100)
                df = informations[informations['key'] == i]
        return df
    
if __name__ == '__main__':
    file_simple = './Template OS HP-UX_3.0.0.xml'
    file_total = './国网指标体系.xlsx'
    data = check_items(file_total,file_simple,'HPUnix')
    data.eq()