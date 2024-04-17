import xml.dom.minidom as xmldom
import pandas as pd

class multi_resolve:
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
        root = self.get_root()
        items = root.getElementsByTagName('item')
        items_item = []
        for item in items:
            if item.parentNode.nodeName == 'items':
                items_item.append(item)
        
        items_information = []
        for item in items_item:
            information = {}
            for i in item.childNodes:
                if i.nodeName == 'name':
                    information['itemname'] = i.firstChild.data
                elif i.nodeName == 'key':
                    information['key'] = i.firstChild.data
                elif i.nodeName == 'value_type':
                    if i.firstChild:
                        information['value_type'] = i.firstChild.data
                elif i.nodeName == 'units':
                    if i.firstChild:
                        information['units'] = i.firstChild.data
                elif i.nodeName == 'applications':
                    if i.firstChild:
                        information['application'] = i.childNodes[1].childNodes[1].firstChild.data
            items_information.append(information)
        return items_information
    
    def get_lld(self):
        root = self.get_root()
        item_prototype = root.getElementsByTagName('item_prototype')
        item_prototypes = []
        for item in item_prototype:
            if item.parentNode.nodeName == 'item_prototypes':
                item_prototypes.append(item)
                
        item_prototypes_information = []
        for item in item_prototypes:
            information = {}
            for i in item.childNodes:
                if i.nodeName == 'name':
                    information['itemname'] = i.firstChild.data
                elif i.nodeName == 'key':
                    information['key'] = i.firstChild.data
                elif i.nodeName == 'value_type':
                    if i.firstChild:
                        information['value_type'] = i.firstChild.data
                elif i.nodeName == 'units':
                    if i.firstChild:
                        information['units'] = i.firstChild.data
                elif i.nodeName == 'applications':
                    if i.firstChild:
                        information['application'] = i.childNodes[1].childNodes[1].firstChild.data
            item_prototypes_information.append(information)
        return item_prototypes_information
    
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
    file = './linux_snmp_common.xml'
    data = multi_resolve(file)
    informations = data.transform_dataframe()
                
