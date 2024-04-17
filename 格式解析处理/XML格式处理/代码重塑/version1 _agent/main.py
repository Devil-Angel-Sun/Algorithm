import numpy as np
import pandas as pd
import xlrd
from xlrd import xldate_as_tuple
import handle_data
import handle_xml

def xml(xlsx_file,i,xml_file, infomations):
    #这里的基础都是xlsx表格
    data1 = xlrd.open_workbook(xlsx_file)
    table = data1.sheets()[i]
    new_tables = handle_data.handle_data(table)
    applications = handle_data.applications(new_tables)
    
    xml_file = xml_file
    handle_xml.create_xml(xml_file,new_tables, applications, infomations)