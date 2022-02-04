import json
import re
import os
import datetime
from config import Config
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import re
import datetime as dt
from file_access import FileAccess
from status_tracker import StatusTracker


class XbrlUiGenerator:

    def get_label(self, key):
        post_fixes = ['_.*_terseLabel_en-US', '_.*_label_en-US', '_.*_label', '']
        for item in post_fixes:
            key1 = f'lab_{key.replace(":", "_")}{item}'
            node = self.data_for_lab.find("link:linkbase").find("link:labelLink").find("link:label", id=re.compile(key1, re.IGNORECASE | re.MULTILINE))
            if node is not None:
                break
            
        return node.text if node is not None else ""

    def generate(self, ticker, year, quarter, doc_type, data_val, data_lab, data_pre, data_calc, data_schema, force=False):

        file_access = FileAccess()
        file_name_postfix = Config.file_prefix(ticker, year, quarter)
        ui_file_name = f'final_ui_{file_name_postfix}.json'
        ui_file_s3_key = Config.get_s3_path(ticker, year, quarter, doc_type, ui_file_name)
        
        if (not force and file_access.file_exists(bucket_name=Config.XBRL_STAGING_BUCKET_NAME, file_path=ui_file_s3_key)):
            return

        pre_path = f'{Config.ROOT_INPUT_DIR}\\pre_{Config.file_prefix(ticker, year, quarter)}.xml'

        self.data_for_pre = BeautifulSoup(data_pre, "xml")
        self.data_for_calc = BeautifulSoup(data_calc, "xml")
        self.data_for_schema = BeautifulSoup(data_schema, "xml")
        self.data_for_lab = BeautifulSoup(data_lab, "xml")
        self.data_for_unit_value = BeautifulSoup(data_val, "xml")

        result = { 'header': { 'ticker': ticker, 'year': year, 'quarter': quarter },  'data': [ { 'roleUri': '', 'terse_label': '', 
            'label_id': '', 'weight': "1", 'periodType': '', 'balance': '', 'items': [] } ] }
        pres_links = self.data_for_pre.findAll('link:presentationLink')
        for pre_link in pres_links:
            calc_link = self.data_for_calc.find("link:calculationLink", { 'xlink:role' : re.compile(pre_link['xlink:role']) })
            all_loc_items = []
            for loc_item in pre_link.findAll('link:loc'):
                label_key = self.get_label_key(loc_item['xlink:label'])
                label = self.get_label(label_key)
                new_item = { 'roleUri': pre_link['xlink:role'], 'terse_label': label, 'label_id': loc_item['xlink:label'], 'order': 0, 'weight': "1",
                    'periodType': '', 'balance': '', 'items': [] }
                element_node = self.data_for_schema.find("xs:schema").find("xs:element", id=label_key)
                if element_node is not None:
                    new_item['periodType'] = element_node['xbrli:periodType'] if element_node.has_attr('xbrli:periodType') else ''
                    new_item['balance'] = element_node['xbrli:balance'] if element_node.has_attr('xbrli:balance') else ''
                all_loc_items.append(new_item)
            
            for pres_arc in pre_link.findAll('link:presentationArc'):
                parent_loc = list(filter(lambda i: i['label_id'] == pres_arc['xlink:from'], all_loc_items))
                child_loc = list(filter(lambda i: i['label_id'] == pres_arc['xlink:to'], all_loc_items))
                if len(parent_loc) > 0 and len(child_loc) > 0:
                    from_label = self.get_label_key(pres_arc['xlink:from'])
                    to_label = self.get_label_key(pres_arc['xlink:to'])
                    from_label = from_label.replace("Abstract", "")
                    to_label = to_label.replace("Abstract", "")
                    calc_node = calc_link.find("link:calculationArc", { 'xlink:to': re.compile(f'.*{to_label}.*', re.IGNORECASE) })
                    if pre_link['xlink:role'] == "http://www.lumentum.com/role/CONDENSEDCONSOLIDATEDSTATEMENTSOFCASHFLOWS":
                        pass
                    if(calc_node is not None):
                        child_loc[0]['weight'] = calc_node['weight']

                    child_loc[0]['order'] = pres_arc['order']
                    parent_loc[0]['items'].append(child_loc[0])
                else:
                    raise Exception("boom")

            for item in all_loc_items:
                if 'order' not in item or item['order'] == 0:
                    result['data'].append(item)

        ui_complete_path = file_access.put_file(bucket_name=Config.XBRL_STAGING_BUCKET_NAME, ticker=ticker, year=year, quarter=quarter,
            doc_type=doc_type, file_name=ui_file_name, content=json.dumps(result, indent=4))

        status_tracker = StatusTracker()
        status_tracker.update_row(ticker=ticker, year=year, quarter=quarter, document_type=doc_type, 
            data={ 'xbrl_presentation_file_path': ui_complete_path })
        

    def get_label_key(self, link_label):
        label_parts = link_label.split("_")
        label_key = label_parts[1] + "_" + label_parts[2]
        return label_key

if __name__ == "__main__":
    parser = XbrlUiGenerator()

    parser.generate(ticker="LITE", year=2020, quarter="Q3")
    
    
