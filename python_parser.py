import os
import re
import ast
import sys

                
def get_python_files(directory):
    """
    Return a list of all python files in the given directory. This 
    includes the contents of subdirectories.
    Note: fails if the it receives non-raw string input with single '\' 
        symbols
    """
    
    output = list()

    for path, dirs, files in os.walk(directory):
        for file in files:
            python_file_pattern = re.compile(".*.py$")

            if python_file_pattern.match(file):
                output.append(os.path.abspath(os.path.join(path, file)))
    return output


def filter_python_files(files):
    """Remove files that do not perform unit testing
    will be removed.    
    """

    for file in files:
        with open(file, 'r') as f:
            tree = ast.parse(f.read())
            imports = get_imports(tree)
            if 'unittest' in imports:
                continue
            else:
                files.remove(file)
    return files


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


    #are checking for
    return is_descendant_of(inheritance_dictionary,inheritance_dictionary[child],parent)
    
def get_test_case_asts(file_list):
    """return an object for each TestCase
    
    Return an of ASTs for each test case in the given python file.
    
    Note: Currently does not support multi-base inheritance structures
    """
    #a list of tuples that pairs class definition asts with their file of 
    #origin
    class_asts = list()
 
    for file in file_list:

        #convert file to ast
        working_file = open(file).read()
        file_ast = ast.parse(working_file, file)

        #discover all of the class definitions in the file ast
        for node in file_ast.body:
            if(isinstance(node, ast.ClassDef)):
                pair = node, file
                class_asts.append(pair)
        
    for pair in class_asts:
        baseVisitor = BaseClassVisitor() 
        baseVisitor.visit(pair[0])
            
    #the key of the inheritance_dictionary is a child class, the value is that 
    #class's parent.
    inheritance_dictionary = baseVisitor.inheritance
    
    #a list of names of the file's test cases
    test_case_names = list()
    
    #discover if each class is a TestCase
    for key, value in baseVisitor.inheritance.items():
        if(is_descendant_of(inheritance_dictionary,key,"TestCase")):
            test_case_names.append(key)
    
    test_case_asts = list()
    #checks each class AST against the list of classes that inherit from 
    #TestCase to isolate the test case ASTs
    for pair in class_asts:
        if(pair[0].name in test_case_names):
            test_case = ParsedTestCase(pair[1],pair[0].name)
            test_case_asts.append(pair[0])
            
    return test_case_asts

def get_test_asts(testcase_ast):
    """List test methods in each test case AST.

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
        
    for node in method_asts:
        if(test_method_pattern.match(node.name)):
            test_method_asts.append(node)
            
    return test_method_asts

        
class BaseClassVisitor(ast.NodeVisitor):
    """Visits AST nodes to find each class's bass classes.

    return a list of base classes for each file.

    Note: Currently does not support multi-base inheritance structures.
    """
    # the key is a child class, the value is that classes parent

    inheritance = dict()

    def visit_ClassDef(self, node):
        for base in node.bases:
            try:
                self.inheritance[node.name] = base.attr
            except:
                pass

            try:
                self.inheritance[node.name] = base.id
            except:
                pass


class ImportVisitor(ast.NodeVisitor):
    """Visits AST nodes to find imports in each file.

    Return import names in each file.
    """
    def visit_Import(self, node):
        for alias in node.names:
            return alias.name

def get_imports(tree):
    """Gets imports using the import visitor.

    Return a list of imports from a given tree.
    """
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            importVisitor = ImportVisitor()
            t = importVisitor.visit_Import(node)
            imports.append(t)
    return imports
    

class ParsedTestCase:
    """Represents a single unittest test case
    
    An object that associates the name of a given unittest test case 
    with its file and with a list of ASTs, one for each of its test methods.
    """

    def __init__(self,file_,test_case_name_):
        self.file = file_
        self.test_case_name = test_case_name_
        self.method_asts = list()
