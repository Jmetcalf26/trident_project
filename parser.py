import clang.cindex
import astor
from helper_functions import *
from ast import *


def create_ast_list(node_list):
    nl = []
    for n in node_list:
        nl.append(create_ast_node(n))
    return nl 

def create_ast_node(n, name_opt=Load()):
    # determine the type of node to create
    stars()
    nt = str(n.kind)[11:]
    tokens = list(n.get_tokens())
    children = list(n.get_children())
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
        node.body = create_ast_list(children)

    if nt == "WHILE_STMT":
        print("creating a new While...")
        if len(children) > 2:
            node = While(create_ast_node(children[0]), create_ast_list(children[1].get_children()), [create_ast_node(children[2])])
        else:
            node = While(create_ast_node(children[0]), create_ast_list(children[1].get_children()), [])
        
    if nt == "IF_STMT":
        print("creating a new If...")
        if len(children) > 2:
            node = If(create_ast_node(children[0]), create_ast_list(children[1].get_children()), [create_ast_node(children[2])])
        else:
            node = If(create_ast_node(children[0]), create_ast_list(children[1].get_children()), [])
        
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

        # add a list of nodes for the arguments to the function
        node.args.args = create_ast_list(children[:num_args])

        # add a list of nodes for the body of the function, using the guaranteed compound statement as the last child to cut it out entirely
        node.body = create_ast_list(children[len(children)-1].get_children())

        # it does not need a returns, I'm not 100% sure why at this point but it just works without one.

    if nt == "DECL_STMT":
        print("creating a new something or another...")
        node = create_ast_node(children[0])

    # value=List(
    #     elts=[
    #             Constant(value=1)],
    #         ctx=Load())),

    if nt == "VAR_DECL":
        node = Assign([Name(n.spelling, Store())], List([create_ast_node(children[0])], Load()))

    if nt == "RETURN_STMT":
        print("creating a new Return...")
        node = Return()
        node.value = create_ast_node(children[0])


    if nt == "UNEXPOSED_EXPR":
        print("creating a new UNEXPOSED_EXPR (If)...")
        print_node_info(n)
        node = create_ast_node(children[0])

    # Subscript(
    #     value=Name(id='a', ctx=Load()),
    #     slice=Constant(value=0),
    #     ctx=Load()),

    if nt == "DECL_REF_EXPR":
        print("creating a new Name...")
        if n.spelling == 'printf':
            name = 'print'
        else:
            name = n.spelling
        if "FUNCTION" in str(n.referenced.kind):
            node = Name(name, name_opt)
        else:
            node = Subscript(Name(name, Load()), Constant(0), name_opt)

    if nt == "CALL_EXPR":
        print_node_info(n)
        extended_node_info(n)
        node = Call([], [], [])
        #node.func = Name(children[0].spelling, Load())
        node.func = create_ast_node(children[0])
        node.args = create_ast_list(children[1:])
        # function calls are not going to work until I figure out how to properly couch function calls that
        # appear on a statement by themselves
        # just adding an expr to all of them breaks all function calls that are not entire statements
        # node = Expr(node)


    if nt == "UNARY_OPERATOR":
        operator = tokens[0].spelling
        print("operator:", operator)
        op = translate_u_operator(operator)
        node = UnaryOp(op, create_ast_node(children[0]))

        
    if nt == "BINARY_OPERATOR":
        node = BinOp()
        
        operator = tokens[len(list(children[0].get_tokens()))].spelling
        print("operator:", operator)
        if operator in ['==', '!=', '<', '<=', '>', '>=']:
            node = Compare(create_ast_node(children[0]), [translate_operator(operator)], [create_ast_node(children[1])])
        elif operator == "=":
            print("EQUALS SIGN, ASSIGNMENT")
            node = Assign([create_ast_node(children[0], Store())], create_ast_node(children[1]))
        else: 
            node.op = translate_operator(operator)
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

root_ast = add_main_check(root_ast)



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

