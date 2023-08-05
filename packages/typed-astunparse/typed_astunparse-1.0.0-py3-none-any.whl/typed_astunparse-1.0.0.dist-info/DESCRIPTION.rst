
================
typed-astunparse
================

.. image:: https://img.shields.io/pypi/v/typed-astunparse.svg
    :target: https://pypi.python.org/pypi/typed-astunparse
    :alt: package version from PyPI

.. image:: https://travis-ci.org/mbdevpl/typed-astunparse.svg?branch=master
    :target: https://travis-ci.org/mbdevpl/typed-astunparse
    :alt: build status from Travis CI

.. image:: https://coveralls.io/repos/github/mbdevpl/typed-astunparse/badge.svg?branch=master
    :target: https://coveralls.io/github/mbdevpl/typed-astunparse?branch=master
    :alt: test coverage from Coveralls

.. image:: https://landscape.io/github/mbdevpl/typed-astunparse/master/landscape.svg?style=flat
    :target: https://landscape.io/github/mbdevpl/typed-astunparse/master
    :alt: code health from Landscape

.. image:: https://codeclimate.com/github/mbdevpl/typed-astunparse/badges/gpa.svg
    :target: https://codeclimate.com/github/mbdevpl/typed-astunparse
    :alt: code GPA from Code Climate

.. image:: https://codeclimate.com/github/mbdevpl/typed-astunparse/badges/issue_count.svg
    :target: https://codeclimate.com/github/mbdevpl/typed-astunparse
    :alt: issue count from Code Climate

.. image:: https://img.shields.io/pypi/l/typed-astunparse.svg
    :alt: license

.. role:: bash(code)
    :language: bash

.. role:: python(code)
    :language: python

The *typed-astunparse* is to *typed-ast* as *astunparse* is to *ast*. In short: unparsing of Python
3.5 abstract syntax trees (AST) with type comments and variable annotations.

The built-in *ast* module has capabilites to parse Python source code into AST. It does not,
however, have the capability to generate source code from the AST. That's where *astunparse* comes
in. Using a refactored version of an obscure script found in official Python repository, it provides
code generation capability for built-in AST.

Built-in *ast* and *astunparse* modules, however, completely ignore type comments introduced in
PEP 484. They treat them like all other comments, so when you parse the code using
:python:`compile()`, your type comments will be lost. There is no place for them in the AST, so
obviously they also cannot be unparsed.

Moreover, neither module accepts variable annotations introduced in PEP 526. They cause syntax
errors. The *typed-ast* module provides an updated AST including type comments defined in PEP 484
and variable annotations introduced in PEP 526. It also provides a parser for Python code using
those features.

Unfortunately, *typed-ast* also doesn't provide any means to go from AST to source code. This is
where this module, *typed-astunparse*, comes in. It provides unparser for AST defined in
*typed-ast*.


------------
requirements
------------

This package is intended for Python 3.5 and later. It was tested on 64 bit Ubuntu, but it might work
on other systems too.

typed-astunparse depends on:

-  astunparse

-  typed-ast


------------
installation
------------

For simplest installation use :bash:`pip`:

.. code:: bash

    pip3.5 install typed-astunparse

You can also build your own version:

.. code:: bash

    git clone https://github.com/mbdevpl/typed-astunparse
    cd typed-astunparse
    python3.5 -m unittest discover # make sure the tests pass
    python3.5 setup.py bdist_wheel
    ls -1tr dist/*.whl | tail -n 1 | xargs pip3.5 install


-----
usage
-----

Example of roundtrip from code through AST to code:

.. code:: python

    import typed_ast
    import typed_astunparse

    code = 'my_string = None # type: str'
    roundtrip = typed_astunparse.unparse(typed_ast.ast35.parse(code))
    print(roundtrip)

    code = 'my_string: str = None'
    roundtrip = typed_astunparse.unparse(typed_ast.ast35.parse(code))
    print(roundtrip)

for more examples see :bash:`examples.ipynb` notebook.


-----
links
-----

-  *ast*:

   https://docs.python.org/3/library/ast.html

   https://greentreesnakes.readthedocs.io/

-  *astunparse*:

   https://pypi.python.org/pypi/astunparse

   https://github.com/simonpercivall/astunparse

   https://astunparse.readthedocs.io/en/latest/

-  PEP 483 - The Theory of Type Hints:

   https://www.python.org/dev/peps/pep-0483/

-  PEP 484 - Type Hints:

   https://www.python.org/dev/peps/pep-0484/

-  PEP 526 - Syntax for Variable Annotations:

   https://www.python.org/dev/peps/pep-0526/

-  *typed-ast*:

   https://pypi.python.org/pypi/typed-ast

   https://github.com/dropbox/typed_ast


