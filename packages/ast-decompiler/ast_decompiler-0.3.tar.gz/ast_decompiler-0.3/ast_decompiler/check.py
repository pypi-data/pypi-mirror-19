from ast_decompiler import decompile
import ast
from tests.tests import check
import os

for dirname, _, files in sorted(os.walk('/home/jelle/ans')):
    for file in files:
        if file.endswith('.py'):
            filename = dirname + '/' + file
            print filename
            text = open(filename).read()
            try:
                ast.parse(text)
            except SyntaxError:
                print 'error in', filename
            else:
                check(text)
