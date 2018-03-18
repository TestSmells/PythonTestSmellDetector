import test_smell

class EagerTest(test_smell.TestSmell):
    name = "Lazy Test"
    
    def test_for_smell(self, file_list):
        dummy_code_call(self, file_list)
        
class LazyTest(test_smell.TestSmell):
    name = "Lazy Test"
    
    def test_for_smell(self, file_list):
        dummy_code_call(self, file_list)
    
def dummy_code_call(smell, file_list):
    print("{0} runs on project".format(smell.name))   