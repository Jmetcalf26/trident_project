from ast import *
from enum import Enum
from clang.cindex import TypeKind, CursorKind


def is_LValueToRValue(node):
    l_values = [CursorKind.DECL_REF_EXPR, CursorKind.ARRAY_SUBSCRIPT_EXPR, CursorKind.UNARY_OPERATOR]
    return list(node.get_children())[0].kind in l_values
def is_FunctionToPointerDecay(node):
    return node.referenced is not None and node.referenced.kind == CursorKind.FUNCTION_DECL
def is_ArrayToPointerDecay(node):
    array_values = [TypeKind.CONSTANTARRAY, TypeKind.VARIABLEARRAY, TypeKind.DEPENDENTSIZEDARRAY, TypeKind.INCOMPLETEARRAY]
    return node.type.get_canonical().kind == TypeKind.POINTER and list(node.get_children())[0].type.get_canonical().kind in array_values
def is_NoOp(node):
    return node.type.get_canonical().spelling == "const char *" and list(node.get_children())[0].type.get_canonical().spelling == "char *"
 

def bin(a):
    print("{0:b}".format(a))

def is_child(children, node_type):
    for c in children:
        if str(c.kind)[11:] == node_type:
            return True
    return False
            

def add_overflow_check(n, node):
    stars()
    print("INSIDE INT ERROR CHECK")
    stars()
    #largest_value_of_data_size = 2 ** max_place_value - 1
    #smallest_value_of_data_size = 2 ** min_place_value - 1
    #if value > largest_value_of_data_size:
    node = Module([node], [])
    if get_type(n) == "INT":
       check = If(Compare(Name(n.spelling), [Gt()], [Constant((2 ** 31) -1)]), [Expr([Call(Name('print'), [Constant('NOOOO')], [])])], [])
       check.orelse.append(If(Compare(Name(n.spelling), [Lt()], [Constant( -2 ** 31 )]), [Expr([Call(Name('print'), [Constant('NOOOO')], [])])], []))
       node.body.append(check)

    if get_type(n) == "UINT":
       check = If(Compare(Name(n.spelling), [Gt()], [Constant((2 ** 32) -1)]), [Expr([Call(Name('print'), [Constant('NOOOO')], [])])], [])
       node.body.append(check)

    stars()
    print("LEAVING INT ERROR CHECK")
    stars()
    return node

def print_node_info(n):
    print("n.kind", n.kind)
    print("n.spelling", n.spelling)
    #if "ARRAY" in str(n.type.get_canonical().kind):
    #print('element_type:', n.type.element_type.spelling)
    #print('element_type size:', n.type.element_type.get_size())
    #print('element_count:', n.type.element_count)
    print('get_array_element_type:', n.type.get_array_element_type().spelling)
    print('get_array_element_type size:', n.type.get_array_element_type().get_size())
    print('get_canonical().spelling:', n.type.get_canonical().spelling)
    print('get_canonical().kind:', n.type.get_canonical().kind)
    print('get_class_type():', n.type.get_class_type().kind.spelling)
    print('get_size():', n.type.get_size())
    print('get_pointee().kind:', n.type.get_pointee().kind)
    print('get_pointee().kind.spelling:', n.type.get_pointee().kind.spelling)
    print('get_pointee().spelling:', n.type.get_pointee().spelling)
    print('get_pointee().get_size():', n.type.get_pointee().get_size())
    print('get_pointee().get_array_element_type().size:', n.type.get_pointee().get_array_element_type().get_size())
    num_args = len(list(n.get_arguments()))
    print('num_args:', num_args)
    children = list(n.get_children())
    print('num_children:', len(children))
    tokens = list(n.get_tokens())
    print('num_tokens:', len(tokens))
    print("arguments:", end=' ')
    for a in n.get_arguments():
        print(a.spelling, end=' ')
    print()

    print('children:')
    for c in children:
        print(str(c.kind)[11:], c.spelling)
    print("|".join(t.spelling for t in n.get_tokens()))
    return

def get_type(node):
    return str(node.type.get_canonical().kind)[9:]

