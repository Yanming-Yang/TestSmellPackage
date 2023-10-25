from generate_AST import get_classes_info, distinguish_test_and_production_file, get_funcs, get_AST, get_production_func
from process_project import get_all_java_files, get_datafile, find_func, match_token
import javalang

def get_funcs_in_file(production_files):
    func_in_files = []
    production_file_new = []
    func_in_produc_code, import_info, production_files_new = get_production_func(production_files, [], [])
    for production_file in production_files_new:
        flag = 0

        if 'Test' not in production_file or 'test' not in production_file:
            try:
                tree = get_AST(production_file)
                if tree != None:
                    classes_in_file = get_classes_info(tree)
                    func_in_files.append(get_funcs(classes_in_file))
                    production_file_new.append(production_file)
            except  javalang.parser.JavaSyntaxError as e:
                continue 
    return func_in_files, production_file_new

def detect_test_in_production(func_in_files, production_file_new):
    test_in_production = []
    for i in range(len(func_in_files)):
        for func in func_in_files[i]:
            annotations = func.annotations
            if annotations != None:
                for anno in annotations:
                    if 'Test' == str(anno.name):
                        test_in_production.append((production_file_new[i], func.name))
    return test_in_production


def run_TS_7(project):
    projects = []
    all_files = get_all_java_files(project)
    test_files, production_files = distinguish_test_and_production_file(all_files)
    func_in_files, production_file_new = get_funcs_in_file(production_files)
    test_in_production = detect_test_in_production(func_in_files, production_file_new)

    try:
        if len(production_file_new) != 0 and float(float(len(test_in_production)) / float(len(production_file_new))) >= 0.5:
            projects.append(projects)
    except ZeroDivisionError as e:
        pass

    for i in projects:
        print(i)
    return len(test_in_production), test_in_production
    # return len(project), project





        


    
