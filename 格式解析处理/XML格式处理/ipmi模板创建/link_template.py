from pyzabbix import ZabbixAPI
from get_information import Get_message
import sched, time, os,json, glob, re
import pandas as pd

zapi = ZabbixAPI('http://192.168.50.100:18080')
zapi.login('Admin','zabbix')

# 判断是否为所需要的模板，存储在files_list中
files = glob.glob('./templates_xml/*.xml')
files_list =[]
for i in files:
    if re.compile('^[0-9]{1}.*$').match(i.split('/')[-1]): # 判断是否以数字开头
        files_list.append(i)


# def get_template_id(file):
#     '''获取所有模板的id和名字信息,并取出所需模板的templateid'''
#     template_list = zapi.template.get(output=["templateid","name"])
#     name = 'Template' + file.split('/')[-1].split('.')[0]+' of IPMI'
#     return int([i['templateid'] for i in template_list if i['name'] == name][0])

# 获取主机Id
excel_path = './host.xlsx'
gm = Get_message(excel_path = excel_path)
host_ids = gm.get_hosts_id()

def get_template_id(template):
    '''获取所有模板的id和名字信息,并取出所需模板的templateid'''
    template_list = zapi.template.get(output=["templateid","name"])
    name = 'Template ' + template.split('/')[-1].split('.xml')[0]+' of IPMI'
    return int([i['templateid'] for i in template_list if i['name'] == name][0])

for templateid in files_list:
    for hostid in host_ids:
        if templateid.split('/')[-1].split('.xml')[0].split('_')[1] == host_ids[hostid]:
            zapi.template.massadd(templates = get_template_id(templateid), hosts={"hostid": hostid})