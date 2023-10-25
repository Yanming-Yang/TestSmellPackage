from generate_AST import get_statement_type_list_in_test_func, get_func_in_test_file, distinguish_test_and_production_file, get_func_info, get_func_info_file
from process_project import get_all_java_files, get_datafile, find_func, match_token

def detect_random_num(project):
    random_test_cases = []
    func_in_test = []
    test_import_info = []
    test_func_info = []
    
    test_files, _ = distinguish_test_and_production_file(get_all_java_files(project))
    func_in_test, test_import_info, test_files_new = get_func_in_test_file(test_files, func_in_test, test_import_info)


    test_func_info = get_func_info(func_in_test, test_func_info)
    func_in_test_info_2 = get_func_info_file(func_in_test, test_files_new, [])

    if len(test_files_new) > 0 and test_import_info != None:
        for i in range(len(test_files_new)):
            flag = 0
            if test_import_info[i] != None:
                for import_info in test_import_info[i]:
                    if 'java.util.Random' in import_info.path or 'java.util.*' in import_info.path or 'RandomStringUtils' in import_info.path:
                        flag = 1
            try:
                for j in range(len(func_in_test[i])):
                    if ('Random' in str(func_in_test[i][j]) or 'random' in str(func_in_test[i][j])) and flag == 1:      
                        file_name = test_files_new[i]
                        func_name = func_in_test_info_2[i][j]
                        detect_create_new_random_with_para(func_in_test[i][j], random_test_cases, file_name, func_name)
        
            except RecursionError as e:
                pass
    print(random_test_cases)
    return list(set(random_test_cases))

