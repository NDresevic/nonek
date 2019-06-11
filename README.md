# nonek
Creation of my own simple programming language with grammar that describes it, editor as a plugin for Sublime Text and compiler for the language.

Grammar is described in `grammar.txt`, theme and file to enable editor in Sublime Text are in folder `editor`. 

In order to compile the program, techniques that are used are disassembling the input string to tokens, parsing, construction of abstract syntax tree, visiting the tree... 
Generated tree can be seen by running `getastdot.py` and pasting the output to Webgraphviz (http://www.webgraphviz.com/). Program is compiled to Python language in file `getastpython.py`.
