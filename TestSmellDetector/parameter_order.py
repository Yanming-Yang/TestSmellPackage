# from selectors import EpollSelector
# from this import s
from turtle import st
from process_project import get_all_java_files, get_datafile, find_func, match_token
from generate_AST import get_statement_type_list_in_test_func, get_func_in_test_file, distinguish_test_and_production_file, get_func_info, get_production_func, get_func_info_file

Basic_type = ['List', 'String', 'Map', 'Byte', 'HashMap']

def process_assertEquals_ForStatement(sta, paras_ast):
    statements = sta.body
    if statements != None:
        for sta_For in statements:
            if 'assertEquals' in str(sta_For) and 'StatementExpression' in str(type(sta_For)):
                if 'MethodInvocation' in str(type(sta_For.expression)) and 'assertEquals' == str(sta_For.expression.member):
                    paras_ast = sta_For.expression.arguments
            elif 'assertEquals' in str(sta_For) and 'IfStatement' in str(type(sta_For)):
                paras_ast = process_assertEquals_IfStatement(sta_For, paras_ast)
            elif 'assertEquals' in str(sta_For) and 'ForStatement' in str(type(sta_For)):
                paras_ast = process_assertEquals_ForStatement(sta_For, paras_ast)
            elif 'assertEquals' in str(sta_For) and 'TryStatement' in str(type(sta_For)):
                paras_ast = process_assertEquals_TryStatement(sta_For, paras_ast)
            elif 'assertEquals' in str(sta_For) and 'BlockStatement' in str(type(sta_For)):
                paras_ast = process_assertEquals_BlockStatement(sta_For, paras_ast)
            elif 'assertEquals' in str(sta_For) and 'WhileStatement' in str(type(sta_For)):
                paras_ast = process_assertEquals_WhileStatement(sta_For, paras_ast)
            elif 'assertEquals' in str(sta_For) and 'SwitchStatement' in str(type(sta_For)):
                paras_ast = process_assertEquals_SwitchStatement(sta_For, paras_ast)
            elif 'assertEquals' in str(sta_For) and 'SynchronizedStatement' in str(type(sta_For)):
                paras_ast = process_assertEquals_SynchronizedStatement(sta_For, paras_ast)
            elif 'assertEquals' in str(sta_For) and 'DoStatement' in str(type(sta_For)):
                paras_ast = process_assertEquals_DoStatement(sta_For, paras_ast)
            elif 'assertEquals' in str(sta_For) and 'LocalVariableDeclaration' in str(type(sta_For)):
                paras_ast = process_assertEquals_LocalVariableDeclaration(sta_For, paras_ast)
            elif 'assertEquals' in str(sta_For):
                paras_ast = normal_statement_process(sta_For, paras_ast)
    return paras_ast

