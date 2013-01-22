
# docdoc.py 
Generates Python documentation in [Markdown](http://daringfireball.net/projects/markdown/) using [Python](http://python.org) docstrings.

This module is an early experimentation to see how feasible it is to only use
docstrings and class/function definitions as the source for documentation.
Since the idea of Python is self-documenting, this should suffice for most small projects.

Markdown is chosen becuase the author likes it.  Thanks, John Gruber.

## Usage (as a module)
    >>> from docdoc import docdoc
    >>> print docodc(<filepath>)

## Usage (from terminal)
    $ ./docdoc.py <filepath>

Author: [Xavier Ho](mailto:contact@xavierho.com)


## DocumentationGenerator (ast.NodeVisitor)
Extracts docstrings from a Python AST node.

This class should be used like an [ast.NodeVisitor][1]; see __main__ for an
example.  Once the parsing is done, the caller can use `format_doc()` to
retrieve the final markdown for further use.

[1]: http://docs.python.org/2/library/ast.html#ast.NodeVisitor


### __init__ (self)
Constructor.


### add_doc (self, name, args, documentation, level=1, decorators=None)
Records a documentation item.


### format_doc (self)
Return the final markdown string with the documentation items.


### visit_Module (self, module_node)
Automatically called when visiting a Module.


### visit_ClassDef (self, class_node)
Automatically called when visiting a ClassDef.


### parse_ClassDef (self, node, level=2)
Extracts documentation from a ClassDef.


### parse_FunctionDef (self, node, level=2)
Extracts documentation from a FunctionDef.


### parse_Literals (self, node)
Extracts Python literals from a value/expression node.


## docdoc (filepath)
Parses the Python source file.  Returns documentation in markdown.


