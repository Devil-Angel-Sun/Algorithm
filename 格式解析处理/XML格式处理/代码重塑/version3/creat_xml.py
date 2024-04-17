import xml.etree.ElementTree as ET
import prettyXml
from get_excel import get_excel
import prettyXml

class create_xml:
    def __init__(self,xml_file,json_data, excel):
        self.sheet = excel
        self.json_data = json_data
        self.xml_file = xml_file

    def get_data(self):
        ge = get_excel(self.sheet)
        rule = ge.get_rule()
        items = ge.get_items()
        conditions = ge.get_conditions()
        item_prototypes = ge.get_item_prototypes()
        macro = ge.get_macro()
        value_map = ge.get_value_map()
        return rule,items,conditions,item_prototypes,macro,value_map
    
    def creat_title(self):
        with open(self.xml_file, 'w') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write('<zabbix_export>\n')
            f.write('</zabbix_export>\n')

        #使用ET模块对xml文件进行解析
        tree = ET.parse(self.xml_file)
        root = tree.getroot()

        # 创建版本标签
        sub_version = ET.SubElement(root,'version')
        sub_version.text = self.json_data['version']
        
        #创建groups标签 -- 模板来自的主机组
        sub_groups = ET.SubElement(root,'groups')
        groups_group = ET.SubElement(sub_groups, 'group')
        group_name = ET.SubElement(groups_group,'name')
        group_name.text = self.json_data['group']
        
        # 模板信息
        sub_templates = ET.SubElement(root,'templates')
        templates_template = ET.SubElement(sub_templates, 'template')
        name = ['template','name','description']
        for i in name:
            template_general = ET.SubElement(templates_template, i)
            template_general.text = self.json_data[i]

        # 模板所属组别
        template_groups = ET.SubElement(templates_template, 'groups')
        groups_group = ET.SubElement(template_groups, 'group')
        group_name = ET.SubElement(groups_group, 'name')
        group_name.text = self.json_data['group']
        
        # 模板的应用集
        template_applications = ET.SubElement(templates_template, 'applications')
        for i in self.json_data['applications']:
            applications_appliaction = ET.SubElement(template_applications, 'application')
            application_name = ET.SubElement(applications_appliaction, 'name')
            application_name.text = i
        self.rule(templates_template)
        self.items(templates_template)
        self.macros(templates_template)
#         self.value_maps(root)
        
        prettyXml.prettyXml(root, '   ', '\n')            #执行美化方法
        #ET.dump(root) 
        print('写入')
        tree.write(self.xml_file) 

    def rule(self,templates_template):
        template_rules = ET.SubElement(templates_template, 'discovery_rules')
        rule,items,conditions,item_prototypes,macro,value_map = self.get_data()
        for i in rule:
            column = list(i.keys())
            rules_rule = ET.SubElement(template_rules, 'discovery_rule')
            #print(column)
            for j in column:
                if j == 'evaltype':
                    rule_filter = ET.SubElement(rules_rule, 'filter')
                    filter_evaltype = ET.SubElement(rule_filter, 'evaltype')
                    filter_evaltype.text = i[j]
                    self.condition(i['name'],rule_filter)
                elif j == 'master_item':
                    rule_master = ET.SubElement(rules_rule, 'master_item')
                    master_key = ET.SubElement(rule_master, 'key')
                    master_key.text = i[j]
                elif j == 'preprocessing':
                    rule_pre = ET.SubElement(rules_rule, 'preprocessing')
                    pre_step = ET.SubElement(rule_pre, 'step')
                    step_type = ET.SubElement(pre_step, 'type')
                    step_type.text = i[j].split(',')[0]
                    type_parems = ET.SubElement(pre_step, 'params')
                    type_parems.text = i[j].split(',')[1]
                    
                else:
                    rule_name = ET.SubElement(rules_rule, j)
                    rule_name.text = i[j]
                    
            self.item_prototypes(i['name'],rules_rule)
            
            
    def condition(self, name, rule_filter):
        rule,items,conditions,item_prototypes,macro,value_map = self.get_data()
        filter_conditions = ET.SubElement(rule_filter, 'conditions')
        for i in conditions:
            if i['TYPE'] == name:
                conditions_condition = ET.SubElement(filter_conditions, 'condition')
                condition_macro = ET.SubElement(conditions_condition, 'macro')
                condition_macro.text = i['macro']
                condition_value = ET.SubElement(conditions_condition, 'value')
                condition_value.text = i['value']
                condition_formulaid = ET.SubElement(conditions_condition, 'formulaid')
                condition_formulaid.text = i['formulaid']
        
    def item_prototypes(self, name, rules_rule):
        rule,items,conditions,item_prototypes,macro,value_map = self.get_data()
        rule_item_prototypes = ET.SubElement(rules_rule, 'item_prototypes')
        for i in item_prototypes:
