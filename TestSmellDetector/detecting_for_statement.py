from generate_AST import get_statement_type_list_in_test_func, get_func_in_test_file, distinguish_test_and_production_file, get_func_info, get_func_info_file
from process_project import get_all_java_files, get_datafile, find_func, match_token


def detect_not_good_loop(project_path):
    func_in_test = []
    test_func_info = []
    test_import_info = []
    type_info_all_funcs = []

    ForStatementTestFunc = []

    test_files, _ = distinguish_test_and_production_file(get_all_java_files(project_path))
    func_in_test, test_import_info, test_files_new = get_func_in_test_file(test_files, func_in_test, test_import_info)
    type_info_all_funcs = get_statement_type_list_in_test_func(func_in_test, type_info_all_funcs)
    test_func_info = get_func_info(func_in_test, test_func_info)
    func_in_test_info_2 = get_func_info_file(func_in_test, test_files_new, [])

    for i in range(len(func_in_test)):
        for j in range(len(func_in_test[i])):
            flag_2 = 0
            if func_in_test[i][j].body != None:
                flag = 0
                for anno in func_in_test[i][j].annotations:
                    if 'Test' == str(anno.name):
                        flag = 1
                    if 'Test' == str(anno.name) and anno.element != None:
                        for ele in anno.element:
                            if str(ele.name) == 'enabled' and 'Literal' in str(type(ele.value)) and 'false' in str(ele.value.value):
                                flag = -1
                                break
                if flag == 1:
                    variables_type = []
                    variables_name = []
                    variables_time = []
                    for sta in func_in_test[i][j].body:
                        if 'LocalVariableDeclaration' in str(type(sta)) and len(func_in_test[i][j].body) == 2:
                            if 'VariableDeclarator' in str(type(sta.declarators[0])):
                                if 'Creator' in str(type(sta.declarators[0].initializer)):
                                    variables_name.append(str(sta.declarators[0].name))
                                    variables_type.append(str(sta.type.name))
                                elif 'MethodInvocation' in str(type(sta.declarators[0].initializer)):
                                    variables_name.append(str(sta.declarators[0].name))
                                    variables_type.append(str(sta.type.name))
                        if 'ForStatement' in str(type(sta)) and 'assert' in str(sta):
                            flag_2 = 1

                if flag_2 == 1 and flag == 1:   
                    # print(func_in_test_info_2[i][j][3])      
                    for sta in func_in_test[i][j].body:
                        if 'ForStatement' in str(type(sta)) and 'BlockStatement' in str(type(sta.body)):
                            if 'EnhancedForControl' in str(type(sta.control)):
                                for n in range(len(variables_name)):
                                    if variables_name[n] in str(sta.control) and variables_type[n] in str(sta.control):
                                        ForStatementTestFunc.append(str(test_files_new[i]) + '|' + str(func_in_test_info_2[i][j][3]))
                            elif 'ForControl' == str(type(sta.control)) and 'BinaryOperation' in str(type(sta.control.condition)):
                                for m in range(len(variables_name)):
                                    if variables_name[m] in str(sta.control.condition):
                                        ForStatementTestFunc.append(str(test_files_new[i]) + '|' + str(func_in_test_info_2[i][j][3]))
                            
    return list(set(ForStatementTestFunc))


