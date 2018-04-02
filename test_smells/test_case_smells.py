from test_smells.test_smell import TestSmell

class GeneralFixture(TestSmell):
    name = "General Fixture"
    
    def test_for_smell(self, test_case_ast):
        dummy_code_call(self, test_case_ast)
        
class ConstructorInitializaion(TestSmell):
    name = "General Fixture"
    
    def test_for_smell(self, test_case_ast):
        dummy_code_call(self, test_case_ast)
        
class DefaultTest(TestSmell):
    name = "General Fixture"
    
    def test_for_smell(self, test_case_ast):
        dummy_code_call(self, test_case_ast)
    
def dummy_code_call(smell,test_case_ast):
    print("{0} runs on {1}".format(smell.name,test_case_ast.name))   
