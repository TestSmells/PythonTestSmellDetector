import os
import re
import ast

class BaseClassVisitor(ast.NodeVisitor):
    """Visits AST nodes to find each class's bass classes.
    
    return a list of base classes for each file.
    
    Note: Currently does not support multi-base inheritance structures
    """
    #the key is a child class, the value is that classes parent
    inheritance = dict()
    
    def visit_ClassDef(self,node):
        for base in node.bases:
            try:
                self.inheritance[node.name] = base.attr
            except:
                pass
                
            try:
                self.inheritance[node.name] = base.id
            except:
                pass
                
                
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
                output.append(os.path.join(directory, file).replace('\\', '/'))

    return output
    
    
def filter_python_files(files):
    """Remove files that do not perform unit testing
    
    Returns the given list of files with all the files that do not 
    perform unit testing removed. All non python files, files that do 
    not import unittest, and files that do not contain any test cases 
    will be removed.    
    """
    
    pass
    
    
def is_descendant_of(inheritance_dictionary, child, parent):
    """Tells if a given child class is a descendant of another class.

    the key of the inheritance_dictionary is a child class, the value is that 
    class's parent.
    """

    #base case 1: the child does not have a recorded parent class
    keys_list = inheritance_dictionary.keys()
    if child not in keys_list:
        return False
        
    #base case 2: the child's parent is the descendant we are checking for
    if(inheritance_dictionary[child] == parent):
        return True

    #recursive case: the child's parent is recorded but not the descendant we 
    #are checking for
    return is_descendant_of(inheritance_dictionary,inheritance_dictionary[child],parent)
    
    
def get_test_case_asts(file):
    """List test case ASTs in file
    
    Return a list of ASTs for each test case in the given python file.
    
    Note: Currently does not support multi-base inheritance structures
    
    Note: Only works for single file now. FIXING THIS IS IMPORTANT. 
    """
    
    #convert file to ast
    working_file = open(file).read()
    file_ast = ast.parse(working_file, file)
    
    class_asts = list()
    
    #discover all of the class definitions in the file ast
    for node in file_ast.body:
        if(isinstance(node, ast.ClassDef)):
            class_asts.append(node)
    
    for class_ast in class_asts:
        baseVisitor = BaseClassVisitor() 
        baseVisitor.visit(class_ast)
        
    #the key of the inheritance_dictionary is a child class, the value is that 
    #class's parent.
    inheritance_dictionary = baseVisitor.inheritance
    
    #a list of names of the file's test cases
    test_case_names = list()
    
    for key, value in baseVisitor.inheritance.items():
        if(is_descendant_of(inheritance_dictionary,key,"TestCase")):
            test_case_names.append(key)
    
    test_case_asts = list()
    
    #checks each class AST against the list of class names to isolate the test 
    #case ASTs
    for node in class_asts:
        if(node.name in test_case_names):
            test_case_asts.append(node)
            
    return test_case_asts
    
    
def get_test_asts(testcase_ast):
    """List tests in test case AST
    
    Return a list of test method ASTs from a given test case AST.
    
    Note: test_method_prefix should become an optional argument at a later time
    Note: should handle cases where runTest is overridden too
    """
    
    method_asts = list()
    
    #discover all the method definitions in the test case's AST
    for node in testcase_ast.body:
        if(isinstance(node, ast.FunctionDef)):
            method_asts.append(node)
            
    test_method_asts = list()
    
    test_method_prefix = "test"
        
    test_method_pattern = re.compile('{}\.*'.format(test_method_prefix))
        
    print(test_method_pattern.match("test_method_1"))
        
    for node in method_asts:
        if(test_method_pattern.match(node.name)):
            print(node.name)
            test_method_asts.append(node)
            
    return test_method_asts
        
    
class ParsedTestCase:
    """Represents a single unittest test case
    
    An object that associates the name of a given unittest test case 
    with its file and with ASTs for each of its test methods.
    """

    def __init__(self,file_,test_case_,method_ast_):
        self.file = file_
        self.test_case = test_case_
        self.method_ast = method_ast_
        
        