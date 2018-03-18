import test_method_smells

def project_rule_runner(python_files):
    """Run rules that need the entire python project to detect a smell"""
    #dummy code
    print("project_rule_runner")
    return list()
    
def test_case_rule_runner(test_case_ast):
    """Run rules that only need a test case to detect a smell"""
    #dummy code
    print("test_case_rule_runner")
    return list()
    
def test_method_rule_runner(test_method_ast):
    """Run rules that need the entire test method to detect a smell"""
    
    method_smell_list = list()
    method_smell_list.append(test_method_smells.AssertionRoulette())
    method_smell_list.append(test_method_smells.MagicNumberTest())
    method_smell_list.append(test_method_smells.MysteryGuest())
    
    output = list()
    
    for smell in method_smell_list:
        output.append(smell.test_for_smell(test_method_ast))
    
    return output
    