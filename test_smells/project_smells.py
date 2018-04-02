from test_smells.test_smell import TestSmell

class EagerTest(TestSmell):
    name = "Lazy Test"
    
    def test_for_smell(self, file_list):
        dummy_code_call(self, file_list)
        
class LazyTest(TestSmell):
    name = "Lazy Test"
    
    def test_for_smell(self, file_list):
        dummy_code_call(self, file_list)
    
def dummy_code_call(smell, file_list):
    print("{0} runs on project".format(smell.name))   