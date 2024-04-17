import pandas as pd
from xml.dom import minidom

class host:
    def __init__(self, xlsx_file):
        self.data = pd.read_excel(xlsx_file)
        
    def creat_root(self):
        dom = minidom.Document()
        root_node=dom.createElement('zabbix_export')
        dom.appendChild(root_node)

        # 版本号子节点
        version_node = dom.createElement('version')
        root_node.appendChild(version_node)
        version_text = dom.createTextNode('5.0')
        version_node.appendChild(version_text)

        # groups子节点
        groups_node = dom.createElement('groups')
        root_node.appendChild(groups_node)
        for i in set(self.data['group']):
            group_node = dom.createElement('group')
            groups_node.appendChild(group_node)
            groupname_node = dom.createElement('name')
            group_node.appendChild(groupname_node)
            groupname_text = dom.createTextNode(i)
            groupname_node.appendChild(groupname_text)
        # 每一个结点对象（包括dom对象本身）都有输出XML内容的方法，如：toxml()--字符串, toprettyxml()--美化树形格式。

        # hosts子节点
        hosts_node = dom.createElement('hosts')
        root_node.appendChild(hosts_node)
        for index,row in self.data.iterrows():
            host_node = dom.createElement('host')
            hosts_node.appendChild(host_node)
            # host中host节点
            hhost_node = dom.createElement('host')
            host_node.appendChild(hhost_node)
            hhostname_text = dom.createTextNode(row['id'])
            hhost_node.appendChild(hhostname_text)
            # host中name节点
            name_node = dom.createElement('name')
            host_node.appendChild(name_node)
            nname_text = dom.createTextNode(row['id'])
            name_node.appendChild(nname_text)
            # host中templates节点
            templates_node = dom.createElement('templates')
            host_node.appendChild(templates_node)
            template_node = dom.createElement('template')
            templates_node.appendChild(template_node)
            templatename_node = dom.createElement('name')
            template_node.appendChild(templatename_node)
            templatename_text = dom.createTextNode(row['template'])
            templatename_node.appendChild(templatename_text)
            # host中groups节点
            hgroups_node = dom.createElement('groups')
            host_node.appendChild(hgroups_node)
            hgroup_node = dom.createElement('group')
            hgroups_node.appendChild(hgroup_node)
            hgroupname_node = dom.createElement('name')
            hgroup_node.appendChild(hgroupname_node)
            hgroupname_text = dom.createTextNode(row['group'])
            hgroupname_node.appendChild(hgroupname_text)
            # host中interfaces节点

            interfaces_node = dom.createElement('interfaces')
            host_node.appendChild(interfaces_node)

            interface_node = dom.createElement('interface')
            interfaces_node.appendChild(interface_node)

            ip_node = dom.createElement('ip')
            interface_node.appendChild(ip_node)
            ip_text = dom.createTextNode(row['id'])
            ip_node.appendChild(ip_text)

            interface_ref_node = dom.createElement('interface_ref')
            interface_node.appendChild(interface_ref_node)
            interface_ref_text = dom.createTextNode('if1')
            interface_ref_node.appendChild(interface_ref_text)

            if row['zabbix'] == 'SNMP':
                type_node = dom.createElement('type')
                interface_node.appendChild(type_node)
                type_text = dom.createTextNode('SNMP')
                type_node.appendChild(type_text)

                port_node = dom.createElement('port')
                interface_node.appendChild(port_node)
                port_text = dom.createTextNode('161')
                port_node.appendChild(port_text)

                details_node = dom.createElement('details')
                interface_node.appendChild(details_node)
                community_node = dom.createElement('community')
                details_node.appendChild(community_node)
                community_text = dom.createTextNode('{$SNMP_COMMUNITY}')
                community_node.appendChild(community_text)

            if row['template'] == 'huawei_firewall': # 目前只有防火墙需要修改密码
                macros_node = dom.createElement('macros')
                host_node.appendChild(macros_node)
                macro_node = dom.createElement('macro')
                macros_node.appendChild(macro_node)
                mmacro_node = dom.createElement('macro')
                macro_node.appendChild(mmacro_node)
                mmacro_text = dom.createTextNode('{$SNMP_COMMUNITY}')
                mmacro_node.appendChild(mmacro_text)
                value_node = dom.createElement('value')
                macro_node.appendChild(value_node)
                value_text = dom.createTextNode(row['password'])
                value_node.appendChild(value_text)

            inventory_node = dom.createElement('inventory_mode')
            host_node.appendChild(inventory_node)
            inventory_text = dom.createTextNode('DISABLED')
            inventory_node.appendChild(inventory_text)
        return dom
            
    def headle(self):
        dom = self.creat_root()
        try:
            with open('./dom_write.xml','w',encoding='UTF-8') as fh:
                # 4.writexml()第一个参数是目标文件对象，第二个参数是根节点的缩进格式，第三个参数是其他子节点的缩进格式，
                # 第四个参数制定了换行格式，第五个参数制定了xml内容的编码。
                dom.writexml(fh,indent='',addindent='\t',newl='\n',encoding='UTF-8')
                print('写入xml OK!')
        except Exception as err:
            print('错误信息：{0}'.format(err))

if __name__ == '__main__':
    xlsx_file = './host1.xlsx'
    data = host(xlsx_file)
    data.headle()
    