def detect_create_new_random_with_para(func, random_test_cases, file_name, func_name):
    test_func_content = find_func(file_name, func_name[3]) 
    flag_2 = 0
    flag = 0
    if 'seed' in str(test_func_content) or 'Seed' in str(test_func_content):
        flag_2 = 1

    if 'System.nanoTime' in str(test_func_content) or 'System.currentTimeMillis' in str(test_func_content):
        flag = 1

    if 'Random(seed)' in str(test_func_content) and flag == 1 and flag_2 == 1:
        random_test_cases.append(str(file_name) + '|' + str(func_name))

    # if 'Math' in str(sta) and 'random' in str(sta):
    #     random_test_cases.append(str(file_name) + '|' + str(func_name))
    if 'Math.random()' in str(test_func_content):
        random_test_cases.append(str(file_name) + '|' + str(func_name))

    if 'new Random()' in str(test_func_content) or 'new Random( )' in str(test_func_content):
        random_test_cases.append(str(file_name) + '|' + str(func_name)) 

    if 'Random()' in str(test_func_content):
        random_test_cases.append(str(file_name) + '|' + str(func_name)) 

    if 'RandomStringUtils.' in str(test_func_content) and flag_2 == 0:
        random_test_cases.append(str(file_name) + '|' + str(func_name)) 

    if func.body != None and len(func.body) > 0:
        for sta in func.body:
            if 'LocalVariableDeclaration' in str(type(sta)):
                if flag != 1:
                    flag = sta_fo_time_seed(sta, flag)
                if 'random' in str(sta) or 'Random' in str(sta):
                    sta_for_random(sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'ForStatement' in  str(type(sta)):
                process_ForStatement(sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'TryStatement' in str(type(sta)):
                process_TryStatement(sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'IfStatement' in str(type(sta)):
                process_IfStatement(sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'BlockStatement' in str(type(sta)):
                process_BlockStatement(sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'WhileStatement' in str(type(sta)):
                process_WhileStatement(sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'SwitchStatement' in str(type(sta)):
                process_SwitchStatement(sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'SynchronizedStatement' in str(type(sta)):
                process_SynchronizedStatement(sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'DoStatement' in str(type(sta)):
                process_DoStatement(sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
                


def sta_fo_time_seed(sta, flag):
    if 'VariableDeclarator' in str(type(sta.declarators[0])) and 'MethodInvocation' in str(type(sta.declarators[0].initializer)):
        if (str(sta.declarators[0].initializer.qualifier) == 'System' and  str(sta.declarators[0].initializer.member) == 'nanoTime') or (str(sta.declarators[0].initializer.qualifier) == 'System' and  str(sta.declarators[0].initializer.member) == 'currentTimeMillis'):
            flag = 1
    return flag

def sta_for_random(sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content):
    if 'VariableDeclarator' in str(type(sta.declarators[0])) and 'ClassCreator' in str(type(sta.declarators[0].initializer)):
        arguments = sta.declarators[0].initializer.arguments
        if len(arguments) == 1 and flag == 1 and flag_2 == 1 and 'MemberReference' in str(type(arguments[0])) and (str(arguments[0].member) == 'seed' or str(arguments[0].member) == 'Seed'):
            random_test_cases.append(str(file_name) + '|' + str(func_name))
        elif len(arguments) == 0 or 'new Random( )' in str(test_func_content) or 'new Random()' in str(test_func_content):
            # if 'seed' not in str(test_func_content) and 'Seed' not in str(test_func_content):
            print(file_name)
            random_test_cases.append(str(file_name) + '|' + str(func_name))
    elif 'new Random()' in str(test_func_content):
        random_test_cases.append(str(file_name) + '|' + str(func_name))



def process_ForStatement(sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content):
    statements = sta.body
    if statements != None:
        for sta_For in statements:
            if 'LocalVariableDeclaration' in str(type(sta_For)):
                if flag != 1:
                    flag = sta_fo_time_seed(sta_For, flag)
                if 'random' in str(sta_For) or 'Random' in str(sta_For):
                    sta_for_random(sta_For, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'IfStatement' in str(type(sta_For)):
                process_IfStatement(sta_For, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'ForStatement' in str(type(sta_For)):
                process_ForStatement(sta_For, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'TryStatement' in str(type(sta_For)):
                process_TryStatement(sta_For, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'BlockStatement' in str(type(sta_For)):
                process_BlockStatement(sta_For, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'WhileStatement' in str(type(sta_For)):
                process_WhileStatement(sta_For, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'SwitchStatement' in str(type(sta_For)):
                process_SwitchStatement(sta_For, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'SynchronizedStatement' in str(type(sta_For)):
                process_SynchronizedStatement(sta_For, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'DoStatement' in str(type(sta_For)):
                process_DoStatement(sta_For, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)


def process_TryStatement(sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content):
    block =  sta.block
    catches = sta.catches #catches list catch[0].block
    if block != None:
        for block_sta in block:
            if 'LocalVariableDeclaration' in str(type(block_sta)):
                if flag != 1:
                    flag = sta_fo_time_seed(block_sta, flag)
                if 'random' in str(block_sta) or 'Random' in str(block_sta):
                    sta_for_random(block_sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'ForStatement' in str(type(block_sta)):
                process_ForStatement(block_sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'IfStatement' in str(type(block_sta)):
                process_IfStatement(block_sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'TryStatement' in str(type(block_sta)):
                process_TryStatement(block_sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'BlockStatement' in str(type(block_sta)):
                process_BlockStatement(block_sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'WhileStatement' in str(type(block_sta)):
                process_WhileStatement(block_sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'SwitchStatement' in str(type(block_sta)):
                process_SwitchStatement(block_sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'SynchronizedStatement' in str(type(block_sta)):
                process_SynchronizedStatement(block_sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'DoStatement' in str(type(block_sta)):
                process_DoStatement(block_sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
           
    if catches != None:
        for catch in catches:
            for block_sta in catch.block:
                if 'LocalVariableDeclaration' in str(type(block_sta)):
                    if flag != 1:
                        flag = sta_fo_time_seed(block_sta, flag)
                    if 'random' in str(block_sta) or 'Random' in str(block_sta):
                        sta_for_random(block_sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
                elif 'ForStatement' in str(type(block_sta)):
                    process_ForStatement(block_sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
                elif 'TryStatement' in str(type(block_sta)):
                    process_TryStatement(block_sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
                elif 'IfStatement' in str(type(block_sta)):
                    process_IfStatement(block_sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
                elif 'BlockStatement' in str(type(block_sta)):
                    process_BlockStatement(block_sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
                elif 'WhileStatement' in str(type(block_sta)):
                    process_WhileStatement(block_sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
                elif 'SwitchStatement' in str(type(block_sta)):
                    process_SwitchStatement(block_sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
                elif 'SynchronizedStatement' in str(type(block_sta)):
                    process_SynchronizedStatement(block_sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
                elif 'DoStatement' in str(type(block_sta)):
                    process_DoStatement(block_sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)


def process_IfStatement(sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content):
    if 'random' in str(sta.else_statement) or 'Random' in str(sta.else_statement):
        if sta.else_statement != None and 'IfStatement' in str(type(sta.else_statement)):
            process_IfStatement(sta.else_statement, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
        elif sta.else_statement != None and 'ForStatement' in str(type(sta.else_statement)):
            process_ForStatement(sta.else_statement, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
        elif sta.else_statement != None and 'TryStatement' in str(type(sta.else_statement)):
            process_TryStatement(sta.else_statement, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
        elif sta.else_statement != None and 'BlockStatement' in str(type(sta.else_statement)):
            process_BlockStatement(sta.else_statement, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
        elif sta.else_statement != None and 'WhileStatement' in str(type(sta.else_statement)):
            process_WhileStatement(sta.else_statement, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
        elif sta.else_statement != None and 'SwitchStatement' in str(type(sta.else_statement)):
            process_SwitchStatement(sta.else_statement, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
        elif sta.else_statement != None and 'SynchronizedStatement' in str(type(sta.else_statement)):
            process_SynchronizedStatement(sta.else_statement, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
        elif sta.else_statement != None and 'DoStatement' in str(type(sta.else_statement)):
            process_DoStatement(sta.else_statement, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
      
    elif 'random' in str(sta.then_statement) or 'Random' in str(sta.then_statement):
        if sta.then_statement != None and 'IfStatement' in str(type(sta.then_statement)):
            process_IfStatement(sta.then_statement, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
        elif sta.then_statement != None and 'ForStatement' in str(type(sta.then_statement)):
            process_ForStatement(sta.then_statement, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
        elif sta.then_statement != None and 'TryStatement' in str(type(sta.then_statement)):
            process_TryStatement(sta.then_statement, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
        elif sta.then_statement != None and 'BlockStatement' in str(type(sta.then_statement)):
            process_BlockStatement(sta.then_statement, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
        elif sta.then_statement != None and 'WhileStatement' in str(type(sta.then_statement)):
            process_WhileStatement(sta.then_statement, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
        elif sta.then_statement != None and 'SwitchStatement' in str(type(sta.then_statement)):
            process_SwitchStatement(sta.then_statement, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
        elif sta.else_statement != None and 'SynchronizedStatement' in str(type(sta.then_statement)):
            process_SynchronizedStatement(sta.then_statement, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
        elif sta.else_statement != None and 'DoStatement' in str(type(sta.then_statement)):
            process_DoStatement(sta.then_statement, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
       

def process_SynchronizedStatement(sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content):
    block = sta.block
    if block != None:
        for block_sta in block:
            if 'LocalVariableDeclaration' in str(type(block_sta)):
                if flag != 1:
                    flag = sta_fo_time_seed(block_sta, flag)
                if 'random' in str(block_sta) or 'Random' in str(block_sta):
                    sta_for_random(block_sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'ForStatement' in str(type(block_sta)):
                process_ForStatement(block_sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'IfStatement' in str(type(block_sta)):
                process_IfStatement(block_sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'TryStatement' in str(type(block_sta)):
                process_TryStatement(block_sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'BlockStatement' in str(type(block_sta)):
                process_BlockStatement(block_sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'WhileStatement' in str(type(block_sta)):
                process_WhileStatement(block_sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'SwitchStatement' in str(type(block_sta)):
                process_SwitchStatement(block_sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'SynchronizedStatement' in str(type(block_sta)):
                process_SynchronizedStatement(block_sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'DoStatement' in str(type(block_sta)):
                process_DoStatement(block_sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
          
def process_BlockStatement(sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content):
    statements = sta.statements
    if statements != None:
        for sta_block in statements:
            if 'LocalVariableDeclaration' in str(type(sta_block)):
                if flag != 1:
                    flag = sta_fo_time_seed(sta_block, flag)
                if 'random' in str(sta_block) or 'Random' in str(sta_block):
                    sta_for_random(sta_block, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'IfStatement' in str(type(sta_block)):
                process_IfStatement(sta_block, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'ForStatement' in str(type(sta_block)):
                process_ForStatement(sta_block, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'TryStatement' in str(type(sta_block)):
                process_TryStatement(sta_block, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'BlockStatement' in str(type(sta_block)):
                process_BlockStatement(sta_block, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'WhileStatement' in str(type(sta_block)):
                process_WhileStatement(sta_block, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'SwitchStatement' in str(type(sta_block)):
                process_SwitchStatement(sta_block, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'SynchronizedStatement' in str(type(sta_block)):
                process_SynchronizedStatement(sta_block, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'DoStatement' in str(type(sta_block)):
                process_DoStatement(sta_block, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
          
def process_WhileStatement(sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content):
    sta_while = sta.body
    if sta_while != None:
        if 'random' in str(sta_while) and 'Random' in str(type(sta_while)):
        # if 'LocalVariableDeclaration' in str(type(sta_while)):
        #         if flag != 1:
        #             flag = sta_fo_time_seed(sta_while, flag)
        #         if 'random' in str(sta_while) or 'Random' in str(sta_while):
        #             sta_for_random(sta_while, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            if 'IfStatement' in str(type(sta_while)):
                process_IfStatement(sta_while, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'ForStatement' in str(type(sta_while)):
                process_ForStatement(sta_while, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'TryStatement' in str(type(sta_while)):
                process_TryStatement(sta_while, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'BlockStatement' in str(type(sta_while)):
                process_BlockStatement(sta_while, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'WhileStatement' in str(type(sta_while)):
                process_WhileStatement(sta_while, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'SwitchStatement' in str(type(sta_while)):
                process_SwitchStatement(sta_while, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'SynchronizedStatement' in str(type(sta_while)):
                process_SynchronizedStatement(sta_while, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            elif 'DoStatement' in str(type(sta_while)):
                process_DoStatement(sta_while, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
     
def process_DoStatement(sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content):
    sta_do = sta.body
    if sta_do != None:
        if 'LocalVariableDeclaration' in str(type(sta_do)):
            if flag != 1:
                flag = sta_fo_time_seed(sta_do, flag)
            if 'random' in str(sta_do) or 'Random' in str(sta_do):
                sta_for_random(sta_do, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
        elif 'IfStatement' in str(type(sta_do)):
            process_IfStatement(sta_do, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
        elif 'ForStatement' in str(type(sta_do)):
            process_ForStatement(sta_do, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
        elif 'TryStatement' in str(type(sta_do)):
            process_TryStatement(sta_do, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
        elif 'BlockStatement' in str(type(sta_do)):
            process_BlockStatement(sta_do, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
        elif 'WhileStatement' in str(type(sta_do)):
            process_WhileStatement(sta_do, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
        elif 'SwitchStatement' in str(type(sta_do)):
            process_SwitchStatement(sta_do, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
        elif 'SynchronizedStatement' in str(type(sta_do)):
            process_SynchronizedStatement(sta_do, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
        elif 'DoStatement' in str(type(sta_do)):
            process_DoStatement(sta_do, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
       
def process_SwitchStatement(sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content):
    switch_cases = sta.cases
    if switch_cases != None:
        for case in switch_cases:
            case_sta = case.statements
            for sta in case_sta:
                if 'LocalVariableDeclaration' in str(type(sta)):
                    if flag != 1:
                        flag = sta_fo_time_seed(sta, flag)
                    if 'random' in str(sta) or 'Random' in str(sta):
                        sta_for_random(sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
                elif 'IfStatement' in str(type(sta)):
                    process_IfStatement(sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
                elif 'ForStatement' in str(type(sta)):
                    process_ForStatement(sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
                elif 'TryStatement' in str(type(sta)):
                    process_TryStatement(sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
                elif 'BlockStatement' in str(type(sta)):
                    process_BlockStatement(sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
                elif 'WhileStatement' in str(type(sta)):
                    process_WhileStatement(sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
                elif 'SwitchStatement' in str(type(sta)):
                    process_SwitchStatement(sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
                elif 'SynchronizedStatement' in str(type(sta)):
                    process_SynchronizedStatement(sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
                elif 'DoStatement' in str(type(sta)):
                    process_DoStatement(sta, flag, flag_2, random_test_cases, file_name, func_name, test_func_content)
            
def run_TS_2(project):
    random_test_cases = detect_random_num(project)
    print(len(random_test_cases))
    return len(random_test_cases), random_test_cases








