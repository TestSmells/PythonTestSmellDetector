import python_parser
from test_smell_rule_runners import project_rule_runner
from test_smell_rule_runners import test_case_rule_runner
from test_smell_rule_runners import test_method_rule_runner
import argparse
import sys
import os

def main():
    """Check given project directory for code smells
    
    Identifies all of the python files in the directory (including those in sub 
    directories). Submits files through 3 stages of rule checking based on the 
    scope of the rules (project level, test case level, and test method level).
    Results from all tests are aggregated
    """
    argument_parser = argparse.ArgumentParser(add_help=True)
    argument_parser.add_argument("directory", type=str,
                        help="Directory to detect test smells.")
    args = argument_parser.parse_args()
    
    if len(sys.argv) < 1:
    
        argument_parser.print_help()
        
    else:
    
        if os.path.exists(args.directory) or os.path.isdir(args.directory):

            #Stage 1: project level rule checking
            files = python_parser.get_python_files(os.path.abspath(args.directory))
            results_list = project_rule_runner(files)
            
            #Stage 2: test case level rule checking
            #test_case_pairs_list is a list of test cases paired with their file of origin
            filtered_files = python_parser.filter_python_files(files)
            test_case_pairs_list = python_parser.get_test_case_asts(filtered_files)
            
            for test_case_pair in test_case_pairs_list:
                results_list = results_list + test_case_rule_runner(test_case_pair)
                
            #Stage 3: test method level rule checking
            test_method_list = list()
            
            for test_case_pair in test_case_pairs_list:
                test_method_list = test_method_list + python_parser.get_test_asts(test_case_pair)
            
            for test_method in test_method_list: 
                results_list = results_list + test_method_rule_runner(test_method)
            
            #Output formatting
            format_output(results_list)
            
        else:
            print("Invalid path given.")

            
def format_output(results_list):

    reordered_results = list()

    for result in results_list:
        new_result = None
        
        if len(result) == 2:
            new_result = (result[1], result[0])
            reordered_results.append(new_result)
        
        elif len(result) == 3:
            new_result = (result[2], result[1], result[0])
            reordered_results.append(new_result)

    output_file = "output.txt"
    
    try:
        os.remove(output_file)
    except:
        pass
    
    writing_to = open(output_file, 'w')
    
    for result in reordered_results:
        print(result)
        writing_to.write(str(result) + '\n')
            
            
if __name__ == '__main__':
    main()
    pass