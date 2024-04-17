import json
import xlrd


class get_excel:
    def __init__(self,excel):
        self.sheet = excel
    
    def achieve_data(self):
        try:
            data = xlrd.open_workbook(self.sheet)
            return data
        except Exception as e:
            print("excel表格读取失败：%s" % self)
            return None
    
    def get_sheets_name(self):
        data = self.achieve_data()
        return data.sheet_names()
        
    def handle_excel(self):
        data = self.achieve_data() #获取表格
        sheet_names = self.get_sheets_name() # 获取表名
        results = {} 
        for i in sheet_names: 
            i_data = data.sheet_by_name(i)
            i_title = i_data.row_values(0)
            tmp = []
            for row in range(1,i_data.nrows):
                row_name = i_data.row_values(row)
                #print(row_name)
                array = {}
                for col in range(len(row_name)):
                    if i_data.cell_value(row,col):
                        if i_data.row_values(row) == 'value':
                            cell_info = i_data.cell_value(row, col)
                            array[row_name[col]] = self.translate(cell_info)
                            print(translate(cell_info))
                        else:
                            cell_info = i_data.cell_value(row, col)
                            array[i_title[col]] = cell_info
                    else:
                        pass
                tmp.append(array)
            results[i] = tmp
        return results
    
    def comparison(self, data, row, str_name):
        '''data: 当前表的数据 row: 当前表的某一个行名 str_name: 需要匹配的字符'''
        if row == str_name:
            value = data.cell_value(row,col)
            value = self.translate(value)
        else:
            value = value
        return value            
    
    def translate(self, value):
        if isinstance(value,float):
            value = str(int(value))
        if value == 0:
            value = str(0)
        return value
    
#     def read_json(self):
#         with open('general_information.json', 'r') as rf:
#             data = json.load(rf)
#         return data

    def write_json(self):
        with open('data_json.json','w') as f:
            json.dump(self.handle_excel(),f)
        print('data写入数据成功')
        print('---------------')
        
    
if __name__ == '__main__':
    ge = get_excel('SNMP.xlsx')
    ge.write_json()