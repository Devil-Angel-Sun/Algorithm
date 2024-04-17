import numpy as np
import pandas as pd
import xlrd
from xlrd import xldate_as_tuple

tables = []
def handle_data(table):
    """
    该函数用于将excle表格处理成列表形式，表格的每一行以字典形式存在
    Args:
        table:输入的excel表格,xlsx格式
    return:
        tables：处理完之后的列表形式，每一个列遍元素是以字典形式存在，列表中嵌套字典格式
    """
    for row in range(1,table.nrows):
        array = {}
        array['id'] = table.cell_value(row, 0)
        array['itname'] = table.cell_value(row, 1)
        array['key'] = table.cell_value(row,2)
        if table.cell_value(row,3):
            array['value_type'] = table.cell_value(row,3)
        else:
            pass
        if table.cell_value(row,4):
            array['units'] =  table.cell_value(row,4)
        else:
            pass
        array['description'] = table.cell_value(row,5)
        array['application'] = table.cell_value(row,6)
        tables.append(array)
    return tables

def applications(tables):
    """
    该函数用于处理excel表格中关于application集的唯一值
    Args:
        tables:在handle_data处理过后输出的列表形式的表格，列表中嵌套字典格式
    return:
        applications:excel表格中application集的唯一值，列表格式
    """
    applications = []
    for i in tables:
        applications.append(i['application'])
    #print(list(set(applications)))
    applications = list(set(applications)) #application的唯一值
    return applications
