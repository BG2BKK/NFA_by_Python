NFA_by_Pthony
=============

Abstract:
----------

This program is written in Ubuntu12.04 and in python 2.7. 

This program use data structure 'list' and 'dict' in principle such as 'PDA' , 'NFA','DFA' which we learned in TOC to generate Rules and NFA from expression instead of using 're' module provided by python.

This program use pygraphviz to draw the NFA and output a 'pdf' file. Pygraphviz is a interface of 'graphviz' for python,So you should make sure that you have install pygraphviz if you want to draw a NFA.

Document:
-------------

We have 5 documents in our project directory.
The documents are 'clean.sh','NFA.py','recReg.py','Reg.py' and tf. 

- 1.The file 'clean.sh' is used to clean the tmp files and other trash files, you can type './clean.sh' in Terminal in order to remove the trash files. 

- 2.The file 'tf' is used to store the strings you want to check if it's recognized by the 'regex' you input.

- 3.The file 'recReg.py' is used to receive command and arguments you input and then call the other two source code files 'Reg.py' and 'NFA.py' to deal with the arguments. 'recReg.py' will create a object called 'reg' of class 'Reg' which is in 'Reg.py' and create object 'nfa' in the same way. The main function will use 'reg' to generate Rule sets to recognize strings read from 'tf' and use 'nfa' to generate a NFA according the inputed 'regex'

- 4.The file 'Reg.py' is source code of a class 'Reg', 'Reg' has some functions to deal with the input expression.First 'Reg' will use function 'rmbra' to remove brackets in expression, then use function 'rmBeg' to eliminate '^' in the expression and generate Rule'^',then use function 'rmTai' to eliminate '$' in the expression and generate Rule'$',then use function 'rmStar' to eliminate '*' and and generate Rule'*', then use function 'rmAdd' to eliminate '+' and generate Rule'+'. Then 'reg' will generate RuleSets from the input regex. To check whether the strings is recognized by the RuleSets,the function 'checkRule' will be called to prove it and 'checkRule' is in file 'recReg.py'

- 5.The file 'NFA.py' is source code of a class 'NFA', 'NFA' has some functions to generate RuleSets from the input regex.But you should notice that RuleSets generated by 'NFA.py' is different from those by 'Reg.py', becasue RuleSets generated by 'NFA.py' will be used to generate a NFA which will recognize the input regex. 'NFA.py' will use function 'genNFA' to generate NFA from the RuleSets. After that the function 'drawNFA' will generate a 'dot' file and then python will use pygraphviz which is a interface provided by 'Graphviz' to generate a 'pdf' file.


### How-TO:

#### Installation

Pygraphviz is required.

```bash
sudo apt-get install graphviz graphviz-dev graphviz-doc
pip install pygraphviz
```
If there is something wrong listed below:

```bash
$ python recReg.py -v '(a+b)*c' tf
Traceback (most recent call last):
  File "recReg.py", line 4, in <module>
    import NFA
  File "/home/huang/workspace/python/NFA_by_Python/toc/NFA.py", line 2, in <module>
    import pygraphviz as pgv
  File "/usr/local/lib/python2.7/dist-packages/pygraphviz/__init__.py", line 58, in <module>
    from .agraph import AGraph, Node, Edge, Attribute, ItemAttribute, DotError
  File "/usr/local/lib/python2.7/dist-packages/pygraphviz/agraph.py", line 26, in <module>
    from . import graphviz as gv
  File "/usr/local/lib/python2.7/dist-packages/pygraphviz/graphviz.py", line 28, in <module>
    _graphviz = swig_import_helper()
  File "/usr/local/lib/python2.7/dist-packages/pygraphviz/graphviz.py", line 24, in swig_import_helper
    _mod = imp.load_module('_graphviz', fp, pathname, description)
ImportError: /usr/local/lib/python2.7/dist-packages/pygraphviz/_graphviz.so: undefined symbol: Agundirected

```

please try:

	pip install pygraphviz --install-option="--include-path=/usr/include/graphviz" --install-option="--library-path=/usr/lib/graphviz/"

Open Terminal and enter the source code directory.
#### if you want to generate Rules from the regex '(a+b)*c' to recognize strings stored in tf and generate NFA for regex. Type the command:

```python
python recReg.py -v '(a+b)*c' tf
```

#### if you want to generate Rules from the regex '(a+b)*c' to recognize strings stored in tf and don't want to generate NFA. Type the command:

```python
python recReg.py '(a+b)*c' tf
```

### Example:
```python
We have test almost all of the expression and the tested regex is listed below
(0|1)*
a*b
a+b
a*
a+
(grep)^
(last)$
(a..b)
(a|b)
(a|b)*c(m+n)*
a.*b
(grep)^(last)$
(010)^((a|b)+c+)(b..c)(m*n)*(000)$
```

### ErrorData:
```
We still have bugs to be fixed.
```

```python
  This project is dedicated to DW
```

