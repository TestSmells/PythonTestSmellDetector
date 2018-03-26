import test_smell
import ast_visitors

class AssertionRoulette(test_smell.TestSmell):
    name = "Assertion Roulette"
    
    def test_for_smell(self, method_ast):
        dummy_code_call(self, method_ast)
    
class MagicNumberTest(test_smell.TestSmell):
    name = "Magic Number Test"
    
    def test_for_smell(self, method_ast):
            
        visitor = ast_visitors.MagicNumberVisitor()
        visitor.visit(method_ast)
        
        if visitor.results: 
            output_pair = visitor.results[0]
            output = output_pair[0]
        else:
            output = None
        
        return output
    
class MysteryGuest(test_smell.TestSmell):
    name = "Mystery Guest"
    
    def test_for_smell(self, method_ast):
        dummy_code_call(self, method_ast)
        
class SensitiveEquality(test_smell.TestSmell):
    name = "Sensitive Equality"
    
    def test_for_smell(self, method_ast):
        dummy_code_call(self, method_ast)
    
class ConditionalTestLogic(test_smell.TestSmell):
    name = "Conditional Test Logic"
    
    def test_for_smell(self, method_ast):
        dummy_code_call(self, method_ast)
    
class DuplicateAssertTest(test_smell.TestSmell):
    name = "Duplicate Assert Test"
    
    def test_for_smell(self, method_ast):
        dummy_code_call(self, method_ast)
    
class EmptyTest(test_smell.TestSmell):
    name = "Empty Test"
    
    def test_for_smell(self, method_ast):
        dummy_code_call(self, method_ast)
    
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