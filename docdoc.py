#!/usr/bin/env python
'''Generates Python documentation in Markdown using Python docstrings.

This module is an early experimentation to see how feasible it is to only use
docstrings and class/function definitions as the source for documentation.
Since the idea of [Python](http://python.org) is self-documenting, this should suffice for most small projects.

[Markdown](http://daringfireball.net/projects/markdown/) is chosen becuase the author likes it.  Thanks, John Gruber.

# Usage (as a module)
    >>> from docdoc import docdoc
    >>> print docodc(<filepath>)

# Usage (from terminal)
    $ ./docdoc.py <filepath>

Author: [Xavier Ho](mailto:contact@xavierho.com)
'''
import sys
import ast

class DocumentationGenerator(ast.NodeVisitor):
    '''Extracts docstrings from a Python AST node.

    This class should be used like an [ast.NodeVisitor][1]; see __main__ for an
    example.  Once the parsing is done, the caller can use `format_doc()` to
    retrieve the final markdown for further use.

    [1]: http://docs.python.org/2/library/ast.html#ast.NodeVisitor'''

    def __init__(self):
        '''Constructor.'''
        super(DocumentationGenerator, self).__init__()
        self.doc = []   # (Name, Args, Documentation [, Level[, Decorators]])

    def add_doc(self, name, args, documentation, level=1, decorators=None):
        '''Records a documentation item.'''
        self.doc.append((name, args, documentation, level, decorators or []))

    def format_doc(self):
        '''Return the final markdown string with the documentation items.'''
        output = ''
        for name, args, docstring, level, decorators in self.doc:
            output += '{decorators}\n{heading} {name} {args}\n{docstring}\n\n'.format(
                decorators = '\n'.join(decorators),
                heading = '#' * level,
                args = args if level > 1 else '',
                name = name,
                docstring = docstring
            )
        return output

    def visit_Module(self, module_node):
        '''Automatically called when visiting a Module.'''
        for node in ast.iter_child_nodes(module_node):
            if isinstance(node, ast.FunctionDef):
                self.parse_FunctionDef(node)
            self.visit(node)

    def visit_ClassDef(self, class_node):
        '''Automatically called when visiting a ClassDef.'''
        self.parse_ClassDef(class_node)
        for node in ast.iter_child_nodes(class_node):
            if isinstance(node, ast.FunctionDef):
                self.parse_FunctionDef(node, level=3)
            self.visit(node)

    def parse_ClassDef(self, node, level=2):
        '''Extracts documentation from a ClassDef.'''
        fields = [x for x in ast.iter_fields(node)]
        self.add_doc(
            fields[0][1],
            '({})'.format(', '.join([str(x) for x in fields[1][1]])) if fields[1][1] else '',
            ast.get_docstring(node),
            level=level,
            decorators=fields[3][1]
        )

    def parse_FunctionDef(self, node, level=2):
        '''Extracts documentation from a FunctionDef.'''
        named_args = [x.id for x in node.args.args]
        for i, default in enumerate(node.args.defaults):
            # TODO: Parse defaults
            named_args[len(named_args)-len(node.args.defaults)+i] += '=' + 'value'
        args = ', '.join(named_args)
        if node.args.vararg:
            args = ', '.join([args, '*'+str(node.args.vararg)])
        if node.args.kwarg:
            args = ', '.join([args, '**'+str(node.args.kwarg)])
        self.add_doc(
            node.name,
            '({})'.format(args),
            ast.get_docstring(node),
            level=level
        )

def docdoc(filepath):
    '''Parses the Python source file.  Returns documentation in markdown.'''
    docgen = DocumentationGenerator()
    with open(filepath) as f:
        package = filepath
        source_ast = ast.parse(f.read())
        docgen.add_doc(package, [], ast.get_docstring(source_ast))
        docgen.visit(source_ast)
    return docgen.format_doc()


if '__main__' in __name__:
    print docdoc(sys.argv[1])