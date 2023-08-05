#! /usr/bin/env python
# -*- coding: utf-8 -*-

# for gspread
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import os
import sys
import shutil
import string

#import xml.etree.cElementTree as ET
import lxml.etree as ET

FILE_PATH = {}
LANG_MAP = []
prefix = "'"

def get_spreadsheet(ws_url):

    ######## Get Google Sheet Imformation ######### 
    scope = ['https://spreadsheets.google.com/feeds']                                            
    credentials = ServiceAccountCredentials.from_json_keyfile_name('AutoNameString-2322f16ec2d9.json', scope)
    gc = gspread.authorize(credentials)
    try:
        sh = gc.open_by_url(ws_url)
    except:
        print('\033[1;31merror: Cannot open the google sheet.')
        print('\033[1;33m       Please make sure:')
        print('       (1) The url is valid.')
        print('       (2) The google sheet is shared with "autonamestring@appspot.gserviceaccount.com".')
        print('           (with permission to edit the given google sheet)\n\033[1;m')
        exit()
    return sh


def get_worksheet(sh, ws_name):

    sh_list = sh.worksheets()
    title_list = []
    for name in sh_list:
        title_list.append(name.title)
#    print(title_list)

    if((ws_name in title_list) == False):
        ws = sh.add_worksheet(title = ws_name, rows= "1000", cols = "26")
        return ws,'new'
    else:
        ws = sh.worksheet(ws_name)
    return ws, 'old'


def print_usage():

    print('\n[#] usage: \n')
    print('\033[1;32m' + '    $ python ' + sys.argv[0] + '\033[1;31m' + '  upload  '+ '\033[1;33m' +'[-i "input_dir"] [-u "worksheet_url"] [-n "worksheet_name"]' + '\033[1;m'+ '\n')
    print('    -> Upload the string contents of all the strings.xml files in given directory')
    print('    -> to a given google worksheet.\n')
    print('\033[1;32m' + '    $ python ' + sys.argv[0] + '\033[1;31m' + ' download '+ '\033[1;33m' +'[-o "output_dir"] [-u "worksheet_url"] [-n "worksheet_name"]' + '\033[1;m'+ '\n')
    print('    -> Download and update all the strings.xmls files in the given directroy with ')
    print('    -> contents on the given google worksheet.\n')   
    exit()
    return


def parse_config():
    
    global LANG_MAP
    global FILE_PATH

    try:
        f = open('config', 'r')
    except IOError:
        print('\033[1;31m [-] error: I need a config file... QQ\033[1m')
        exit()

    for line in f:        
        line = line.strip()
        if(line.find('worksheet_name') != -1):
            temp_str = line[len('worksheet_name: '):].strip()
        #    print(temp_str)
            if(len(temp_str) != 0):
                FILE_PATH['ws_name'] = temp_str

        elif(line.find('worksheet_url') != -1):
            temp_str = line[len('worksheet_url: '):].strip()
        #    print(temp_str)
            if(len(temp_str) != 0):
                FILE_PATH['ws_url'] = temp_str

        elif(line.find('language_name_mapping') != -1):

            format_string = line[len('language_name_mapping: {'):-2]
            format_string = format_string.split(',')

            x = []
            for pair in format_string:
                pair = pair.replace('"', "").strip()
                pair = pair.split(':')
                if(pair[1] == 'default'):
                    pair[1] = 'values'
                else:
                    pair[1] = 'values-' + pair[1]
                pair.append(0)
                x.append(pair)
#                print pair
            LANG_MAP = x
    f.close
    return


