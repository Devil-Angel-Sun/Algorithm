import xlrd

class handle_data:
    def __init__(self,sheet):
        self.table = sheet
        
    def handle_col(self):
        columns = []
        for col in range(self.table.ncols):
            column = self.table.cell_value(rowx = 0, colx = col)
            columns.append(column)
        #print(type(columns))
        return columns
    
    def handle_text(self):
        tables = []
        columns = self.handle_col()
        
        #print(type(columns))
        for row in range(1,self.table.nrows):
            array = {}
            for col in range(len(columns)):
                if self.table.cell_value(row, col):
                    cell_info = self.table.cell_value(row, col)
                    array[columns[col]] = cell_info
                else:
                    pass
            tables.append(array)
        return tables
        
    def handle_final(self):
        columns = self.handle_col()
        tables = self.handle_text()
        return columns,tables
        
if __name__ == '__main__':
    x1 = xlrd.open_workbook('snmp.xlsx')
    sheet1 = x1.sheet_by_name('discovery_rule')
    hd = handle_data(sheet1)
    columns = hd.handle_col()
    print(len(columns))
    tables = hd.handle_text()
    print(len(tables))