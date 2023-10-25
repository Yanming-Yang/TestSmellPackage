# from asyncio.windows_events import NULL
from re import L
# from this import s
from turtle import st
import javalang
from javalang.ast import Node
import os
from anytree import AnyNode, RenderTree
from process_project import get_all_java_files, get_datafile, find_func, match_token
import re
from itertools import chain

def get_AST(java_file):
    # programfile = open(java_file, encoding='utf-8')
    try:
        programfile = open(java_file, encoding='latin-1')
        programtext = programfile.read()
        tree = javalang.parse.parse(programtext)
    except (javalang.tokenizer.LexerError, Exception):
        tree = None
    return tree

def get_package_info(tree):
    import_info = None
    if tree != None:
        package_info = tree.children[0]
    return package_info

def get_import_info(tree):
    import_info = None
    if tree != None:
        import_info = tree.children[1]
    return import_info
# each class has attrs:
# ['modifiers', 'annotations', 'documentation', 'name', 'body', 'type_parameters', 'extends', 'implements']
def get_classes_info(tree):
    class_info = None
    if tree != None:
        class_info = tree.children[2]
    return class_info

def get_fields(class_ast):
    # return [field for field in class_ast if 'FieldDeclaration' in type(field)]
    fileds = []
    if class_ast != None:
        for class_i in class_ast:
            for filed in class_i.body:
                if 'FieldDeclaration' in str(type(filed)):
                    fileds.append(filed)
    return fileds

def get_funcs(class_ast):
    # return [func for func in class_i.body for class_i.body in class_ast if 'MethodDeclaration' in type(func)]
    funcs = []
    if class_ast != None:
        for class_i in class_ast:
            for func in class_i.body:
                if 'MethodDeclaration' in str(type(func)):
                    funcs.append(func)
    return funcs

# ------------------------------------------------------------------------------------------

# def detect_private_func_testing(project):
#     all_files = get_all_java_files(project)

#     test_files, production_files = distinguish_test_and_production_file(all_files)

#     func_in_test, test_import_info = get_func_in_test_file(test_files, func_in_test, test_import_info)
#     # file_name; class_name; func_name
#     func_in_produc_code, import_info = get_production_func(production_files, func_in_produc_code, import_info)

#     test_class_info = get_class_info(test_files)

#     production_class_info = get_class_info(production_files)

#     production_func_info = get_func_info(func_in_produc_code, production_func_info)

#     private_production_func_info = get_private_production_func_info(production_func_info)

#     test_func_info = get_func_info(func_in_test, test_func_info)

#     test_statement_types = get_statement_type_list_in_test_func(func_in_test, test_import_info, test_statement_types)

#     normal_test, reflect_funcs_in_test = distinguidh_normal_and_reflect_file(test_import_info, all_files, reflect_funcs_in_test)

#     analysis_import_info_for_private_method_testing(test_import_info, test_files, test_func_info)

#     return testing_protected_method, testing_private_method

def distinguish_test_and_production_file(files):
    test_file = []
    production_file = []
    for file in files:
        if 'Test' in file.split('/')[len(file.split('/')) - 1] and '.java' in file:
            test_file.append(file)
        elif '/test/' in str(file) and '.java' in file:
            test_file.append(file)
        elif '/Test/' in str(file) and '.java' in file:
            test_file.append(file)
        else:
            production_file.append(file)
    # test_file = [file for file in files if ('Test' in file.split('/')[len(file.split('/')) - 1] or '/test/' in str(file) or '/Test/' in str(file)) and '.java' in file]
    # production_file = [file for file in files if file not in test_file and '.java' in file]
    return test_file, production_file

def get_func_in_test_file(test_files, func_in_test, test_import_info):
    test_files_new =[]
    for file in test_files:
        try:
            tree = get_AST(file)
            class_ = get_classes_info(tree)
            func_in_test.append(get_funcs(class_))

            test_import_info.append(get_import_info(tree))
            test_files_new.append(file)
        except javalang.parser.JavaSyntaxError as e:
            continue   
    return func_in_test, test_import_info, test_files_new