def parse_arguments():

    global FILE_PATH
    
    if(len(sys.argv) == 1):
        print_usage()
    
    parse_config()
    for i in range(len(sys.argv)):
        if(sys.argv[i].find('-') == 0):
            if(i+1 < len(sys.argv) and sys.argv[i+1].find('-') != 0):
                if(sys.argv[i] == '-i'):
                    FILE_PATH['input'] = sys.argv[i+1]
                    if(FILE_PATH['input'][-1] == '/'):
                        FILE_PATH['input'] = FILE_PATH['input'][:-1]
                elif(sys.argv[i] == '-o'):
                    FILE_PATH['output'] = sys.argv[i+1]
                    if(FILE_PATH['output'][-1] == '/'):
                        FILE_PATH['output'] = FILE_PATH['output'][:-1]

                elif(sys.argv[i] == '-u'):
                    FILE_PATH['ws_url'] = sys.argv[i+1]
                elif(sys.argv[i] == '-n'):
                    FILE_PATH['ws_name'] = sys.argv[i+1]
                else:
                    print('[-] error: unknown specified flag "%s"' % sys.argv[i])
            else:
                print_usage()

    if(FILE_PATH.get('ws_url') == None):
        print('\033[1;31m[-] error: Give me the worksheet url plz... QAQ\033[1;m')
        exit()
    elif(FILE_PATH.get('ws_name') == None):
        print('\033[1;31m[-] error: Give me the worksheet name plz... QAQ\033[1;m')
        exit()

    if(sys.argv[1] == 'download' and FILE_PATH.get('output') == None):
        print('\033[1;31m[-] error: Give me the output path plz... QAQ\033[1;m')
        exit()    

    if(sys.argv[1] == 'upload' and FILE_PATH.get('input') == None):
        print('\033[1;31m[-] error: Give me the input path plz... QAQ\033[1;m')
        exit()

    if(FILE_PATH.get('input') != None):
        try:
            x = []
            dir_list = os.listdir(FILE_PATH['input'])
            for name in dir_list:
                if(name.find('values') != -1):
                    x.append(name)
            FILE_PATH['dir_list'] = x
            FILE_PATH['dir_list'].sort()
        except OSError:
            print('\033[1;31m[-] error: No such file or directory. "%s"\033[1;m' % (FILE_PATH['input']))

    print(FILE_PATH)
    return


def lang2dir(lang_name):

    global LANG_MAP
    for i in range(len(LANG_MAP)):
        if(lang_name == LANG_MAP[i][0]):
            return LANG_MAP[i][1], i
    return '', -1


def dir2lang(dir_name):

    global LANG_MAP
    for i in range(len(LANG_MAP)):
        if(dir_name == LANG_MAP[i][1]):
            return LANG_MAP[i][0], i
    return '', -1


def escape_check(input_str):

    global prefix

    ### 0. 'true' and 'false' will transform into 'TRUE' and 'FALSE' automatically in google sheet.    
    if(input_str == '-true-'):
        return 'true'
    elif(input_str == '-false-'):
        return 'false'

    ### 1. remove 7 spaces before the string to avoid symbols missing in google sheet.
#    print(input_str.find('.      '))
#    if(input_str.find('.      ') == 0):
#        input_str = input_str[7:]
#    if(input_str.find(prefix) == 0):
#        input_str = input_str[len(prefix):]

    ### 2. single ['] and ["] should be escaped.
    ### chr(92) = '\'
    block = input_str.split("'")
    input_str = block[0]
    for i in range(1, len(block)):
        if(len(input_str) == 0 or input_str[-1] != chr(92)):
            input_str += chr(92)
        input_str += "'" + block[i]
    
    block = input_str.split('"')
    input_str = block[0]
    for i in range(1, len(block)):
        if(len(input_str) == 0 or input_str[-1] != chr(92)):
            input_str += chr(92)
        input_str += '"' + block[i]
    
    return input_str


def inv_escape_check(input_str):

    global prefix

    if(input_str == 'true'):
        return '-true-'
    elif(input_str == 'false'):
        return '-false-'

    ### 0. padding 7 spaces before the string to avoid symbols missing in google sheet.
#    input_str = '.      ' + input_str
#    input_str = prefix + input_str

    return input_str

    
def ANS_xmlfile_to_data(dir_name):

    global FILE_PATH
    global LANG_MAP
    
    ns_order = []
    name_strings = {}
    for name in os.listdir(dir_name):
        path = dir_name + '/' + name + '/strings.xml'
        
#        print(dir_name, os.listdir(dir_name))

        if(os.path.exists(path) == False):
            continue
    
        print('[#] Find strings.xml in "%s"' % (path))
        tree = ET.parse(path)
        root = tree.getroot()
        for child in root:
            
            text = child.text
            name_key = child.attrib['name']

            if(name_strings.get(name_key) == None):
                name_strings[name_key] = {}
                ns_order.append(name_key)
                name_strings[name_key]['translatable'] = child.attrib.get('translatable', '')

            if(name_strings[name_key].get(name) == None):
                if(text[0] == '"' and text[-1] == '"'):
                    text = text[1:-1]
                name_strings[name_key][name] = inv_escape_check(text).encode('utf-8')

        result = dir2lang(name)
        if(result[1] == -1):
            LANG_MAP.append([name, name, 1])
        else:
            LANG_MAP[result[1]][2] = 1

    return name_strings, ns_order


