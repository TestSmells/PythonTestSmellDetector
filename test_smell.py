class TestSmell:
    """Checks for violations of a particular test smell
    
    Subclass this to create classes responsible for detecting test smells. 
    These subclasses handle one smell each, and are given either a list of
    python files, a test case ast, or a test method ast to check
    """
    
    name = None
    visitor = None
    
    def test_for_smell(self, ast):
        self.visitor.visit(ast)
        
        if self.visitor.results["count"] > 0: 
            output = (self.name)
        else:
            output = None
        
        return output
        