def process_assertEquals_IfStatement(sta, paras_ast):
    if 'assertEquals' in str(sta.else_statement):
        if sta.else_statement != None and 'IfStatement' in str(type(sta.else_statement)):
            paras_ast = process_assertEquals_IfStatement(sta.else_statement, paras_ast)
        elif sta.else_statement != None and 'ForStatement' in str(type(sta.else_statement)):
            paras_ast = process_assertEquals_ForStatement(sta.else_statement, paras_ast)
        elif sta.else_statement != None and 'TryStatement' in str(type(sta.else_statement)):
            paras_ast = process_assertEquals_TryStatement(sta.else_statement, paras_ast)
        elif sta.else_statement != None and 'BlockStatement' in str(type(sta.else_statement)):
            paras_ast = process_assertEquals_BlockStatement(sta.else_statement, paras_ast)
        elif sta.else_statement != None and 'WhileStatement' in str(type(sta.else_statement)):
            paras_ast = process_assertEquals_WhileStatement(sta.else_statement, paras_ast)
        elif sta.else_statement != None and 'SwitchStatement' in str(type(sta.else_statement)):
            paras_ast = process_assertEquals_SwitchStatement(sta.else_statement, paras_ast)
        elif sta.else_statement != None and 'SynchronizedStatement' in str(type(sta.else_statement)):
            paras_ast = process_assertEquals_SynchronizedStatement(sta.else_statement, paras_ast)
        elif sta.else_statement != None and 'DoStatement' in str(type(sta.else_statement)):
            paras_ast = process_assertEquals_DoStatement(sta.else_statement, paras_ast)
        elif sta.else_statement != None and 'LocalVariableDeclaration' in str(type(sta.else_statement)):
            paras_ast = process_assertEquals_LocalVariableDeclaration(sta.else_statement, paras_ast)
        elif sta.else_statement != None:
            paras_ast = normal_statement_process(sta.else_statement, paras_ast)
        else:
            print(sta.else_statement)
    else:
        if sta.then_statement != None and 'IfStatement' in str(type(sta.then_statement)):
            paras_ast = process_assertEquals_IfStatement(sta.then_statement, paras_ast)
        elif sta.then_statement != None and 'ForStatement' in str(type(sta.then_statement)):
            paras_ast = process_assertEquals_ForStatement(sta.then_statement, paras_ast)
        elif sta.then_statement != None and 'TryStatement' in str(type(sta.then_statement)):
            paras_ast = process_assertEquals_TryStatement(sta.then_statement, paras_ast)
        elif sta.then_statement != None and 'BlockStatement' in str(type(sta.then_statement)):
            paras_ast = process_assertEquals_BlockStatement(sta.then_statement, paras_ast)
        elif sta.then_statement != None and 'WhileStatement' in str(type(sta.then_statement)):
            paras_ast = process_assertEquals_WhileStatement(sta.then_statement, paras_ast)
        elif sta.then_statement != None and 'SwitchStatement' in str(type(sta.then_statement)):
            paras_ast = process_assertEquals_SwitchStatement(sta.then_statement, paras_ast)
        elif sta.else_statement != None and 'SynchronizedStatement' in str(type(sta.then_statement)):
            paras_ast = process_assertEquals_SynchronizedStatement(sta.then_statement, paras_ast)
        elif sta.else_statement != None and 'DoStatement' in str(type(sta.then_statement)):
            paras_ast = process_assertEquals_DoStatement(sta.then_statement, paras_ast)
        elif sta.else_statement != None and 'LocalVariableDeclaration' in str(type(sta.then_statement)):
            paras_ast = process_assertEquals_LocalVariableDeclaration(sta.then_statement, paras_ast)
        elif sta.else_statement != None:
            paras_ast = normal_statement_process(sta.then_statement, paras_ast)
        else:
            print(sta.else_statement)

    return paras_ast

def process_assertEquals_SynchronizedStatement(sta, paras_ast):
    block = sta.block
    if block != None:
        for block_sta in block:
            if 'assertEquals' in str(block_sta) and 'StatementExpression' in str(type(block_sta)):
                if 'MethodInvocation' in str(type(block_sta.expression)) and 'assertEquals' == str(block_sta.expression.member):
                    paras_ast = block_sta.expression.arguments
            elif 'assertEquals' in str(block_sta) and 'ForStatement' in str(type(block_sta)):
                    paras_ast = process_assertEquals_ForStatement(block_sta, paras_ast)
            elif 'assertEquals' in str(block_sta) and 'IfStatement' in str(type(block_sta)):
                    paras_ast = process_assertEquals_IfStatement(block_sta, paras_ast)
            elif 'assertEquals' in str(block_sta) and 'TryStatement' in str(type(block_sta)):
                paras_ast = process_assertEquals_TryStatement(block_sta, paras_ast)
            elif 'assertEquals' in str(block_sta) and 'BlockStatement' in str(type(block_sta)):
                paras_ast = process_assertEquals_BlockStatement(block_sta, paras_ast)
            elif 'assertEquals' in str(block_sta) and 'WhileStatement' in str(type(block_sta)):
                paras_ast = process_assertEquals_WhileStatement(block_sta, paras_ast)
            elif 'assertEquals' in str(block_sta) and 'SwitchStatement' in str(type(block_sta)):
                paras_ast = process_assertEquals_SwitchStatement(block_sta, paras_ast)
            elif 'assertEquals' in str(block_sta) and 'SynchronizedStatement' in str(type(block_sta)):
                paras_ast = process_assertEquals_SynchronizedStatement(block_sta, paras_ast)
            elif 'assertEquals' in str(block_sta) and 'DoStatement' in str(type(block_sta)):
                paras_ast = process_assertEquals_DoStatement(block_sta, paras_ast)
            elif 'assertEquals' in str(block_sta) and 'LocalVariableDeclaration' in str(type(block_sta)):
                paras_ast = process_assertEquals_LocalVariableDeclaration(block_sta, paras_ast)
            elif 'assertEquals' in str(block_sta):
                paras_ast = normal_statement_process(block_sta, paras_ast)
    return paras_ast