def ANS_data_to_xmlfile(name_string, ns_order, dir_name, file_name):
    
    tree = ET.ElementTree(file='./template_strings.xml')
    root = tree.getroot()    
    root.text = '\n\n    '

    for i in range(len(ns_order)):

        key = ns_order[i]
        translatable = name_string[key].get('translatable', '')
        content = name_string[key][dir_name]

        if(len(translatable) != 0 and len(content) == 0):
            continue

        temp = ET.SubElement(root, 'string')
        temp.text = '"' + escape_check(content).decode('utf-8') + '"'
        
        ### lxml.etree ###
        temp.attrib['name'] = key
        if(len(translatable) != 0):
            temp.attrib['translatable'] = 'false'

        ### xml.etree ###
        '''
        if(len(translatable) != 0):
            temp.attrib = {"name":key, "translatable":"false"}
        else:
            temp.attrib = {"name":key}
        '''

        temp.tail = '\n    '
        if(i == len(ns_order) - 1):
            temp.tail += '\n\n'

    tree.write(file_name)
    return


def ANS_googlesheet_to_data(ws, name_string,  ns_order):

    all_value = ws.get_all_values()
    if(len(all_value) == 0):
        print('\033[1;33m[#] Get no data.\033[1;m')
        return name_string, ns_order, -1
        
    print('[#] Get data from google sheet...')
    rows = len(all_value)
    cols = len(all_value[0])

    ##### Transform language name to dir_name #####
    for j in range(3, cols):
        temp = lang2dir(all_value[0][j])
        if(temp[1] == -1):
            print('\033[1;33m\n[-] Cannot find the dir_name of lang : ' + all_value[0][j])
            print('[-] Please check the language mapping setting in config file.\n\033[1;m')
            LANG_MAP.append([all_value[0][j], all_value[0][j], 1])
        else:               
            LANG_MAP[temp[1]][2] = 1
            all_value[0][j] = temp[0]

    for i in range(1, rows):

        if(len(all_value[i][0]) == 0):
            continue

        key = all_value[i][0]
        ns_order.append(key)
        name_string[key] = name_string.get(key, {})

        tran = all_value[i][1]
        if(len(tran) != 0):
            name_string[key]['translatable'] = 'false'
        #    print(key , tran)

        for j in range(3, cols):
            lang = all_value[0][j]
            name_string[key][lang] = all_value[i][j].encode('utf-8')

    print('\033[1;32m[+] Get data done!\033[1;m')
    return name_string, ns_order, 1


def ANS_data_to_googlesheet(ws, name_string, ns_order):

    global FILE_PATH
    global LANG_MAP
    global prefix

    ###   <Layout>
    ###
    ###   [0, 0] All key \ All Language   [0, 1] description   [0, 2] Lang1   [0, 3] Lang2  ...  [0, n] Lang(n-2)
    ###   [1, 0] Name String key1         [1, 1]      ''       [1, 2] data    [1, 3] data   ...
    ###   [2, 0] Name String key2         [2, 1]      ''       [2, 2] data    [2, 3] data   ...
    ###               ...                            ...              ...            ...
    ###   [m, 0] Name String key(m-1)

    appear_dir_info = [['Translatable', 'translatable', 1], ['Description', 'Description', 1]]
    appear_dir_info +=  [elem for i, elem in enumerate(LANG_MAP) if elem[2] == 1]
 
#    print appear_dir_info

    rows = len(name_string.keys()) + 1
    cols = len(appear_dir_info) + 1
    cell_list = ws.range('A1:' + string.letters[25 + cols] + str(rows))
    for cell, i in zip(cell_list, range(rows * cols)):

        ### "A1" = no content.
        ### "B1" -> "?1" = fill with language name.
        if(i == 0):
            cell.value = ''
        elif(i / cols == 0):
            cell.value = appear_dir_info[i-1][0]
        else:
            ### "A?" = fill with key
            ### "??" = fill the value of key corresponding to lang.
            key = ns_order[(i / cols) - 1]
            if(i % cols == 0):
                cell.value = key.decode('utf-8')
            else:
                dir_name = appear_dir_info[(i % cols) - 1][1]
                cell.value = prefix + name_string[key].get(dir_name, '').decode('utf-8')
    
    ws.update_cells(cell_list)
    print('\033[1;32m[+] Upload seccess!!!\n\033[1;m')
    return