def get_production_func(production_files, func_in_produc_code, import_info):
    production_files_new = []
    for file in production_files:
        try:
            tree = get_AST(file)
            if tree != None:
                class_ = get_classes_info(tree)
                func_in_produc_code.append(get_funcs(class_))
                import_info.append(get_import_info(tree))
                production_files_new.append(file)
        except javalang.parser.JavaSyntaxError as e:
            continue
    return func_in_produc_code, import_info, production_files_new

def get_production_fileds(production_files, func_in_produc_fileds):
    for file in production_files:
        tree = get_AST(file)
        class_ = get_classes_info(tree)
        func_in_produc_fileds.append(get_fields(class_))
    return func_in_produc_fileds

def get_class_info(files, class_info):
    for file in files:
        tree = get_AST(file)
        class_ = get_classes_info(tree)
        class_info_ = (class_.annotations, class_.modifiers, class_.name, class_.extends)
        class_info.append(class_info_)
    return class_info


# class_name, modifier, return_type, func_name
def get_func_info(funcs, func_info):
    funcs = list(chain.from_iterable(funcs))
    for func in funcs:
        func_info_ = (func.annotations, func.modifiers, func.return_type, func.name, func.parameters, func.throws)
        func_info.append(func_info_)
    return func_info

def get_func_info_file(funcs, type_files, func_info_all):
    # funcs = list(chain.from_iterable(funcs))
    for i in range(len(funcs)):
        func_info = []
        for func in funcs[i]:
            func_info_ = (func.annotations, func.modifiers, func.return_type, func.name, func.parameters, func.throws, type_files[i])
            func_info.append(func_info_)
        func_info_all.append(func_info)
    return func_info_all

def get_private_production_func_info(func_infos):
    private_production_func_info = []
    for func_infos_ in func_infos:
        for func_info in func_infos_:
            if 'private' in str(func_info[1]):
                private_production_func_info.append(func_info)
    return private_production_func_info


def get_statement_type_list_in_test_func(funcs, type_info):
    # func_body = [func.body for func in funcs if func.body != None]
    for i in range(len(funcs)):
        for func in funcs[i]:
        # for func in func_body:
            func = func.body
            type_info_ = []
            if func != None:
                for sta in func:
                    type_info_.append(type(sta))
                type_info.append((i, type_info_))
    return type_info

def distinguidh_normal_and_reflect_file(test_import_info, all_files, reflect_test_files, normal_test_files):
    # reflection_str = ['Mock', 'mock', 'Reflect', 'reflect']
    for i in range(len(test_import_info)):
        for j in range(len(test_import_info[i])):
            if 'Mock' in test_import_info[i][j] or 'mock' in test_import_info[i][j] or 'Reflect' in test_import_info[i][j] and 'reflect' in test_import_info[i][j]:
                reflect_test_files.append(all_files[i])
            else:
                normal_test_files.append(all_files[i])
    return reflect_test_files, normal_test_files

def analysis_import_info_for_private_method_testing(test_import_info, test_func_info, test_files, func_in_test, private_production_func_info):
    final_result = []
    info = []
    if test_import_info != None:
        for i in range(len(test_import_info)):
            if test_import_info[i] != None:
                for import_ in test_import_info[i]:
                    if 'java.lang.reflect' in str(import_):
                        print('Type 1:', test_files[i])
                        info = info + check_for_type_1_private_method(i, func_in_test, test_func_info, test_files)
                    elif 'ReflectionTestUtils' in str(import_):
                        print('Type 2:', test_files[i])
                        info = info + check_for_type_2_private_method(i, func_in_test, test_func_info, test_files)
                    elif 'ReflectionUtils' in str(import_):
                        print('Type 3:', test_files[i])
                        info = info + check_for_type_3_private_method(i, func_in_test, test_func_info, test_files)
                    elif 'PowerMockito' in str(import_):
                        print('Type 4:', test_files[i])
                        info = info + check_for_type_4_private_method(i, func_in_test, test_func_info, test_files)
                    elif 'Whitebox' in str(import_):
                        print('Type 4-2:', test_files[i])
                        info = info + check_for_type_4_2_private_method(i, func_in_test, test_func_info, test_files)
                    elif 'powermock.' in str(import_):
                        print('Type 5:', test_files[i])
                        info = info + check_for_type_5_private_method(i, func_in_test, test_func_info, test_files)
    for info_ in info:
        # print(info)
        private_testing = compare_testing_and_production_result(info_[2], info_[3], private_production_func_info)
        if private_testing != None:
            if info_ not in [item[0] for item in final_result]:
                final_result.append((info_, private_testing))
    return final_result

