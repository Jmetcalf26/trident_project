from ast import *
def print_node_info(n):
    print(n.kind, n.spelling)
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

def translate_operator(operator):
    op = None 
    if operator == '+':
        op = Add()
    elif operator == '-':
        op = Sub()
    elif operator == '*':
        op = Mult()
    elif operator == '/':
        op = Div()
    # THIS WILL NEVER BE REACHED BECAUSE THERE IS NONE OF THIS IN C, ADD CHECK TO SEE IF BOTH SIDES ARE INTS TO USE THIS!
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
    # maybe add this one? I don't know, but it's present in the python ast library
    # elif operator == '@':
    #     op = MatMult()
    return op

def add_main_check(rn):
    i = If()
    i.test = Compare()
    i.test.left = Name()
    i.test.left.id = '__name__'
    i.test.left.ctx = Load()
    i.test.ops = []
    i.test.ops = [Eq()]
    c = Constant()
    c.value = '__main__'
    c.kind = None
    i.test.comparators = [c]
    e = Expr()
    ca = Call()
    n = Name()
    n.id = 'main'
    n.ctx = Load()
    ca.func = n
    ca.args = []
    ca.keywords = []
    e.value = ca
    i.body = [e]
    i.orelse = []
    rn.body.append(i)
    return rn

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
    print((' '*depth) + nt, n, end=' ')
    print("|".join(t.spelling for t in n.get_tokens()))
    # for t in n.get_tokens():
    #     print(t.spelling, end=' ')
    # print()

    for c in n.get_children():
        print_c_ast(c, depth+1)
def extended_node_info(n):
    print('spelling:', n.spelling)
    print('raw_comment:', n.raw_comment)
    print('mangled_name:', n.mangled_name)
    print('kind:', n.kind)
    print('lexical_parent:', n.lexical_parent)
    print('semantic_parent:', n.semantic_parent)
    print('linkage:', n.linkage)
    print('referenced:', n.referenced)
    print_node_info(n.referenced)
    typ = n.type
    print('type information:', end='\n\t')
    print("kind:", typ.kind, end='\n\t')
    print("spelling:", typ.spelling, end='\n\t')
    print("get_named_type():", typ.get_named_type(), end='\n\t')
    print("get_fields():", typ.get_fields(), end='\n\t')
    print("get_class_type():", typ.get_class_type(), end='\n\t')
    print("get_array_size():", typ.get_array_size(), end='\n\t')
    print('get_declaration():', typ.get_declaration())
