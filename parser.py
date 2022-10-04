#!/usr/bin/python3
import clang.cindex
from clang.cindex import CursorKind
from clang.cindex import TypeKind
import astor
from helper_functions import *
from ast import *
import sys


def create_stmt_list(node_list):
    return [force_stmt(create_ast_node(n)) for n in node_list]
def create_expr_list(node_list):
    return [create_ast_node(n) for n in node_list]

def force_stmt(n):
    if isinstance(n, stmt):
        return n
    else:
        return Expr(n)

def create_ast_node(n, name_opt=Load()):

    # determine the type of node to create
    stars()
    nt = str(n.kind)[11:]
    tokens = list((t.spelling for t in n.get_tokens()))
    children = list(n.get_children())
    print("IN CREATE AST NODE, I want to create a", nt)
    print("|".join(t for t in tokens))

    if nt == "STRING_LITERAL":
        print("creating a new String...")
        print_node_info(n)
        node = Constant(eval(n.spelling))

    if nt == "INTEGER_LITERAL":
        print("creating a new Constant...")
        print_node_info(n)
        # node = Call(Name('Data', Load()), [Constant(int(tokens[0])), Constant(n.type.get_size())], [])
        node = Constant(int(tokens[0]))

    if nt == "FLOATING_LITERAL":
        print("creating a new Constant...")
        print_node_info(n)
        node = Constant(float(tokens[0]))

    if nt == "CHARACTER_LITERAL":
        print("creating a new Constant...")
        print_node_info(n)
        node = Constant(eval(tokens[0]))

    if nt == "UNEXPOSED_EXPR":
        print("creating a new UNEXPOSED_EXPR (If)...")
        print_node_info(n)
        # node = Call(Name('Data', Load()), [create_ast_node(children[0]), Constant(n.type.get_size())], [])
        node = create_ast_node(children[0])

    if nt == "PARM_DECL":
        print("creating a new arg...")
        node = arg(n.spelling)

    if nt=="COMPOUND_STMT":
        print("creating a new CompoundStmt (If)...")
        node = If(Constant(value=True, kind=None), [], [])
        node.body = create_stmt_list(children)

    if nt == "FOR_STMT":
        print("creating a new For (actually a While)...")
        decl_node = create_ast_node(children[0])
        comp_node = create_ast_node(children[1])
        iter_node = create_ast_node(children[2])
        bod = create_stmt_list(children[3].get_children())
        bod.append(iter_node)

        node = If(Constant(value=True, kind=None), [decl_node, While(comp_node, bod, [])], [])

    if nt == "WHILE_STMT":
        print("creating a new While...")
        node = While(create_ast_node(children[0]), create_stmt_list(children[1].get_children()), [])

    if nt == "IF_STMT":
        print("creating a new If...")
        if len(children) > 2:
            node = If(create_ast_node(children[0]), create_stmt_list(children[1].get_children()), [create_ast_node(children[2])])
        else:
            node = If(create_ast_node(children[0]), create_stmt_list(children[1].get_children()), [])

    if nt == "FUNCTION_DECL":
        if n.type.get_canonical().kind == TypeKind.FUNCTIONPROTO:
            print("ignoring function prototype")
            return
        print("creating a new FunctionDef... num children:", len(list(n.get_children())))
        print("children:")
        for i in n.get_children():
            print(str(i.kind)[11:], i.spelling)
        node = FunctionDef(tokens[1], body=[], decorator_list=[])
        # get the number of arguments
        num_args = len(list(n.get_arguments()))

        # populate all of the argument arrays 
        node.args = add_args()

        # create the child list

        # add a list of nodes for the arguments to the function
        node.args.args = create_expr_list(children[:num_args])

        # add a list of nodes for the body of the function, using the guaranteed compound statement as the last child to cut it out entirely
        node.body = create_stmt_list(children[len(children)-1].get_children())

        # it does not need a returns, I'm not 100% sure why at this point but it just works without one.

    if nt == "DECL_STMT":
        print("creating a new something or another...")
        print_node_info(n)
        node = create_ast_node(children[0])

    if nt == "VAR_DECL":
        print_node_info(n)
        print("get_type(n)", get_type(n))
        if n.spelling == "id_like_to_see_someone_make_this_variable":
            print("making an import statement")
            node = ImportFrom('pheaders.stdio', [alias(name='*')], 0)

        elif get_type(n) == "VARIABLEARRAY":
            print("variable array")
            node = Assign([Name(n.spelling, Store())], List([Call(Name('Pointer', Load()), [BinOp(List([Constant(0)]), Mult(), create_ast_node(children[0])), Constant(0), Constant(n.type.element_type.get_size())], [])], Load()))

        elif get_type(n) == "CONSTANTARRAY":
            print("constant array")
            array_size = n.type.element_count
            array_type = n.type.element_type
            if get_type(children[0]) == "INT":
                array = create_ast_node(children[1])
            elif len(children) > 0:
                array = create_ast_node(children[0])
            else:
                array = List([], Load())
            array.elts.extend([Constant(0)] * (array_size - len(array.elts)))
            node = Assign([Name(n.spelling, Store())], List([Call(Name('Pointer', Load()), [array, Constant(0), Constant(n.type.element_type.get_size())], [])], Load()))
        elif len(children) < 1:
            node = Assign([Name(n.spelling, Store())], List([Constant(0)], Load()))
        else:
            #node = Assign([Name(n.spelling, Store())], List([Call(Name('Data', Load()), [create_ast_node(children[0]), Constant(n.type.get_size())], [])], Load()))
            node = Assign([Name(n.spelling, Store())], List([create_ast_node(children[0])], []), Load())
        if STRICT_TYPING:
            node = add_overflow_check(n, node)
        #if get_type(n) == "POINTER":
            #node.value.elts[0].args[2].value = n.type.get_pointee().get_size()

    if nt == "RETURN_STMT":
        print("creating a new Return...")
        node = Return()
        node.value = create_ast_node(children[0])

    if nt == "DECL_REF_EXPR":
        print("creating a new Name...")
        print_node_info(n)
        if n.referenced.kind == CursorKind.FUNCTION_DECL:
            node = Name(n.spelling, name_opt)
        else:
            node = Subscript(Name(n.spelling, Load()), Constant(0), name_opt)

    if nt == "CALL_EXPR":
        print_node_info(n)
        extended_node_info(n)
        node = Call([], [], [])
        #node.func = Name(children[0].spelling, Load())
        node.func = create_ast_node(children[0])
        # List([create_ast_node(children[0])], Load())
        node.args = [List([c], Load()) for c in create_expr_list(children[1:])]

    if nt == "COMPOUND_ASSIGNMENT_OPERATOR":
        print("creating a new AugAssign...")
        operator = tokens[1][0]
        node = AugAssign(create_ast_node(children[0], name_opt=Store()), translate_operator(operator), create_ast_node(children[1]))

    if nt == "PAREN_EXPR":
        print("creating a new parentheses thing...")
        node = create_ast_node(children[0])

    if nt == "ARRAY_SUBSCRIPT_EXPR":
        print("creating a new array index...")
        print_node_info(n)
        node = Subscript(create_ast_node(children[0]), create_ast_node(children[1]))

    if nt == "INIT_LIST_EXPR":
        print("creating a new List...")
        node = List(create_expr_list(children), Load())


    if nt == "UNARY_OPERATOR":
        print("creating a new unary op...")
        print_node_info(n)
        operator = tokens[0]
        print("operator:", operator)
        if operator == '&':
            size = n.type.get_pointee().get_size()
            if n.type.get_pointee().kind == TypeKind.CONSTANTARRAY:
                size = n.type.get_pointee().get_array_element_type().get_size()
            node = Call(Name('Pointer', Load()), [Name(tokens[1], Load()), Constant(0), Constant(size)], [])
        elif operator == '*':
            node = Call(Attribute(create_ast_node(children[0]), 'deref', Load()), [], [])
        elif '++' in tokens:
            node = AugAssign(create_ast_node(children[0], name_opt=Store()), Add(), Constant(1))
        elif '--' in tokens:
            node = AugAssign(create_ast_node(children[0], name_opt=Store()), Sub(), Constant(1))
        else:
            op = translate_u_operator(operator)
            node = UnaryOp(op, create_ast_node(children[0]))

    if nt == "BINARY_OPERATOR":
        print("creating a new binary op...")

        operator = tokens[len(list(children[0].get_tokens()))]
        print("operator:", operator)
        if operator in ['==', '!=', '<', '<=', '>', '>=']:
            node = Compare(create_ast_node(children[0]), [translate_operator(operator)], [create_ast_node(children[1])])
        elif operator == "=":
            node = Assign([create_ast_node(children[0], name_opt=Store())], create_ast_node(children[1]))
        else:
            print(get_type(children[0]), get_type(children[1]))
            print(children[0].type.get_size(), children[1].type.get_size())
            # overflow = check_for_int_error(operator, children)
            # print(overflow)
            node = BinOp(create_ast_node(children[0]), translate_operator(operator), create_ast_node(children[1]))


    print("new created node:", dump(node))
    stars()
    return node


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
    tu = index.parse(filename, args=['-Iheaders'])
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

root_ast.body.append(add_helper_classes())
root_ast.body.extend(create_stmt_list(childs))
root_ast.body.append(add_main_check())



# stars()
# print("IDEAL PYTHON AST:")
# print(dump(parse(open('simple.py').read()), indent=4))
# stars()
stars()
print("WHAT I GOT:")
print(dump(root_ast, indent=4))
stars()

stars()
print("DIAGNOSTICS REPORT:")
diag = tu.diagnostics
for i in diag:
    print(i)
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