def process_assertEquals_TryStatement(sta, paras_ast):
    block =  sta.block
    catches = sta.catches #catches list catch[0].block
    if block != None:
        for block_sta in block:
            if 'assertEquals' in str(block_sta) and 'StatementExpression' in str(type(block_sta)):
                if 'MethodInvocation' in str(type(block_sta.expression)) and 'assertEquals' == str(block_sta.expression.member):
                    paras_ast = block_sta.expression.arguments
            elif 'assertEquals' in str(block_sta) and 'ForStatement' in str(type(block_sta)):
                paras_ast = process_assertEquals_ForStatement(block_sta, paras_ast)
            elif 'assertEquals' in str(block_sta) and 'IfStatement' in str(type(block_sta)):
                paras_ast = process_assertEquals_IfStatement(block_sta, paras_ast)
            elif 'assertEquals' in str(block_sta) and 'TryStatement' in str(type(block_sta)):
                paras_ast = process_assertEquals_TryStatement(block_sta, paras_ast)
            elif 'assertEquals' in str(block_sta) and 'BlockStatement' in str(type(block_sta)):
                paras_ast = process_assertEquals_BlockStatement(block_sta, paras_ast)
            elif 'assertEquals' in str(block_sta) and 'WhileStatement' in str(type(block_sta)):
                paras_ast = process_assertEquals_WhileStatement(block_sta, paras_ast)
            elif 'assertEquals' in str(block_sta) and 'SwitchStatement' in str(type(block_sta)):
                paras_ast = process_assertEquals_SwitchStatement(block_sta, paras_ast)
            elif 'assertEquals' in str(block_sta) and 'SynchronizedStatement' in str(type(block_sta)):
                paras_ast = process_assertEquals_SynchronizedStatement(block_sta, paras_ast)
            elif 'assertEquals' in str(block_sta) and 'DoStatement' in str(type(block_sta)):
                paras_ast = process_assertEquals_DoStatement(block_sta, paras_ast)
            elif 'assertEquals' in str(block_sta) and 'LocalVariableDeclaration' in str(type(block_sta)):
                paras_ast = process_assertEquals_LocalVariableDeclaration(block_sta, paras_ast)
            elif 'assertEquals' in str(block_sta):
                paras_ast = normal_statement_process(block_sta, paras_ast)

    if catches != None:
        for catch in catches:
            for block_sta in catch.block:
                if 'assertEquals' in str(block_sta) and 'StatementExpression' in str(type(block_sta)):
                    if 'MethodInvocation' in str(type(block_sta.expression)) and 'assertEquals' == str(block_sta.expression.member):
                        paras_ast = block_sta.expression.arguments
                elif 'assertEquals' in str(block_sta) and 'ForStatement' in str(type(block_sta)):
                    paras_ast = process_assertEquals_ForStatement(block_sta, paras_ast)
                elif 'assertEquals' in str(block_sta) and 'IfStatement' in str(type(block_sta)):
                    paras_ast = process_assertEquals_IfStatement(block_sta, paras_ast)
                elif 'assertEquals' in str(block_sta) and 'TryStatement' in str(type(block_sta)):
                    paras_ast = process_assertEquals_TryStatement(block_sta, paras_ast)
                elif 'assertEquals' in str(block_sta) and 'BlockStatement' in str(type(block_sta)):
                    paras_ast = process_assertEquals_BlockStatement(block_sta, paras_ast)
                elif 'assertEquals' in str(block_sta) and 'WhileStatement' in str(type(block_sta)):
                    paras_ast = process_assertEquals_WhileStatement(block_sta, paras_ast)
                elif 'assertEquals' in str(block_sta) and 'SwitchStatement' in str(type(block_sta)):
                    paras_ast = process_assertEquals_SwitchStatement(block_sta, paras_ast)
                elif 'assertEquals' in str(block_sta) and 'SynchronizedStatement' in str(type(block_sta)):
                    paras_ast = process_assertEquals_SynchronizedStatement(block_sta, paras_ast)
                elif 'assertEquals' in str(block_sta) and 'DoStatement' in str(type(block_sta)):
                    paras_ast = process_assertEquals_DoStatement(block_sta, paras_ast)
                elif 'assertEquals' in str(block_sta) and 'LocalVariableDeclaration' in str(type(block_sta)):
                    paras_ast = process_assertEquals_LocalVariableDeclaration(block_sta, paras_ast)
                elif 'assertEquals' in str(block_sta):
                    paras_ast = normal_statement_process(block_sta, paras_ast)
    return paras_ast

