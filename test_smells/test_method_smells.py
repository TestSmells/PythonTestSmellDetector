import ast
import test_smells.test_smell as test_smell
from test_smells.smell_visitor import SmellVisitor

class AssertionRoulette(test_smell.TestSmell):
    
    def __init__(self):
        self.name = "Assertion Roulette"
        self.visitor = AssertionRouletteVisitor()
        
      
class AssertionRouletteVisitor(SmellVisitor):
    """discovers whether a test case has multiple undocumented test cases"""

    def __init__(self):
        
        #tells whether any undocumented assertions have been found
        self.first_assertion_found = False
        super(AssertionRouletteVisitor,self).__init__()
    
    def visit_Expr(self, node):
        try:
            #checks to see if the expression is an assert function
            #checks to see if the expression has a "msg" keyword argument 
            if(is_assert(node) and
               not any(keyword.arg == "msg" and keyword.value != None 
                       for keyword in node.value.keywords)):
               
                print("Point A")
                
                if not(self.first_assertion_found):
                    print("Point B1")
                    self.first_assertion_found = True
                    
                else:
                    print("Point B2")
                    self.results["count"] += 1
                       
                self.results["lines"].append(node.lineno)
                
        except:
            pass

        super().generic_visit(node)
        
        
class ConditionalTestLogic(test_smell.TestSmell):
    def __init__(self):
        self.name = "Conditional Test Logic"
        self.visitor = ConditionalTestLogicVisitor()
        
        
class ConditionalTestLogicVisitor(SmellVisitor):
    """Marks whether a test file has conditional test logic"""
    
    def visit_If(self, node):
        self.results["count"] += 1
        self.results["lines"].append(node.lineno)

        super().generic_visit(node)
        
    def visit_For(self, node):
        self.results["count"] += 1
        self.results["lines"].append(node.lineno)

        super().generic_visit(node)
        
    def visit_While(self, node):
        self.results["count"] += 1
        self.results["lines"].append(node.lineno)

        super().generic_visit(node)
        
    def visit_With(self, node):
        self.results["count"] += 1
        self.results["lines"].append(node.lineno)

        super().generic_visit(node)
        
    
class DuplicateAssertTest(test_smell.TestSmell):
    def __init__(self):
        self.name = "Duplicate Assert Test"
        self.visitor = DuplicateAssertTestVisitor()
        
        
class DuplicateAssertTestVisitor(SmellVisitor):
    def __init__(self):
        
        self.discovered_asserts = set()
        super(DuplicateAssertTestVisitor,self).__init__()
        
    def visit_Expr(self, node):
        try:
            #checks to see if the expression is an assert function
            if(is_assert(node)):
                
                if any(expression_equality(node,disc_assert) for disc_assert in 
                       self.discovered_asserts):
                    self.results["count"] += 1
                    self.results["lines"].append(node.lineno)
                else:
                    self.discovered_asserts.add(node)
                    
        except:
            pass

        super().generic_visit(node)
        
    
class EmptyTest(test_smell.TestSmell):
    name = "Empty Test"
    
    def test_for_smell(self, method_ast):
        if(len(method_ast.body) == 1 and
           isinstance(method_ast.body[0],ast.Pass)):
            return self.name
    
class ExceptionCatchingAndThrowing(test_smell.TestSmell):
    
    def __init__(self):
        self.name = "Exception Catching And Throwing"
        self.visitor = ExceptionCatchingAndThrowingVisitor()
        
        
class ExceptionCatchingAndThrowingVisitor(SmellVisitor):
    """Marks whether a test method has conditional test logic"""
    
    def visit_Try(self, node):
    
        self.results["count"] += 1
        self.results["lines"].append(node.lineno)

        super().generic_visit(node)
      
    
class MagicNumberTest(test_smell.TestSmell):

    def __init__(self):
        self.name = "Magic Number Test"
        self.visitor = MagicNumberVisitor()
        
        
