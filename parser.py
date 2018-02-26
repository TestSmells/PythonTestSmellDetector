import os
import re
import ast
import argparse
import sys


def get_python_files(directory):
    """List python files in directory.

    Return a list of all python files in the given directory. This
    includes the contents of subdirectories.

    Note: fails if the it receives non-raw string input with single '\'
        symbols
    """

    output = list()

    for root, dirs, files in os.walk(directory):
        for file in files:
            python_file_pattern = re.compile(".*.py$")
            if python_file_pattern.match(file):
                output.append(os.path.abspath(os.path.join(directory, file)))
    return output


def filter_python_files(files):
    """Remove files that do not perform unit testing

    Returns the given list of files with all the files that do not
    perform unit testing removed. All non python files, files that do
    not import unittest, and files that do not contain any test cases
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
    """List test methods in each test case AST.

    Return a list of test method ASTs from a given test case AST.
    """

    pass


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


def main():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("directory", type=str,
                        help="Directory to detect test smells.")
    args = parser.parse_args()
    if len(sys.argv) < 1:
        parser.print_help()
    else:
        if os.path.exists(args.directory) or os.path.isdir(args.directory):
            files = get_python_files(os.path.abspath(args.directory))
            filteredFiles = filter_python_files(files)
            for f in filteredFiles:
                getTestCases = get_test_case_asts(f)
        else:
            print("Invalid path given.")

if __name__ == '__main__':
    main()
