import os
import re

def get_python_files(directory):
    """List python files in directory
    
    Return a list of all python files in the given directory. This 
    includes the contents of subdirectories.
    
    Note: fails if the it receives non-raw string input with single '\' 
        symbols
    """
    
    output = list()
    
    #print(directory)
    
    for root, dirs, files in os.walk(directory):
    
        for file in files:
            #print(os.path.join(directory, file))
            
            python_file_pattern = re.compile(".*.py$")
            
            if(python_file_pattern.match(file)):
                output.append(os.path.join(directory, file))

    return output
    
def filter_python_files(files):
    """Remove files that do not perform unit testing
    
    Returns the given list of files with all the files that do not 
    perform unit testing removed. All non python files, files that do 
    not import unittest, and files that do not contain any test cases 
    will be removed.
    """
    
    pass
    
def get_test_case_asts(file):
    """List test case ASTs in file
    
    Return a list of ASTs for each test case in the given python file.
    """
    
    pass
    
def get_test_asts(testcase_ast):
    """List tests in test case AST
    
    Return a list of test method ASTs from a given test case AST.
    """
    
    pass
    
class ParsedTestCase:
    """Represents a single unittest test case
    
    An object that associates the name of a given unittest test case 
    with its file and with ASTs for each of its test methods.
    """

    def __init__(self,file_,test_case_,method_ast_):
        self.file = file_
        self.test_case = test_case_
        self.method_ast = method_ast_
        
        