TypeCat = Enum('TypeCat', 'INTEGRAL FLOATING POINTER UNKNOWN')

def type_category(node):
    return {
        TypeKind.BLOCKPOINTER: TypeCat.POINTER,
        TypeKind.CONSTANTARRAY: TypeCat.POINTER,
        TypeKind.DEPENDENTSIZEDARRAY: TypeCat.POINTER,
        TypeKind.INCOMPLETEARRAY: TypeCat.POINTER,
        TypeKind.MEMBERPOINTER: TypeCat.POINTER,
        TypeKind.NULLPTR: TypeCat.POINTER,
        TypeKind.POINTER: TypeCat.POINTER,
        TypeKind.VARIABLEARRAY: TypeCat.POINTER,

        TypeKind.BOOL: TypeCat.INTEGRAL,
        TypeKind.CHAR16: TypeCat.INTEGRAL,
        TypeKind.CHAR32: TypeCat.INTEGRAL,
        TypeKind.ENUM: TypeCat.INTEGRAL,
        TypeKind.INT: TypeCat.INTEGRAL,
        TypeKind.INT128: TypeCat.INTEGRAL,
        TypeKind.LONG: TypeCat.INTEGRAL,
        TypeKind.LONGLONG: TypeCat.INTEGRAL,
        TypeKind.SCHAR: TypeCat.INTEGRAL,
        TypeKind.SHORT: TypeCat.INTEGRAL,
        TypeKind.UCHAR: TypeCat.INTEGRAL,
        TypeKind.UINT: TypeCat.INTEGRAL,
        TypeKind.UINT128: TypeCat.INTEGRAL,
        TypeKind.ULONG: TypeCat.INTEGRAL,
        TypeKind.ULONGLONG: TypeCat.INTEGRAL,
        TypeKind.USHORT: TypeCat.INTEGRAL,
        TypeKind.WCHAR: TypeCat.INTEGRAL,

        TypeKind.COMPLEX: TypeCat.FLOATING,
        TypeKind.DOUBLE: TypeCat.FLOATING,
        TypeKind.FLOAT: TypeCat.FLOATING,
        TypeKind.FLOAT128: TypeCat.FLOATING,
        TypeKind.LONGDOUBLE: TypeCat.FLOATING,
    }.get(node.kind, TypeCat.UNKNOWN)

def translate_u_operator(operator):
    op = None 
    if operator == '!':
        op = Not()
    elif operator == '-':
        op = USub()
    elif operator == '+':
        op = UAdd()
    elif operator == '~':
        op = Invert()
    return op

def translate_operator(operator, lhs_cat=TypeCat.UNKNOWN, rhs_cat=TypeCat.UNKNOWN):
    op = None 
    # Relational Operators
    if operator == '==':
        op = Eq()
    if operator == '!=':
        op = NotEq()
    if operator == '<':
        op = Lt()
    if operator == '<=':
        op = LtE()
    if operator == '>':
        op = Gt()
    if operator == '>=':
        op = GtE()
    # Arithmetic Operators
    if operator == '+':
        op = Add()
    elif operator == '-':
        op = Sub()
    elif operator == '*':
        op = Mult()
    elif operator == '/':
        if lhs_cat is TypeCat.FLOATING or rhs_cat is TypeCat.FLOATING:
            op = FloorDiv()
        else:
            op = Div()
    # THIS WILL NEVER BE REACHED BECAUSE THERE IS NONE OF THIS IN C, ADD CHECK TO SEE IF BOTH SIDES ARE INTS TO USE THIS!
    # (done - see above)
    elif operator == '//':
        op = FloorDiv()
    elif operator == '%':
        op = Mod()
    # SAME WITH THIS ONE
    elif operator == '**':
        op = Pow()
    elif operator == '<<':
        op = LShift()
    elif operator == '>>':
        op = RShift()
    elif operator == '|':
        op = BitOr()
    elif operator == '^':
        op = BitXor()
    elif operator == '&':
        op = BitAnd()
    elif operator == '&&':
        op = And()
    elif operator == '||':
        op = Or()

    # maybe add this one? I don't know, but it's present in the python ast library
    # elif operator == '@':
    #     op = MatMult()
    return op

