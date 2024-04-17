import xml.dom.minidom as xmldom
import pandas as pd

class simple_zabbix:
    def __init__(self, file):
        self.file = file
        
    def read_xml(self):
        # 得到文档对象
        doc = xmldom.parse(self.file)
        return doc
    
    def get_root(self):
        # 得到根对象
        doc = self.read_xml()
        root = doc.documentElement
        return root
    
    def get_items(self):
        informations_items = []
        root = self.get_root()
        item_template = root.getElementsByTagName('item')
        # 针对items项
        for item in item_template:
            if item.parentNode.nodeName == 'items':
                item_infomation = {}
                for child in item.childNodes:
                    if child.nodeName == 'name':
                        item_infomation['itemname'] = child.firstChild.data
                    elif child.nodeName == 'key':
                        item_infomation['key'] = child.firstChild.data
                    elif child.nodeName == 'applications':
                        if child.firstChild:
                            item_infomation['application'] = child.childNodes[1].childNodes[1].firstChild.data   
                informations_items.append(item_infomation)
        return informations_items
    
    def get_lld(self):
        # 针对lld项
        informations_lld = []
        root = self.get_root()
        lld_template = root.getElementsByTagName('discovery_rule')
        for lld in lld_template:
            if lld.parentNode.nodeName == 'discovery_rules':
                lld_information = {}
                for child in lld.childNodes:
                    if child.nodeName == 'name':
                        lld_information['discovery_rule'] = child.firstChild.data
                    elif child.nodeName == 'item_prototypes':
                        prototypes = child.childNodes[1].childNodes
                        for prototype in prototypes:
                            if prototype.nodeName == 'name':
                                lld_information['itemname'] = prototype.firstChild.data
                            elif prototype.nodeName == 'key':
                                lld_information['key'] = prototype.firstChild.data
                            elif prototype.nodeName == 'applications':
                                if child.firstChild:
                                    lld_information['application'] = prototype.childNodes[1].childNodes[1].firstChild.data 
                informations_lld.append(lld_information)
        return informations_lld
    
    def get_allitems(self):
        informations_items = self.get_items()
        informations_lld = self.get_lld()
        for i in informations_lld:
            informations_items.append(i)
        return informations_items
    
    def transform_dataframe(self):
        informations = self.get_allitems()
        data = pd.DataFrame(informations)
        return data
    
if __name__ == '__main__':
    file = './Template OS HP-UX_3.0.0.xml'
    data = simple_zabbix(file)
    informations = data.transform_dataframe()
                

    