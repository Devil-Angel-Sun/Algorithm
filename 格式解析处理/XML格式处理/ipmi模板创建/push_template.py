import os
from pyzabbix import ZabbixAPI
import glob
zapi = ZabbixAPI('http://192.168.50.100:18080')
zapi.login('Admin','zabbix')

rules = {
    'applications': {
        'createMissing': True,
    },
    'discoveryRules': {
        'createMissing': True,
        'updateExisting': True
    },
    'graphs': {
        'createMissing': True,
        'updateExisting': True
    },
    'groups': {
        'createMissing': True
    },
    'hosts': {
        'createMissing': True,
        'updateExisting': True
    },
    'images': {
        'createMissing': True,
        'updateExisting': True
    },
    'items': {
        'createMissing': True,
        'updateExisting': True
    },
    'maps': {
        'createMissing': True,
        'updateExisting': True
    },
    'screens': {
        'createMissing': True,
        'updateExisting': True
    },
    'templateLinkage': {
        'createMissing': True,
    },
    'templates': {
        'createMissing': True,
        'updateExisting': True
    },
    'templateScreens': {
        'createMissing': True,
        'updateExisting': True
    },
    'triggers': {
        'createMissing': True,
        'updateExisting': True
    },
    'valueMaps': {
        'createMissing': True,
        'updateExisting': True
    },
}
path = './templates_xml'
if os.path.isdir(path):
    #file = path/*.xml
    files = glob.glob(path+'/*.xml')
    for file in files:
        print(file)
        with open(file, 'r') as f:
            template = f.read()
            try:
                zapi.confimport('xml', template, rules)
            except ZabbixAPIException as e:
                print(e)
else:
    print('I need a xml file')