#!/usr/bin/env python
'''Generates Python documentation in [Markdown](http://daringfireball.net/projects/markdown/) using [Python](http://python.org) docstrings.

This module is an early experimentation to see how feasible it is to only use
docstrings and class/function definitions as the source for documentation.
Since the idea of Python is self-documenting, this should suffice for most small projects.

Markdown is chosen becuase the author likes it.  Thanks, John Gruber.

This module was created quickly, so many features are missing.  If you would like to see something implemented, please [create an issue](https://github.com/Spaxe/docdoc/issues).

## Installation
Get the module from Github (cheeseshop package coming soon):

    $ git clone git://github.com/Spaxe/docdoc.git

Add the module's path to ypur `$PYTHONPATH`.

## Usage (as a module)
    >>> from docdoc import docdoc
    >>> print docodc(<filepath>)

## Usage (from terminal)
    $ ./docdoc.py <filepath>
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
                docstring = docstring or ''
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
            '({})'.format(', '.join([self.parse_Literals(x) for x in fields[1][1]])) if fields[1][1] else '',
            ast.get_docstring(node),
            level=level,
            decorators=fields[3][1]
        )

    def parse_FunctionDef(self, node, level=2):
        '''Extracts documentation from a FunctionDef.'''
        named_args = [x.id for x in node.args.args]
        for i, default in enumerate(node.args.defaults):
            named_args[len(named_args)-len(node.args.defaults)+i] += '=' + self.parse_Literals(default)
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

    def parse_Literals(self, node):
        '''Extracts Python literals from a value/expression node.'''
        if isinstance(node, ast.Attribute):
            return self.parse_Literals(node.value) + '.' + str(node.attr)
        elif isinstance(node, ast.Name):
            return str(node.id)
        try:
            return str(ast.literal_eval(node))
        except Exception as e:
            return str(node)

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