#             prototypes_prototype = ET.SubElement(rule_item_prototypes, 'item_prototype')
            if i['TYPE'] == name:
                prototypes_prototype = ET.SubElement(rule_item_prototypes, 'item_prototype')
                for j in list(i.keys()):
                    if j in [ 'name', 'type', 'snmp_oid', 'key', 'delay', 'history', 'value_type', 'trends', 'units', 'params', 'description']:
                        prototype_name = ET.SubElement(prototypes_prototype, j)
                        prototype_name.text = i[j]
                    elif j == 'application':
                        prototype_application = ET.SubElement(prototypes_prototype, 'applications')
                        applications_application = ET.SubElement(prototype_application, 'application')
                        application_name = ET.SubElement(applications_application, 'name')
                        application_name.text = i[j]
                    elif j == 'application_prototype':
                        prototype_application_prototypes = ET.SubElement(prototypes_prototype, 'application_prototypes')
                        application_prototypes_application_prototype = ET.SubElement(prototype_application_prototypes, 'application_prototype')
                        application_prototype_name = ET.SubElement(application_prototypes_application_prototype, 'name')
                        application_prototype_name.text = i[j]
                    elif j == 'preprocessing':
                        prototype_preprocessing = ET.SubElement(prototypes_prototype, 'preprocessing')
                        for m in range(3):
                            if i['preprocessing'].split(',')[m]:
                                preprocessing_step = ET.SubElement(prototype_preprocessing, 'step')
                                step_type = ET.SubElement(preprocessing_step, 'type')
                                step_type.text = i['preprocessing'].split(',')[m]
                                step_params = ET.SubElement(preprocessing_step, 'params')
                                step_params.text = i['preprocessing_params'].split(',')[m]
                            else:
                                pass
                    elif j == 'master_item':
                        prototype_master_item = ET.SubElement(prototypes_prototype, 'master_item')
                        master_item_key = ET.SubElement(prototype_master_item, 'key')
                        master_item_key.text = i[j]
#             if i['name']  == 'Interface {#IFNAME}({#IFALIAS}): Operational status':
#                 prototype_valuemap = ET.SubElement(prototypes_prototype, 'valuemap')
#                 valuemap_name = ET.SubElement(prototype_valuemap, 'name')
#                 valuemap_name.text = 'IF-MIB::ifOperStatus'
#             elif i['name'] == 'Interface {#IFNAME}({#IFALIAS}): Interface type':
#                 prototype_valuemap = ET.SubElement(prototypes_prototype, 'valuemap')
#                 valuemap_name = ET.SubElement(prototype_valuemap, 'name')
#                 valuemap_name.text = 'IF-MIB::ifType'                        
                        
    def items(self,templates_template):
        rule,items,conditions,item_prototypes,macro,value_map = self.get_data()
        template_items = ET.SubElement(templates_template, 'items')
        for i in items:
            column = list(i.keys())
            items_item = ET.SubElement(template_items, 'item')
            for j in column:
                if j in ['name', 'type', 'snmp_oid', 'key', 'history', 'value_type', 'units','params']:
                    if i[j]:
                        item_name = ET.SubElement(items_item, j)
                        item_name.text = i[j]
                elif j == 'application':
                    item_applications = ET.SubElement(items_item, 'applications')
                    applications_application = ET.SubElement(item_applications, 'application')
                    application_name = ET.SubElement(applications_application, 'name')
                    application_name.text = i[j]
                elif j == 'preprocessing':
                    if i[j].split(',')[0]:
                        item_preprocessing = ET.SubElement(items_item, 'preprocessing')
                        preprocessing_step1 = ET.SubElement(item_preprocessing, 'step')
                        step1_type = ET.SubElement(preprocessing_step1, 'type')
                        step1_type.text = i[j].split(',')[0]
                        type1_parems = ET.SubElement(preprocessing_step1, 'params')
                        type1_parems.text = i[j].split(',')[1]

    def macros(self,templates_template):
        rule,items,conditions,item_prototypes,macro,value_map = self.get_data()
        template_macros = ET.SubElement(templates_template, 'macros')
        for i in macro:
            macros_macro = ET.SubElement(template_macros, 'macro')
            macro_macro = ET.SubElement(macros_macro, 'macro')
            macro_macro.text = i['macro']
            macro_value = ET.SubElement(macros_macro, 'value')
            macro_value.text = str(i['value'])
        
#     def value_maps(self, root):
#         rule,items,conditions,item_prototypes,macro,value_map = self.get_data()
#         sub_value_maps = ET.SubElement(root, 'value_maps')
#         maps_map = ET.SubElement(sub_value_maps, 'value_map')
#         name = []
#         for i in value_map:
#             name.append(i['name'])
#         map_name = ET.SubElement(maps_map, 'name')
#         map_name.text = list(set(name))[0]
#         name_mappings = ET.SubElement(map_name, 'mappings')
#         for i in value_map:
#             if i['name'] == list(set(name))[0]:
#                 mappings_mapping = ET.SubElement(name_mappings, 'mapping')
#                 mapping_value = ET.SubElement(mappings_mapping, 'value')
#                 mapping_value.text = str(int(i['value']))
#                 mapping_newvalue = ET.SubElement(mappings_mapping, 'newvalue')
#                 mapping_newvalue.text = i['newvalue']
                
#         map_name = ET.SubElement(maps_map, 'name')
#         map_name.text = list(set(name))[1]
#         name_mappings = ET.SubElement(maps_map, 'mappings')
#         for i in value_map:
#             if i['name'] == list(set(name))[1]:
#                 mappings_mapping = ET.SubElement(name_mappings, 'mapping')
#                 mapping_value = ET.SubElement(mappings_mapping, 'value')
#                 mapping_value.text = str(int(i['value']))
#                 mapping_newvalue = ET.SubElement(mappings_mapping, 'newvalue')
#                 mapping_newvalue.text = i['newvalue']
        
                        
                    
        
        
if __name__ == '__main__':
    from general import information
    d = {'version':'5.0','group':'SNMP','name': 'LINUX_SNMP', 'template':'LINUX_SNMP', 'description':'the template of snmp in linux', 'applications':['Network Interface', 'Storage', 'CPU', 'Memory']}
    gi = information(d)
    json_data = gi.final()
    cx = create_xml('xml_file.xml',json_data, 'snmp.xlsx')
   
    cx.creat_title()