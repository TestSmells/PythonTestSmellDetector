class TestSmell:
    """Checks for violations of a particular test smell
    
    Subclass this to create classes responsible for detecting test smells. 
    These subclasses handle one smell each, and are given either a list of
    python files, a test case ast, or a test method ast to check
    """
    
    name = None
    
    def test_for_smell(self, input):
        pass
        