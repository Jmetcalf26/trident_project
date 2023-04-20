#!/usr/bin/python3
import clang_lib.cindex
from clang_lib.cindex import CursorKind, TypeKind, BinaryOperator
from clang_lib.cindex import TypeKind
from clang_lib.cindex import BinaryOperator
import astor
from helper_functions import *
from ast import *
import sys, re
l_values = [CursorKind.DECL_REF_EXPR, CursorKind.ARRAY_SUBSCRIPT_EXPR, CursorKind.UNARY_OPERATOR]
array_values = [TypeKind.CONSTANTARRAY, TypeKind.VARIABLEARRAY, TypeKind.DEPENDENTSIZEDARRAY, TypeKind.INCOMPLETEARRAY]

def debug(x):
    global y
    y = x
    raise RuntimeError('debug')

switch_counter = 0
switch_stack = []
IGNORE_NODES = False

def create_stmt_list(node_list):
    stmt_list = [force_stmt(create_ast_node(n)) for n in node_list]
    if not stmt_list:
        return [Pass()]
    return stmt_list
def create_expr_list(node_list):
    return [create_ast_node(n) for n in node_list]

def force_stmt(n):
    if isinstance(n, stmt):
        return n
    else:
        return Expr(n)

def create_ast_node(n, name_opt=Load()):
    global switch_counter, switch_stack, STRICT_TYPING, IGNORE_NODES, l_values
    # determine the type of node to create
    nt = str(n.kind)[11:]
    tokens = list((t.spelling for t in n.get_tokens()))
    children = list(n.get_children())

    if n.spelling not in preprocessing:
        stars()
        print("NODE TYPE:", nt) 
        print("TOKENS:", end=' ')
        print("|".join(t for t in tokens))

    start_pattern = re.compile('custom_[a-z]*_inclusion_START')
    end_pattern = re.compile('custom_[a-z]*_inclusion_END')
    if bool(start_pattern.match(n.spelling)):
        IGNORE_NODES = True
    elif bool(end_pattern.match(n.spelling)):
        IGNORE_NODES = False
        print("IGNORE NODE MODE IS TURNED ON!")
        stars()
        return

    if IGNORE_NODES:
        print("IGNORE NODE MODE IS TURNED ON!")
        stars()
        return
    # *************************************** 
    # ******* CURRENTLY WORKING NODE ********
    # *************************************** 
    if nt == "NULL_STMT":
        print_node_info(n)
        return
    if nt == "CXX_UNARY_EXPR":
        print_node_info(n)
        extended_node_info(n)

        if tokens[0] == 'sizeof':
            if len(children) > 0:
                size = children[0].type.get_size()
                print("size:", size)
                node = Call(Name('sizeof'), [create_ast_node(children[0]), Constant(size)], [])
            else:
                size = csizeof(' '.join(tokens))
                op = tokens.index('(')+1
                cp = tokens.index(')')
                node = Call(Name('sizeof'), [Constant(' '.join(tokens[op:cp])), Constant(size)], [])
        
    if nt == "TYPEDEF_DECL":
        print_node_info(n)
        print("n.underlying_typedef_type", n.underlying_typedef_type.kind)
        '''
        try:
            node = create_ast_node(children[[c.kind for c in children].index(CursorKind.STRUCT_DECL)])
        except Exception:
            return
        '''
        node = Assign([Name(n.spelling+'_TYPEDEF')], Constant(0))

    if nt == "STRUCT_DECL":

        print_node_info(n)
        args = [arg(c.spelling) for c in children]
        args.insert(0, arg('self'))
        init = FunctionDef('__init__', arguments(args=args, defaults=[Constant(0)]*(len(args)-1)), [], [])
        init.body = [Assign([Attribute(Name('self'), c.spelling, Store())], Name(c.spelling)) for c in children]  

        struct_name = n.displayname if n.displayname else n.type.get_canonical().spelling
        node = ClassDef(struct_name, [], [], [init], [])

    if nt == "MEMBER_REF_EXPR":
        print_node_info(n)
        node = Attribute(create_ast_node(children[0]), Name(n.spelling))

    if nt == "TYPE_REF":
        print('creating a new typeref...')
        #print("n.underlying_typedef_type", n.underlying_typedef_type.kind)
        print_node_info(n)
        #extended_node_info(n)
        return

    # *************************************** 
    # *************************************** 
    # *************************************** 


    # *************************************** 
    # ************ PREPROCESSING ************ 
    # *************************************** 
    if nt == "INCLUSION_DIRECTIVE":
        print("creating a new Import statement...")
        print_node_info(n)
        if n.kind.is_preprocessing():
            return
    if nt == "MACRO_INSTANTIATION":
        if n.kind.is_preprocessing():
            return
        print("creating a new macro instantiation...")
        print_node_info(n)
        return

    if nt == "MACRO_DEFINITION":
        if tokens[0] in preprocessing:
            return
        print_node_info(n)
        if tokens[0] == "_stdio_inclusion":
            node = ImportFrom('pheaders.stdio', [alias(name='*')], 0)
        elif tokens[0] == "_stdlib_inclusion":
            node = ImportFrom('pheaders.stdlib', [alias(name='*')], 0)
        elif tokens[0] == "_string_inclusion":
            node = ImportFrom('pheaders.string', [alias(name='*')], 0)
        elif tokens[0] == "_unistd_inclusion":
            node = ImportFrom('pheaders.unistd', [alias(name='*')], 0)
        elif tokens[0] == "_time_inclusion":
            node = ImportFrom('pheaders.time_py', [alias(name='*')], 0)
        elif tokens[0] == "_alloca_inclusion":
            node = ImportFrom('pheaders.alloca', [alias(name='*')], 0)
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
        print([t.kind for t in list(n.get_tokens())])
        #print([t.kind for t in list(n.get_tokens())])
        print_node_info(n)
        extended_node_info(n)
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
        try:
            list_node = children[[c.kind for c in children].index(CursorKind.INIT_LIST_EXPR)]
        except Exception:
            list_node = None
        try:
            num_element_node = children[[c.kind for c in children].index(CursorKind.INTEGER_LITERAL)]
        except Exception:
            try:
                num_element_node = children[[c.kind for c in children].index(CursorKind.BINARY_OPERATOR)] 
            except Exception:
                num_element_node = None
        try:
            type_ref_node = children[[c.kind for c in children].index(CursorKind.TYPE_REF)]
        except Exception:
            type_ref_node = None
        try:
            string_node = children[[c.kind for c in children].index(CursorKind.STRING_LITERAL)]
        except Exception:
            string_node = None

        print('NODES IN THE VAR_DECL')
        if list_node:
            print('list node', list_node.kind)
        if num_element_node:
            print('num_element_node', num_element_node.kind)
        if type_ref_node:
            print('type_ref_node', type_ref_node.kind)
        print()
        print("get_type(n)", get_type(n))
        print_node_info(n)
        #extended_node_info(n)

        if n.spelling == "id_like_to_see_someone_make_this_variable":
            print("making an import statement")
            node = ImportFrom('pheaders.stdio', [alias(name='*')], 0)


        elif get_type(n) == "VARIABLEARRAY":
            print("variable array")
            node = Assign([Name(n.spelling, Store())], 
                          Call(Name('variable'),
                               [BinOp(List([Constant(0)]), Mult(), create_ast_node(children[0]))],
                               [keyword('size', Constant(n.type.element_type.get_size()))]))
            print('its time to pay the piper')
            sys.exit(1)

        elif get_type(n) == "CONSTANTARRAY":
            print("constant array")
            print('n.type', n.type.get_canonical().kind)
            if type_ref_node:
                array_size = n.type.get_canonical().element_count
                array_type = n.type.get_canonical().element_type
            else:
                array_size = n.type.element_count
                array_type = n.type.element_type
            print('array_size', array_size)
            print('array_type', array_type.kind)

            array = List([], Load())
            if list_node:
                array = create_ast_node(list_node)
                array.elts.extend([Constant(0)] * (array_size - len(array.elts)))
                node = Assign([Name(n.spelling, Store())], 
                              Call(Name('variable'),
                                   [Call(Name('Pointer'), 
                                         [array, Constant(0), Constant(array_type.get_size())], [])],
                                   [keyword('size', Constant(8))]))
            elif string_node:
                array = create_ast_node(string_node)

                node = Assign([Name(n.spelling, Store())], 
                              Call(Name('variable'),
                                   [array],
                                   [keyword('size', Constant(8))]))
            else:
                node = Assign([Name(n.spelling, Store())], 
                              Call(Name('variable'),
                                   [Call(Name('Pointer'), 
                                         [BinOp(List([Constant(0)]), Mult(), create_ast_node(num_element_node)), Constant(0), Constant(array_type.get_size())], [])],
                                   [keyword('size', Constant(8))]))

        # THIS MEANS STRUCT!
        elif get_type(n) == "RECORD":
            print("STRUCT MODE ACTIVATE")
            struct_name = n.type.get_declaration().spelling
            lhs = [Name(n.spelling, Store())]
            if list_node:
                rhs = Call(Name(struct_name), create_expr_list(list_node.get_children()), [])
            else:
                rhs = create_ast_node(children[-1])
            node = Assign(lhs, 
                          Call(Name('variable'),
                               [rhs],
                               [keyword('size', Constant(n.type.get_size()))]))
        #elif get_type(n) == "POINTER":
            #node = Assign([Name(n.spelling, Store())], create_ast_node(children[0]))
        elif len(children) < 1 or (len(children) == 1 and type_ref_node):
            node = Assign([Name(n.spelling, Store())],
                          Call(Name('variable'),
                               [Constant(None)], 
                               [keyword('size', Constant(n.type.get_size()))]))
        else:
            #node = Assign([Name(n.spelling, Store())], create_ast_node(children[0]))
            print(n.type.spelling, "whoo")
            if type_ref_node:
                child = create_ast_node(children[1])
            else:
                child = create_ast_node(children[0])

            node = Assign([Name(n.spelling, Store())],
                          Call(Name('variable'),
                               [child], 
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
        node = Attribute(Call(Name('Deref', Load()), 
                    [create_ast_node(children[0]),
                     create_ast_node(children[1])],
                    []), 'value', Load())
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
        print('type_num', n.type._kind_id)
        print(get_type(n))

        type_num = n.type._kind_id
        if (type_num > 7 and type_num < 13) or (type_num > 15 and type_num < 24):
            node = Call(Name('int'), [create_ast_node(children[0])], [])

        if (type_num > 3 and type_num < 8) or (type_num > 12 and type_num < 16):
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
        #print('smelvin', children[0].kind)
        #child = create_ast_node(children[0])
        
        #extended_node_info(n)

        # FUNCTION CALL <FunctionToPointerDecay>
        # CONST CHAR TO CHAR <NoOp>
        if is_FunctionToPointerDecay(n) or is_NoOp(n):
            node = create_ast_node(children[0])

        # L-VALUE TO R-VALUE <LValueToRValue>
        elif is_LValueToRValue(n):
            node = Attribute(create_ast_node(children[0]), 'value', Load())

        # ARRAY TO POINTER <ArrayToPointerDecay>
        elif is_ArrayToPointerDecay(n) and children[0].kind == CursorKind.UNEXPOSED_EXPR:
            print("WOAH DUDE!")
            node = Attribute(create_ast_node(children[0]), 'value', Load())

        # IMPLICIT CAST TYPE 1
        else:
            print("implicit cast")
            casted_type = n.type.kind
            original_type = children[0].type.kind

            # IMPLICIT POINTER CAST
            if get_type(n) == "POINTER":
                print("pointer:")
                casted_type = n.type.get_pointee().kind
                original_type = children[0].type.get_pointee().kind
                print("  outer (casted) unexposed type:", casted_type)
                print("  inner (original) unexposed type:", original_type)

                # create a pointer alias for the new type
                if casted_type == original_type or original_type == TypeKind.INVALID:
                    node = create_ast_node(children[0])
                else:
                    node = Call(Name('Pointer_alias', Load()), 
                                [create_ast_node(children[0]), 
                                 Constant(n.type.get_pointee().get_size())], [])

                if original_type == TypeKind.VOID:
                    node = create_ast_node(children[0])

            # IMPLICIT VARIABLE CAST
            else:
                print("outer (casted) unexposed type:", casted_type)
                print("inner (original) unexposed type:", original_type)
                # create a node that does the appropriate cast based on the differing sizes
                if casted_type == original_type:
                    node = create_ast_node(children[0])
                elif casted_type in [TypeKind.INT, TypeKind.CHAR_S]:
                    if original_type in [TypeKind.CHAR_S, TypeKind.INT]:
                        node = create_ast_node(children[0])
                    else:
                        node = Call(Name('int'), [create_ast_node(children[0])], [])
                elif casted_type == TypeKind.DOUBLE or casted_type == TypeKind.FLOAT:
                    node = Call(Name('float'), [create_ast_node(children[0])], [])
                else:
                    node = create_ast_node(children[0])



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

    if nt == "UNARY_OPERATOR":
        print("creating a new unary op...")
        print_node_info(n)
        print("get_num_template_arguments():", n.get_num_template_arguments())
        operator = tokens[0]

        print("operator:", operator)
        if operator == '&':
            size = n.type.get_pointee().get_size()
            if n.type.get_pointee().kind == TypeKind.CONSTANTARRAY:
                size = n.type.get_pointee().get_array_element_type().get_size()
            #else:
                #print("UH OH, NEW TYPE HAS APPEARED FOR ADDRESSING (&)!")
                #sys.exit(1)
            node = Attribute(create_ast_node(children[0]), 'pointer', Load())
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
        operator = n.binary_operator
        print("operator:", operator)
        print_node_info(n)

        #raise ValueError()
        if operator.value == 19 or operator.value == 20 :
            node = BoolOp(translate_operator(operator), create_expr_list(children))

        elif operator.value in range(10, 16):
            node = Compare(create_ast_node(children[0]), [translate_operator(operator)], [create_ast_node(children[1])])
        elif operator.value == 21:
            #node = Assign([create_ast_node(children[0], name_opt=Store())], create_ast_node(children[1]))
            node = Assign([Attribute(create_ast_node(children[0], name_opt=Store()), 'value')], create_ast_node(children[1]))
        else:
            #print('types of children:', get_type(children[0]), get_type(children[1]))
            #print('sizeschildren[0].type.get_size(), children[1].type.get_size())
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
        args = []
        for c in children:
            if c.kind == CursorKind.PARM_DECL:
                args.append(c)
        node.args.args = create_expr_list(args)
        node.args.defaults=[Constant(0)]*(len(args))

        # add a list of nodes for the body of the function, using the guaranteed compound statement as the last child to cut it out entirely
        node.body = []
        for c in args:
            node.body.append(Assign([Name(c.spelling)], 
                                    Call(Name('variable'), 
                                         [Name(c.spelling)], 
                                         [keyword('size', Constant(c.type.get_size()))])))
        node.body.extend(create_stmt_list(children[len(children)-1].get_children()))

    # it does not need a returns, I'm not 100% sure why at this point but it just works without one.

    # ************************************** 
    # ************************************** 
    # ************************************** 

    print("new created node:", dump(node))
    stars()
    return node