def process_assertEquals_BlockStatement(sta, paras_ast):
    statements = sta.statements
    if statements != None:
        for sta_block in statements:
            if 'assertEquals' in str(sta_block) and 'StatementExpression' in str(type(sta_block)):
                if 'MethodInvocation' in str(type(sta_block.expression)) and 'assertEquals' == str(sta_block.expression.member):
                    paras_ast = sta_block.expression.arguments
            elif 'assertEquals' in str(sta_block) and 'IfStatement' in str(type(sta_block)):
                paras_ast = process_assertEquals_IfStatement(sta_block, paras_ast)
            elif 'assertEquals' in str(sta_block) and 'ForStatement' in str(type(sta_block)):
                paras_ast = process_assertEquals_ForStatement(sta_block, paras_ast)
            elif 'assertEquals' in str(sta_block) and 'TryStatement' in str(type(sta_block)):
                paras_ast = process_assertEquals_TryStatement(sta_block, paras_ast)
            elif 'assertEquals' in str(sta_block) and 'BlockStatement' in str(type(sta_block)):
                paras_ast = process_assertEquals_BlockStatement(sta_block, paras_ast)
            elif 'assertEquals' in str(sta_block) and 'WhileStatement' in str(type(sta_block)):
                paras_ast = process_assertEquals_WhileStatement(sta_block, paras_ast)
            elif 'assertEquals' in str(sta_block) and 'SwitchStatement' in str(type(sta_block)):
                paras_ast = process_assertEquals_SwitchStatement(sta_block, paras_ast)
            elif 'assertEquals' in str(sta_block) and 'SynchronizedStatement' in str(type(sta_block)):
                paras_ast = process_assertEquals_SynchronizedStatement(sta_block, paras_ast)
            elif 'assertEquals' in str(sta_block) and 'DoStatement' in str(type(sta_block)):
                paras_ast = process_assertEquals_DoStatement(sta_block, paras_ast)
            elif 'assertEquals' in str(sta_block) and 'LocalVariableDeclaration' in str(type(sta_block)):
                paras_ast = process_assertEquals_LocalVariableDeclaration(sta_block, paras_ast)
            elif 'assertEquals' in str(sta_block):
                paras_ast = normal_statement_process(sta_block, paras_ast)
    return paras_ast

def process_assertEquals_WhileStatement(sta, paras_ast):
    sta_while = sta.body
    if sta_while != None:
        if 'assertEquals' in str(sta_while) and 'StatementExpression' in str(type(sta_while)):
            if 'MethodInvocation' in str(type(sta_while.expression)) and 'assertEquals' == str(sta_while.expression.member):
                paras_ast = sta_while.expression.arguments
        elif 'assertEquals' in str(sta_while) and 'IfStatement' in str(type(sta_while)):
            paras_ast = process_assertEquals_IfStatement(sta_while, paras_ast)
        elif 'assertEquals' in str(sta_while) and 'ForStatement' in str(type(sta_while)):
            paras_ast = process_assertEquals_ForStatement(sta_while, paras_ast)
        elif 'assertEquals' in str(sta_while) and 'TryStatement' in str(type(sta_while)):
            paras_ast = process_assertEquals_TryStatement(sta_while, paras_ast)
        elif 'assertEquals' in str(sta_while) and 'BlockStatement' in str(type(sta_while)):
            paras_ast = process_assertEquals_BlockStatement(sta_while, paras_ast)
        elif 'assertEquals' in str(sta_while) and 'WhileStatement' in str(type(sta_while)):
            paras_ast = process_assertEquals_WhileStatement(sta_while, paras_ast)
        elif 'assertEquals' in str(sta_while) and 'SwitchStatement' in str(type(sta_while)):
            paras_ast = process_assertEquals_SwitchStatement(sta_while, paras_ast)
        elif 'assertEquals' in str(sta_while) and 'SynchronizedStatement' in str(type(sta_while)):
            paras_ast = process_assertEquals_SynchronizedStatement(sta_while, paras_ast)
        elif 'assertEquals' in str(sta_while) and 'DoStatement' in str(type(sta_while)):
            paras_ast = process_assertEquals_DoStatement(sta_while, paras_ast)
        elif 'assertEquals' in str(sta_while) and 'LocalVariableDeclaration' in str(type(sta_while)):
            paras_ast = process_assertEquals_LocalVariableDeclaration(sta_while, paras_ast)
        elif 'assertEquals' in str(sta_while):
            paras_ast = normal_statement_process(sta_while, paras_ast)
    return paras_ast