def get_reflection_info(sta):
    func_name = ''
    arguments = []
    args = 0
    class_name = ''
    if 'VariableDeclaration' in str(type(sta)):
        if 'ClassReference' in str(type(sta.declarators[0].initializer)):
            class_invoker = sta.declarators[0].initializer.type
            if 'ReferenceType' in str(type(class_invoker)):
                class_name = class_invoker.name
            
            invoked_body = sta.declarators[0].initializer.selectors
            for inv_body in invoked_body:
                if 'MethodInvocation' in str(type(inv_body)) and 'getDeclaredMethod' in str(inv_body.member):
                    arguments = inv_body.arguments
                    if 'Literal' in str(type(arguments[0])):
                        func_name = arguments[0].value.replace('"', '')   
                    if len(arguments) > 1:
                        args = len(arguments) - 1
    return func_name, args, class_name

def check_for_type_1_private_method(index_i, func_in_test, test_func_info, test_files):
    private_method_testing_info = []
    private_func_name_in_test = ''
    for i in range(len(func_in_test[index_i])):
        if 'getDeclaredMethod' in str(func_in_test[index_i][i]):
            func_name = test_func_info[index_i][i][3]
            # print(func_name)
            test_func_content = find_func(test_files[index_i], func_name)
            for statement in test_func_content:
                if 'getDeclaredMethod' in statement:
                    # print(func_in_test[index_i][i])
                    useful_content = statement.split('getDeclaredMethod')[1]
                    # useful_content_2 = statement.split('getDeclaredMethod')[0]
                    private_func_name_in_test, arguments = get_arguments(useful_content, 0)
                    info = (test_files[index_i], test_func_info[index_i][i][3], private_func_name_in_test, arguments)
                    private_method_testing_info.append(info)
    return private_method_testing_info

def check_for_type_2_private_method(index_i, func_in_test, test_func_info, test_files):
    private_method_testing_info = []
    private_func_name_in_test = ''

    for i in range(len(func_in_test[index_i])):
        if 'invokeMethod' in str(func_in_test[index_i][i]):
            func_name = test_func_info[index_i][i][3]
            test_func_content = find_func(test_files[index_i], func_name)
            for statement in test_func_content:
                if 'invokeMethod' in statement:
                    useful_content = statement.split('invokeMethod')[1]
                    private_func_name_in_test, arguments = get_arguments(useful_content, 1)
                    info = (test_files[index_i], test_func_info[index_i][i][3], private_func_name_in_test, arguments)
                    private_method_testing_info.append(info)
    return private_method_testing_info

def check_for_type_3_private_method(index_i, func_in_test, test_func_info, test_files):
    private_method_testing_info = []
    private_func_name_in_test = ''

    try:
        for i in range(len(func_in_test[index_i])):
            if 'invokeMethod' in str(func_in_test[index_i][i]):
                func_name = test_func_info[index_i][i][3]
                test_func_content = find_func(test_files[index_i], func_name)
                for statement in test_func_content:
                    if 'invokeMethod' in statement:
                        useful_content = statement.split('invokeMethod')[1]
                        # useful_content_2 = statement.split('invokeMethod')[0]
                        private_func_name_in_test, arguments = get_arguments(useful_content, 0)
                        info = (test_files[index_i], test_func_info[index_i][i][3], private_func_name_in_test, arguments)
                        private_method_testing_info.append(info)
    except RecursionError as e:
        pass
            
    return private_method_testing_info

