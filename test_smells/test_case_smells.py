from test_smells.test_smell import TestSmell
from test_smells.smell_visitor import SmellVisitor
import python_parser
import ast

class GeneralFixture(TestSmell):
    name = "General Fixture"
    
    def test_for_smell(self, test_case_ast):
        dummy_code_call(self, test_case_ast)
        
        
class ConstructorInitialization(TestSmell):
    name = "General Fixture"
    
    def __init__(self):
        self.name = "Constructor Initialization"
        self.visitor = ConstructorInitializationVisitor()
 
 
class ConstructorInitializationVisitor(SmellVisitor):

    def visit_FunctionDef(self, node):
        if(node.name == "__init__"):
            self.results["count"] += 1
            self.results["lines"].append(node.lineno)
            
        super().generic_visit(node)
       
        
class DefaultTest(TestSmell):
    
    def __init__(self):
        self.name = "Default Test"
        self.visitor = ConstructorInitializationVisitor()
        self.default_case_names = list()
        self.default_case_names.append("MyTestCase")
        
    def test_for_smell(self, ast):
        if(ast.name in self.default_case_names):
            return self.name
            
    
class GeneralFixture(TestSmell):

    def __init__(self):
        self.name = "General Fixture"
        self.visitor_1 = GeneralFixtureSetUpVisitor()
        self.visitor_2 = GeneralFixtureTestMethodVisitor()
        
    def test_for_smell(self, ast):
        
        self.visitor_1.visit(ast)
        
        #a list of attributes assigned in setUp
        attributes = self.visitor_1.attribute_lst
        
        #ast needs to be passed as a tuple because get_test_asts is
        #primarily for use by smell_detector
        test_methods = python_parser.get_test_asts((ast,None))
        
        for test in test_methods:
        
            self.visitor_2.visit(test[0])
            
        #remove all attributes found being used from the list
        attributes -= self.visitor_2.found_attributes   
        
        if(len(attributes) > 0):
            return self.name
        
        
class GeneralFixtureSetUpVisitor(SmellVisitor):
    def __init__(self):
        self.attribute_lst = set()
        super(GeneralFixtureSetUpVisitor,self).__init__()

    def visit_FunctionDef(self, node):
    
        setupMethodName = "setUp"
        
        if node.name == setupMethodName:

            #check all the items in the setUp function
            for body_item in ast.walk(node):
                if isinstance(body_item, ast.Assign): 

                    for target in body_item.targets:
                        try:
                            #ensure the assignment is to an attribute
                            if(target.value.id == "self"): 
                                self.attribute_lst.add(target.attr)
                                
                        except:
                            pass
                        
        else:
            pass
        super().generic_visit(node)
        
        
class GeneralFixtureTestMethodVisitor(SmellVisitor):

    def __init__(self):
        self.found_attributes = set()
        super(GeneralFixtureTestMethodVisitor,self).__init__()
    
    def visit_Attribute(self, node):
        if(node.value.id == "self"):
            self.found_attributes.add(node.attr)

    
    
def dummy_code_call(smell,test_case_ast):
    print("{0} runs on {1}".format(smell.name,test_case_ast.name))   
