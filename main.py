#!/usr/bin/python3
import clang.cindex
from clang.cindex import CursorKind
from clang.cindex import TypeKind
import astor
from helper_functions import *
from parser import *
from ast import *
import sys


# create the index
index = clang.cindex.Index.create()
# create the translation unit
filename = 'simple.c'
if len(sys.argv) > 1:
    if '-i' in sys.argv:
        try:
            filename = sys.argv[sys.argv.index('-i')+1]
        except:
            print("Usage: ./parser.py -i <filename>")
            sys.exit(1)
try:
    #tu = index.parse(filename, args=['-Iheaders'])
    #tu = index.parse(filename, args=['-Iheaders'], options=clang.cindex.TranslationUnit.PARSE_INCLUDE_BRIEF_COMMENTS_IN_CODE_COMPLETION)
    #tu = index.parse(filename, args=['-I../headers'], options=clang.cindex.TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD)
    #tu = index.parse(filename, args=['-I../headers'])
    tu = index.parse(filename, args=['-Iheaders'], options=clang.cindex.TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD)
except:
    print("Invalid filename")
    exit(1)
print("Translation Unit:", tu.spelling, '\n')
# get the root cursor
root = tu.cursor
# get the diagnostic
STRICT_TYPING = False
if len(sys.argv) > 1:
    if sys.argv[1] == '--strict-typing' or sys.argv[1] == '-s':
        STRICT_TYPING = True
stars()
print("DIAGNOSTICS REPORT:")
diag = tu.diagnostics
for i in diag:
    print(i)
stars()

stars()
print("C AST:")
print_c_ast(root, 0)
stars()
#stars()
#print("IDEAL PYTHON AST:")
#print(dump(parse(open('simple.py').read()), indent=4))
#stars()

root = tu.cursor
root_ast = Module([],[])
childs = list(root.get_children())

root_ast.body.append(ImportFrom(module='helper_classes', names=[alias(name='*')], level=0))
root_ast.body.append(Assign([Name("𐓄")], Call(Name("Trigger"), [], [])))
root_ast.body.extend(create_stmt_list(childs))
print(root_ast.body)
root_ast.body.append(add_main_check())

#root_ast.body = root_ast.body[362:]

# stars()
# print("IDEAL PYTHON AST:")
# print(dump(parse(open('simple.py').read()), indent=4))
# stars()
stars()
print("WHAT I GOT:")
for i in range(len(root_ast.body)):
    try:
        if root_ast.body[i].name == 'main':
            print("HEY", i)
    except:
        pass
print(dump(root_ast, indent=4))
stars()


stars()
print("RESULTING PYTHON CODE FROM C CODE:")
print(astor.to_source(root_ast))
output = astor.to_source(root_ast)
stars()

stars()
#of_name = input("Enter filename to save output to, no file extension [press enter for default]: ")
#if of_name == "":
of_name = "output_file"
of = open(of_name+'.py', 'w')
of.write(output)
print("CODE SAVED TO " + of_name + ".py")
stars()

