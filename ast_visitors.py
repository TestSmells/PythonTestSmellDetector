import ast

class SmellVisitor(ast.NodeVisitor):

    def __init__(self):
            self.results = dict()
            self.results["count"] = 0
            self.results["lines"] = list()
            

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
    
    
class SensitiveEqualityVisitor(SmellVisitor):
    """Marks whether a test file has sensitive equality"""
    
    def visit_Expr(self, node):
        
        try:
            #checks to see if the expression is an assert function
            #checks to see if the expression references __str__
            #should we check for __repr__??
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
        
        
def is_assert(node):
    """Tells whether a given node is an assert method
    
    Examines the given node to determine if it it a unittest assert method. 
    Checks function name against the list of unittest assert function names.
    """

    assert_function_list = list()
    
    assert_function_list.append("assertEquals")
    assert_function_list.append("assertNotEquals")
    assert_function_list.append("assertTrue")
    assert_function_list.append("assertFalse")
    assert_function_list.append("assertIs")
    assert_function_list.append("assertIsNot")
    assert_function_list.append("assertIsNone")
    assert_function_list.append("assertIsNotNone")
    assert_function_list.append("assertIn")
    assert_function_list.append("assertNotIn")
    assert_function_list.append("assertNotIn")
    assert_function_list.append("assertIsInstance")
    assert_function_list.append("assertIsNotInstance")
    

    return node.value.func.id in assert_function_list
    
def node_equality(node_1, node_2):
    return node_1.dump == node_2.dump
 
 
def expression_equality(node_1, node_2):
    return ast.dump(node_1) == ast.dump(node_2)
    
    #print("point B")
    #if not isinstance(node_1, ast.Expr) or not isinstance(node_2, ast.Expr):
    #    return False
    
    #try:
    #    if(node_1.value.func.id != node_2.value.func.id):
    #        return False
    #    while i <= node_1.value.args:
    #        if(node_1.value.args[i] == node_2.value.args[i]):
    #            return True
    #except:
    #    pass
        
    #return False
 
    