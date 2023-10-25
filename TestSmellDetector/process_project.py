import os
from turtle import st
import pandas as pd

def get_datafile(dict):
    return pd.to_pickle(dict)

def get_file_suffix(file):
    return file.split('.java')[0].split('/')[len(file.split('.java')[0].split('/')) - 1]

def get_all_java_files(project_folder):
    files_list = []
    for root, dirs, files in os.walk(project_folder):
        if len(files) > 0:
            for file_ in files:
                if '.java' in file_:
                    files_list.append(root + '/' + file_)
    return files_list 

def get_folder_section(file):
    return file.replace('.java', '').split('/')[:-2]

def get_folder_path(file):
    return file.replace('/' + file.split('/')[len(file.split('/')) -1], '')


# def find_func(sourcefile, func_name):
#     func = []
#     tmp = 0
#     flag = ''
#     with open(sourcefile, 'r') as f:
#         lines = f.readlines()

#     for line in lines:
#         if func_name in line and  '(' in line and ')' in line and '{' in line:
#             flag = True
#             tmp = tmp + 1
#             func.append(line)
#             continue
#         elif '}' in line:
#             tmp = tmp - 1
#             func.append(line)
#             continue
#         elif tmp != 0:
#             func.append(line)
#             continue
#         elif tmp == 0 and flag == True:
#             flag = False
#             break
#     return func

def find_func(sourcefile, func_name):
    func = ''
    tmp = 0
    flag = ''
    with open(sourcefile, 'rb') as f:
        lines = f.readlines()
    for line in lines:
        line = line.decode('utf-8', 'ignore')
        # print(line)
        if func_name in line and  '(' in line and ')' in line and '{' in line:
            flag = True
            tmp = tmp + 1
            # func = func + line
            continue
        elif '}' in line:
            tmp = tmp - 1
            func = func + line
            continue
        elif tmp != 0:
            func = func + line
            continue
        elif tmp == 0 and flag == True:
            flag = False
            break
    func = func.replace('//', '').replace('\n', '').replace('/t', '').replace('}', '')
    func.split(';')
    return func.split(';')

def match_token(statement, token):
    tmp = 0
    tmp_str = ''
    if token == '(':
        for i in range(len(statement)):
            if statement[i] == token and tmp == 0:
                tmp = tmp + 1
            elif i == ')':
                tmp = tmp -1
                if tmp != 0:
                    tmp_str = tmp_str + statement[i]
                else:
                    break
            else:
                tmp_str = tmp_str + statement[i]
    return tmp_str




    