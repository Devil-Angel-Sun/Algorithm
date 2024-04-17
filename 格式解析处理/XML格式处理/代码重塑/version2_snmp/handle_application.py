import numpy as np
import pandas as pd
import xlrd

class handle_application:
    
    def __init__(self,tables):
        self.tables = tables
    
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