def process_assertEquals_DoStatement(sta, paras_ast):
    sta_do = sta.body
    if sta_do != None:
        if 'assertEquals' in str(sta_do) and 'StatementExpression' in str(type(sta_do)):
            if 'MethodInvocation' in str(type(sta_do.expression)) and 'assertEquals' == str(sta_do.expression.member):
                paras_ast = sta_do.expression.arguments
        elif 'assertEquals' in str(sta_do) and 'IfStatement' in str(type(sta_do)):
            paras_ast = process_assertEquals_IfStatement(sta_do, paras_ast)
        elif 'assertEquals' in str(sta_do) and 'ForStatement' in str(type(sta_do)):
            paras_ast = process_assertEquals_ForStatement(sta_do, paras_ast)
        elif 'assertEquals' in str(sta_do) and 'TryStatement' in str(type(sta_do)):
            paras_ast = process_assertEquals_TryStatement(sta_do, paras_ast)
        elif 'assertEquals' in str(sta_do) and 'BlockStatement' in str(type(sta_do)):
            paras_ast = process_assertEquals_BlockStatement(sta_do, paras_ast)
        elif 'assertEquals' in str(sta_do) and 'WhileStatement' in str(type(sta_do)):
            paras_ast = process_assertEquals_WhileStatement(sta_do, paras_ast)
        elif 'assertEquals' in str(sta_do) and 'SwitchStatement' in str(type(sta_do)):
            paras_ast = process_assertEquals_SwitchStatement(sta_do, paras_ast)
        elif 'assertEquals' in str(sta_do) and 'SynchronizedStatement' in str(type(sta_do)):
            paras_ast = process_assertEquals_SynchronizedStatement(sta_do, paras_ast)
        elif 'assertEquals' in str(sta_do) and 'DoStatement' in str(type(sta_do)):
            paras_ast = process_assertEquals_DoStatement(sta_do, paras_ast)
        elif 'assertEquals' in str(sta_do) and 'LocalVariableDeclaration' in str(type(sta_do)):
            paras_ast = process_assertEquals_LocalVariableDeclaration(sta_do, paras_ast)
        elif 'assertEquals' in str(sta_do):
            paras_ast = normal_statement_process(sta_do, paras_ast)
    return paras_ast


def process_assertEquals_SwitchStatement(sta, paras_ast):
    switch_cases = sta.cases
    if switch_cases != None:
        for case in switch_cases:
            case_sta = case.statements
            for sta in case_sta:
                if 'assertEquals' in str(sta) and 'StatementExpression' in str(type(sta)):
                    if 'MethodInvocation' in str(type(sta.expression)) and 'assertEquals' == str(sta.expression.member):
                        paras_ast = sta.expression.arguments
                elif 'assertEquals' in str(sta) and 'IfStatement' in str(type(sta)):
                    paras_ast = process_assertEquals_IfStatement(sta, paras_ast)
                elif 'assertEquals' in str(sta) and 'ForStatement' in str(type(sta)):
                    paras_ast = process_assertEquals_ForStatement(sta, paras_ast)
                elif 'assertEquals' in str(sta) and 'TryStatement' in str(type(sta)):
                    paras_ast = process_assertEquals_TryStatement(sta, paras_ast)
                elif 'assertEquals' in str(sta) and 'BlockStatement' in str(type(sta)):
                    paras_ast = process_assertEquals_BlockStatement(sta, paras_ast)
                elif 'assertEquals' in str(sta) and 'WhileStatement' in str(type(sta)):
                    paras_ast = process_assertEquals_WhileStatement(sta, paras_ast)
                elif 'assertEquals' in str(sta) and 'SwitchStatement' in str(type(sta)):
                    paras_ast = process_assertEquals_SwitchStatement(sta, paras_ast)
                elif 'assertEquals' in str(sta) and 'SynchronizedStatement' in str(type(sta)):
                    paras_ast = process_assertEquals_SynchronizedStatement(sta, paras_ast)
                elif 'assertEquals' in str(sta) and 'DoStatement' in str(type(sta)):
                    paras_ast = process_assertEquals_DoStatement(sta, paras_ast)
                elif 'assertEquals' in str(sta) and 'LocalVariableDeclaration' in str(type(sta)):
                    paras_ast = process_assertEquals_LocalVariableDeclaration(sta, paras_ast)
                elif 'assertEquals' in str(sta):
                    paras_ast = normal_statement_process(sta, paras_ast)
    return paras_ast

