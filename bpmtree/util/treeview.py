'''JSON Generator for D3.js'''
from collections import defaultdict
import pandas as pd
from bpmtree.util.treefilepath import BPMFilePath

def dict_to_jstree(dicttree):
    '''Function to convert nested Python defaultdicts to jstree-compatible dicts'''
    result = []
    for key, value in dicttree.items():
        node = {'text': key}
        if isinstance(value, dict):
            node['children'] = dict_to_jstree(value)
        result.append(node)
    return result

def generate_jstree_json(industry):
    '''Function to generate jstree-compatible JSON from CSV'''
    # Load CSV into DataFrame

    bpmfilepath = BPMFilePath(industry)
    filepath = bpmfilepath.get_treefile_location()

    # filepath = f"bpmtreeview/{industry}/businesscontext.csv"
    treedf = pd.read_csv(
        filepath, sep='|', quotechar='"', encoding='utf-8')
    # Convert DataFrame to nested defaultdict
    tree = lambda: defaultdict(tree)
    dicttree = tree()

    for row in treedf.itertuples():
        # dicttree[row[1]][row[2]][row[3]][row[4]][row[5]][row[6]][row[7]][row[8]] = row[8]
        # business_domain|business_domain_desc|business_sub_domain|business_sub_domain_desc|business_capability|business_capability_desc|business_sub_capability|business_sub_capability_desc|combinedbusinesscontext|json
        dicttree[row[1] + " - " + row[2]][row[3] + " - " + row[4]][row[5] + " - " + row[6]][row[7] + " - " + row[7]][row[9] + " - " + row[10]] = row[10]
        # dicttree[row[1]][row[2]][row[3]][row[4]][row[5]][row[6]][row[7]][row[8]] = row[8]

    # Convert defaultdict to jstree JSON
    json_output = dict_to_jstree(dicttree)
    return json_output
