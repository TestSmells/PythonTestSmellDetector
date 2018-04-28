from test_smells.test_smell import TestSmell
import python_parser
import re
import ast

class EagerTest(TestSmell):
    name = "Lazy Test"
    
    def test_for_smell(self, file_list):
        dummy_code_call(self, file_list)
        
class LazyTest(TestSmell):

    name = "Lazy Test"
    
    def __init__(self):
        
        #production methods are keys, client test methods are values
        #key format: (file path, class name, method name)
        self.prod_test_association = dict()
        
    def test_for_smell(self, file_list):
		
        #identify production files
        production_files = python_parser.filter_python_files_complement(file_list)
        
        #discover module level (or non-method) functions
        for file in production_files:
            
            function_names = python_parser.get_classless_functions(file)
            
            #store the names of production functions with their modules
            for function in function_names:
                self.prod_test_association[(file, None, function)] = set()
            
            #prod_test_association[(file,function_name)]
        
        production_classes = list() 
        
        #identify production classes
        for file in production_files:
            production_classes = python_parser.get_module_classes(file)
            
            for class_ast in production_classes:
                for method in python_parser.get_class_methods(class_ast):
                    self.prod_test_association[(file,class_ast.name,method)] = set()
                
        #discover test files
        test_files = python_parser.filter_python_files(file_list)
        
        #identify each test method
        test_cases = python_parser.get_test_case_asts(test_files)
        test_methods = list()
        for case in test_cases:
        
            methods = python_parser.get_test_asts(case)
            
            print("methods[0]: {}".format(methods[0]))
            
            test_methods = test_methods + methods
            
        visitor = MethodCallVisitor()
        
        #discover what method calls are made in each test method
        for method in test_methods:
            visitor.visit(method[0])
            
            print("methods called by {}: {}".format(method[0].name, 
                  visitor.methods_called))
            
            for call_double in visitor.methods_called:
            
                for method_triple in self.prod_test_association.keys():
                    #if this matches a call to a class, store the 
                    #association
                    if((method_triple[1],method_triple[2]) == call_double):
                       
                        self.prod_test_association[method_triple].add((method[0].name, method[1]))
                        
                    module_pattern = re.compile(r'\\(\w*)\.py')
                    module_search = module_pattern.search(method_triple[0])
                    module_name = module_search.group(1) 
                     
                    if((module_name, method_triple[2]) == call_double):
                        self.prod_test_association[method_triple].add((method[0].name, method[1]))
                        
            #reset the visitor
            visitor.methods_called = list()
            
        
        for key in self.prod_test_association.keys():
            print("{}:".format(key))
            print("    {}".format(self.prod_test_association[key]))
            
        output = set()
            
        for key in self.prod_test_association.keys():
            if len(self.prod_test_association[key]) >= 2:
                for call in self.prod_test_association[key]:
                    output.add(("Lazy Test",call[0],call[1]))
                    
        return list(output)
            
        
class MethodCallVisitor(ast.NodeVisitor):
    def __init__(self):
        
        #keep track of variable assignment within a test method
        self.var_assignment = dict()
        
        #list of method calls found
        self.methods_called = list()
        
        super(MethodCallVisitor,self).__init__()
        
    def visit_Attribute(self, node):
        #works only if attribute is a function, fails and passes it 
        #over otherwise
        try:
            function_call = None
            
            if(self.var_assignment.get(node.value.id,False)):
                obj_type = self.var_assignment[node.value.id]
            else:
                obj_type = node.value.id
   
            function_call = (obj_type, node.attr)
            
            self.methods_called.append(function_call)

        except:
            pass
            
    def visit_Assign(self, node):
        for target in node.targets:
            try:
                self.var_assignment[target.id] = node.value.func.id
                print(str(node.value.func.id) + " <-- " + str(target.id))
            except:
                pass
            
def dummy_code_call(smell, file_list):
    print("{0} runs on project".format(smell.name))