def process_assertEquals_LocalVariableDeclaration(sta, paras_ast):
    sta_local_varible = sta.declarators
    if sta_local_varible != None:
        for declarator in sta_local_varible:
            sta_local = declarator.initializer
            if 'assertEquals' in str(sta_local) and 'StatementExpression' in str(type(sta_local)):
                if 'MethodInvocation' in str(type(sta_local.expression)) and 'assertEquals' == str(sta_local.expression.member):
                    paras_ast = sta_local.expression.arguments
            elif 'assertEquals' in str(sta_local) and 'IfStatement' in str(type(sta_local)):
                paras_ast = process_assertEquals_IfStatement(sta_local, paras_ast)
            elif 'assertEquals' in str(sta_local) and 'ForStatement' in str(type(sta_local)):
                paras_ast = process_assertEquals_ForStatement(sta_local, paras_ast)
            elif 'assertEquals' in str(sta_local) and 'TryStatement' in str(type(sta_local)):
                paras_ast = process_assertEquals_TryStatement(sta_local, paras_ast)
            elif 'assertEquals' in str(sta_local) and 'BlockStatement' in str(type(sta_local)):
                paras_ast = process_assertEquals_BlockStatement(sta_local, paras_ast)
            elif 'assertEquals' in str(sta_local) and 'WhileStatement' in str(type(sta_local)):
                paras_ast = process_assertEquals_WhileStatement(sta_local, paras_ast)
            elif 'assertEquals' in str(sta_local) and 'SwitchStatement' in str(type(sta_local)):
                paras_ast = process_assertEquals_SwitchStatement(sta_local, paras_ast)
            elif 'assertEquals' in str(sta_local) and 'SynchronizedStatement' in str(type(sta_local)):
                paras_ast = process_assertEquals_SynchronizedStatement(sta_local, paras_ast)
            elif 'assertEquals' in str(sta_local) and 'DoStatement' in str(type(sta_local)):
                paras_ast = process_assertEquals_DoStatement(sta_local, paras_ast)
            elif 'assertEquals' in str(sta_local) and 'LocalVariableDeclaration' in str(type(sta_local)):
                paras_ast = process_assertEquals_LocalVariableDeclaration(sta_local, paras_ast)
            elif 'assertEquals' in str(sta_local):
                paras_ast = normal_statement_process(sta_local, paras_ast)
            
    return paras_ast


def process_return_statement(sta, paras_ast):
    sta_return = sta.expression
    normal_statement_process(sta_return, paras_ast)
    return paras_ast

