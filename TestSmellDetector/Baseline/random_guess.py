import random
import pandas as pd
from generate_AST import get_all_java_files, distinguish_test_and_production_file, get_func_in_test_file, get_func_info

# random guess:
# 1. PMT
# 2. RDT
# 3. PTO 
# 4. PWO 
# 5. LT
# 6. RT 


def random_guess(data):
    random_classification = []
    for i in range(len(data)):
        random_classification.append(random.randint(1,6))
    return random_classification

def get_func_signature(projects):
    func_name = []
    for project in projects:
        all_files = get_all_java_files(project)
        test_files, production_files = distinguish_test_and_production_file(all_files)
        func_in_test, test_import_info, test_files_new = get_func_in_test_file(test_files, [], [])
        for i in range(len(func_in_test)):
            for func_ in func_in_test[i]:
                func_name.append((test_files_new[i], func_.name))
    return func_name

def get_ground_truth_for_PMT(result_file, project_names):
    result = pd.read_pickle(result_file)['ts_1_result']
    PMT = []
    print(result[0][0][0])
    print(result[0][0][1])
    for i in range(len(result)):
        for project_name in project_names:
            if project_name in str(result[i][0][0]):
                # print(result[i])
                PMT.append(result[i][0][0] + '|' + result[i][0][1])
    print(PMT)
    return PMT

def get_ground_truth_for_RDT(result_file, project_names):
    result = pd.read_pickle(result_file)['ts_1_result']
    RDT = []
    for i in range(len(result)):
        for project_name in project_names:
            if project_name in str(result[i]):
                RDT.append(result[i])
                break
    return RDT

def get_ground_truth_for_POW(result_file, project_names):
    result = pd.read_pickle(result_file)['ts_1_result']
    POW = []
    for i in range(len(result)):
        for project_name in project_names:
            if project_name in str(result[i][0]):
                # print(result[i])
                print(result[i][0])
                print(result[i][1][0][0][0])
                POW.append(result[i][0] + '|' + str(result[i][1][0][0][0]))
    # print(POW)
    return POW

def get_ground_truth_for_LT(result_file, project_names):
    result = pd.read_pickle(result_file)['ts_1_result']
    LT = []
    for i in range(len(result)):
        for project_name in project_names:
            if project_name in str(result[i]):
                LT.append(result[i])
                break
    return LT

def get_ground_truth_for_RT(result_file, project_names):
    result = pd.read_pickle(result_file)['ts_1_result']
    RT = []
    for i in range(len(result)):
        for project_name in project_names:
            if project_name in str(result[i][0][len(result[i][0]) - 1]):
                RT.append(result[i][0][len(result[i][0]) - 1] + '|' + result[i][0][3])
                # print(result[i][0][6] + '|' + result[i][0][3])
    return RT


def evaluation(TS, random_classification, func_name, type_index):
    num = 0
    num_2 = 0
    for i in range(len(random_classification)):
        if random_classification[i] == type_index:
            num_2 = num_2 + 1
            for j in range(len(TS)):
                # print(func_name[i])
                if func_name[i][1] in TS[j] and func_name[i][0] in TS[j]:
                    num = num + 1
                    break

    Recall = float(num) / float(len(TS))
    Precision = float(num) / float(num_2)
    print(num)
    print(len(TS))
    print(num_2)
    print(Recall)
    print(Precision)
    F1 = 0
    if Precision != 0 and Recall != 0:
        F1 = float(2 * Precision * Recall) / float(Precision + Recall)
    print(F1)


def random_guess_for_PTO(projects):
    random_classification = []
    for i in range(len(projects)):
        random_classification.append(random.randint(1,6))

    correct_num = 0
    num_1 = 0
    for i in range(len(projects)):
        if random_classification[i] == 3:
            num_1 = num_1 + 1
        if 'functionaljava' in projects[i] and random_classification[i] == 3:
            correct_num = correct_num + 1
        elif 'zipkin' in projects[i] and random_classification[i] == 3:
            correct_num = correct_num + 1

    Precision = float(correct_num) / float(num_1)
    Recall = float(correct_num) / 2
    print(num_1)
    print(correct_num)
    print(Precision)
    print(Recall)
    print(random_classification)
    F1 = 0
    if Precision != 0 and Recall != 0:
        F1 = float(2 * Precision * Recall) / float(Precision + Recall)
    print(F1)


result_file1 = r'ts_1_result_final.pkl'
# project = [r'../repos/fastjson']
project = [ r'../repos/fastjson', r'../repos/orientdb', r'../repos/hapi-fhir', r'../repos/ninja', r'../repos/functionaljava', r'../repos/JSqlParser', r'../repos/zipkin']
func_name = get_func_signature(project)
random_classification = random_guess(func_name)
TS = random_guess_for_PTO(result_file1, ['fastjson', 'orientdb', 'hapi-fhir', 'ninja', 'functionaljava', 'JSqlParser', 'zipkin'])
evaluation(TS, random_classification, func_name, 3)
# ['fastjson', 'orientdb', 'hapi-fhir', 'ninja', 'functionaljava', 'JSqlParser', 'zipkin']
random_guess_for_PTO(project)