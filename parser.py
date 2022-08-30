import clang.cindex
import astor
from helper_functions import *
from ast import *

def print_node_info(n):
    num_args = len(list(n.get_arguments()))
    print('num_args:', num_args)
    children = list(n.get_children())
    print('num_children:', len(children))
    print("arguments:", end=' ')
    for a in n.get_arguments():
        print(a.spelling, end=' ')
    print()

    print('children:')
    for c in children:
        print(str(c.kind)[11:], c.spelling)
    print("|".join(t.spelling for t in n.get_tokens()))
    return

def create_ast_list(node_list):
    nl = []
    for n in node_list:
        nl.append(create_ast_node(n))
    return nl 

def create_ast_node(n):
    # determine the type of node to create
    stars()
    nt = str(n.kind)[11:]
    tokens = list(n.get_tokens())
    print("IN CREATE AST NODE, I want to create a", nt)

    # in the case of an int, a literal integer is created, with only a value
    if nt == "INTEGER_LITERAL":
        print("creating a new Constant...")
        node = Constant(int(tokens[0].spelling))

    if nt == "PARM_DECL":
        print("creating a new arg...")
        node = arg(n.spelling)

    if nt=="COMPOUND_STMT":
        print("creating a new CompoundStmt (If)...")
        node = If(Constant(value=True, kind=None), [], [])
        children = list(n.get_children())
        node.body = create_ast_list(children)

    if nt == "FUNCTION_DECL":
        print("creating a new FunctionDef... num children:", len(list(n.get_children())))
        print("children:")
        for i in n.get_children():
            print(str(i.kind)[11:], i.spelling)
        node = FunctionDef(tokens[1].spelling, body=[], decorator_list=[])
        # get the number of arguments
        num_args = len(list(n.get_arguments()))

        # populate all of the argument arrays 
        node.args = add_args() 

        # create the child list
        children = list(n.get_children())

        # add a list of nodes for the arguments to the function
        node.args.args = create_ast_list(children[:num_args])

        # add a list of nodes for the body of the function, using the guaranteed compound statement as the last child to cut it out entirely
        node.body = create_ast_list(children[len(children)-1].get_children())

        # it does not need a returns, I'm not 100% sure why at this point but it just works without one.

    if nt == "RETURN_STMT":
        print("creating a new Return...")
        node = Return()
        print_node_info(n)
        node.value = create_ast_node(list(n.get_children())[0])


    if nt == "UNEXPOSED_EXPR":
        print("creating a new UNEXPOSED_EXPR (If)...")
        print_node_info(n)
        extended_node_info(n)
        node = create_ast_node(list(n.get_children())[0])

    if nt == "DECL_REF_EXPR":
        print("creating a new Name...")
        node = Name(n.spelling, Load())
        extended_node_info(n)
        print_node_info(n)

    if nt == "CALL_EXPR":
        node = Call([], [], [])
        children = list(n.get_children())
        print_node_info(n)
        node.func = create_ast_node(children[0])
        node.args = create_ast_list(children[1:])

    if nt == "BINARY_OPERATOR":
        print_node_info(n)
        node = BinOp()

        children = list(n.get_children())
        operator = tokens[len(list(children[0].get_tokens()))].spelling
        print("operator:", operator)
        node.op = translate_operator(operator)
        if operator == '+':
            node.op = Add()
        elif operator == '-':
            node.op = Sub()
        elif operator == '*':
            node.op = Mult()
        elif operator == '/':
            node.op = Div()
        node.left = create_ast_node(children[0])
        node.right = create_ast_node(children[1])
        
    print("new created node:", dump(node)) 
    stars()
    return node


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

root = tu.cursor
root_ast = Module([],[])
childs = list(root.get_children())
root_ast.body = create_ast_list(childs)

# root_ast = add_main_check(root_ast)



stars()
print("IDEAL PYTHON AST:")
print(dump(parse(open('simple.py').read()), indent=4))
stars()
stars()
print("WHAT I GOT:")
print(dump(root_ast, indent=4))
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

