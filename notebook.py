import statistics
from js import fileName, fileText


def find_table(tables, row_name="", col_name=""):
    """ Find the table that contains the row that we are looking for
    """
    for table in tables:
        if table.find_all(string=re.compile(row_name))or row_name == "":
            if table.find_all(string=re.compile(col_name)) or col_name == "":
                return table
    
    return
        
def get_value(table, row_name='', col_name=''):
    """ Parse the table and get the value of column <col_name> and row <row_name>
    """
    header = table.findChildren(['th'])
    rows = table.findChildren(['tr'])

    col_idx = -1
    
    for c, col in enumerate(header):
        if col.string and re.search(col_name, col.string):
            col_idx = c
            break

    if col_idx >= 0:
        for row in rows:
            cells = row.findChildren('td')
            for cell in cells:
                if cell.string and re.search(row_name, cell.string):
                    return cells[col_idx].string
    
    return ""
            
def get_info(soup, col_name, row_name):
    """ get desired entry based on col/row name """
    tables = soup.findChildren('table')

    if len(tables) > 0:
        table = find_table(tables, row_name, col_name)
    else:
        print("Did not find ANY tables!")
        return

    if table:
        value = get_value(table, row_name=row_name, col_name=col_name).strip()
        return value
    else:
        print("Did not find a table with col_name \"%s\" and row_name \"%s\"!" % (col_name, row_name))

    return

def make_soup(filename):
    """ load file and create parseable data structure """
    # with open(filename, 'r') as f:
    #     contents = f.read()

    soup = BeautifulSoup(filename)
    
    return soup

def run(filename, queries):
    ''' run queries on one file'''
    soup = make_soup(filename)
    
    result = []
    for query in queries:
        row_name = query[0]
        col_name = query[1]
        
        info = get_info(soup, col_name, row_name)
        
        result.append([query[0], query[1], info])
    
    return result
        
def find_files(folder, pattern="*htm*"):
    ''' fine awr files, based on pattern'''
    def either(c):
        return '[%s%s]' % (c.lower(), c.upper()) if c.isalpha() else c

    return glob.glob(os.path.join(folder, ''.join(map(either, pattern))))

def create_key(query):
    ''' Create key based on the query. This key is e.g. used as column name in output'''
    if query[0] == "":
        r = query[1]
    elif query[1] == "":
        r = query[0]
    else:
        r = query[0] + "_" + query[1]
        
    return r.replace("\\","")


def create_keys(queries):
    ''' Creates keys based on the query. This key is e.g. used as column name in output'''
    keys = []
    for query in queries:
        keys.append(create_key(query))
        
    return keys


import re
from bs4 import BeautifulSoup
import os
import pandas as pd
import glob

# folder = 'C:\\foobar\\foobar'
# folder = '/tmp'
#folder = 'C:\\Users\\masandma\\OneDrive - Microsoft\\Arbeit\\ORCAS\\ORACLE\\customers\\Bawagpsk\\awr'
# folder = 'C:\\Users\masandma\\Desktop\\OPTSK00561730\\OPTSK00561730'
# folder = 'C:\\Users\\masandma\\OneDrive - Microsoft\\Arbeit\\ORCAS\\ORACLE\\customers\\AH'
# folder = 'C:\\Users\\masandma\\Desktop\\coba'
folder = "C:\\fakepath\\"

# queries are of the form [row_name, col_name],
# either element can be empty quotes
queries=[
    ['user calls', 'per Second'],
    ['user commits', 'per Second'],
    ['Begin Snap:', 'Snap Time'],
    ['End Snap:', 'Snap Time'],
    ["", "Host Name"],
    ["", "DB Name"],
    ["", "Edition"],
    ["", "RAC"],
    ["", "CDB"],
    ["", "Release"],
    ["", "Platform"],
    ["", "CPUs"],
    ['Host Mem \(MB\):', 'Begin'],
    ['SGA use \(MB\):', 'Begin'],
    ['PGA use \(MB\):', 'Begin'],
    ['Memory Usage %:','End'],
    ['user calls','per Trans'],
    ['user commits','per Trans'],
    ['Redo size \(bytes\)', 'Per Second'],
    ['DB CPU', '% DB time'],
    ['physical read total IO requests','per Second'],
    ['physical write total IO requests', 'per Second'],
    ['physical read total bytes','per Second'],
    ['physical write total bytes', 'per Second'],
    ['log file sync','Avg wait'],
    ["", "Table Scans"],
    ['compatible','Begin value'],
    ['optimizer_features_enable','Begin value'],
]

filenames = [fileName]
# filenames = find_files(folder)

if len(filenames) == 0:
    print("didn't find any files!")
else:
    keys = create_keys(queries)
    res_dict = {}
    res_dict['filename'] = filenames
    for key in keys:
        res_dict[key] = []

    for filename in filenames:
        info = run(fileText, queries)

        for entry in info:
            key = create_key(entry)
            res_dict[key].append(entry[2])

    df = pd.DataFrame(res_dict)
    df.to_csv("coba.csv")

df.to_csv(index=False)
