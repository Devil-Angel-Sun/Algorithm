import xlrd 
from handle_data import handle_data
from handle_application import handle_application
import handle_xml

def xml(xlsx_file,i,xml_file, infomations):
    #这里的基础都是xlsx表格

    data1 = xlrd.open_workbook(xlsx_file)
    table = data1.sheets()[i] #目前只支持i=3，因为xlsx前两个表格中不存在type字段
    new_tables = handle_data.handle_data(table)
    applications = handle_application.applications(new_tables)
    
    #xml_file = 'snmp_file.xml'
    handle_xml.create_xml(xml_file,new_tables, applications, infomations)