def normal_statement_process(sta, paras_ast):
    if 'StatementExpression' in str(type(sta)):
        paras_ast = sta.expression.arguments
    elif 'ClassCreator' in str(type(sta)):
        sta_creator = sta.body
        if sta_creator != None:
            for sta_return in sta_creator:
                if 'assertEquals' in str(sta_return) and 'StatementExpression' in str(type(sta_return)):
                    if 'MethodInvocation' in str(type(sta_return.expression)) and 'assertEquals' == str(sta_return.expression.member):
                        paras_ast = sta_return.expression.arguments
                elif 'assertEquals' in str(sta_return) and 'IfStatement' in str(type(sta_return)):
                    paras_ast = process_assertEquals_IfStatement(sta_return, paras_ast)
                elif 'assertEquals' in str(sta_return) and 'ForStatement' in str(type(sta_return)):
                    paras_ast = process_assertEquals_ForStatement(sta_return, paras_ast)
                elif 'assertEquals' in str(sta_return) and 'TryStatement' in str(type(sta_return)):
                    paras_ast = process_assertEquals_TryStatement(sta_return, paras_ast)
                elif 'assertEquals' in str(sta_return) and 'BlockStatement' in str(type(sta_return)):
                    paras_ast = process_assertEquals_BlockStatement(sta_return, paras_ast)
                elif 'assertEquals' in str(sta_return) and 'WhileStatement' in str(type(sta_return)):
                    paras_ast = process_assertEquals_WhileStatement(sta_return, paras_ast)
                elif 'assertEquals' in str(sta_return) and 'SwitchStatement' in str(type(sta_return)):
                    paras_ast = process_assertEquals_SwitchStatement(sta_return, paras_ast)
                elif 'assertEquals' in str(sta_return) and 'SynchronizedStatement' in str(type(sta_return)):
                    paras_ast = process_assertEquals_SynchronizedStatement(sta_return, paras_ast)
                elif 'assertEquals' in str(sta_return) and 'DoStatement' in str(type(sta_return)):
                    paras_ast = process_assertEquals_DoStatement(sta_return, paras_ast)
                elif 'assertEquals' in str(sta_return) and 'LocalVariableDeclaration' in str(type(sta_return)):
                    paras_ast = process_assertEquals_LocalVariableDeclaration(sta_return, paras_ast)
                elif 'assertEquals' in str(sta_return):
                    paras_ast = normal_statement_process(sta_return, paras_ast)

    return paras_ast


def detect_parameter_order(func, func_ast, func_name, funcs_names_list, position):
    paras_token = []
    paras_asts = []
    wrong_para_order = []
    for i in range(len(func_ast)):
        try:
            if 'assertEquals' in str(func_ast[i]) or 'assertSame' in str(func_ast[i]) or 'assertArrayEquals' in str(func_ast[i]) or 'assertNotSame' in str(func_ast[i]) or 'assertEqualsNoOrder' in str(func_ast[i]):
                paras_ast = []
                if 'StatementExpression' in str(type(func_ast[i])):
                    if 'MethodInvocation' in str(type(func_ast[i].expression)) and 'assertEquals' == str(func_ast[i].expression.member):
                        paras_ast = func_ast[i].expression.arguments
                elif 'TryStatement' in str(type(func_ast[i])):
                    paras_ast = process_assertEquals_TryStatement(func_ast[i], paras_ast)
                elif 'ForStatement' in str(type(func_ast[i])):
                    paras_ast = process_assertEquals_ForStatement(func_ast[i], paras_ast)
                elif 'IfStatement' in str(type(func_ast[i])):
                    paras_ast = process_assertEquals_IfStatement(func_ast[i], paras_ast)
                elif 'BlockStatement' in str(type(func_ast[i])):
                    paras_ast = process_assertEquals_BlockStatement(func_ast[i], paras_ast)
                elif 'WhileStatement' in str(type(func_ast[i])):
                    paras_ast = process_assertEquals_WhileStatement(func_ast[i], paras_ast)
                elif 'SwitchStatement' in str(type(func_ast[i])):
                    paras_ast = process_assertEquals_SwitchStatement(func_ast[i], paras_ast)
                elif 'ReturnStatement' in str(type(func_ast[i])):
                    paras_ast = process_return_statement(func_ast[i], paras_ast)
                elif 'SynchronizedStatement' in str(type(func_ast[i])):
                    paras_ast = process_assertEquals_SynchronizedStatement(func_ast[i], paras_ast)
                elif 'DoStatement' in str(type(func_ast[i])):
                    paras_ast = process_assertEquals_DoStatement(func_ast[i], paras_ast)
                elif 'LocalVariableDeclaration' in str(type(func_ast[i])):
                    paras_ast = process_assertEquals_LocalVariableDeclaration(func_ast[i], paras_ast)
                elif 'ClassCreator' in str(type(func_ast[i])):
                    paras_ast = normal_statement_process(func_ast[i], paras_ast)
                else:
                    print(str(type(func_ast[i])))
                    print(func_ast[i])

                paras_ = []
                if paras_ast != None:
                    for para in paras_ast:
                        if 'Literal' in str(type(para)):
                            paras_.append(para.value)
                        elif 'MemberReference' in str(type(para)):
                            paras_.append(para.member)
                        elif 'MethodInvocation' in str(type(para)):
                            tmp_str = str(para.qualifier) + '.' + str(para.member) + '(' + str(para.arguments) + ')'
                            paras_.append(tmp_str)
                        elif 'Cast' in str(type(para)):
                            if 'MethodInvocation' in str(type(para.expression)):
                                paras_.append(para.expression.member)
                        elif 'ClassCreator' in str(type(para)):
                            paras_.append(para.type.name)
                        else:
                            paras_.append(para)
            
                    if len(paras_ast) > 1 and len(paras_) > 1:
                        paras_asts.append((func_name, paras_ast))
                        paras_token.append((func_name, paras_))
        except RecursionError as e:
            pass

    for i in range(len(paras_asts)):
        position_ = position
        if len(paras_asts[i]) > 0 and len(paras_asts[i][1]) > 1 and len(paras_token[i][1]) > 1:
            if position == 1 and len(paras_asts[i][1]) == 3 and len(paras_token[i][1]) == 3:
                if 'Literal' in str(type(paras_asts[i][1][0])) and '"' in paras_asts[i][1][0].value:
                    position_ = position_ + 1
                elif 'MethodInvocation' in str(type(paras_asts[i][1][0])) and 'essage' in str(paras_asts[i][1][0]):
                    position_ = position_ + 1
            
            if 'Literal' in str(type(paras_asts[i][1][position_])):
                wrong_para_order.append(paras_asts)
            elif 'MemberReference' in str(type(paras_asts[i][1][position_])) and len(para_occurance_times(paras_token[i][1][position_], func_ast)) > 0:
                for j in range(len(para_occurance_times(paras_token[i][1][position_], func_ast))):
                    if 'LocalVariableDeclaration' in str(type(func_ast[j])):
                        for declarator in func_ast[j].declarators:
                            if paras_token[i][1][position] == str(declarator.name):
                                if 'Literal' in str(type(declarator.initializer)):
                                    wrong_para_order.append(paras_asts)
                                elif 'ClassCreator' in str(type(declarator.initializer)) and str(declarator.initializer.type.name) in Basic_type:
                                    wrong_para_order.append(paras_asts)
        # elif len(paras_asts[i]) > 0 and len(paras_asts[i][1]) <= 1:
        #     print(paras_asts[i])
        
    return wrong_para_order  
                    
