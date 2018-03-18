import test_smell

class GeneralFixture(test_smell.TestSmell):
    name = "General Fixture"
    
    def test_for_smell(self, test_case_ast):
        dummy_code_call(self, test_case_ast)
        
class ConstructorInitializaion(test_smell.TestSmell):
    name = "General Fixture"
    
    def test_for_smell(self, test_case_ast):
        dummy_code_call(self, test_case_ast)
        
class DefaultTest(test_smell.TestSmell):
    name = "General Fixture"
    
    def test_for_smell(self, test_case_ast):
        dummy_code_call(self, test_case_ast)
    
def dummy_code_call(smell,test_case_ast):
    print("{0} runs on {1}".format(smell.name,test_case_ast.name))   
