from generate_AST import distinguish_test_and_production_file
from process_project import get_all_java_files, get_file_suffix, get_folder_section, get_folder_path
import difflib

def test_folder_into_production(folder, production_files):
    flag = 0
    test_production_folder = folder.replace('/test/', '/main/')
    for production_file in production_files:
        produc_file = get_folder_path(production_file)
        if difflib.SequenceMatcher(None, produc_file, test_production_folder).quick_ratio() > 0.8:
            flag = 1
            break
    return flag

def detector_test_and_production_file_organization(project):
    all_files = get_all_java_files(project)
    test_files, production_files = distinguish_test_and_production_file(all_files)
    flag_count = 0
    bad_organization = []
    bad_organization_files = []
    for test_file in test_files:
        test_folder = get_folder_path(test_file)
        flag = test_folder_into_production(test_folder, production_files)
        flag_count = flag_count + flag
        if flag == 0:
            bad_organization_files.append(test_file)
    
    if len(test_files) != 0 and float(flag_count) / float(len(test_files)) < 0.5:
        bad_organization.append((project, bad_organization_files))
        print(bad_organization)
    return bad_organization


def detector_test_and_production_file_organization_old(project):
    all_files = get_all_java_files(project)
    test_files, production_files = distinguish_test_and_production_file(all_files)

    mapping_file_pair = []

    for test_file in test_files:
        file_suffix = get_file_suffix(test_file)
        file_suffix_production = file_suffix.replace('Test', '')
        
        for production_file in production_files:
            if file_suffix_production == get_file_suffix(production_file):
                mapping_file_pair.append((test_file, production_file))

    diff_test = []
    bad_organization = 0
    for file_pair in mapping_file_pair:
        test_file = file_pair[0]
        production_file = file_pair[1]

        test_folder = get_folder_section(test_file)
        production_folder = get_folder_section(production_file)

        if len(test_folder) != len(production_folder):
            bad_organization = bad_organization + 1
        else:
            for i in range(len(test_folder)):
                diff_location = 0
                if test_folder[i] != production_folder[i]:
                    diff_location = diff_location + 1
                diff_test.append(diff_location)

    for diff in diff_test:
        if diff > 1:
            bad_organization = bad_organization + 1
    
    if len(mapping_file_pair) > 0:
        bad_organization_ratio = float(float(bad_organization) / float(len(mapping_file_pair)))
    else:
        bad_organization_ratio = 1
    if len(test_files) > 0:
        test_mapping_ratio = float(float(len(mapping_file_pair)) / float(len(test_files)))
    else:
        test_mapping_ratio = 0
    
    if bad_organization_ratio >= 0.8:
        print(project + ' dones follow the organization best practice!')
        return 1
    else:
        print(project + ' does not follows the organization best practice!')
        return 0

def run_TS_3(project):
    result = detector_test_and_production_file_organization(project)
    print(result)
    return len(result), result



                




            



            
        

    




