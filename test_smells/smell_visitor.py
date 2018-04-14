import ast

class SmellVisitor(ast.NodeVisitor):

    def __init__(self):
            self.results = dict()
            self.results["count"] = 0
            self.results["lines"] = list()