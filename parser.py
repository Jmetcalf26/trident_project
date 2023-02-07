#!/usr/bin/python3
import clang.cindex
from clang.cindex import CursorKind
from clang.cindex import TypeKind
import astor
from helper_functions import *
from ast import *
import sys
l_values = [CursorKind.DECL_REF_EXPR, CursorKind.ARRAY_SUBSCRIPT_EXPR, CursorKind.UNARY_OPERATOR]

def debug(x):
    global y
    y = x
    raise RuntimeError('debug')

switch_counter = 0
switch_stack = []

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
    global switch_counter, switch_stack, STRICT_TYPING
    global l_values
    # determine the type of node to create
    nt = str(n.kind)[11:]
    tokens = list((t.spelling for t in n.get_tokens()))
    children = list(n.get_children())

    if not n.kind.is_preprocessing():
        stars()
        print("IN CREATE AST NODE, I want to create a", nt) 
        print("|".join(t for t in tokens))

    # *************************************** 
    # ******* CURRENTLY WORKING NODE ********
    # *************************************** 


    if nt == "TYPEDEF_DECL":
        print_node_info(n)
        return

    if nt == "STRUCT_DECL":
        print_node_info(n)
        node = ClassDef(n.spelling, [Name(c.spelling) for c in children], [], [Pass()], [])
    if nt == "MEMBER_REF_EXPR":
        print_node_info(n)
        node = Attribute(create_ast_node(children[0]), Name(n.spelling))
    if nt == "TYPE_REF":
        print_node_info(n)
        return

    # *************************************** 
    # *************************************** 
    # *************************************** 


    # *************************************** 
    # ************ PREPROCESSING ************ 
    # *************************************** 
    if nt == "INCLUSION_DIRECTIVE":
        if n.kind.is_preprocessing():
            return
        print("creating a new Import statement...")
        print_node_info(n)
        extended_node_info(n)
        return
    if nt == "MACRO_INSTANTIATION":
        if n.kind.is_preprocessing():
            return
        print("creating a new macro instantiation...")
        print_node_info(n)
        extended_node_info(n)
        return

    if nt == "MACRO_DEFINITION":
        if tokens[0] == "_stdio_inclusion":
            node = ImportFrom('pheaders.stdio', [alias(name='*')], 0)
        elif tokens[0] == "_stdlib_inclusion":
            node = ImportFrom('pheaders.stdlib', [alias(name='*')], 0)
        elif tokens[0] == "_string_inclusion":
            node = ImportFrom('pheaders.string', [alias(name='*')], 0)
        elif tokens[0] == "_unistd_inclusion":
            node = ImportFrom('pheaders.unistd', [alias(name='*')], 0)
        else:
            return
    # *************************************** 
    # *************************************** 
    # *************************************** 
        

    # ************************************** 
    # ************** LITERALS ************** 
    # ************************************** 
    if nt == "STRING_LITERAL":
        print("creating a new String...")
        print_node_info(n)
        text = Constant(eval(bytes(n.spelling, 'utf-8').decode()))
        #print(bytes(ord(x) for x in n.spelling).decode())
        a = bytes(map(ord, n.spelling))
        text = Constant(eval(tokens[0]))
        node = BinOp(Name("𐓄"), BitOr(), text)
        
    if nt == "INTEGER_LITERAL":
        print("creating a new Constant...")
        print_node_info(n)
        # node = Call(Name('Data', Load()), [Constant(int(tokens[0])), Constant(n.type.get_size())], [])
        node = Constant(literal_eval(tokens[0]))

    if nt == "FLOATING_LITERAL":
        print("creating a new Constant...")
        print_node_info(n)
        node = Constant(float(tokens[0]))

    if nt == "CHARACTER_LITERAL":
        print("creating a new Constant...")
        print_node_info(n)
        node = Call(func=Name(id='ord', ctx=Load()), args=[Constant(eval(tokens[0]))], keywords=[])
    # ************************************** 
    # ************************************** 
    # ************************************** 
        

    # ************************************** 
    # ************* VARIABLES ************** 
    # ************************************** 
    if nt == "DECL_REF_EXPR":
        print("creating a new Name...")
        print_node_info(n)

        if n.referenced.kind == CursorKind.ENUM_CONSTANT_DECL:
            node = Subscript(Name(n.referenced.semantic_parent.spelling), Constant(n.spelling))
        elif n.referenced.kind == CursorKind.FUNCTION_DECL:
            node = Name(n.spelling, name_opt)
        else:
            node = Name(n.spelling, name_opt)


    if nt == "DECL_STMT":
        print("creating a new something or another...")
        print_node_info(n)
        node = Module(create_stmt_list(children))

    if nt == "VAR_DECL":
        print_node_info(n)
        print("get_type(n)", get_type(n))
        if n.spelling == "id_like_to_see_someone_make_this_variable":
            print("making an import statement")
            node = ImportFrom('pheaders.stdio', [alias(name='*')], 0)

        elif get_type(n) == "VARIABLEARRAY":
            print("variable array")
            node = Assign([Name(n.spelling, Store())], 
                          Call(Name('variable'),
                               [Call(Name('Pointer', Load()), 
                                     [BinOp(List([Constant(0)]), Mult(), create_ast_node(children[0])),
                                      Constant(0), 
                                      Constant(n.type.element_type.get_size())],
                                     [])],
                               [keyword('size', Constant(8))]
                               ))

        elif get_type(n) == "CONSTANTARRAY":
            print("constant array")
            array_size = n.type.element_count
            array_type = n.type.element_type
            array = List([], Load())

            if get_type(children[0]) == "INT":
                print("integer")
                if len(children) == 2:
                    array = create_ast_node(children[1])
            elif len(children) > 0:
                array = create_ast_node(children[0])

            array.elts.extend([Constant(0)] * (array_size - len(array.elts)))
            # remnant from when everything was an array index
            #node = Assign([Name(n.spelling, Store())], 
            #              List([Call(Name('Pointer', Load()),
            #                         [array,
            #                          Constant(0), 
            #                          Constant(n.type.element_type.get_size())],
            #                         [])],
            #                   Load()))

            node = Assign([Name(n.spelling, Store())], 
                          Call(Name('variable'),
                               [Call(Name('Pointer', Load()),
                                     [array,
                                      Constant(0), 
                                      Constant(n.type.element_type.get_size())],
                                     [])], 
                               [keyword('size', Constant(8))]
                               ))

        elif get_type(n) == "RECORD":
            print_type_info(n.type)
            print("GIVE ME CAR:", n.type.get_declaration().spelling)
            struct_name = n.type.get_declaration().spelling
            lhs = [Name(n.spelling, Store())]
            rhs = Call(Name(struct_name), create_expr_list(children[1:]), [])
            node = Assign(lhs, rhs)
        #elif get_type(n) == "POINTER":
            #node = Assign([Name(n.spelling, Store())], create_ast_node(children[0]))
        elif len(children) < 1:
            node = Assign([Name(n.spelling, Store())], Constant(None))
        else:
            #node = Assign([Name(n.spelling, Store())], create_ast_node(children[0]))
            node = Assign([Name(n.spelling, Store())],
                          Call(Name('variable'),
                               [create_ast_node(children[0])], 
                               [keyword('size', Constant(children[0].type.get_size()))]))
        #if STRICT_TYPING:
            #node = add_overflow_check(n, node)
    if nt == "COMPOUND_ASSIGNMENT_OPERATOR":
        print_node_info(n)
        print("creating a new AugAssign...")

        for i in tokens:
            if '=' in i:
                operator = i[0]
        print("HEY IM PRINTING HERE", operator)
        node = AugAssign(create_ast_node(children[0], name_opt=Store()), 
                         translate_operator(operator), 
                         create_ast_node(children[1]))

    if nt == "ARRAY_SUBSCRIPT_EXPR":
        print("creating a new array index...")
        print_node_info(n)
        #node = Subscript(create_ast_node(children[0]), create_ast_node(children[1]))
        node = Call(Name('Deref', Load()), 
                    [create_ast_node(children[0]),
                     create_ast_node(children[1])],
                    [])
        

    if nt == "INIT_LIST_EXPR":
        print("creating a new List...")
        node = List(create_expr_list(children), Load())
    # ************************************** 
    # ************************************** 
    # ************************************** 


    # **************************************
    # ************* EXPRESSIONS ************
    # **************************************
    if nt == "CSTYLE_CAST_EXPR":
        print("creating a new cast...")
        print_node_info(n)
        print("n.type.get_align():", n.type.get_align())
        print(get_type(n))
        if get_type(n) == "INT":
            node = Call(Name('int'), [create_ast_node(children[0])], [])
        
        if get_type(n) == "CHAR_S":
            node = Call(Name('chr'), [create_ast_node(children[0])], [])
        if get_type(n) == "POINTER":
            stars()
            print("CHILD OF POINTER:")
            print_node_info(children[0])
            node = Call(Name('Pointer_alias', Load()), 
                        [create_ast_node(children[0]), 
                         Constant(n.type.get_pointee().get_size())], [])

    if nt == "UNEXPOSED_EXPR":
        print("creating a new UNEXPOSED_EXPR...")
        print_node_info(n)
        print('smelvin', children[0].kind)
        #child = create_ast_node(children[0])
        
        #extended_node_info(n)

        # FUNCTION CALL
        if n.referenced is not None and n.referenced.kind == CursorKind.FUNCTION_DECL:
            node = create_ast_node(children[0])
        # L-VALUE TO R-VALUE
        elif children[0].kind in l_values:
            node = Attribute(create_ast_node(children[0]), 'value', Load())
        # IMPLICIT CAST TYPE 1
        #elif children[0].kind == CursorKind.UNEXPOSED_EXPR:
        else:
            print("implicit cast")
            casted_type = n.type.kind
            original_type = children[0].type.kind
            if get_type(n) == "POINTER":
                print("pointer:")
                print("  outer (casted) unexposed type:", n.type.get_pointee().kind)
                print("  inner (original) unexposed type:", children[0].type.get_pointee().kind)
                # create a pointer alias for the new type
                node = create_ast_node(children[0])
            else:
                print("outer (casted) unexposed type:", casted_type)
                print("inner (original) unexposed type:", original_type)
                # create a node that does the appropriate cast based on the differing sizes
                if casted_type == original_type:
                    node = create_ast_node(children[0])
                elif casted_type == TypeKind.INT:
                    node = Call(Name('int'), [create_ast_node(children[0])], [])
                elif casted_type == TypeKind.DOUBLE or casted_type == TypeKind.FLOAT:
                    node = Call(Name('float'), [create_ast_node(children[0])], [])
                elif casted_type == TypeKind.CHAR_S:
                    node = Call(Name('chr'), [create_ast_node(children[0])], [])
                else:
                    node = create_ast_node(children[0])
        #else:
            #node = create_ast_node(children[0])



    if nt == "PARM_DECL":
        print("creating a new arg...")
        node = arg(n.spelling)

    if nt == "PAREN_EXPR":
        print("creating a new parentheses thing...")
        node = create_ast_node(children[0])

    if nt == "CALL_EXPR":
        print("creating a new Function Call...")

        print_node_info(n)
        node = Call([], [], [])
        node.func = create_ast_node(children[0])
        node.args = [c for c in create_expr_list(children[1:])]
        #node.args = create_expr_list(children[1:])

    if nt == "UNARY_OPERATOR":
        print("creating a new unary op...")
        print_node_info(n)
        print("get_num_template_arguments():", n.get_num_template_arguments())
        operator = tokens[0]
        print("operator:", operator)
        # LOOK AT THIS, THE WAY THAT THE TOKEN IS BEING REFERENCED BREAKS FOR ARRAYS
        if operator == '&':
            size = n.type.get_pointee().get_size()
            if n.type.get_pointee().kind == TypeKind.CONSTANTARRAY:
                size = n.type.get_pointee().get_array_element_type().get_size()

            node = Attribute(create_ast_node(children[0]), 'pointer', Load())
            #else:
            #    print("UH OH, NEW TYPE HAS APPEARED FOR ADDRESSING (&)!")
            #    sys.exit(1)
        elif operator == '*':
            node = Call(Name('Deref'), [create_ast_node(children[0])], [])

        elif '++' in tokens:
            node = AugAssign(create_ast_node(children[0], name_opt=Store()), Add(), Constant(1))
        elif '--' in tokens:
            node = AugAssign(create_ast_node(children[0], name_opt=Store()), Sub(), Constant(1))
        else:
            op = translate_u_operator(operator)
            node = UnaryOp(op, create_ast_node(children[0]))

    if nt == "BINARY_OPERATOR":
        print("creating a new binary op...")
        print_node_info(n)
        operator = tokens[len(list(children[0].get_tokens()))]
        print("operator:", operator)
        if operator in ['||', '&&']:
            node = BoolOp(translate_operator(operator), create_expr_list(children))

        elif operator in ['==', '!=', '<', '<=', '>', '>=']:
            node = Compare(create_ast_node(children[0]), [translate_operator(operator)], [create_ast_node(children[1])])
        elif operator == "=":
            node = Assign([Attribute(create_ast_node(children[0], name_opt=Store()), 'value')], create_ast_node(children[1]))
        else:
            print(get_type(children[0]), get_type(children[1]))
            print(children[0].type.get_size(), children[1].type.get_size())
            # overflow = check_for_int_error(operator, children)
            # print(overflow)
            ltc, rtc = map(type_category,children)
            node = BinOp(create_ast_node(children[0]), translate_operator(operator,ltc,rtc), create_ast_node(children[1]))

    if nt == "ENUM_DECL":
        print_node_info(n)

        keys = [Constant(c.spelling) for c in children]
        values = [Constant(c.enum_value) for c in children]
        node = Assign([Name(n.spelling)], Dict(keys, values))
        
        #node = Module([])
        #enum_value = 0
        #for c in children: 
        #    if len(list(c.get_children())) < 1:
        #        node.body.append(Assign([Name(c.spelling, Store())], Constant(enum_value)))
        #    else:
        #        node.body.append(Assign([Name(c.spelling, Store())], Constant(create_ast_node(list(c.get_children())[0]))))
        #        print("child tokens:", list(c.get_tokens()))
        #        #enum_value = int(list(c.get_tokens())[2])+1

    if nt == "ENUM_CONSTANT_DECL":
        print_node_info(n)
        print("enum value:", n.enum_value)
        node = Assign([Name(n.spelling)], Constant(n.enum_value))

    # **************************************
    # **************************************
    # **************************************

    # **************************************
    # *********** CONTROL FLOW *************
    # **************************************
    if nt == "IF_STMT":
        print("creating a new If...")
        print_node_info(n)
        if children[1].kind == CursorKind.COMPOUND_STMT:
            c = create_stmt_list(children[1].get_children())
        else:
            c = [force_stmt(create_ast_node(children[1]))]
        if len(children) > 2:
            node = If(create_ast_node(children[0]), c, [create_ast_node(children[2])])
        else:
            node = If(create_ast_node(children[0]), c, [])
    if nt == "CONDITIONAL_OPERATOR":
        print_node_info(n)
        if len(children) > 2:
            node = If(create_ast_node(children[0]), [force_stmt(create_ast_node(children[1]))], [force_stmt(create_ast_node(children[2]))])
        else:
            node = If(create_ast_node(children[0]), [force_stmt(create_ast_node(children[1]))], [])

    if nt == "FOR_STMT":
        print("creating a new For (actually a While)...")
        print_node_info(n)
        decl_node = create_ast_node(children[0])
        comp_node = create_ast_node(children[1])
        iter_node = create_ast_node(children[2])
        if children[3].kind == CursorKind.COMPOUND_STMT:
            bod = create_stmt_list(children[3].get_children())
        else:
            bod = [force_stmt(create_ast_node(children[3]))]
        bod.append(iter_node)

        node = Module([decl_node, While(comp_node, bod, [])], [])

    if nt == "WHILE_STMT":
        print("creating a new While...")
        if children[1].kind == CursorKind.COMPOUND_STMT:
            node = While(create_ast_node(children[0]), create_stmt_list(children[1].get_children()), [])
        else:
            node = While(create_ast_node(children[0]), [force_stmt(create_ast_node(children[1]))], [])

    if nt == "SWITCH_STMT":
        print_node_info(n)

        node = Module([])
        state_name = "__switch_state_status"+str(switch_counter)
        switch_name = "__switch_var_value"+str(switch_counter) 
        switch_stack.append((state_name, switch_name))
        switch_counter += 1

        state = Assign([Name(state_name, Store())], List([Constant(0)], Load()))
        switch_value = Assign([Name(switch_name, Store())], List([create_ast_node(children[0])], Load()))
        
        node.body.append(state)
        node.body.append(switch_value)
        print("ASDFASDF")
        cases = list(children[1].get_children())
        for i in cases:
            print(i.kind)
        no = create_ast_node(cases[0]) 
        for i in range(1, len(cases)):
            if cases[i].kind == CursorKind.CASE_STMT or cases[i].kind == CursorKind.DEFAULT_STMT:
                node.body.append(no)
                no = create_ast_node(cases[i])
            elif cases[i].kind == CursorKind.BREAK_STMT:
                no.body.append(Assign([Name(state_name, Store())], List([Constant(2)], Load())))
                i+=1
            else:
                no.body.append(force_stmt(create_ast_node(cases[i])))
        node.body.append(no)

        switch_stack.pop()

    if nt == "CASE_STMT":
        print_node_info(n)

        # look at index -1 for the correct
        state_name, switch_name = switch_stack[-1]
        #condition= BoolOp(And(), [Compare(Name(switch_name), [Eq()], [create_ast_node(children[0])]), Compare(Name(switch_name), [Eq()], [create_ast_node(children[0])])])
        #node = If(condition, create_stmt_list(children[1].get_children()), [])
        print(children[1])
        if children[1].kind == CursorKind.BREAK_STMT:
            chi = Assign([Name(state_name, Store())], List([Constant(2)], Load()))
        else:
            chi = force_stmt(create_ast_node(children[1]))

        # remnant from when everything was an array index
        #node = If(test=BoolOp(op=Or(), values=[Compare(left=Subscript(Name(state_name, ctx=Load()), Constant(0), name_opt), ops=[Eq()], comparators=[Constant(value=1)]), BoolOp(op=And(), values=[Compare(left=Subscript(Name(state_name, ctx=Load()), Constant(0), name_opt), ops=[Eq()], comparators=[Constant(value=0)]), Compare(left=Subscript(Name(switch_name, ctx=Load()), Constant(0), name_opt), ops=[Eq()], comparators=[create_ast_node(children[0])])])]), body=[chi], orelse=[])
        node = If(test=BoolOp(op=Or(), values=[Compare(left=Name(state_name, ctx=Load()), ops=[Eq()], comparators=[Constant(value=1)]), BoolOp(op=And(), values=[Compare(left=Name(state_name, ctx=Load()), ops=[Eq()], comparators=[Constant(value=0)]), Compare(left=Name(switch_name, ctx=Load()), ops=[Eq()], comparators=[create_ast_node(children[0])])])]), body=[chi], orelse=[])
        #if is_child(children[1].get_children(), "BREAK_STMT"):
            #print("THIS CASE HAS A BREAK STATEMENT!")
            #node.body.insert(Assign([Name(state_name, Store())], List([Constant(2)], Load())), 0)
        
    if nt == "DEFAULT_STMT":
        print_node_info(n)
        state_name, switch_name = switch_stack[-1]
        if children[0].kind == CursorKind.BREAK_STMT:
            # remnant from when everything was an array index
            #chi = Assign([Subscript(Name(state_name, ctx=Load()), Constant(0), Store())], List([Constant(2)], Load()))
            chi = Assign([Name(state_name, ctx=Load())], List([Constant(2)], Load()))
        else:
            chi = force_stmt(create_ast_node(children[0]))
        # remnant from when everything was an array index
        #node = Subscript(Name(n.spelling, Load()), Constant(0), name_opt)
        node = Name(n.spelling, Load())
        # remnant from when everything was an array index
        #node = If(test=Compare(left=Subscript(Name(state_name, ctx=Load()), Constant(0), name_opt), ops=[Lt()], comparators=[Constant(value=2)]), body=[chi], orelse=[])
        node = If(test=Compare(left=Name(state_name, ctx=Load()), ops=[Lt()], comparators=[Constant(value=2)]), body=[chi], orelse=[])

    # ************************************** 
    # ************* STATEMENTS ************* 
    # ************************************** 
    if nt == "COMPOUND_STMT":
        print("creating a new CompoundStmt (If)...")
        node = If(Constant(value=True, kind=None), [], [])
        node.body = create_stmt_list(children)

    if nt == "RETURN_STMT":
        print("creating a new Return...")
        node = Return()
        node.value = create_ast_node(children[0])

    if nt == "BREAK_STMT":
        node = Break()

    if nt == "CONTINUE_STMT":
        node = Continue()
    # ************************************** 
    # ************************************** 
    # ************************************** 


    # ************************************** 
    # ******* FUNCTIONS AND CLASSES ******** 
    # ************************************** 
    if nt == "FUNCTION_DECL":
        print_node_info(n)
        print("n.is_definition():", n.is_definition())
        print("n.kind.is_declaration():", n.kind.is_declaration())
        if not n.is_definition():
            print("ignoring function prototype")
            return

        print("creating a new FunctionDef... num children:", len(list(n.get_children())))
        print("children:")
        for i in n.get_children():
            print(str(i.kind)[11:], i.spelling)

        name_token = n.spelling
        print("BADABING:", name_token)
        node = FunctionDef(name_token, body=[], decorator_list=[])
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
    # ************************************** 
    # ************************************** 
    # ************************************** 

    print("new created node:", dump(node))
    stars()
    return node

