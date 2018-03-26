import ast

class MagicNumberVisitor(ast.NodeVisitor):
    """Creates a list of assert functions with magic number parameters"""

    def __init__(self):
        self.results = dict()
        self.results["count"] = 0
        self.results["lines"] = list()
    
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
    
    
class SensitiveEqualityVisitor(ast.NodeVisitor):
    """Marks whether a test file has sensitive equality"""
    
    def __init__(self):
        self.results = dict()
        self.results["count"] = 0
        self.results["lines"] = list()
    
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
     
     
class ConditionalTestLogicVisitor(ast.NodeVisitor):
    """Marks whether a test file has sensitive equality"""
    
    def __init__(self):
        self.results = dict()
        self.results["count"] = 0
        self.results["lines"] = list()
    
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