class MagicNumberVisitor(SmellVisitor):
    """Creates a list of assert functions with magic number parameters"""

    def visit_Expr(self, node):
        try:
            #checks to see if the expression is an assert function
            #checks to see if the expression has any parameters that are numbers
            if(is_assert(node) and
               any(isinstance(arg, ast.Num) for arg in node.value.args)):
                self.results["count"] += 1
                self.results["lines"].append(node.lineno)
                
        except:
            pass

        super().generic_visit(node)

    
class MysteryGuest(test_smell.TestSmell):

    def __init__(self):
        self.name = "Mystery Guest"
        self.visitor = MysteryGuestVisitor()
    
    
class MysteryGuestVisitor(SmellVisitor):
    """Discovers which methods call Open()"""
    
    def __init__(self):
    
        #methods used for accessing external files 
        #key: module name
        #value: list of file-accessing functions in an external module
        self.external_access = dict()
        self.external_access["os"] = ["fdopen",]
        super(MysteryGuestVisitor,self).__init__()
        
    
    def visit_Call(self, node):
        try:
            #checks to see if the expression is an "open()" function 
            #call
            if(node.func.id == "open"):
                self.results["count"] += 1
                self.results["lines"].append(node.lineno)
                
        except:
            pass
            
        try:
            #checks to see if the expression is an "open()" function 
            #call
            for key in self.external_access.keys():
                print("id: {}".format(node.func.value.id))
                print("attr: {}".format(node.func.attr))
                if(node.func.value.id == key and node.func.attr in self.external_access[key]):
                    self.results["count"] += 1
                    self.results["lines"].append(node.lineno)
                
        except:
            pass

        super().generic_visit(node)
        
        
class RedundantAssert(test_smell.TestSmell):
    def __init__(self):
        self.name = "Redundant Assert"
        self.visitor = RedundantAssertVisitor()
        
        
class RedundantAssertVisitor(SmellVisitor):
    """Creates a list of assert functions that have literals as parameters"""
    
    def __init__(self):
    
        self.results = dict()
        self.results["count"] = 0
        self.results["lines"] = list()
            
        self.one_parameter_asserts = ["assertTrue",
                                      "assertFalse",
                                      "assertIsNone",
                                      "assertIsNotNone"]
             
        self.two_parameter_asserts = ["assertEqual", 
                                      "assertNotEqual", 
                                      "assertIs", 
                                      "assertIsNot",
                                      "assertIn",
                                      "assertNotIn",
                                      "assertIsInstance",
                                      "assertNotIsInstance",
                                      "assertAlmostEqual",
                                      "assertNotAlmostEqual",
                                      "assertGreater",
                                      "assertGreaterEqual",
                                      "assertLess",
                                      "assertLessEqual",
                                      "assertRegex",
                                      "assertNotRegex",
                                      "assertCountEqual",
                                      "assertMultiLineEqual",
                                      "assertSequenceEqual",
                                      "assertListEqual",
                                      "assertTupleEqual",
                                      "assertSetEqual",
                                      "assertDictEqual"]
        
    def visit_Call(self, node):
    
        try:
            #checks to see if the method call is a 2 parameter assert function
            #checks to see if both of the call's parameters are literals
            if(node.func.id in self.two_parameter_asserts):
               
                #will fail if either argument is not a literal
                try:
                    ast.literal_eval(node.args[0]) 
                    ast.literal_eval(node.args[1])
                    
                    self.results["count"] += 1
                    self.results["lines"].append(node.lineno)
                except:
                    pass
        except:
            pass
            
        try:
            #checks to see if the expression is a single-parameter assert function
            #checks to see if the expression's parameter is a literal
            if(node.func.id in self.one_parameter_asserts):
               
                #will fail if the argument is not a literal
                try:
                    ast.literal_eval(node.args[0]) 
                    
                    self.results["count"] += 1
                    self.results["lines"].append(node.lineno)
                except:
                    pass
        except:
            pass

        super().generic_visit(node)
                
    
class RedundantPrint(test_smell.TestSmell):
    def __init__(self):
        self.name = "Redundant Print"
        self.visitor = RedundantPrintVisitor()
        
        
