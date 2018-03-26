import test_method_smells
import test_case_smells
import project_smells

def project_rule_runner(python_files):
    """Run rules that need the entire python project to detect a smell"""
    
    project_smell_list = list()
    project_smell_list.append(project_smells.EagerTest())
    
    output = list()
    
    for smell in project_smell_list:
    
        result = smell.test_for_smell(python_files)
        
        if result is not None:
            output = output + result
    
    return output
    
def test_case_rule_runner(test_case_ast_pair):
    """Run rules that only need a test case to detect a smell
    
    Accepts a pair with a test case AST and their file of origin, and runs each 
    of the defined test case rules on the AST."""
    
    test_case_smell_list = list()
    test_case_smell_list.append(test_case_smells.GeneralFixture())
    
    output = list()
    
    for smell in test_case_smell_list:
    
        result = smell.test_for_smell(test_case_ast_pair[0])
        
        if result is not None:
            output = output + result
    
    return output
    
def test_method_rule_runner(test_method_ast_pair):
    """Run rules that need the entire test method to detect a smell"""
    
    #all of the smells run in the test_method_rule_runner get added to the 
    #method_smell_list
    method_smell_list = list()
    method_smell_list.append(test_method_smells.MagicNumberTest())
    method_smell_list.append(test_method_smells.SensitiveEquality())
    method_smell_list.append(test_method_smells.ConditionalTestLogic())
    
    output = list()
    
    for smell in method_smell_list:
    
        result = smell.test_for_smell(test_method_ast_pair[0])
        
        if result is not None:
        
            result_pair = (result, test_method_ast_pair[1])
            
            output.append(result_pair)
    
    return output
    