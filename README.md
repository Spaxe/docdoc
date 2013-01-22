
# docdoc.py 
Generates Python documentation in Markdown using Python docstrings.

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


## DocumentationGenerator (<_ast.Attribute object at 0x1004b3a90>)
Extracts docstrings from a Python AST node.

This class should be used like an [ast.NodeVisitor][1]; see __main__ for an
example.  Once the parsing is done, the caller can use `format_doc()` to
retrieve the final markdown for further use.

[1]: http://docs.python.org/2/library/ast.html#ast.NodeVisitor


### __init__ (self)
Constructor.


### add_doc (self, name, args, documentation, level=value, decorators=value)
Records a documentation item.


### format_doc (self)
Return the final markdown string with the documentation items.


### visit_Module (self, module_node)
Automatically called when visiting a Module.


### visit_ClassDef (self, class_node)
Automatically called when visiting a ClassDef.


### parse_ClassDef (self, node, level=value)
Extracts documentation from a ClassDef.


### parse_FunctionDef (self, node, level=value)
Extracts documentation from a FunctionDef.


## docdoc (filepath)
Parses the Python source file.  Returns documentation in markdown.

