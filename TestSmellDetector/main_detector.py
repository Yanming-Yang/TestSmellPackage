import argparse
import process_project as pp
import generate_AST as ga
import detect_random as dr
import detect_file_organization as dfo
import parameter_order as po
import detecting_for_statement as dfs
import detect_test_in_production as dtp



def main_detector(project, test_smell_types):
    result = []
    for type_ in test_smell_types:
        if int(type_) == 1:
            len_1, test_smell_1 = ga.run_TS_1(project)
            print('-----------------type 1-----------------')
            print(test_smell_1)
            print('-----------------end 1------------------')
            # return len_1, test_smell_1
        if int(type_) == 2:
            len_2, test_smell_2 = dr.run_TS_2(project)
            print('-----------------type 2-----------------')
            print(test_smell_2)
            print('-----------------end 2------------------')
            # return len_2, test_smell_2
        if int(type_) == 3:
            len_3, test_smell_3 = dfo.run_TS_3(project)
            print('-----------------type 3-----------------')
            print(test_smell_3)
            print('-----------------end 3------------------')
            # return len_3, test_smell_3
        if int(type_) == 4:
            len_4, test_smell_4 = po.run_TS_4(project)
            print('-----------------type 4-----------------')
            print(test_smell_4)
            print('-----------------end 4------------------')
            # return len_4, test_smell_4
        if int(type_) == 5:
            len_5, test_smell_5 = dfs.run_TS_5_new(project)
            print('-----------------type 5-----------------')
            print(test_smell_5)
            print('-----------------end 5------------------')
            # return len_5, test_smell_5
        if int(type_) == 6:
            len_6, test_smell_6 = dfs.run_TS_6(project)
            print('-----------------type 6-----------------')
            print(test_smell_6)
            print('-----------------end 6------------------')
            # return len_6, test_smell_6 
        if int(type_) == 7:
            len_7, test_smell_7 = dtp.run_TS_7(project)
            print('-----------------type 7-----------------')
            print(test_smell_7)
            print('-----------------end 7------------------')
            # return len_7, test_smell_7

def main_detector_2(project, test_smell_types):
    if int(test_smell_types) == 1:
        len_1, test_smell_1 = ga.run_TS_1(project)
        print(test_smell_1)
        return len_1, test_smell_1
    if int(test_smell_types) == 2:
        len_2, test_smell_2 = dr.run_TS_2(project)
        print(test_smell_2)
        return len_2, test_smell_2
    if int(test_smell_types) == 3:
        len_3, test_smell_3 = dfo.run_TS_3(project)
        print(test_smell_3)
        return len_3, test_smell_3
    if int(test_smell_types) == 4:
        len_4, test_smell_4 = po.run_TS_4(project)
        print(test_smell_4)
        return len_4, test_smell_4
    if int(test_smell_types) == 5:
        len_5, test_smell_5 = dfs.run_TS_5_new(project)
        print(test_smell_5)
        return len_5, test_smell_5
    if int(test_smell_types) == 6:
        len_6, test_smell_6 = dfs.run_TS_6(project)
        print(test_smell_6)
        return len_6, test_smell_6
    if int(test_smell_types) == 7:
        len_7, test_smell_7 = dtp.run_TS_7(project)
        print(test_smell_7)
        return len_7, test_smell_7

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='detect new type test smells.')
    parser.add_argument('-project', required=True, type=str, help='the path of software project that be tested smells.')
    parser.add_argument('-test_smell_types', required=True, nargs='+', type=str, help='the type of test smell you want to detect.')
    args = parser.parse_args()
    main_detector(args.project, args.test_smell_types)









    