def add_main_check():
    return If(Compare(Name('__name__', Load()), [Eq()], [Constant('__main__')]), [Expr(Call(Name('main', Load()), [], []))], [])

# def add_pointer_class():
#     #  class ast.ClassDef(name, bases, keywords, starargs, kwargs, body, decorator_list)
#     cd = ClassDef('Pointer', [], [], decorator_list=[])
#     fd = FunctionDef('_init__', arguments([], [arg('self'), arg('array'), arg('index')], defaults=[]), [Assign([Attribute(Name('self', Load()), 'array', Store())], Name('array', Load())), Assign([Attribute(Name('self', Load()), 'index', Store())], Name('index', Load()))], [])
#     fd2 = FunctionDef('get', arguments([], [], defaults=[]), [Return(Subscript(Attribute(Name('self', Load()), 'array', Load()), Attribute(Name('self', Load()), 'index', Load()), Load()))], [])
#     cd.body = [fd, fd2]
#     return cd

def add_helper_classes():
    cd = ImportFrom(
            module='helper_classes',
            names=[alias(name='*')],
            level=0)
    return cd

def add_args():
    e = []
    n = None
    return arguments(e, e, n, e, e, n, e)

    # posonlyargs = []
    # args = []
    # vararg = None
    # kwonlyargs = []
    # kw_defaults = []
    # kwarg = None
    # defaults = []
    # return arguments(posonlyargs, args, vararg, kwonlyargs, kw_defaults, kwarg, defaults)

def stars():
    print("\n"+"*"*50)


def print_c_ast(n, depth): 
    nt = str(n.kind)[11:]
    if nt == "MACRO_DEFINITION":
        return
    print((' '*depth) + nt, end=' ')
    print("|".join(t.spelling for t in n.get_tokens()))
    # for t in n.get_tokens():
    #     print(t.spelling, end=' ')
    # print()

    for c in n.get_children():
        print_c_ast(c, depth+1)

def cursor_bools(n):
    print('n.kind.is_attribute', n.kind.is_attribute())
    print('n.kind.is_declaration', n.kind.is_declaration())
    print('n.kind.is_expression', n.kind.is_expression())
    print('n.kind.is_invalid', n.kind.is_invalid())
    print('n.kind.is_preprocessing', n.kind.is_preprocessing())
    print('n.kind.is_reference', n.kind.is_reference())
    print('n.kind.is_statement', n.kind.is_statement())
    print('n.kind.is_translation_unit', n.kind.is_translation_unit())
    print('n.kind.is_unexposed', n.kind.is_unexposed())

def extended_node_info(n):
    print('n.is_const_method()', n.is_const_method())
    print('n.is_mutable_field()', n.is_mutable_field())
    print('spelling:', n.spelling)
    print('raw_comment:', n.raw_comment)
    print('result_type:', n.result_type)
    print_type_info(n.result_type)
    print('mangled_name:', n.mangled_name)
    print('kind:', n.kind)
    print('lexical_parent:', n.lexical_parent)
    print('semantic_parent:', n.semantic_parent)
    print('linkage:', n.linkage)
    print('referenced:', n.referenced)
    cursor_bools(n)
    if n.referenced is not None:
        print('='*10)
        print_node_info(n.referenced)
        print('='*10)
    print_type_info(n.type)

def print_type_info(typ):
    print('-'*10, end='\n\t')
    print('type information:', end='\n\t')
    print("kind:", typ.kind.spelling, end='\n\t')
    print("spelling:", typ.spelling, end='\n\t')
    print("get_named_type():", typ.get_named_type(), end='\n\t')
    print("get_fields():", typ.get_fields(), end='\n\t')
    print("get_result():", typ.get_result().kind.spelling, end='\n\t')
    print("get_class_type():", typ.get_class_type(), end='\n\t')
    print("get_array_size():", typ.get_array_size(), end='\n\t')
    print('get_declaration():', typ.get_declaration())
    print('-'*10, end='\n\t')

