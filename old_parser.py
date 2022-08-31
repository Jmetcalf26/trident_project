import clang.cindex
import astor
from helper_functions import *
from ast import *

def create_ast_list(pt, parent, n):
    

def create_ast_node(pt, parent, n):
    # determine the type of node to create
    stars()
    nt = str(n.kind)[11:]
    tokens = list(n.get_tokens())
    print("IN CREATE AST NODE, I want to create a", nt)

    # in the case of an int, a literal integer is created, with only a value
    if nt == "INTEGER_LITERAL":
        print("creating a new Constant...")
        node = Constant(int(tokens[0].spelling))
        if pt == "RETURN_STMT":
            parent.value = node
        if pt == "CALL_EXPR":
            parent.args.append(node)

    if nt == "PARM_DECL":
        print("creating a new arg...")
        node = arg(n.spelling)
        parent.args.args.append(node)
        print("parent args:", parent.args.args)

    # a function definition takes the following arguments:
      #  name - a raw string of the function name.

      #  args - an arguments node.

      #  body - the list of nodes inside the function.

      #  decorator_list - the list of decorators to be applied, stored outermost first (i.e. the first in the list will be applied last).

      #  returns - the return annotation.
        
    if nt == "FUNCTION_DECL":
        print("creating a new FunctionDef... num children:", len(list(n.get_children())))
        print("children:")
        for i in n.get_children():
            print(str(i.kind)[11:], i.spelling)
        node = FunctionDef(tokens[1].spelling, body=[], decorator_list=[])
        print("arguments:", end=' ')
        for a in n.get_arguments():
            print(a.spelling, end=' ')
        print()
        # total cop out for function with no args! 
        node.args = add_args() 
        # it does not need a returns, I'm not 100% sure why at this point but it just works without one.
        parent.body.append(node)

    # there is no equivalent to a compound statement in python ASTs, so instead for a 'block' like
    # the compound statement functions as I am simply using an If True: statement.
    if nt == "COMPOUND_STMT":
        print("creating a new CompoundStmt (If)...")
        # node = Pass()
        node = If(Constant(value=True, kind=None), [], [])
        parent.body.append(node)

    if nt == "RETURN_STMT":
        print("creating a new Return...")
        node = Return()
        parent.body.append(node)
    if nt == "UNEXPOSED_EXPR":
        print("creating a new UNEXPOSED_EXPR (If)...")
        node = If(Constant(value=True, kind=None), [], [])
        if pt == "CALL_EXPR":
            parent.func = node
        elif pt == "RETURN_STMT":
            parent.value = node
        else:
            parent.body.append(node)

    if nt == "DECL_REF_EXPR":
        print("creating a new Name...")
        node = Name(n.spelling, Load())
        parent.body.append(node)

    if nt == "CALL_EXPR":
        node = Call([], [])
    print("new created node:", dump(node)) 
    stars()
    return node

def rec_ast_node(n, new_ast, depth):

    # print out information about the node for diagnostic purposes
    nt = str(n.kind)[11:]

    # get the children into their own list
    child_list = list(n.get_children())

    # create a list of new nodes to be added to the body of the previous statement
    for child in child_list:
        node = create_ast_node(nt, new_ast, child)
        rec_ast_node(child, node, depth+1)

    # for c in range(len(child_list)):
    #     if nt == "RETURN_STMT":
    #         new_ast.value = rec_ast_node(child_list[c], child_nodes[c], depth+1)
    #     elif str(child_list[c].kind)[11:] == "PARM_DECL":
    #         new_ast.args.args = rec_ast_node(child_list[c], child_nodes[c], depth+1)
    #     else:
    #         new_ast.body.append(rec_ast_node(child_list[c], child_nodes[c], depth+1))
    if len(list(n.get_children()))==0:
        print("leaf node")
    return new_ast

# create the index
index = clang.cindex.Index.create()
# create the translation unit
tu = index.parse("simple.c")
print("Translation Unit:", tu.spelling, '\n')
# get the root cursor
root = tu.cursor
stars()
print("C AST:")
print_c_ast(root, 0)
stars()
stars()
print("IDEAL PYTHON AST:")
print(dump(parse(open('simple.py').read()), indent=4))
stars()
root_ast = Module([],[])
#print_ast(root, 0)
root_ast = rec_ast_node(root, root_ast, 0)
root_ast = add_main_check(root_ast)


stars()
print("WHAT I GOT:")
print(dump(root_ast))
stars()


print()

stars()
print("RESULTING PYTHON CODE FROM C CODE:")
print(astor.to_source(root_ast))
output = astor.to_source(root_ast)
stars()

stars()
of_name = input("Enter filename to save output to, no file extension [press enter for default]: ")
if of_name == "":
    of_name = "output_file"
of = open(of_name+'.py', 'w')
of.write(output)
print("CODE SAVED TO " + of_name + ".py")
stars()