def para_occurance_times(para, func_ast):
    times = []
    for i in range(len(func_ast)):
        if para in func_ast[i]:
            times.append(i)
    return times

def detect_para_order_in_project(project):
    para_order_wrong = []
    func_in_produc_code = []
    import_info = []
    func_in_test = []
    test_import_info = []

    test_files, production_files = distinguish_test_and_production_file(get_all_java_files(project))
    func_in_produc_code, import_info, production_files_new = get_production_func(production_files, func_in_produc_code, import_info)
    func_in_test, test_import_info, test_file_new = get_func_in_test_file(test_files, func_in_test, test_import_info)
    func_in_test_info = get_func_info(func_in_test, [])
    production_func_info = get_func_info(func_in_produc_code, [])
    func_in_test_info_2 = get_func_info_file(func_in_test, test_file_new, [])

    production_name_info = [func[3] for func in production_func_info]

    index = 0
    for i in range(len(func_in_test)):
        import_info_file = test_import_info[i]
        flag = -1
        position = -1

        if import_info_file != None:
            for import_ in import_info_file:
                if 'org.testng.Assert' in str(import_):
                    flag = 0
            for import_ in import_info_file:
                if 'org.junit.Assert' in str(import_):
                    flag = 1

        if flag == 1:
            position = 1
        elif flag == 0:
            position = 0

        if flag != -1:
            for j in range(len(func_in_test[i])):
                index = count_index(func_in_test, i, j)
                test_func_name = func_in_test_info_2[i][j][3]
                func_str = find_func(test_files[i], test_func_name)
                func_ast = func_in_test[i][j]
                result = []
                if func_ast != None and func_ast.body != None:
                    result = detect_parameter_order(func_str, func_ast.body, test_func_name, production_name_info, position)
                if len(result) > 0:
                    para_order_wrong.append((test_files[i], result))

    return para_order_wrong

def count_index(func_in_test, i, j):
    index = 0
    if i > 0:
        for i_ in range(i):
            index = index + len(func_in_test[i_]) - 1
        index = index + j + 1
    else:
        index = j
    return index


def run_TS_4(project):
    para_order_wrong = detect_para_order_in_project(project)
    print(len(para_order_wrong))
    return len(para_order_wrong), para_order_wrong


