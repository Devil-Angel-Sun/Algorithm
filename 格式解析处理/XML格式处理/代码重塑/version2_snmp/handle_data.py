import numpy as np
import pandas as pd
import xlrd

class handle_data:
    
    def __init__(self,table):
        self.table = table
        
        
    def handle_data(table):
        """
        该函数用于将excle表格处理成列表形式，表格的每一行以字典形式存在
        Args:
            table:输入的excel表格,xlsx格式
        return:
            tables：处理完之后的列表形式，每一个列遍元素是以字典形式存在，列表中嵌套字典格式
        """
        tables = []
        columns = []
        for col in range(table.ncols):  
            column = table.cell_value(rowx=0, colx=col)
            columns.append(column)
        print(columns)

        for row in range(1,table.nrows):
            array = {}
            for col in range(len(columns)):
                if table.cell_value(row,col):
                    cell_info = table.cell_value(row,col)
                    array[columns[col]] = cell_info
                else:
                    pass    
            tables.append(array)
        return tables




