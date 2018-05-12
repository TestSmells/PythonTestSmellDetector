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
    """Remove files that do not perform unit testing"""
    
    output = list()
    
    for file in files:
        with open(file, 'r', encoding="utf8") as f:
        
            #sometimes we get code written for older versions of python
            #the ast library can't handle these
            try:
                tree = ast.parse(f.read())
                 
                imports = get_imports(tree)
                if 'unittest' in imports:
                    output.append(file)
                else:
                    continue
                    
                f.close()
                
            except SyntaxError:
                print ("A syntax error occured while trying to read " +
                    "project files")
            
    return output
	
	
def filter_python_files_complement(files):
    """Remove files that perform unit testing"""

    output = list()
    
    for file in files:
        with open(file, 'r') as f:
            tree = ast.parse(f.read())
            imports = get_imports(tree)
            if 'unittest' not in imports:
                output.append(file)
            else:
                continue
            f.close()
    return output


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
        working_file = open(file, 'r', encoding="utf8").read()
        file_ast = ast.parse(working_file, file)

        #discover all of the class definitions in the file ast
        for node in file_ast.body:
            if(isinstance(node, ast.ClassDef)):
                #an ast node paired with its file of origin
                pair = node, file
                class_asts.append(pair)
      
    baseVisitor = BaseClassVisitor() 
    
    for pair in class_asts:
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
            test_case_asts.append(pair) 
            
    return test_case_asts

def get_test_asts(testcase_ast_pair):
    """List test methods in each test case AST.

    Return a list of test method ASTs from a given test case AST.
    
    Note: test_method_prefix should become an optional argument at a later time
    Note: should handle cases where runTest is overridden too
    """

    method_ast_pairs = list()
    #discover all the method definitions in the test case's AST
    for node in testcase_ast_pair[0].body:
        if(isinstance(node, ast.FunctionDef)):
        
            pair = node, testcase_ast_pair[1]
            method_ast_pairs.append(pair)
            
    test_method_ast_pairs = list()
    
    test_method_prefix = "test"
        
    test_method_pattern = re.compile('{}\.*'.format(test_method_prefix))
        
    for pair in method_ast_pairs:
        if(test_method_pattern.match(pair[0].name)):
            test_method_ast_pairs.append(pair)
            
    return test_method_ast_pairs
    
def get_classless_functions(file):
    """List functions in a given module
    
    Take a module ast and return a list of function asts that reside in the
    given module ast
    """
    
    visitor = ClasslessFunctionVisitor()
    
    open_file = open(file).read()
    
    file_ast = ast.parse(open_file)
    
    visitor = ClasslessFunctionVisitor()
    
    visitor.visit(file_ast)
    
    return visitor.function_list
    
    
    
    pass
    
    
def get_module_classes(file):
    """List classes in a given module
    
    Take a module ast and return a list of class asts that reside in the given 
    module ast
    """
    
    open_file = open(file).read()
    
    file_ast = ast.parse(open_file)
    
    output = list()
    
    for node in ast.walk(file_ast):
        if isinstance(node,ast.ClassDef):
            output.append(node)
            
    return output
 
    
def get_class_methods(class_ast):
    """List methods in a given class
    
    Take a class ast and return a list of method asts that reside in the given 
    module ast
    """
    output = list()
    
    #only checks definitions immediately in body to avoid nested class methods
    for node in class_ast.body:
        if isinstance(node,ast.FunctionDef):
            output.append(node.name)
    
    return output
        
        
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
    
    
class ClasslessFunctionVisitor(ast.NodeVisitor):
    """Visit each function that does not exist inside a class

    Given a module, store the name of each fuction that does not reside within a class
    """
    def __init__(self):
        self.function_list = list()

    def visit_ClassDef(self, node):
        pass
        
    def visit_FunctionDef(self, node):
        self.function_list.append(node.name)
    

class ParsedTestCase:
    """Represents a single unittest test case
    
    An object that associates the name of a given unittest test case 
    with its file and with a list of ASTs, one for each of its test methods.
    """

    def __init__(self,file_,test_case_name_):
        self.file = file_
        self.test_case_name = test_case_name_
        self.method_asts = list()