class RedundantPrintVisitor(SmellVisitor):
    """Marks whether a test method has any print statements"""

    def visit_Expr(self, node):
        try:
            #checks to see if the expression is an print function
            if(is_print(node)):
                self.results["count"] += 1
                self.results["lines"].append(node.lineno)
                
        except:
            pass

        super().generic_visit(node)
        
    
class ResourceOptimism(test_smell.TestSmell):
    name = "Resource Optimism"
    
    def test_for_smell(self, method_ast):
        dummy_code_call(self, method_ast)
        
        
class SensitiveEquality(test_smell.TestSmell):
    
    def __init__(self):
        self.name = "Sensitive Equality"
        self.visitor = SensitiveEqualityVisitor()
        

class SensitiveEqualityVisitor(SmellVisitor):
    """Marks whether a test file has sensitive equality"""
    
    def visit_Expr(self, node):
        
        try:
            #checks to see if the expression is an assert function
            #checks to see if the expression references __str__
            if(is_assert(node) and
               any(isinstance(arg, ast.Attribute) for arg in node.value.args)):

                #print(dump(node.value.args[))
                for arg in node.value.args:
                    try:
                        if(arg.attr is "__str__"):
                            
                            self.results["count"] += 1
                            self.results["lines"].append(node.lineno)
                    except:
                        pass
        except:
            pass

        super().generic_visit(node)
    
    
class SkippedTest(test_smell.TestSmell):
    name = "Skipped Test"
    
    def test_for_smell(self, method_ast):
        for decorator in method_ast.decorator_list:
            try:
                if(decorator.attr == "skip"):
                    return self.name
                
            except:
                pass
    
    
class SleepyTest(test_smell.TestSmell):
    name = "Sleepy Test"
    
    def __init__(self):
        self.name = "Sleepy Test"
        self.visitor = SleepyTestVisitor()
        
        
class SleepyTestVisitor(SmellVisitor):
    """Marks whether a test method has any calls to time.sleep()"""

    #what about if an alias is used?
    def visit_Attribute(self, node):
        try:

            if(node.value.id == "time" and node.attr == "sleep"):
                self.results["count"] += 1
                self.results["lines"].append(node.lineno)
                
        except:
            pass

        super().generic_visit(node)
    
    
class UnknownTest(test_smell.TestSmell):
    name = "Unknown Test"
    
    def test_for_smell(self, method_ast):
        dummy_code_call(self, method_ast)
        
        
def is_assert(node):
    """Tells whether a given node is an assert method
    
    Examines the given node to determine if it it a unittest assert method. 
    Checks function name against the list of unittest assert function names.
    """

    assert_function_list = ("assertEquals",
                            "assertNotEquals",
                            "assertTrue",
                            "assertFalse",
                            "assertIs",
                            "assertIsNot",
                            "assertIsNone",
                            "assertIsNotNone",
                            "assertIn",
                            "assertNotIn",
                            "assertNotIn",
                            "assertIsInstance",
                            "assertIsNotInstance",
                            "assertRaises",
                            "assertRaisesRegexp",
                            "assertalmostEqual",
                            "assertNotAlmostEqual",
                            "assertGreater",
                            "assertGreaterEqual",
                            "assertLess",
                            "assertLessEqual",
                            "assertRegexpMatches",
                            "assertNotRegexpMatches",
                            "assertItemsEqual",
                            "assertDictContainsSubset")

    return node.value.func.id in assert_function_list
    
    
def is_print(node):
    """Tells whether a given node is a method that prints to output
    
    Examines the given node to determine if it is has the same name as one of
    the IO methods that prints to output
    """

    print_function_list = list()
    
    print_function_list.append("print")

    return node.value.func.id in print_function_list
        
    
def node_equality(node_1, node_2):
    return node_1.dump == node_2.dump
 
 
def expression_equality(node_1, node_2):
    return ast.dump(node_1) == ast.dump(node_2)
    
    
def dummy_code_call(smell,method_ast):
    print("{0} runs on {1}".format(smell.name,method_ast.name))