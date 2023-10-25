import os
import pandas as pd
from main_detector import main_detector_2
from generate_AST import get_all_java_files, distinguish_test_and_production_file, get_func_in_test_file

def get_all_projects(project_path):
    dirs = os.listdir(project_path)
    return dirs

def get_all_funcs(projects_path, dirs):
    funcs = 0
    for dir in dirs:
        funcs_i = 0
        dir_str = projects_path + '/' + dir
        all_files = get_all_java_files(dir_str)
        test_files, production_files = distinguish_test_and_production_file(all_files)
        func_in_test, test_import_info, test_files_new = get_func_in_test_file(test_files, [], [])
        for i in func_in_test:
            funcs_i = funcs_i + len(i)
        funcs = funcs + funcs_i
    return funcs

def get_all_funcs_2(dir_str):
    funcs = 0
    # for dir in dirs:
    funcs_i = 0
    all_files = get_all_java_files(dir_str)
    test_files, production_files = distinguish_test_and_production_file(all_files)
    func_in_test, test_import_info, test_files_new = get_func_in_test_file(test_files, [], [])
    for i in func_in_test:
        funcs_i = funcs_i + len(i)
    funcs = funcs + funcs_i
    return funcs
        

def run_test_smell(projects_path, dirs, type_, pkl_path):
    item_dict = pd.DataFrame()
    for dir in dirs:
        dir_str = projects_path + '/' + dir
        # args = os.system('python main_detector.py -project ' + dir_str + ' -test_smell_types ' + str(type_))
        len_result, result = main_detector_2(dir_str, type_)
        if len_result != 0:
            item_dict_tmp = ({'project': dir_str, 'ts_1_num': len_result, 'ts_1_result': result})
            
            item_dict = pd.concat([item_dict, pd.DataFrame(item_dict_tmp)], ignore_index=True)
            print(item_dict)
    item_dict.to_pickle(pkl_path)

projects_path = r'../repos'
pkl_path_1 = r'./ts_1_result_final.pkl'
pkl_path_2 = r'./ts_2_result_final.pkl'
pkl_path_3 = r'./ts_3_result_final.pkl'
pkl_path_4 = r'./ts_4_result_final.pkl'
pkl_path_5 = r'./ts_5_result_final.pkl'
pkl_path_6 = r'./ts_6_result_final.pkl'
pkl_path_7 = r'./ts_7_result_final.pkl'

dirs = get_all_projects(projects_path)
run_test_smell(projects_path, dirs, 2, pkl_path_2)