from handle_data import handle_data
import xlrd

class get_excel:
    def __init__(self,excel):
        self.sheet = excel
        
    def handle_excel(self, name):
        x1 = xlrd.open_workbook(self.sheet)
        sheet1 = x1.sheet_by_name(name)
        hd = handle_data(sheet1)
        columns,tables_rule = hd.handle_final()
        return tables_rule
    
    def get_rule(self):
        return self.handle_excel('discovery_rule')
    
    def get_items(self):
        return self.handle_excel('items')

    def get_conditions(self):
        return self.handle_excel('conditions')
    
    def get_item_prototypes(self):
        return self.handle_excel('item_prototypes')
    
    def get_macro(self):
        return self.handle_excel('macro')
    
    def get_value_map(self):
        return self.handle_excel('value_map')
    
if __name__ == '__main__':
    ge = get_excel('snmp.xlsx')
    rule = ge.get_rule()
    items = ge.get_items()
    conditions = ge.get_conditions()
    item_prototypes = ge.get_item_prototypes()
    macro = ge.get_macro()
    value_map = ge.get_value_map()