def detect_for_statement(project_path):
    type_info = []
    func_in_test = []
    test_func_info = []
    test_import_info = []
    type_info_all_funcs = []

    ForStatementTestFunc = []
    ReturnStatementTestFunc = []
    WhileStatementTestFunc = []


    test_files, _ = distinguish_test_and_production_file(get_all_java_files(project_path))
    func_in_test, test_import_info, test_files_new = get_func_in_test_file(test_files, func_in_test, test_import_info)
    type_info_all_funcs = get_statement_type_list_in_test_func(func_in_test, type_info_all_funcs)
    test_func_info = get_func_info(func_in_test, test_func_info)
    func_in_test_info_2 = get_func_info_file(func_in_test, test_files_new, [])


    for i in range(len(func_in_test)):
        for j in range(len(func_in_test[i])):
            if func_in_test[i][j].body != None:
                flag = 0
                for anno in func_in_test[i][j].annotations:
                    if 'Test' == str(anno.name):
                        flag = 1
                    if 'Test' == str(anno.name) and anno.element != None:
                        for ele in anno.element:
                            if str(ele.name) == 'enabled' and 'Literal' in str(type(ele.value)) and 'false' in str(ele.value.value):
                                flag = -1
                                break
                if flag == 1:
                    for sta in func_in_test[i][j].body:
                        if 'ForStatement' in str(type(sta)) and 'BlockStatement' in str(type(sta.body)) and 'assert' in str(sta):
                            if 'condition' in sta.control.attrs and  'BinaryOperation' in str(type(sta.control.condition)):
                                if 'Literal' in str(type(sta.control.condition.operandr)) and type(sta.control.condition.operandr.value) == int:
                                    if str(type(sta.control.condition.operandr)) == 'MethodInvocation' and str(sta.control.condition.operandr.member) == 'len':
                                        for sta_block in sta.body.statements:
                                            if 'StatementExpression' in str(type(sta_block)) and 'MethodInvocation' in str(type(sta_block.expression)) and 'assert' in str(sta_block.expression.member):
                                                ForStatementTestFunc.append((func_in_test_info_2[i][j], test_files[i]))
                                                break
                                            elif 'StatementExpression' in str(type(sta.body)) and 'MethodInvocation' in str(type(sta.body.expression)) and 'assert' in str(sta.body.expression.member):
                                                ForStatementTestFunc.append((func_in_test_info_2[i][j], test_files[i]))
                                                break
                                            elif 'AssertStatement' in str(type(sta.body)):
                                                ForStatementTestFunc.append((func_in_test_info_2[i][j], test_files[i]))
                                                break
                                            else:
                                                print(sta.body)
                                elif 'EnhancedForControl' in str(type(sta.control)) and 'Literal' in str(type(sta.control.iterable)) and type(sta.control.iterable.value) == int:
                                    for sta_block in sta.body.statements:
                                        if 'StatementExpression' in str(type(sta_block)) and 'MethodInvocation' in str(type(sta_block.expression)) and 'assert' in str(sta_block.expression.member):
                                            ForStatementTestFunc.append((func_in_test_info_2[i][j], test_files[i]))
                                            break
                                        elif 'StatementExpression' in str(type(sta.body)) and 'MethodInvocation' in str(type(sta.body.expression)) and 'assert' in str(sta.body.expression.member):
                                            ForStatementTestFunc.append((func_in_test_info_2[i][j], test_files[i]))
                                            break
                                        elif 'AssertStatement' in str(type(sta.body)):
                                            ForStatementTestFunc.append((func_in_test_info_2[i][j], test_files[i]))
                                            break
                                        else:
                                            print(sta)
                                elif 'ForControl' in str(type(sta.control)) and 'BinaryOperation' in str(type(sta.control.condition)) and 'Literal' in str(type(sta.control.condition.operandr)) and type(sta.control.condition.operandr.value) == int:
                                    for sta_block in sta.body.statements:
                                        if 'StatementExpression' in str(type(sta_block)) and 'MethodInvocation' in str(type(sta_block.expression)) and 'assert' in str(sta_block.expression.member):
                                            ForStatementTestFunc.append((func_in_test_info_2[i][j], test_files[i]))
                                            break
                                        elif 'StatementExpression' in str(type(sta.body)) and 'MethodInvocation' in str(type(sta.body.expression)) and 'assert' in str(sta.body.expression.member):
                                            ForStatementTestFunc.append((func_in_test_info_2[i][j], test_files[i]))
                                            break
                                        elif 'AssertStatement' in str(type(sta.body)):
                                            ForStatementTestFunc.append((func_in_test_info_2[i][j], test_files[i]))
                                            break
                                        else:
                                            print(sta.body)
                                # else:
                                #     print(sta)

                        if 'WhileStatement' in str(type(sta)) and 'BlockStatement' in str(type(sta.body)):
                            if 'BinaryOperation' in str(type(sta.condition)) and 'Literal' in str(type(sta.condition.operandr)) and type(sta.condition.operandr.value) == int:
                                for sta_block in sta.body.statements:
                                    if 'StatementExpression' in str(type(sta_block)) and 'MethodInvocation' in str(type(sta_block.expression)) and 'assert' in str(sta_block.expression.member):
                                        ForStatementTestFunc.append((func_in_test_info_2[i][j], test_files[i]))
                                        WhileStatementTestFunc.append((func_in_test_info_2[i][j], test_files[i]))
                                        break
                            elif 'Literal' in str(type(sta.condition)):
                                for sta_block in sta.body.statements:
                                    if 'StatementExpression' in str(type(sta_block)) and 'MethodInvocation' in str(type(sta_block.expression)) and 'assert' in str(sta_block.expression.member):
                                        ForStatementTestFunc.append((func_in_test_info_2[i][j], test_files[i]))
                                        WhileStatementTestFunc.append((func_in_test_info_2[i][j], test_files[i]))
                                        break
                            # else:
                                # print(sta)


                        if 'ReturnStatement' in str(type(sta)) and sta.expression != None and 'null' not in str(sta) and flag != 0:
                            ReturnStatementTestFunc.append((func_in_test_info_2[i][j], test_files[i]))
                            break
                            
    return ForStatementTestFunc, ReturnStatementTestFunc, WhileStatementTestFunc


def run_TS_5_new(project):
    result = detect_not_good_loop(project)
    if result == None:
        result = []
    return len(result), result

def run_TS_5(project):
    ForStatementTestFunc, ReturnStatementTestFunc, WhileStatementTestFunc = detect_for_statement(project)
    # print(ForStatementTestFunc)
    print(WhileStatementTestFunc)
    return len(ForStatementTestFunc), ForStatementTestFunc

def run_TS_6(project):
    ForStatementTestFunc, ReturnStatementTestFunc, WhileStatementTestFunc = detect_for_statement(project)
    print(ReturnStatementTestFunc)
    return len(ReturnStatementTestFunc), ReturnStatementTestFunc








