import test_smell
import ast_visitors
import ast

class AssertionRoulette(test_smell.TestSmell):
    #Note: does not currently identify commented assertions as documented
    
    def __init__(self):
        self.name = "Assertion Roulette"
        self.visitor = ast_visitors.AssertionRouletteVisitor()
    
class MagicNumberTest(test_smell.TestSmell):

    def __init__(self):
        self.name = "Magic Number Test"
        self.visitor = ast_visitors.MagicNumberVisitor()

    
class MysteryGuest(test_smell.TestSmell):
    name = "Mystery Guest"
    
    def test_for_smell(self, method_ast):
        dummy_code_call(self, method_ast)
        
        
class SensitiveEquality(test_smell.TestSmell):
    
    def __init__(self):
        self.name = "Sensitive Equality"
        self.visitor = ast_visitors.SensitiveEqualityVisitor()
    
    
class ConditionalTestLogic(test_smell.TestSmell):
    def __init__(self):
        self.name = "Conditional Test Logic"
        self.visitor = ast_visitors.ConditionalTestLogicVisitor()
    
class DuplicateAssertTest(test_smell.TestSmell):
    def __init__(self):
        self.name = "Duplicate Assert Test"
        self.visitor = ast_visitors.DuplicateAssertTestVisitor()
    
class EmptyTest(test_smell.TestSmell):
    name = "Empty Test"
    
    def test_for_smell(self, method_ast):
        if(len(method_ast.body) == 1 and
           isinstance(method_ast.body[0],ast.Pass)):
            return self.name
    
class ExceptionCatchingAndThrowing(test_smell.TestSmell):
    name = "Exception Catching and Throwing"
    
    def test_for_smell(self, method_ast):
        dummy_code_call(self, method_ast)
    
class SkippedTest(test_smell.TestSmell):
    name = "Skipped Test"
    
    def test_for_smell(self, method_ast):
        dummy_code_call(self, method_ast)
    
class RedundantPrint(test_smell.TestSmell):
    name = "Redundant Print"
    
    def test_for_smell(self, method_ast):
        dummy_code_call(self, method_ast)
    
class RedundantAssert(test_smell.TestSmell):
    name = "Redundant Assert"
    
    def test_for_smell(self, method_ast):
        dummy_code_call(self, method_ast)
    
class ResourceOptimism(test_smell.TestSmell):
    name = "Resource Optimism"
    
    def test_for_smell(self, method_ast):
        dummy_code_call(self, method_ast)
    
class SleepyTest(test_smell.TestSmell):
    name = "Sleepy Test"
    
    def test_for_smell(self, method_ast):
        dummy_code_call(self, method_ast)
    
class UnknownTest(test_smell.TestSmell):
    name = "Unknown Test"
    
    def test_for_smell(self, method_ast):
        dummy_code_call(self, method_ast)
    
def dummy_code_call(smell,method_ast):
    print("{0} runs on {1}".format(smell.name,method_ast.name))