def ANS_output_files(name_string, ns_order):

    global FILE_PATH
    global LANG_MAP
    
    output_dir_list = [elem[1] for i, elem in enumerate(LANG_MAP) if elem[2] == 1 ] 

    if(os.path.exists(FILE_PATH['output']) == False):
        os.mkdir(FILE_PATH['output'])
    else:

        #####   If the output directory exists, check the state of old data and   ##### 
        #####   warn the user whether delete inconsistent name_strings or not.    #####
        
        old_name_string, old_ns_order = ANS_xmlfile_to_data(FILE_PATH['output'])
        deleted_ns = [x for x in old_ns_order if (x not in ns_order) == True]
 
        if(len(deleted_ns) != 0):
            print('\033[1;33m\n[#] These name_strings will be deleted from all the strings.xml file:\n\033[1;m')
            for i in range(len(deleted_ns)):
                print('    [%d] <string name=\033[1;36m"%s"\033[1;m>' % (i, deleted_ns[i]))
            print('\033[1;33m\n[#] Are you sure to do it? (y/n) \033[1;m')
            
            if(raw_input() != 'y'):
                print('\033[1;33m[#] Do nothing.\033[1;m')
                exit()

    for dir_name in output_dir_list:

        dir_path = FILE_PATH['output'] + '/' + dir_name
        if(os.path.exists(dir_path) == False):
            os.mkdir(dir_path)
 
        ANS_data_to_xmlfile(name_string, ns_order, dir_name, dir_path + '/strings.xml') 
  
    return


def ANS_merge_data(ws, name_string, ns_order):

    ##### Merger old content into to-be-upload contents #####
    name_string, old_ns_order, flag = ANS_googlesheet_to_data(ws, name_string, [])
    if(flag == -1):
        print('\033[1;32m[+] No old data, no need to merge\033[1;m')
        return name_string, ns_order
    else: 
        print('[#] Merging old data to new data.')
        for key in ns_order:
            if((key in old_ns_order) == False):
                old_ns_order.append(key)
        ns_order = old_ns_order

    print('\033[1;32m[+] Merge done!\033[1;m')
    return name_string, ns_order


def ANS_move_old(sh, ws):

    ws_old = get_worksheet(sh, file_path['ws_name'] + '_old')[0]
    all_value = ws.get_all_values()
    rows = len(all_value)

    if(rows != 0):
        print('[#] moving old contents to another sheet...')
        cols = len(all_value[0])
            
        cell_list = ws_old.range('a1:' + string.letters[25 + cols] + str(rows))
        for cell, i in zip(cell_list, range(rows * cols)):
            cell.value = all_value[i / cols][i % cols]
        ws_old.update_cells(cell_list)
    
        cell_list = ws.range('a1:' + string.letters[25 + cols] + str(rows))
        for cell in cell_list:
            cell.value = ''
        ws.update_cells(cell_list)
        print('\033[1;32m[+] move success!!!\033[1;m')
    return
 

def ANS_upload():

    global FILE_PATH
    global LANG_MAP

    sh = get_spreadsheet(FILE_PATH['ws_url'])
    ws, flag = get_worksheet(sh, FILE_PATH['ws_name'])

    '''
    ##### Move the old contents to another sheet '[sheet_name]_old' #####
    ##### Clean the old contents in the sheet '[sheet_name]'        #####
    if(flag == 'old'):
        print('')
        #ANS_move_old(sh, ws)
    else:
        print('\033[1;32m[+] No old contents to be moved.\033[1;m')
    '''

    ##### Get name string contents from strings.xml files.          #####
    ##### Merge the old data on the worksheet with new data.        #####

    print('[#] Start uploading, please wait...')
    
    name_string, ns_order = ANS_xmlfile_to_data(FILE_PATH['input'])
    name_string, ns_order = ANS_merge_data(ws, name_string, ns_order)
    ANS_data_to_googlesheet(ws, name_string, ns_order)

    return

    
def ANS_download():

    global FILE_PATH
    global LANG_MAP

    sh = get_spreadsheet(FILE_PATH['ws_url'])
    ws, flag = get_worksheet(sh, FILE_PATH['ws_name'])    
    if(flag == 'new'):
        print('\033[1;31m\n[-] error: The worksheet doesn\'t exsit... QAQ\033[1;m')
        print('\033[1;31m[-]        Are you sure you give the right worksheet name?\033[1;m\n')
        sh.del_worksheet(ws)
        exit()

    print('[#] Downloading the content...')
    name_string, ns_order, flag = ANS_googlesheet_to_data(ws, {}, [])
    if(flag == -1):
        print('\033[1;31m\n[-] error: Download fail. (No data)\033[1;m')
        print('\033[1;31m[-]        Please check the worksheet.\033[1;m\n')
        exit()
    else:       
        print('\033[1;32m[+] Download done!\033[1;m')

    ANS_output_files(name_string, ns_order)
    print('\033[1;32m[+] Update success!!!\033[1;m\n')
    return


if __name__ == '__main__':
  
    parse_arguments() 

    if(len(sys.argv) > 1 and sys.argv[1] == 'upload'):

        ANS_upload()

    elif(len(sys.argv) > 1 and sys.argv[1] == 'download'):
        
        ANS_download()

    else: 
        print_usage()