def check_for_type_4_private_method(index_i, func_in_test, test_func_info, test_files):
    private_method_testing_info = []
    private_func_name_in_test = ''

    for i in range(len(func_in_test[index_i])):
        if 'when' in str(func_in_test[index_i][i]):
            func_name = test_func_info[index_i][i][3]
            test_func_content = find_func(test_files[index_i], func_name)
            for statement in test_func_content:
                if 'when' in statement:
                    useful_content = statement.split('when')[1]
                    # useful_content_2 = statement.split('when')[0]
                    private_func_name_in_test, arguments = get_arguments(useful_content, 1)
                    info = (test_files[index_i], test_func_info[index_i][i][3], private_func_name_in_test, arguments)
                    private_method_testing_info.append(info)
    return private_method_testing_info

def check_for_type_4_2_private_method(index_i, func_in_test, test_func_info, test_files):
    private_method_testing_info = []
    private_func_name_in_test = ''

    for i in range(len(func_in_test[index_i])):
        if 'Whitebox' in str(func_in_test[index_i][i]) and 'invokeMethod' in str(func_in_test[index_i][i]):
            func_name = test_func_info[index_i][i][3]
            test_func_content = find_func(test_files[index_i], func_name)
            for statement in test_func_content:
                if 'Whitebox' in statement and 'invokeMethod' in statement:
                    useful_content = statement.split('invokeMethod')[1]
                    # useful_content_2 = statement.split('invokeMethod')[0]
                    private_func_name_in_test, arguments = get_arguments(useful_content, 1)
                    info = (test_files[index_i], test_func_info[index_i][i][3], private_func_name_in_test, arguments)
                    private_method_testing_info.append(info)
    return private_method_testing_info

def check_for_type_5_private_method(index_i, func_in_test, test_func_info, test_files):
    private_method_testing_info = []
    private_func_name_in_test = ''

    for i in range(len(func_in_test[index_i])):
        if 'MemberMatcher' in str(func_in_test[index_i][i]) and 'method' in str(func_in_test[index_i][i]):
            func_name = test_func_info[index_i][i][3]
            test_func_content = find_func(test_files[index_i], func_name)
            for statement in test_func_content:
                if 'MemberMatcher' in statement and 'method' in statement:
                    useful_content = statement.split('method')[1]
                    private_func_name_in_test, arguments = get_arguments(useful_content, 1)
                    info = (test_files[index_i], test_func_info[index_i][i][3], private_func_name_in_test, arguments)
                    private_method_testing_info.append(info)
    return private_method_testing_info

def get_arguments(statement, num):
    token = '('
    func_name = ''
    arguments = []
    func_ = match_token(statement, token).replace('(', '').replace(')', '').replace(';','')

    if len(func_.split(',')) > num:
        func_name = func_.split(',')[num].replace('"', '')
        arguments = func_.split(',')
    elif ',' not in func_:
        func_name = func_.replace('"', '')

    return func_name, arguments

def compare_testing_and_production_result(private_func_name_in_test, arguments, private_production_func_info):
    private_method_testing = None
    private_func_name_in_test = str(private_func_name_in_test).replace('"', '')
    for i in range(len(private_production_func_info)):
        if private_func_name_in_test == str(private_production_func_info[i][3]):
            if (arguments == [] or arguments == None) and (len(private_production_func_info[i][4]) == 0):
                private_method_testing = private_production_func_info[i]
            elif arguments != [] and arguments != None:
                if len(arguments) - 1 == len(private_production_func_info[i][4]):
                        # if str(private_production_func_info[i][4][i].name) in str(arguments[i]) or str(private_production_func_info[i][4][i].name) == str(arguments[i]):
                    private_method_testing = private_production_func_info[i]
    return private_method_testing

def run_TS_1(project):
    all_files = get_all_java_files(project)
    test_files, production_files = distinguish_test_and_production_file(all_files)
    func_in_test, test_import_info, test_files_new = get_func_in_test_file(test_files, [], [])
    func_in_produc_code, import_info, production_files_new = get_production_func(production_files, [], [])
    test_func_info = get_func_info_file(func_in_test, test_files_new, [])
    production_func_info = get_func_info_file(func_in_produc_code, production_files_new, [])
    private_production_func_info = get_private_production_func_info(production_func_info)
    result = analysis_import_info_for_private_method_testing(test_import_info, test_func_info, test_files_new, func_in_test, private_production_func_info)
    return len(result), result


    