from test_smells.test_smell import TestSmell
from test_smells.smell_visitor import SmellVisitor

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
    name = "General Fixture"
    
    def test_for_smell(self, test_case_ast):
        dummy_code_call(self, test_case_ast)
    
    
def dummy_code_call(smell,test_case_ast):
    print("{0} runs on {1}".format(smell.name,test_case_ast.name))   
