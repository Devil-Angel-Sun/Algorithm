import xml.etree.ElementTree as ET

def create_xml(xml_file, tables, applications, infomation):
    """
    将excel表格中的内容处理成xml格式
    Args:
        xml_file: 待输出的xml文件名，一个空的xml格式
        tables:需要转为xml格式的表格，列表嵌套字典格式
        applications:唯一值的application集，列表格式
        infomation:基础信息，包含version,主机组名称，模板信息等，列表格式
        
    Return:
        
    """
    with open(xml_file, 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<zabbix_export>\n')
        f.write('</zabbix_export>\n')
    
    #使用ET模块对xml文件进行解析
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # 创建版本标签
    sub_version = ET.SubElement(root,'version')
    sub_version.text = infomation[0]
    
    #创建groups标签 -- 模板来自的主机组
    sub_groups = ET.SubElement(root,'groups')
    groups_group = ET.SubElement(sub_groups, 'group')
    group_name = ET.SubElement(groups_group,'name')
    group_name.text = infomation[1]
    
    # 创建模板
    sub_templates = ET.SubElement(root,'templates')
    templates_templete = ET.SubElement(sub_templates, 'template')
    template_templete = ET.SubElement(templates_templete, 'template')
    template_templete.text = infomation[2] # 输入模板名称
    template_name = ET.SubElement(templates_templete, 'name')
    template_name.text = infomation[3] #输入模板的可见的名称
    template_description = ET.SubElement(templates_templete, 'description')
    template_description.text = infomation[4] # 输入模板的描述
    
    #创建模板中的元素 -- group
    templates_groups = ET.SubElement(templates_templete, 'groups')
    groups_group = ET.SubElement(templates_groups, 'group')
    group_name = ET.SubElement(groups_group, 'name')
    group_name.text = 'Templates'
    
    # 创建模板中的元素 -- application
    templates_applications = ET.SubElement(templates_templete, 'applications')
    for i in applications:
        application_application = ET.SubElement(templates_applications, 'application')
        application_name = ET.SubElement(application_application, 'name')
        application_name.text = i   # 这里只需要修改文本即可
        
    
    # 创建模板中的元素 -- items
    templiates_items = ET.SubElement(templates_templete, 'items')
    for i in tables:
        items_item = ET.SubElement(templiates_items, 'item')
        item_name = ET.SubElement(items_item, 'name')
        item_name.text = i['itname']   # itname
        item_key = ET.SubElement(items_item, 'key')
        item_key.text = i['key']    # key_
        if 'value_type' in i.keys():
            item_value_type = ET.SubElement(items_item, 'value_type')
            item_value_type.text = i['value_type']  # 数值类型
        else:
            pass
        if 'units' in i.keys():
            item_units = ET.SubElement(items_item, 'units')
            item_units.text = i['units'] # 数值单位
        else:
            pass
        item_description = ET.SubElement(items_item, 'description')
        item_description.text = i['description'] #描述
        item_applications = ET.SubElement(items_item, 'applications')
        applications_application = ET.SubElement(item_applications, 'application')
        application_name = ET.SubElement(applications_application, 'name')
        application_name.text = i['application']   # 应用集    

    #sub_value_maps = ET.SubElement(root,'value_maps')
    
    #上面创建的内容都在一行上面显示，不利于我们的查看，对标签执行美化，标签前面添加是的的缩进
    prettyXml(root, '   ', '\n')            #执行美化方法
    #ET.dump(root)                 #显示出美化后的XML内容

    tree.write(xml_file)                   #将修改写入本地xml文件
    
def prettyXml(element, indent, newline, level = 0): 
    """
    对标签执行美化，为标签添加缩进
    Args:
        element:craet_xml中的Elment类
        indent:用于缩进
        newline:用于换行
        level:
        
    """
    # 判断element是否有子元素
    if element:  
        if element.text == None or element.text.isspace(): # 如果element的text没有内容
            element.text = newline + indent * (level + 1)
        else:
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)

    # 将elemnt转成list
    temp = list(element) 
    for subelement in temp:
        if temp.index(subelement) < (len(temp) - 1): # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致
            subelement.tail = newline + indent * (level + 1)
        else:  # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个
            subelement.tail = newline + indent * level
        prettyXml(subelement, indent, newline, level = level + 1) # 对子元素进行递归操作



       